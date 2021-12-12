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
        useritem_matrix = self.create_ui_matrix()
        self.add(useritem_matrix.scale(0.7))
        self.play(FadeIn(Text("User-Item Matrix").scale(0.7).next_to(useritem_matrix, UP, buff=0.5)))
        self.wait(1)

    def create_ui_matrix(self):
        matrix_size = (5, 4)

        # create table with example values
        poss_vals = list(range(6))
        # # if matrix is bigger and more entries are needed
        # poss_vals_prob = np.array([20] + [1]*5) / 25
        # dummy_vals = np.random.choice(poss_vals, matrix_size, p=poss_vals_prob)
        dummy_vals = np.zeros(matrix_size)
        for vals in dummy_vals:
            # ensure that every row has at least one value
            vals[np.random.randint(len(vals))] = np.random.randint(1, 5)
        for i in range(matrix_size[1]):
            # ensure that every column has at least one value
            dummy_vals[np.random.randint(matrix_size[0])][i] = np.random.randint(1, 5)
        poss_objs = [(Text(str(i)) if i > 0 else Text(" ")) for i in poss_vals]
        dummy_objs = [list(map(lambda v : poss_objs[int(v)].copy(), vs)) for vs in dummy_vals]
        table = MobjectTable(dummy_objs, include_outer_lines=False).scale(0.7)

        # add row images
        user_img = ImageMobject("./scene_images/user.png").scale(0.15)
        row_img = user_img.copy()
        for _ in range(matrix_size[0] - 1):
            row_img.add(user_img.copy().next_to(row_img, DOWN, buff=0.4))
        row_img.next_to(table, LEFT).align_to(table, UP)
        # add column images
        poss_imgs_fn = ["game", "dance", "cat", "tree"]
        poss_imgs = [ImageMobject(f"./scene_images/{fn}.png").scale(0.25) for fn in poss_imgs_fn]
        col_img = poss_imgs[0].copy()
        for i in range(1, len(poss_imgs)):
            col_img.add(poss_imgs[i].copy().next_to(col_img, RIGHT, buff=0.25))
        col_img.next_to(table, UP).align_to(table, LEFT)

        # group table and images together
        useritem_matrix = Group(table, row_img, col_img)
        return useritem_matrix
