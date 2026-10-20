"""SPK-Steg-08: each RGB channel carries one piece, prefixed with a 16-bit bit-length."""
from PIL import Image

FLAG = 'SPKctf{rgb_channels_split}'

def split_flag(flag=FLAG):
    b = flag.encode('ascii')
    a, r = divmod(len(b), 3)
    lens = [a + (i < r) for i in range(3)]
    return [b[:lens[0]], b[lens[0]:lens[0]+lens[1]], b[lens[0]+lens[1]:]]

def bits_of_bytes(data):
    for value in data:
        for bit in range(7, -1, -1):
            yield (value >> bit) & 1

def build(cover, output):
    image = Image.open(cover).convert('RGB')
    w,h=image.size
    pixels=bytearray(image.tobytes())
    pieces=split_flag()
    for channel,fragment in enumerate(pieces):
        payload = len(fragment).to_bytes(2,'big') + fragment
        bits=list(bits_of_bytes(payload))
        if len(bits)>w*h:
            raise ValueError('Image too small for payload')
        for p, bit in enumerate(bits):
            off=p*3 + channel
            pixels[off] = (pixels[off] & 0xfe) | bit
    out = Image.frombytes('RGB',(w,h),bytes(pixels))
    out.save(output,format='PNG')
    return [piece.decode('ascii') for piece in pieces]

def reveal(filename):
    image=Image.open(filename).convert('RGB')
    pixels=image.tobytes()
    channels=[]
    count=image.width*image.height
    for channel in range(3):
        def get_byte(index):
            value=0
            for k in range(8):
                value=(value<<1) | (pixels[(index*8+k)*3+channel] & 1)
            return value
        if count < 16: raise ValueError('Image too small')
        n=get_byte(0)*256+get_byte(1)
        if (n+2)*8>count: raise ValueError('Invalid length header')
        channels.append(bytes(get_byte(j+2) for j in range(n)).decode('ascii'))
    return channels, ''.join(channels)
