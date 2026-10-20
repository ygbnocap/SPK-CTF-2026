"""SPK-Steg-07 seeded LSB codec. Positions selected by deterministic PRNG."""
import random
from PIL import Image
SEED = 1962
MAGIC = b'SPK7'

def positions(total, seed):
    rng = random.Random(seed)
    visited = set()
    while len(visited) < total:
        pos = rng.randrange(total)
        if pos not in visited:
            visited.add(pos)
            yield pos

def bits(data):
    for byte in data:
        for offset in range(7, -1, -1):
            yield (byte >> offset) & 1

def hide(src, output, text, seed=SEED):
    image = Image.open(src).convert('RGB')
    w, h = image.size
    data = text.encode('utf-8')
    if len(data) > 4096:
        raise ValueError('Message too long')
    payload = MAGIC + len(data).to_bytes(2, 'big') + data
    if len(payload)*8 > w*h:
        raise ValueError('Image too small')
    pixels = image.load()
    pos_iter = positions(w*h, seed)
    for bit in bits(payload):
        index = next(pos_iter)
        x, y = index % w, index // w
        r, g, b = pixels[x, y]
        pixels[x, y] = ((r & ~1) | bit, g, b)
    image.save(output, format='PNG')

def reveal(src, seed=SEED):
    image = Image.open(src).convert('RGB')
    w, h = image.size
    pix = image.load()
    stream = positions(w*h, seed)
    def read(num_bytes):
        result = bytearray()
        for _ in range(num_bytes):
            value = 0
            for _ in range(8):
                index = next(stream)
                x, y = index % w, index // w
                value = (value << 1) | (pix[x, y][0] & 1)
            result.append(value)
        return bytes(result)
    if read(4) != MAGIC:
        raise ValueError('Magic mismatch: incorrect seed or image')
    length = int.from_bytes(read(2), 'big')
    if length > 4096 or (length + 6) * 8 > w * h:
        raise ValueError('Invalid length')
    return read(length).decode('utf-8')
