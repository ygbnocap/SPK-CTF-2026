#!/usr/bin/env python3
import subprocess
from pathlib import Path
folder = Path(__file__).resolve().parent
pdf = folder / 'contract.pdf'
expected = 'SPKctf{invisible_pdf_text}'
assert pdf.is_file(), 'contract.pdf not found; run python3 gen.py'
res = subprocess.run(['pdftotext', str(pdf), '-'], capture_output=True, text=True, check=True)
assert expected in res.stdout, 'Flag not found in PDF text layer'
print('PASS: hidden flag recovered from contract.pdf via pdftotext')
