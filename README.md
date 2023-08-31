# BrainfuckMC

Project by Jeff Jewett. I built a Minecraft redstone Brainfuck interpreter. It has some quirks compared to regular Brainfuck so I made this companion Python interpreter to test out programs.

## What is Brainfuck?

Brainfuck is a minimal Turing-complete programming language. It only has 8 operations:
- `>` : shift the pointer right
- `<` : shift the pointer left
- `+` : increment the pointer value
- `-` : decrement the pointer value
- `.` : print the pointer value
- `,` : read input into the pointer value
- `[` : open a while loop. the condition is 'pointer value != 0'
- `]` : close a while loop

There are no variables--just a large memory tape. Different implementations have variations for cell size, wraparound, memory bounds, etc. More information about the Brainfuck language at https://brainfuck.org/

## Minecraft Brainfuck?

Yes, that's right. I used 2-way flying machines for the instruction pointer and memory pointer. I used droppers with non-stackable items to get decimal values, 0-9. More details about this are coming in a video I am making.

There are several quirks compared to traditional Brainfuck:
- Decimal cell values: Rather than a full byte (0-255), values can only be in the range 0-9. This means that ASCII values cannot be handled. 
- No wraparound: Values will be clipped to 0-9. If `+` is executed on a value of `9`, the value will not change.
- `|` instruction: Because there is no ASCII to print a new line, this provides a newline functionality, or in Minecraft it clears the display.

## brainfuck.py

This is a reimplementation of the BrainfuckMC redstone interpreter in Python. It has some additional debugging features.

## mcprint.py

This is a utility that prints the instructions stripped of all comments and in groups of 15, just how they are grouped in the redstone.

## Programs

I have developed and edited some programs that work with the interpreter.

### Addition (addition.b)

This does multidigit addition (up to 9 digits). Inputs are formatted `na..amb..b`, where `n` is the number of digits of the first operand with digits `a..a` and `m` is the number of digits of the second operand with digits `b..b`. It will output `a..a+b..b`. Example: `3512232` gives the result of `512+32`.

### Sorting (bubble_sort.b, ins_sort.b)

These programs sort the input digits. For example, the input `31415` will output `11345`. There are a bubble sort and insertion sort implementation.

### Doubling (pow2.b)

This executes a non-terminating doubling sequence. It accepts an optional input value in reverse digit order or defaults to start at 1 if input is empty/zero. For example, input `0` outputs `1,2,4,8,16,32,...` and input `321` outputs `123,246,492,984,1968,...`.