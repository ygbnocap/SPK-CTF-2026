"""SPK Steg-09: custom LSB format for 16-bit PCM mono WAV.
Layout: 32 bit BE payload size, then 16 clear prefix bytes, then XOR suffix.
Bits stored MSB-first in LSB of every signed 16-bit PCM sample.
"""
import struct, wave
from pathlib import Path

FLAG = b'SPKctf{deep_audio_steganography}'


def payload(flag: bytes) -> bytes:
    if len(flag) <= 16:
        raise ValueError('Flag must be longer than 16 bytes')
    key = flag[:16]
    return key + bytes(b ^ key[i % 16] for i, b in enumerate(flag[16:]))


def decode_payload(data: bytes) -> bytes:
    if len(data) < 17:
        raise ValueError('Insufficient bytes')
    key = data[:16]
    return key + bytes(b ^ key[i % 16] for i, b in enumerate(data[16:]))


def bits_of(data: bytes):
    for byte in data:
        for shift in range(7, -1, -1):
            yield (byte >> shift) & 1


def hide(samples: bytes, flag: bytes) -> bytes:
    body = payload(flag)
    message = struct.pack('>I', len(body)) + body
    if 2 * len(message) * 8 > len(samples):
        raise ValueError('Insufficient WAV samples')
    output = bytearray(samples)
    for i, bit in enumerate(bits_of(message)):
        output[i * 2] = (output[i * 2] & 0xfe) | bit
    return bytes(output)


def read_bits(samples: bytes, start: int, count: int) -> bytes:
    out = bytearray()
    for byte_idx in range((count + 7) // 8):
        value = 0
        for j in range(8):
            bit_index = start + 8 * byte_idx + j
            value = (value << 1) | (samples[bit_index * 2] & 1)
        out.append(value)
    return bytes(out)


def extract(path: Path) -> bytes:
    with wave.open(str(path), 'rb') as w:
        if (w.getnchannels(), w.getsampwidth(), w.getcomptype()) != (1, 2, 'NONE'):
            raise ValueError('Expected uncompressed 16-bit mono PCM')
        frames = w.readframes(w.getnframes())
    if len(frames) < 64:
        raise ValueError('WAV too short')
    n = struct.unpack('>I', read_bits(frames, 0, 32))[0]
    if not (17 <= n <= min(4096, len(frames) // 16 - 4)):
        raise ValueError(f'Invalid embedded length: {n}')
    return decode_payload(read_bits(frames, 32, n * 8))
