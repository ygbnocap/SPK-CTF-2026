"""Organizer-only solution. Never upload with the challenge."""
import argparse
from pathlib import Path
from codec import reveal
p = argparse.ArgumentParser()
p.add_argument('file', nargs='?', default=str(Path(__file__).parent / 'campus.png'))
p.add_argument('--seed', type=int, default=1962)
a = p.parse_args()
print(reveal(a.file, a.seed))
