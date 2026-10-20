#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
from solve import solve
import struct,zlib,io
ROOT=Path(__file__).resolve().parent
p=ROOT/'palette.png'
raw=p.read_bytes()
with Image.open(io.BytesIO(raw)) as im:
    im.load()
    assert im.mode=='P' and im.size==(960,600)
    used=set(im.getdata())
    assert max(used)<16
    assert len(im.getpalette())==768
assert solve(p)=='SPKctf{png_structure_abuse}'
pos=raw.find(b'\x00\x00\x00\x00IEND\xaeB`\x82')
assert pos!=-1
pos+=12
n=struct.unpack('>I',raw[pos:pos+4])[0]
assert raw[pos+4:pos+8]==b'prVt'
assert raw[pos+8:pos+8+n]==b'SPKctf{png_structure_abuse}'
assert struct.unpack('>I',raw[pos+8+n:pos+12+n])[0]==zlib.crc32(raw[pos+4:pos+8+n])&0xffffffff
print('PASS: valid indexed PNG, flag recovered from unused palette RGB, trailing prVt confirmed')
