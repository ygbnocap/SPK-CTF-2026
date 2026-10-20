#!/usr/bin/env python3
"""Generate WAV artifact. Only Python standard library needed."""
import math
import random
import struct
import wave
from pathlib import Path
from codec import FLAG, hide, extract

BASE = Path(__file__).resolve().parent
OUT = BASE / 'deep.wav'
RATE = 24000
DURATION = 6
rng = random.Random(2026)

# Gentle radio-static sound, with a pair of soft tones.
samples = bytearray()
for i in range(RATE * DURATION):
    t = i / RATE
    level = (2400 * (rng.random() * 2 - 1)
             + 900 * math.sin(2 * math.pi * 327 * t)
             + 450 * math.sin(2 * math.pi * 611 * t))
    samples.extend(struct.pack('<h', int(max(-32768, min(32767, level)))))

frames = hide(samples, FLAG)
with wave.open(str(OUT), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(RATE)
    w.writeframes(frames)

assert extract(OUT) == FLAG, 'round-trip failed'
print(f'PASS: {OUT.name} created, extracted flag matches')
