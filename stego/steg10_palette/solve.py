#!/usr/bin/env python3
"""Organizer solution: recover the flag from unused PLTE RGB entries."""
from pathlib import Path
from PIL import Image
import io,sys,struct

def solve(path):
    raw=Path(path).read_bytes()
    im=Image.open(io.BytesIO(raw))
    if im.mode!='P':raise ValueError('Not indexed PNG')
    palette=im.getpalette()
    used=set(im.getdata())
    unused=[i for i in range(len(palette)//3) if i not in used]
    # In this task the embedded payload starts at the first unused entry.
    data=b''.join(bytes(palette[i*3:i*3+3]) for i in unused)
    first=data.find(b'SPKctf{')
    if first<0:raise ValueError('No flag in unused colors')
    last=data.find(b'}',first)
    if last<0:raise ValueError('Unterminated flag')
    return data[first:last+1].decode('ascii')
if __name__=='__main__':
    print(solve(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('palette.png')))
