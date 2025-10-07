from manim import *
import numpy as np

SCALE_FACTOR = 1

# Adjust vertical video frame
tmp_pixel_height = config.pixel_height
config.pixel_height = config.pixel_width
config.pixel_width = tmp_pixel_height

config.frame_height = config.frame_height / SCALE_FACTOR  # or 5.5 if you want it even tighter
config.frame_width = config.frame_height * 9 / 16
FRAME_HEIGHT = config.frame_height
FRAME_WIDTH = config.frame_width

from manim import *

class TrigAllInOne(Scene):
    def construct(self):
        tag = Text("@themathsociety", font_size=16, font="rise jeans").to_edge(DOWN, buff=0.7)
        self.add(tag)

        question = MathTex(r"\boldsymbol{f(x)} = \frac{\boldsymbol{12}}{\sqrt{\boldsymbol{x}}} \quad \textbf{and} \quad \boldsymbol{g(x)} = \boldsymbol{3}( \boldsymbol{2x} + \boldsymbol{1})", font_size=16)
        self.play(Create(question, run_time=3))
        self.play(question.animate.shift(UP * 2.5))
        a = Tex(r"(a) Find g(5)", font_size=16)
        self.wait(1)
        self.play(Create(a.next_to(question, DOWN)))
        self.wait(1)
        step1 = Tex(r"g(5) = 3(2 x 5 + 1)", font_size=16)
        step2 = Tex(r"= 3 x 11 = 33", font_size=16, color=BLUE)
        self.play(Create(step1.next_to(a, DOWN),run_time=2))
        self.wait(1)
        self.play(Create(step2.next_to(step1, DOWN), run_time=2))

        b = Tex(r"(b) Find gf(9)", font_size=16)
        self.wait(1)
        self.play(Create(b.next_to(step2, DOWN)))
        self.wait(1)
        line1 = MathTex(r"f(9) = \frac{12}{\sqrt{9}} = \frac{12}{3} = 4", font_size=16)
        line2 = MathTex(r"g(4) = 3(2(4) + 1)", font_size=16)
        line3 = MathTex(r"= 3(9) = 27", font_size=16, color=BLUE)
        self.play(Create(line1.next_to(step2, DOWN, buff=0.5), run_time=2))
        self.wait(1)
        self.play(Create(line2.next_to(line1, DOWN), run_time=2))
        self.wait(1)
        self.play(Create(line3.next_to(line2, DOWN), run_time=2))
        self.wait(1)

        c = Tex(r"(c) Find g–1(6)", font_size=16)
        self.wait(1)
        self.play(Create(c.next_to(line3, DOWN)))
        self.wait(1)
        line1c = Tex("Input for inverse function = output for original function", font_size=16)
        line2c = MathTex(r"6 = 3(2x + 1)", font_size=16)
        line3c = MathTex(r"6 = 6x + 3", font_size=16)
        line4c = MathTex(r"3 = 6x", font_size=16)
        line5c = MathTex(r"x = \frac{1}{2}", font_size=16, color=BLUE)
        self.play(Create(line1c.next_to(line3, DOWN, buff=0.5), run_time=2))
        self.wait(1)
        self.play(Create(line2c.next_to(line1c, DOWN), run_time=2))
        self.wait(1)
        self.play(Create(line3c.next_to(line2c, DOWN), run_time=2))
        self.wait(1)
        self.play(Create(line4c.next_to(line3c, DOWN), run_time=2))
        self.wait(1)
        self.play(Create(line5c.next_to(line4c, DOWN), run_time=2))


