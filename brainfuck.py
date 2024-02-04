import argparse
import re
from engine import BfEngine
parser = argparse.ArgumentParser()

parser.add_argument("-p", "--program", help="Brainfuck program text")
parser.add_argument("-b", "--brainfile", help="Brainfuck program file")
parser.add_argument("-i", "--input", help="Input digit string")
parser.add_argument("-d", "--inputfile", help="Input file")
parser.add_argument("-l", "--log", help="debug statements", action='store_true')
parser.add_argument("-m", "--max", help="max cell value")
args = parser.parse_args()

program = args.program

if program is None:
    with open(args.brainfile, "r") as f:
        program = f.read()

input = args.input or ''

if input is None:
    with open(args.inputfile, "r") as f:
        input = f.read()

program = re.sub('[^\.,\+\-<>|#\[\]&]', '', program)
input = re.sub('[^0-9]', '', input)

print('Program (len ' + str(len(program)) + '): ' + program)
print('Input: ' + input)

input += '0' * 100
memsize = 1000
maxmemsize = 100000
mem = [0] * memsize
p = 0
inp = 0
com = 0
stack = []
numcommands = 0
maxcommands = 2000
numskipped = 0
output = ''
cellsize = int(args.max or 9)

# engine = BfEngine(program, input, maxCommands=maxcommands, outputMethod=0)

def printmem(msg = ''):
    if len(msg) == 0:
        msg = 'Memory'
    print(f'{msg}: ', end='')
    print(mem[:40])

while com < len(program):
    c = program[com]
    if c == '+':
        mem[p] = mem[p]+1
        if mem[p] > cellsize:
            if args.log:
                printmem('cellsize')
            mem[p] = cellsize
    elif c == '-':
        mem[p] = max(mem[p]-1, 0)
    elif c == '>':
        p += 1
        if p == len(mem):
            mem.append(0)
        if p > maxmemsize:
            raise Exception("maximum memory reached")
    elif c == '<':
        p = max(p-1, 0)
    elif c == '.':
        output += str(mem[p])
    elif c == ',':
        mem[p] = int(input[inp])
        inp += 1
    elif c == '[':
        if mem[p] > 0:
            stack.append(com)
        else:
            oldcom = com
            depth = 1
            while depth > 0:
                com += 1
                if com >= len(program):
                    raise Exception("Unmatched [ at command " + str(oldcom))
                c = program[com]
                if c == '[':
                    depth += 1
                elif c == ']':
                    depth -= 1
            numskipped += com - oldcom
    elif c == ']':
        if len(stack) == 0:
            raise Exception("Unmatched ] at command " + str(com) + ", total: " + str(numcommands))
        if mem[p] > 0:
            oldcom = com
            com = stack[-1]
            numskipped += oldcom - com
        else:
            oldcom = stack.pop()
    elif c == '|':
        # new line/clear output
        output += '\n'
    elif c == '&' and args.log is not None:
        print('')
        print('breakpoint reached')
    elif c == '#' and args.log:
        printmem()
    com += 1
    numcommands += 1
    if numcommands > maxcommands:
        print(output)
        raise Exception("Exceeded max time")

print(f'Output: {output}')

if args.log:
    print('Memory: ', end='')
    print(mem[:40])
print('Finished with ' + str(numcommands) + ' commands (' + str(numskipped) + ' skipped)')
            