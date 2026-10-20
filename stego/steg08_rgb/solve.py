import argparse
from codec import reveal
parser=argparse.ArgumentParser(description='SPK Steg-08 organizer solver')
parser.add_argument('file',nargs='?',default='rgb.png')
args=parser.parse_args()
parts,flag=reveal(args.file)
for channel,chunk in zip('RGB',parts): print(f'{channel}: {chunk}')
print('FLAG:',flag)
