#!/usr/bin/env python3
"""Generate Steg-05. Requires steghide and Pillow. Fails if either verification fails."""
from pathlib import Path
from PIL import Image
import shutil, subprocess, tempfile, sys

HERE = Path(__file__).resolve().parent
FLAG = 'SPKctf{steghide_metadata_key}'
PASSWORD = 'aperture1972'
ARTIST = 'SPKashka (aperture1972)'
DESCRIPTION = 'Photographer signed the print. Check Artist for the key.'

def call(*args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

def add_exif_without_reencoding(jpeg_bytes):
    """Insert EXIF APP1 after JPEG SOI. JPEG compressed pixels remain byte-for-byte unchanged."""
    if jpeg_bytes[:2] != b'\xff\xd8':
        raise ValueError('Expected JPEG SOI')
    exif = Image.Exif()
    exif[315] = ARTIST
    exif[270] = DESCRIPTION
    payload = exif.tobytes()
    if len(payload) + 2 > 65535:
        raise ValueError('EXIF segment too large')
    segment = b'\xff\xe1' + (len(payload) + 2).to_bytes(2, 'big') + payload
    return jpeg_bytes[:2] + segment + jpeg_bytes[2:]

def main():
    if not shutil.which('steghide'):
        sys.exit('ERROR: Install steghide: sudo apt-get install -y steghide')
    source = HERE / 'original.jpg'
    if not source.exists():
        sys.exit('ERROR: original.jpg not found')
    with Image.open(source) as im:
        if im.format != 'JPEG':
            sys.exit('ERROR: source must be JPEG')
        dims = im.size
    out = HERE / 'photo.jpg'
    if out.exists():
        out.unlink()  # never leave a stale result behind
    (HERE / 'hidden.txt').write_text(FLAG + '\n', encoding='utf-8')
    try:
        with tempfile.TemporaryDirectory(prefix='spk-steg05-') as tmp:
            temp = Path(tmp)
            stego = temp / 'stego.jpg'
            extracted = temp / 'extracted.txt'
            call('steghide', 'embed', '-cf', str(source), '-ef', str(HERE / 'hidden.txt'),
                 '-sf', str(stego), '-p', PASSWORD, '-f')
            # Steghide can discard original EXIF; insert our APP1 only AFTER embedding.
            candidate = temp / 'photo.jpg'
            candidate.write_bytes(add_exif_without_reencoding(stego.read_bytes()))
            with Image.open(candidate) as im:
                exif = im.getexif()
                assert im.format == 'JPEG' and im.size == dims
                assert exif.get(315) == ARTIST, f'Artist mismatch: {exif.get(315)!r}'
                assert exif.get(270) == DESCRIPTION
                im.verify()
            call('steghide', 'extract', '-sf', str(candidate), '-xf', str(extracted),
                 '-p', PASSWORD, '-f')
            assert extracted.read_text(encoding='utf-8') == FLAG + '\n', 'Extracted flag mismatch'
            out.write_bytes(candidate.read_bytes())
        print('PASS: JPEG valid; EXIF Artist + ImageDescription verified; steghide extraction verified')
        print('OUTPUT:', out)
        print('Artist:', ARTIST)
        print('FLAG:', FLAG)
    except (subprocess.CalledProcessError, AssertionError, ValueError, OSError) as err:
        if out.exists():
            out.unlink()
        if isinstance(err, subprocess.CalledProcessError):
            print(err.stderr, file=sys.stderr)
        sys.exit(f'FAIL: {err}')

if __name__ == '__main__':
    main()
