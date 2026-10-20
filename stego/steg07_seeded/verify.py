from pathlib import Path
from codec import reveal
base = Path(__file__).resolve().parent
expected = 'SPKctf{seeded_lsb_recovery}'
assert reveal(base / 'campus.png', 1962) == expected
try:
    reveal(base / 'campus.png', 1953)
except ValueError:
    pass
else:
    raise AssertionError('Incorrect seed unexpectedly succeeded')
print('PASS: correct flag recovered with 1962; wrong seed rejected')
