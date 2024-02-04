from manim import *
FRAME_WIDTH=8
class ScrollingTape(Scene):
    def construct(self):
        nums = list(range(100))
        max_boxes = 10
        box_width = 1.5
        
        tape = VGroup()
        for i in range(max_boxes):
            box = Square()
            label = Integer(0).move_to(box.get_center())
            box.add(label)
            tape.add(box)
            
        tape.arrange(RIGHT, buff=0)
        
        def update_tape(tape, dt):
            for box, i in zip(tape, range(len(tape))):
                if box.get_right()[0] < -FRAME_WIDTH:
                    box.move_to(tape[-1].get_right() + RIGHT*box_width)
                    label = Integer(nums[i]).move_to(box.get_center())
                    box.set_submobjects([label])
                else:
                    box.shift(LEFT*box_width*dt) 
                    
        tape.add_updater(update_tape)
        
        self.add(tape)
        self.wait(10)