#!/usr/bin/env python3
"""
SPK-Steg-04 «Голос эфира»
Создаёт radio.wav: шумовая запись с сообщением, видимым в спектрограмме.
Зависимости: numpy, Pillow
Установка: python -m pip install numpy pillow
Запуск: python gen.py
"""
import math
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FLAG = "SPKctf{spectrogram_message}"
OUTPUT = "radio.wav"
SAMPLE_RATE = 44100
COLUMN_SECONDS = 0.045
WIDTH, HEIGHT = 360, 72
FREQ_MIN, FREQ_MAX = 700, 7800

def make_bitmap(text):
    # Render readable block lettering onto a dark bitmap.
    image = Image.new("L", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 17)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    # Fit text while preserving clear character shapes.
    if text_w > WIDTH - 8:
        font = ImageFont.truetype("DejaVuSansMono.ttf", max(8, int(17 * (WIDTH - 8) / text_w)))
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = max(2, (WIDTH - text_w) // 2)
    y = max(0, (HEIGHT - text_h) // 2 - bbox[1])
    draw.text((x, y), text, fill=255, font=font)
    # Slightly thicken thin strokes so they survive typical spectrogram settings.
    image = image.point(lambda p: 255 if p > 30 else 0)
    return np.asarray(image) > 0

def main():
    bitmap = make_bitmap(FLAG)
    n_per_col = int(SAMPLE_RATE * COLUMN_SECONDS)
    rng = np.random.default_rng(2026)
    chunks = []
    # Each image column is encoded as a set of quiet simultaneous tones.
    # Frequency is mapped top-to-bottom; time moves left-to-right.
    for x in range(WIDTH):
        t = np.arange(n_per_col, dtype=np.float64) / SAMPLE_RATE
        chunk = 0.12 * rng.normal(0, 1, n_per_col)
        rows = np.where(bitmap[:, x])[0]
        for row in rows:
            frac = row / max(1, HEIGHT - 1)
            freq = FREQ_MAX - frac * (FREQ_MAX - FREQ_MIN)
            phase = rng.uniform(0, 2 * math.pi)
            chunk += 0.10 * np.sin(2 * math.pi * freq * t + phase)
        # Smooth joins between time columns.
        fade = min(500, n_per_col // 5)
        if fade:
            ramp = np.linspace(0, 1, fade)
            chunk[:fade] *= ramp
            chunk[-fade:] *= ramp[::-1]
        chunks.append(chunk)
    audio = np.concatenate(chunks)
    peak = np.max(np.abs(audio))
    audio = np.clip(audio / max(peak, 1e-9) * 0.92, -1, 1)
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(OUTPUT, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm.tobytes())
    print(f"Создан {OUTPUT}: {len(pcm)/SAMPLE_RATE:.1f} сек.")
    print("Флаг для CTFd:", FLAG)
    print("Проверьте radio.wav в Audacity в режиме Spectrogram.")

if __name__ == "__main__":
    main()
