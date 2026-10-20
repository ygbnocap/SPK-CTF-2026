#!/usr/bin/env python3
"""Organiser solution (never publish with challenge)."""
import argparse
from pathlib import Path
from codec import extract

p = argparse.ArgumentParser()
p.add_argument('input', nargs='?', default='deep.wav')
args = p.parse_args()
print(extract(Path(args.input)).decode('ascii'))
