from pathlib import Path
from codec import build, FLAG, reveal
folder=Path(__file__).resolve().parent
parts=build(folder/'source.png', folder/'rgb.png')
recovered,flag=reveal(folder/'rgb.png')
assert recovered==parts and flag==FLAG
print('PASS:', flag)
print('Fragments:', parts)
print('Generated:', folder/'rgb.png')
