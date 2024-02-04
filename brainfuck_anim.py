from itertools import zip_longest
import math
from manim import *
from collections import deque

TEXT_SIZE_FACTOR = 0.7

class Tape(VGroup):
    @staticmethod
    def labelUpdater(tape, label, idx):
        rawIdx = tape.getArrayIdxFromLabelIdx(idx)
        value = str(tape.array[rawIdx]) if rawIdx < len(tape.array) else ''
        # if label.text != value:
        #     label.become(Text(value, font_size=DEFAULT_FONT_SIZE * self.boxScale))
        lcolor = tape.labelColors.get(value, WHITE)
        if tape.arrowScroll.get_value() == rawIdx:
            lcolor = tape.pointerColor
        label.set_color(lcolor)
        label.move_to(RIGHT * (rawIdx-tape.scroll.get_value()-tape.offsetX) * tape.boxScale + DOWN * tape.offsetY)
        if rawIdx < 0 or rawIdx >= len(tape.array):
            label.move_to(RIGHT * 100)

    def __init__(self, array, numboxes, offsetY = 0, pointerQueue=None):
        super().__init__()
        self.array = array
        self.numboxes = numboxes + 6
        self.arrowHeight = 1.5
        self.padding = 4
        self.scroll = ValueTracker(-self.padding)
        self.screenWidth = 16
        self.offsetX = self.numboxes / 2
        self.offsetY = -offsetY
        self.boxScale = self.screenWidth / self.numboxes
        if pointerQueue is not None:
            self.scrollPositions = self.processScrollPositions(pointerQueue, self.numboxes - 2 * self.padding)
        else:
            self.scrollPositions = []
        self.scrollPosIdx = 0
        self.labelColors = { '#': GREY_E }
        self.defaultPointerColor = '#9af5f3'
        self.pointerColor = self.defaultPointerColor
        # self.add_updater(lambda tape: tape.move_to([-self.scroll.get_value(), 0, 0]))

        def boxUpdater(box, idx):
            minIdx = math.floor(self.scroll.get_value())
            rawIdx = minIdx + idx - (minIdx % self.numboxes)
            if idx < (minIdx % self.numboxes):
                rawIdx += self.numboxes
            box.move_to(RIGHT * (rawIdx-self.scroll.get_value()-self.offsetX) * self.boxScale + DOWN * self.offsetY)
            if rawIdx < 0 or rawIdx >= len(self.array):
                box.move_to(RIGHT * 100)

        self.labels = []
        for i in range(min(self.numboxes, len(self.array))):
            box = Square(side_length=self.boxScale)
            box.add_updater(lambda box, idx=i: boxUpdater(box, idx))
            label = Text(text=str(array[i]), font_size=DEFAULT_FONT_SIZE * self.boxScale)
            self.labels.append(label)
            label.add_updater(lambda label, idx=i: Tape.labelUpdater(self, label, idx))
            self.add(box, label)

        self.arrowScroll = ValueTracker(0)
        arrow = Arrow(start=DOWN * self.arrowHeight, end=DOWN*0.1).add_updater(
            lambda arr: arr.move_to(RIGHT * (self.arrowScroll.get_value()-self.scroll.get_value()-self.offsetX) * self.boxScale + DOWN * (self.offsetY + 0.5*self.arrowHeight))
        )
        self.add(arrow)

    def absoluteArrowPosition(self):
        return RIGHT * (self.arrowScroll.get_value()-self.scroll.get_value()-self.offsetX) * self.boxScale + DOWN * self.offsetY

    def processScrollPositions(self, values, numboxes):
        print(values)
        trends = [x - values[i - 1] for i, x in enumerate(values)]
        trends[0] = values[0]
        scrollStart = 0
        scrollPositions = []
        
        def find_next_bigger(lst, idx, X):
            smallest = lst[idx]
            for i in range(idx+1, len(lst)):
                if lst[i] < smallest:
                    smallest = lst[i]
                if lst[i] > X:
                    return i, smallest
            return -1, smallest
        
        def find_next_smaller(lst, idx, X):
            biggest = lst[idx]
            for i in range(idx+1, len(lst)):
                if lst[i] > biggest:
                    biggest = lst[i]
                if lst[i] < X:
                    return i, biggest
            return -1, biggest

        for idx, _ in enumerate(values):
            trend = trends[idx]
            if trend > 0:
                biggerIdx, minVal = find_next_bigger(values, idx, scrollStart + numboxes)
                if biggerIdx > 0 and minVal > scrollStart:
                    scrollStart += 1

            if trend < 0:
                biggerIdx, maxVal = find_next_smaller(values, idx, scrollStart)
                if biggerIdx > 0 and maxVal < scrollStart + numboxes:
                    scrollStart -= 1

            scrollPositions.append(scrollStart)
        print(scrollPositions)
        return scrollPositions

    def moveArrow(self, pos):
        self.updateText()
        anims = [
            self.arrowScroll.animate.set_value(pos),
        ]
        if self.scrollPosIdx < len(self.scrollPositions):
            scrollPos = self.scrollPositions[self.scrollPosIdx] if len(self.scrollPositions) > 0 else pos
            anims.append(self.scroll.animate.set_value(scrollPos - self.padding))
            self.scrollPosIdx += 1
        return AnimationGroup(
            *anims
        )
    
    def getArrayIdxFromLabelIdx(self, labelIdx):
        minIdx = math.floor(self.scroll.get_value())
        arrayIdx = minIdx + labelIdx - (minIdx % self.numboxes)
        if labelIdx < (minIdx % self.numboxes):
            arrayIdx += self.numboxes
        return arrayIdx
    
    def updateText(self):
        for idx, label in enumerate(self.labels):
            arrayIdx = self.getArrayIdxFromLabelIdx(idx)
            arrayValue = str(self.array[arrayIdx]) if arrayIdx < len(self.array) else ''
            if arrayValue != label.text:
                newLabel = Text(arrayValue, font_size=DEFAULT_FONT_SIZE * self.boxScale).move_to(label).set_color(label.color)
                newLabel.add_updater(lambda label, idx=idx: Tape.labelUpdater(self, label, idx))
                # label.become(newLabel)
                self.add(newLabel)
                self.remove(label)
                # Tape.labelUpdater(self, label, idx)
                self.labels[idx] = newLabel
                # self.remove(label)

    
    def setColors(self, colors):
        self.labelColors = colors

class InputText(VGroup):
    def __init__(self, inputArray):
        super().__init__()
        self.topLeft = LEFT * 5 + UP * 3 + DOWN * TEXT_SIZE_FACTOR
        self.inputArray = inputArray
        self.displayChars = 10
        self.label = Text('Input:', font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        # self.label.move_to(topLeft)
        self.label.next_to(LEFT * 5 + UP * 3, RIGHT, buff=0)
        self.inputValues = Text(' '.join(self.inputArray[:self.displayChars]), font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        # self.inputValues.move_to(LEFT * 5 + UP * 2)
        self.inputValues.next_to(self.topLeft, RIGHT, buff=0)
        self.add(self.label, self.inputValues)

    def shiftInput(self, inpP):
        newInput = Text(' '.join(self.inputArray[inpP:inpP+self.displayChars]), font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        self.inputValues.become(newInput).next_to(self.topLeft, RIGHT, buff=0)

class OutputText(VGroup):
    def __init__(self, outputObj):
        super().__init__()
        self.topRight = RIGHT * 2 + UP * 2.5
        self.outputObj = outputObj
        self.displayChars = 12
        self.nRows = 5
        self.label = Text('Output:', font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        # self.label.move_to(topLeft)
        self.label.next_to(RIGHT * 1 + UP * 3, LEFT, buff=0)
        # outputObj.output = '0123456789012345\n678901234567\n01234\n012345680'
        outputText = self.lastNRows(outputObj.output, self.nRows, self.displayChars)
        self.inputValues = Text(outputText, font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        # self.inputValues.move_to(LEFT * 5 + UP * 2)
        self.inputValues.next_to(self.topRight, RIGHT, buff=0)
        self.add(self.label, self.inputValues)

    def lastNRows(self, output, n, rowLength):
        return '\n'.join([' '.join(row[-rowLength:]) for row in output.split('\n')[-n:]])

    def printOutput(self):
        outputText = self.lastNRows(self.outputObj.output, self.nRows, self.displayChars)
        newInput = Text(outputText, font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        self.inputValues.become(newInput).next_to(self.topRight, RIGHT, buff=0)
        
class BrainfuckAnim(Scene):
    @staticmethod
    def doanimation(args):
        BrainfuckAnim.args = args
        with tempconfig({"quality": "high_quality", "preview": False, "disable_caching": True, "renderer": "opengl"}):
            scene = BrainfuckAnim()
            scene.render()

    def construct(self):
        self.memPos = (-5, 1)
        self.boxSize = 0.4
        self.memScroll = 0
        self.instrTime = 0.4
        
        from engine import BfEngine
        #run the program in advance to predict camera scrolling
        prerun = BfEngine(BrainfuckAnim.args, animation=DummyAnimation(), outputMethod=2)
        prerun.run()
        self.shiftQueue = list(prerun.animation.shiftQueue)
        self.instrQueue = list(prerun.animation.instrQueue)

        self.engine = BfEngine(BrainfuckAnim.args, animation=self, outputMethod=1)
        self.engine.run()

    def start(self):
        # scrollVal = Text(text=str(memoryScroll.get_value())) \
        #     .add_updater(lambda dn: dn.become(Text(str(memoryScroll.get_value())))) \
        #     .move_to([-2,2,0])
        # self.add(scrollVal)
        self.memTape = Tape(self.engine.memory, 18, offsetY=0.5, pointerQueue=self.shiftQueue).move_to(ORIGIN)
        self.instrTape = Tape(self.engine.instructions, 18, offsetY=-2, pointerQueue=self.instrQueue).move_to(ORIGIN)
        self.inputText = InputText(self.engine.input)
        self.outputText = OutputText(self.engine.output)
        self.instrLabel = Text('Instructions', font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR).next_to(DOWN * 1.2 + LEFT * 7, RIGHT)
        self.memLabel = Text('Memory', font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR).next_to(UP * 1.2 + LEFT * 7, RIGHT)
        self.add(self.memTape, self.instrTape, self.inputText, self.outputText, self.instrLabel, self.memLabel)

    def shift(self, pos):
        self.memTape.pointerColor = self.memTape.defaultPointerColor
        self.play(self.memTape.moveArrow(pos), run_time=0.1)

    def instruction(self, pos):
        self.play(self.instrTape.moveArrow(pos), run_time=self.instrTime)

    def addition(self):
        self.memTape.pointerColor = '#5cfa4d'
        self.memTape.updateText()
        self.wait(0.1)

    def subtraction(self):
        self.memTape.pointerColor = '#f7350a'
        self.memTape.updateText()
        self.wait(0.1)

    def enable(self):
        self.instrTape.setColors({ '#': GRAY_E })

    def disable(self):
        self.instrTape.setColors({ c:GRAY_E for c in ['+','-','>','<','.',',','+','#','|']})

    def readInput(self, inpP):
        self.memTape.pointerColor = self.memTape.defaultPointerColor
        self.inputText.shiftInput(inpP+1)
        text = Text(str(self.engine.input[inpP]), font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        text.move_to(self.inputText.topLeft)
        self.play(text.animate.shift(self.memTape.absoluteArrowPosition() - self.inputText.topLeft), run_time=0.5)
        self.remove(text)
        self.memTape.updateText()

    def printOutput(self, output):
        self.memTape.pointerColor = self.memTape.defaultPointerColor
        text = Text(str(output), font_size=DEFAULT_FONT_SIZE * TEXT_SIZE_FACTOR)
        text.move_to(self.memTape.absoluteArrowPosition())
        # text.generate_target()
        # text.target(self.outputText.inputValues)
        self.play(text.animate.shift(self.outputText.topRight - self.memTape.absoluteArrowPosition()), run_time=0.5)
        self.remove(text)
        self.outputText.printOutput()

    def end(self):
        self.instruction(self.engine.instP)
        self.wait(0.4)
        
class DummyAnimation:
    def __init__(self) -> None:
        self.shiftQueue = deque()
        self.instrQueue = deque()

    def start(self):
        pass

    def shift(self, pos):
        self.shiftQueue.append(pos)

    def instruction(self, pos):
        self.instrQueue.append(pos)

    def addition(self):
        pass

    def subtraction(self):
        pass

    def enable(self):
        pass
        
    def disable(self):
        pass

    def readInput(self, inpP):
        pass

    def printOutput(self, output):
        pass

    def end(self):
        pass