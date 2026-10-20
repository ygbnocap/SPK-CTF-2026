#!/usr/bin/env python3
"""Solver/checker for SPK-Steg-04 «Голос эфира».

Reconstructs the hidden bitmap from radio.wav's frequency components and saves
it as recovered.png. If Tesseract OCR is installed, it also attempts to read
and print the flag automatically.

Dependencies: numpy, scipy, Pillow
Optional OCR: pytesseract + the Tesseract executable
Usage: python solve.py [radio.wav] [recovered.png]
"""
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps, ImageFilter
from scipy.signal import stft

WIDTH, HEIGHT = 360, 72
SAMPLE_RATE_EXPECTED = 44100
COLUMN_SECONDS = 0.045
FREQ_MIN, FREQ_MAX = 700.0, 7800.0


def load_wav(path):
    with wave.open(str(path), "rb") as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
    if sample_width != 2:
        raise ValueError(f"Expected 16-bit PCM WAV, got {sample_width * 8}-bit")
    audio = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1)
    if rate != SAMPLE_RATE_EXPECTED:
        raise ValueError(f"Expected {SAMPLE_RATE_EXPECTED} Hz, got {rate} Hz")
    return audio, rate


def recover_bitmap(audio, rate):
    # The generator encodes one bitmap column in each 45 ms audio chunk.
    # Analyse chunks independently to preserve the time axis and use a heavily
    # zero-padded FFT to estimate energy near each expected row frequency.
    samples_per_col = int(rate * COLUMN_SECONDS)
    nfft = 16384
    freqs = np.fft.rfftfreq(nfft, d=1.0 / rate)
    window = np.hanning(samples_per_col)
    bitmap = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

    for x in range(WIDTH):
        chunk = audio[x * samples_per_col:(x + 1) * samples_per_col]
        if len(chunk) != samples_per_col:
            break
        spectrum = np.abs(np.fft.rfft(chunk * window, n=nfft))
        row_energy = np.zeros(HEIGHT, dtype=np.float64)
        for row in range(HEIGHT):
            frac = row / (HEIGHT - 1)
            target = FREQ_MAX - frac * (FREQ_MAX - FREQ_MIN)
            band = np.where(np.abs(freqs - target) <= 35.0)[0]
            if len(band) == 0:
                band = np.array([int(np.argmin(np.abs(freqs - target)))])
            row_energy[row] = spectrum[band].max()

        # Tonal pixels stand above the noise floor. A per-column threshold
        # adapts to the changing number of encoded tones.
        # In this artifact, signal-bearing bins are typically around 1.5–2x
        # the median noise amplitude. This percentile-based cutoff worked well
        # for the supplied generator while adapting to each column.
        threshold = np.percentile(row_energy, 65) * 1.8
        bitmap[:, x] = (row_energy > threshold).astype(np.uint8) * 255

    return Image.fromarray(bitmap, mode="L").filter(ImageFilter.MaxFilter(3))


def main():
    wav_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("radio.wav")
    image_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("recovered.png")
    if not wav_path.exists():
        raise SystemExit(f"File not found: {wav_path}\nUsage: python solve.py [radio.wav] [recovered.png]")

    audio, rate = load_wav(wav_path)
    image = recover_bitmap(audio, rate)
    image.save(image_path)
    print(f"[+] Reconstructed spectrogram bitmap: {image_path}")

    try:
        import pytesseract
        # Upscale and invert: the original lettering is bright on a dark background.
        ocr_image = ImageOps.invert(image).resize((image.width * 3, image.height * 3))
        text = pytesseract.image_to_string(ocr_image, config="--psm 7")
        cleaned = "".join(text.split())
        print("[+] OCR result:", text.strip() or "(no text recognized)")
        if "SPKctf{" in cleaned and "}" in cleaned:
            start = cleaned.find("SPKctf{")
            end = cleaned.find("}", start)
            print("[+] Possible flag:", cleaned[start:end + 1])
        else:
            print("[!] OCR did not confidently identify the flag; inspect recovered.png.")
    except ImportError:
        print("[*] Optional OCR not installed. Open recovered.png and read the flag.")
        print("    For OCR: install pytesseract and the Tesseract OCR executable.")


if __name__ == "__main__":
    main()
