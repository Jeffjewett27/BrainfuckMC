import argparse
import re
parser = argparse.ArgumentParser()

parser.add_argument("-b", "--brainfile", help="Brainfuck program file")
args = parser.parse_args()

with open(args.brainfile, "r") as f:
    program = f.read()

n=15
a=8
program = re.sub('[^\.,\+\-<>|\[\]]', '', program)
program = [program[max(i, 0):i+n] for i in range(a-n, len(program), n)]
program = '\n'.join(program)

print(program)