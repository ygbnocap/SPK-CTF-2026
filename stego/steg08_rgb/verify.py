from pathlib import Path
from PIL import Image, ImageChops
from codec import reveal,FLAG,split_flag
base=Path(__file__).resolve().parent
image=base/'rgb.png'
assert image.is_file(), 'rgb.png missing; run gen.py'
assert Image.open(image).format=='PNG'
chunks,flag=reveal(image)
assert flag==FLAG, f'Bad flag: {flag!r}'
assert chunks==[part.decode('ascii') for part in split_flag()]
assert ImageChops.difference(Image.open(base/'source.png').convert('RGB'),Image.open(image).convert('RGB')).getbbox() is not None
print('PASS: PNG valid; separate R/G/B payloads reconstruct',FLAG)
