from manim import *
import numpy as np


class VideoScene(Scene):
    def construct(self):
        self.next_section(skip_animations=False)
        intro_text = Text("How does TikTok decide your FYP?")
        self.add(intro_text)
        self.wait(1)
        self.remove(intro_text)

        self.next_section("information collection", skip_animations=False)
        # TODO
        self.wait()

        self.next_section("user-item matrix", skip_animations=False)
        self.show_matrix()

    def show_matrix(self):
        matrix_size = (5, 4)

        poss_vals = list(range(6))
        poss_vals_prob = np.array([20] + [1]*5) / 25
        dummy_vals = np.random.choice(poss_vals, matrix_size, p=poss_vals_prob)
        for vals in dummy_vals:
            # ensure that every row has at least one value
            vals[np.random.randint(len(vals))] = np.random.randint(1, 5)
        for i in range(matrix_size[1]):
            # ensure that every column has at least one value
            dummy_vals[np.random.randint(matrix_size[0])][i] = np.random.randint(1, 5)
        poss_objs = [(Text(str(i)) if i > 0 else Text(" ")) for i in poss_vals]
        dummy_objs = [list(map(lambda v : poss_objs[v].copy(), vs)) for vs in dummy_vals]
        
        # TODO: extend the table with Mobject images at the left and top

        table = MobjectTable(dummy_objs, include_outer_lines=False)
        self.add(table)
        self.wait(1)
        self.remove(table)
