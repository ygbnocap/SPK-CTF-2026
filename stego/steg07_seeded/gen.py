from pathlib import Path
from codec import hide, reveal, SEED
BASE = Path(__file__).resolve().parent
FLAG = 'SPKctf{seeded_lsb_recovery}'
hide(BASE / 'original.jpg', BASE / 'campus.png', FLAG)
assert reveal(BASE / 'campus.png') == FLAG
print(f'PASS: {BASE / "campus.png"} generated and extracted with seed {SEED}')
