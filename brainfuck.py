from bfconfig import BfConfig

class StdOut:
    def __init__(self, method = 0) -> None:
        self.method = method
        self.output = ''

    def print(self, val):
        self.output += str(val)
        if self.method == 0:
            print(val, end='')
            

    def final(self):
        if self.method == 2:
            return
        if self.method == 1:
            print(self.output, end='')
        print('')

class BfEngine:
    OPEN_LOOP = '['
    CLOSE_LOOP = ']'
    INCREMENT = '+'
    DECREMENT = '-'
    SHIFT_UP = '>'
    SHIFT_DOWN = '<'
    PRINT = '.'
    READ = ','
    NEWLINE = '|'
    DEBUG = '#'

    def __init__(self, args, animation = None, outputMethod = 0) -> None:
        
        self.instructions = args.program
        self.input = args.input + ('0'*1000)
        self.memory = [0] * 1000
        self.instP = 0
        self.inpP = 0
        self.memP = 0
        self.stack = 0
        self.dir = 1
        self.active = True
        self.output = StdOut(outputMethod)
        self.numCommands = 0
        self.maxCommands = int(args.max or 10000)
        self.cellMax = 9
        self.wrap = args.wrap
        self.animation = animation

    def isFinished(self):
        return self.instP >= len(self.instructions) or self.numCommands > self.maxCommands    
    
    def handleWrap(self, value):
        if self.wrap:
            return (value + self.cellMax + 1) % (self.cellMax + 1)
        return max(0, min(value, self.cellMax))

    def tick(self):
        if self.isFinished():
            return
        inst = self.instructions[self.instP]
        if self.animation:
            self.animation.instruction(self.instP)
        if inst == BfEngine.OPEN_LOOP:
            self.stack += 1
            if self.active:
                if self.memory[self.memP] == 0:
                    self.active = False
                    if self.animation:
                        self.animation.disable()
                else:
                    self.stack = 0
        elif inst == BfEngine.CLOSE_LOOP:
            self.stack -= 1
            if self.active:
                if self.memory[self.memP] != 0:
                    self.dir = -1
                    self.active = False
                    if self.animation:
                        self.animation.disable()
                else:
                    self.stack = 0
        elif self.active:
            if inst == BfEngine.INCREMENT:
                # self.memory[self.memP] = min(self.cellMax, self.memory[self.memP] + 1)
                self.memory[self.memP] = self.handleWrap(self.memory[self.memP] + 1)
                if self.animation:
                    self.animation.addition()
            elif inst == BfEngine.DECREMENT:
                # self.memory[self.memP] = max(0, self.memory[self.memP] - 1)
                self.memory[self.memP] = self.handleWrap(self.memory[self.memP] - 1)
                if self.animation:
                    self.animation.subtraction()
            elif inst == BfEngine.SHIFT_UP:
                self.memP += 1
                if self.animation:
                    self.animation.shift(self.memP)
            elif inst == BfEngine.SHIFT_DOWN:
                self.memP = max(0, self.memP - 1)
                if self.animation:
                    self.animation.shift(self.memP)
            elif inst == BfEngine.PRINT:
                self.output.print(self.memory[self.memP])
                if self.animation:
                    self.animation.printOutput(self.memory[self.memP])
            elif inst == BfEngine.READ:
                self.memory[self.memP] = int(self.input[self.inpP])
                if self.animation:
                    self.animation.readInput(self.inpP)
                self.inpP += 1
            elif inst == BfEngine.NEWLINE:
                self.output.print('\n')
            elif inst == BfEngine.DEBUG:
                self.printmem()
        if self.stack == 0:
            self.active = True
            self.dir = 1
            if self.animation:
                self.animation.enable()
        self.instP += self.dir
        self.numCommands += 1

    def printmem(self, msg = ''):
        if len(msg) == 0:
            msg = 'Memory'
        print(f'{msg}: ', end='')
        print(self.memory[:40])

    def run(self):
        if self.animation:
            self.animation.start()
        while not self.isFinished():
            self.tick()
        self.output.final()
        if self.animation:
            self.animation.end()

if __name__ == "__main__":
    args = BfConfig.parseConfig()
    print(f'Executing with {args}')
    if args.animate:
        from brainfuck_anim import BrainfuckAnim
        BrainfuckAnim.doanimation(args)
    else:
        engine = BfEngine(args)
        engine.run()