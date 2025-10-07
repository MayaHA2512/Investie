from manim import *
import numpy as np

SCALE_FACTOR = 1

tmp_pixel_height = config.pixel_height
config.pixel_height = config.pixel_width
config.pixel_width = tmp_pixel_height

config.frame_height = config.frame_height / SCALE_FACTOR
config.frame_width = config.frame_height * 9 /16
FRAME_HEIGHT= config.frame_height
FRAME_WIDTH = config.frame_width

class TikTok(Scene):
    def setup(self, add_border =True):
        if add_border:
            self.border = Rectangle(
                width=FRAME_WIDTH,
                height=FRAME_HEIGHT,
                color=WHITE
            )

    def construct(self):
        # Title and TikTok tag
        title = Text("Q: Expand and simplify: (2x - 3)(x + 4)", font_size=36)
        tag = Text("@themathsociety", font_size=24).to_edge(DOWN, buff=0.4)
        self.play(Write(title))
        self.add(tag)
        self.wait(1)

        # Shift up to make space
        title.to_edge(UP, buff=1.2)

        # Incorrect student working
        wrong_working = Tex(
            "2x \\times x = 2x^2 \\\\ -3 \\times 4 = -12 \\\\ \\text{Answer: } 2x^2 - 12",
            font_size=40
        )
        wrong_working.next_to(title, DOWN, buff=1)
        self.play(Write(wrong_working))
        self.wait(1.5)

        # Mark as wrong
        cross = Cross(wrong_working, color=RED)
        self.play(Create(cross))
        self.wait(1)

        # Fade out mistake
        self.play(FadeOut(wrong_working), FadeOut(cross))
        self.wait(0.5)

        # Correct working
        correct_working = Tex(
            "2x \\times x = 2x^2 \\\\ 2x \\times 4 = 8x \\\\ -3 \\times x = -3x \\\\ -3 \\times 4 = -12",
            font_size=40
        )
        correct_working.next_to(title, DOWN, buff=1)
        self.play(Write(correct_working))
        self.wait(2)

        # Final simplification
        final_answer = Tex("2x^2 + 8x - 3x - 12 = 2x^2 + 5x - 12", font_size=42, color=GREEN)
        final_answer.next_to(correct_working, DOWN, buff=0.8)
        self.play(Write(final_answer))
        self.wait(2)

        # End
        self.play(FadeOut(correct_working), FadeOut(final_answer), FadeOut(title))
        self.wait(0.5)