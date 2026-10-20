#!/usr/bin/env python3
"""Validate playable WAV and extraction, plus check XOR is actually used."""
from pathlib import Path
import wave
from codec import FLAG, extract, read_bits, payload

path = Path(__file__).resolve().parent / 'deep.wav'
with wave.open(str(path), 'rb') as wav:
    assert wav.getnchannels() == 1
    assert wav.getsampwidth() == 2
    assert wav.getframerate() == 24000
    assert wav.getnframes() == 144000
    frames = wav.readframes(wav.getnframes())
actual = extract(path)
assert actual == FLAG
assert payload(FLAG)[16:] != FLAG[16:]
assert read_bits(frames, 32, 16 * 8) == FLAG[:16]
print('PASS: valid 16-bit PCM WAV, correct LSB prefix, XOR suffix recovered')
print(actual.decode('ascii'))
