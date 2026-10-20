#!/usr/bin/env python3
"""Build SPK-Steg-10 indexed PNG with secret bytes in unused PLTE colors."""
from pathlib import Path
from PIL import Image, ImageDraw
import math, struct, zlib
ROOT=Path(__file__).resolve().parent
FLAG=b'SPKctf{png_structure_abuse}'
W,H=960,600
COLORS=[(8,13,31),(21,31,57),(34,50,81),(47,77,110),(38,110,126),(42,147,148),(99,193,163),(202,230,195),(249,215,143),(247,150,102),(203,91,113),(130,71,119),(82,55,101),(227,236,229),(100,133,173),(173,188,199)]

def make_art():
    im=Image.new('P',(W,H),0)
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,H),fill=0)
    # night city skyline and glowing horizon
    d.rectangle((0,355,W,600),fill=1)
    for x in range(0,W,24):
        height=65+((x*19+23)%135)
        d.rectangle((x,385-height,x+19,389),fill=2 if x%3 else 3)
        for y in range(399-height,375,13):
            for xx in range(x+4,x+19,9):
                if (xx+y)//11%4==0:d.rectangle((xx,y,xx+3,y+5),fill=8)
    # pixel stars
    for i in range(130):
        x=(i*223+47)%W; y=(i*131+19)%280
        c=7 if i%5==0 else 14
        d.rectangle((x,y,x+2+(i%3),y+2+(i%3)),fill=c)
    # moon and circuits
    d.ellipse((715,55,840,180),fill=8)
    d.ellipse((735,42,856,165),fill=0)
    d.rounded_rectangle((155,118,650,472),radius=24,fill=12,outline=6,width=8)
    d.rounded_rectangle((177,140,627,450),radius=13,fill=1,outline=4,width=5)
    # screen arcs
    for y in range(172,414,27):
        d.line([(204,y),(260,y),(280,y+8),(400,y+8)],fill=4,width=4)
        d.rectangle((225,y-3,239,y+3),fill=6)
    # pixel lock motif
    d.arc((386,178,534,325),180,360,fill=8,width=24)
    d.rounded_rectangle((370,258,550,375),radius=15,fill=5,outline=7,width=7)
    d.ellipse((448,286,475,313),fill=0)
    d.rectangle((459,307,465,340),fill=0)
    # glowing digital terminals
    for x in (40,675,800):
        d.rounded_rectangle((x,460,x+110,505),radius=7,fill=3,outline=6,width=3)
        d.rectangle((x+14,477,x+75,482),fill=7)
    d.rectangle((0,536,W,600),fill=0)
    for x in range(0,W,40):
        d.line((x,540,x-55,600),fill=3,width=2)
    for y in (548,563,582):d.line((0,y,W,y),fill=2,width=2)
    # All drawn pixels are indexes 0..15
    pal=COLORS[:]
    for i in range(0,len(FLAG),3):
        b=FLAG[i:i+3]
        pal.append(tuple(b + b'\0'*(3-len(b))))
    while len(pal)<256:
        i=len(pal)
        pal.append(((i*53+31)%256,(i*97+17)%256,(i*139+7)%256))
    im.putpalette([v for rgb in pal for v in rgb])
    return im

def chunk(kind,data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)

def main():
    path=ROOT/'palette.png'
    image=make_art()
    image.save(path,format='PNG',optimize=False)
    content=path.read_bytes()
    assert content.endswith(b'\x00\x00\x00\x00IEND\xaeB`\x82')
    # Nonstandard trailing chunk intentionally placed after IEND, per challenge brief
    content+=chunk(b'prVt',FLAG)
    path.write_bytes(content)
    print('Created',path, 'bytes:',len(content))

if __name__=='__main__':main()
