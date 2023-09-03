import argparse
import re
parser = argparse.ArgumentParser()

parser.add_argument("-b", "--brainfile", help="Brainfuck program file")
parser.add_argument("-r", "--row", action='store_true')
args = parser.parse_args()

with open(args.brainfile, "r") as f:
    program = f.read()

n=15
a=8
program = re.sub('[^\.,\+\-<>|\[\]]', '', program)
program = [program[max(i, 0):i+n] for i in range(a-n, len(program), n)]
rowchars = ['.','|','>','<','+','-',',',']','[']

def printrows(segment):
    for i in range(9):
        rowtext = ''.join([(c if c==rowchars[i] else '_') for c in segment])
        print(rowtext)

if args.row:
    for segment in program:
        printrows(segment)
        print()
else:
    program_block = '\n'.join(program)
    print(program_block)