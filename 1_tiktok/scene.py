from manim import *
import numpy as np


class VideoScene(Scene):
    def construct(self):
        self.next_section(skip_animations=False)
        intro_text = Text("How does TikTok decide your FYP?")
        self.play(Write(intro_text))
        self.wait()
        self.clear()

        self.next_section("information collection", skip_animations=False)
        # TODO
        tmp_text = Text("TODO: Brief description of information collection").scale(0.5)
        self.add(tmp_text)
        self.wait()
        self.clear()

        self.next_section("user-item matrix", skip_animations=False)
        # show user-item matrix
        useritem_matrix = self.create_ui_matrix()
        self.add(useritem_matrix.scale(0.6).shift(DOWN))
        uim_text = Text("User-Item Matrix").scale(0.6).next_to(useritem_matrix, UP, buff=1.5)
        self.play(Write(uim_text))
        self.wait()
        # brace users
        br_users = Brace(useritem_matrix.submobjects[1], LEFT)
        text_users = Text("users").scale(0.6).next_to(br_users, LEFT)
        self.add(br_users, text_users)
        self.wait()
        # brace items
        br_items = Brace(useritem_matrix.submobjects[2], UP)
        text_items = Text("items").scale(0.6).next_to(br_items, UP)
        self.add(br_items, text_items)
        self.wait()
        # box table contents
        box_table = SurroundingRectangle(useritem_matrix.submobjects[0], color=YELLOW)
        self.play(Create(box_table))
        self.wait()
        self.remove(box_table)
        self.wait()
        # highlight known ratings
        anims = []
        for entry in useritem_matrix.submobjects[0].get_entries():
            if entry.text != "?":
                entry.set_color(RED)
        self.wait()
        known_text = Text("known ratings R", t2c={"[-3:]": RED}).scale(0.6).next_to(useritem_matrix, RIGHT)
        self.play(Write(known_text))
        # specify predicted ratings
        for entry in useritem_matrix.submobjects[0].get_entries():
            if entry.text == "?":
                entry.set_color(BLUE)
        predicted_text = Text("predicted ratings P", t2c={"[-3:]": BLUE}).scale(0.6).next_to(known_text, DOWN).align_to(known_text, LEFT)
        self.play(Write(predicted_text))
        self.wait()
        self.clear()

        self.next_section("deep collaborative filtering", skip_animations=False)
        title_text = Text("Deep Collaborative Filtering")
        self.play(Write(title_text))
        self.play(title_text.animate.to_edge(UP))
        # show user-item matrix
        self.add(useritem_matrix)
        self.add(uim_text.next_to(useritem_matrix, UP))
        # user-user similarity
        box_users = SurroundingRectangle(useritem_matrix.submobjects[1], color=YELLOW)
        uu_text = Text("user-user similarity").scale(0.6).next_to(useritem_matrix, RIGHT)
        self.play(Create(box_users), Write(uu_text))
        self.wait()
        # item-item similarity
        box_items = SurroundingRectangle(useritem_matrix.submobjects[2], color=YELLOW)
        ii_text = Text("item-item similarity").scale(0.6).next_to(uu_text, DOWN).align_to(known_text, LEFT)
        self.play(Create(box_items), Write(ii_text))
        self.wait()

        self.next_section("user based models", skip_animations=False)
        self.remove(box_items, ii_text)
        self.play(uu_text.animate.move_to(ii_text))
        uum_text = Text("User-based models", weight=BOLD).scale(0.6).next_to(uu_text, UP)
        self.play(Write(uum_text))
        self.wait()
        # remove user-item matrix
        self.remove(box_users, useritem_matrix, uim_text)
        self.wait()
        # add two users thinking of the same thing
        user1_img = ImageMobject("./scene_images/user.png").scale(0.4).shift(DOWN + LEFT * 3)
        user2_img= user1_img.copy().shift(RIGHT * 3)
        thought_img = ImageMobject("./scene_images/thought.png").scale(0.5).shift(UP + LEFT * 1.5)
        tree_img = ImageMobject("./scene_images/tree.png").scale(0.3).shift(UP + LEFT * 1.5)
        self.add(user1_img, user2_img, thought_img, tree_img)
        self.wait()
        thought_points1 = [
            Dot(point=ORIGIN+LEFT*3+UR*0.25, radius = 0.08),
            Dot(point=ORIGIN+UL*0.25, radius=0.08)
        ]
        self.add(*thought_points1)
        self.wait(0.5)
        thought_points2 = [
            Dot(point=ORIGIN+LEFT*3+UR*0.5, radius = 0.1),
            Dot(point=ORIGIN+UL*0.5, radius=0.1)
        ]
        self.add(*thought_points2)
        self.wait(0.5)
        self.remove(user2_img, thought_img, tree_img, *thought_points1, *thought_points2)
        # unknown user A rating
        userA_img = ImageMobject("./scene_images/user.png").scale(0.2).shift(LEFT * 4)
        userA_text = Text("User A", color=YELLOW).scale(0.6).next_to(userA_img, UP)
        userA = Group(userA_img, userA_text)
        self.play(ReplacementTransform(user1_img, userA_img))
        self.add(userA_text)
        userA_rating_text = Text("?", color=BLUE).next_to(userA, DOWN)
        cactus_img = ImageMobject("./scene_images/cactus.png").scale(0.25).next_to(userA_rating_text, LEFT)
        self.play(Write(userA_rating_text), FadeIn(cactus_img))
        # users similar to user A
        user_img = ImageMobject("./scene_images/user.png").scale(0.2)
        user_peers_img = user_img.next_to(userA_img, RIGHT, buff=0.8).copy()
        for _ in range(3):
            user_peers_img.add(user_img.copy().next_to(user_peers_img, RIGHT))
        br_user_peers = Brace(user_peers_img, UP)
        user_peers_text = Text("similar interests").scale(0.6).next_to(br_user_peers, UP)
        self.play(ShowIncreasingSubsets(user_peers_img), Write(user_peers_text))
        self.add(br_user_peers)
        self.wait()
        # ratings of the peers
        user_peers_ratings = [3, 4, 5, 4]
        user_peers_ratings_text = Text(str(user_peers_ratings[0]), color=RED).next_to(user_peers_img, DOWN).align_to(user_peers_img, LEFT).shift(RIGHT*0.2)
        for i in range(1, len(user_peers_ratings)):
            user_peers_ratings_text.add(Text(str(user_peers_ratings[i]), color=RED).next_to(user_peers_img.submobjects[i-1], DOWN))
        self.play(ShowIncreasingSubsets(user_peers_ratings_text))
        self.wait()
        # predict unknown user A rating
        user_peers_ratings_text_box = SurroundingRectangle(user_peers_ratings_text, color=YELLOW, buff=0.2)
        self.play(Create(user_peers_ratings_text_box))
        new_userA_rating_text = Text(str(int(sum(user_peers_ratings)/len(user_peers_ratings))), color=BLUE, weight=BOLD).move_to(userA_rating_text)
        self.play(ReplacementTransform(userA_rating_text, new_userA_rating_text))
        self.play(Uncreate(user_peers_ratings_text_box))
        self.wait()

        self.next_section("item based models", skip_animations=False)
        # remove user-based model stuff
        self.remove(userA, userA_img, userA_text, user1_img, user_peers_img, br_user_peers, user_peers_text, user_peers_ratings_text, userA_rating_text, new_userA_rating_text, cactus_img)
        self.wait()
        # show user-item matrix
        self.add(useritem_matrix, uim_text.next_to(useritem_matrix, UP))
        self.wait()
        # item-item similarity
        iim_text = Text("Item-based models", weight=BOLD).scale(0.6).next_to(ii_text, UP)
        self.play(Create(box_items), ReplacementTransform(uu_text, ii_text), ReplacementTransform(uum_text, iim_text))
        self.wait()
        # remove user-item matrix
        self.remove(box_items, useritem_matrix, uim_text)
        self.wait()
        # unknown item X rating
        itemX_img = ImageMobject("./scene_images/cactus.png").scale(0.25).shift(LEFT * 4)
        itemX_text = Text("Item X", color=YELLOW).scale(0.6).next_to(itemX_img, UP)
        itemX = Group(itemX_img, itemX_text)
        self.add(itemX)
        itemX_rating_text = Text("?", color=BLUE).next_to(itemX, DOWN)
        user_img = ImageMobject("./scene_images/user.png").scale(0.2).next_to(itemX_rating_text, LEFT)
        self.play(Write(itemX_rating_text), FadeIn(user_img))
        # items similar to item X
        item_peers_img = ImageMobject("./scene_images/plant0.png").scale(0.25).next_to(itemX_img, RIGHT, buff=0.7)
        for i in range(1, 4):
            item_peers_img.add(ImageMobject(f"./scene_images/plant{i}.png").scale(0.25).next_to(item_peers_img, RIGHT, buff=0.))
        br_item_peers = Brace(item_peers_img, UP)
        item_peers_text = Text("similar items").scale(0.6).next_to(br_item_peers, UP)
        self.play(ShowIncreasingSubsets(item_peers_img), Write(item_peers_text))
        self.add(br_item_peers)
        self.wait()
        # ratings of the peers
        item_peers_ratings = [4, 5, 2, 5]
        item_peers_ratings_text = Text(str(item_peers_ratings[0]), color=RED).next_to(item_peers_img, DOWN).align_to(item_peers_img, LEFT).shift(RIGHT*0.2)
        for i in range(1, len(item_peers_ratings)):
            item_peers_ratings_text.add(Text(str(item_peers_ratings[i]), color=RED).next_to(item_peers_img.submobjects[i-1], DOWN))
        self.play(ShowIncreasingSubsets(item_peers_ratings_text))
        self.wait()
        # predict unknown item X rating
        item_peers_ratings_text_box = SurroundingRectangle(item_peers_ratings_text, color=YELLOW, buff=0.2)
        self.play(Create(item_peers_ratings_text_box))
        new_itemX_rating_text = Text(str(int(sum(item_peers_ratings)/len(item_peers_ratings))), color=BLUE, weight=BOLD).move_to(itemX_rating_text)
        self.play(ReplacementTransform(itemX_rating_text, new_itemX_rating_text))
        self.play(Uncreate(item_peers_ratings_text_box))
        self.wait(2)

        self.next_section("advantages and disadvantages", skip_animations=False)
        # add back user-based stuff
        uu_text = Text("user-user similarity").scale(0.6).move_to(ii_text)
        uum_text = Text("User-based models", weight=BOLD).scale(0.6).move_to(iim_text)
        user_based_group = Group(userA, user_peers_img, br_user_peers, user_peers_text, user_peers_ratings_text, userA_rating_text, new_userA_rating_text, cactus_img, uum_text, uu_text)
        self.add(user_based_group.next_to(item_peers_ratings_text, DOWN).align_to(user_img, LEFT))
        self.wait(2)
        # remove item-based and user-based stuff
        self.remove(userA, user_peers_img, br_user_peers, user_peers_text, user_peers_ratings_text, userA_rating_text, new_userA_rating_text, cactus_img, ii_text,
                    itemX, item_peers_img, br_item_peers, item_peers_text, item_peers_ratings_text, itemX_rating_text, new_itemX_rating_text, user_img, uu_text)
        self.wait(2)
        # memory-based models
        mb_text = Text("Memory-based models", weight=BOLD).scale(0.8).next_to(title_text, DOWN)
        self.play(ReplacementTransform(Group(uum_text, iim_text), mb_text))
        self.wait()
        # advantages
        advan_text = Text("Advantages", color=YELLOW).scale(0.6).next_to(mb_text, DOWN).shift(LEFT * 3)
        self.play(Write(advan_text))
        self.wait()
        advan_list = BulletedList(
            "simple and intuitive",
            "easy to justify why a specific \\\item is recommended",
            "easy to interpret the outcome",
            font_size=35,
        ).next_to(advan_text, DOWN).align_to(advan_text, LEFT).shift(LEFT * 1.2)
        self.play(advan_list)
        self.wait()
        # disadvantages
        disadvan_text = Text("Disadvantages", color=YELLOW).scale(0.6).next_to(mb_text, DOWN).shift(RIGHT * 3)
        self.play(Write(disadvan_text))
        self.wait()
        disadvan_list = BulletedList(
            "grouping similar users or items \\\can be computationally costly",
            "limited coverage because of sparsity \\\of the user-item matrix",
            font_size=35,
        ).next_to(disadvan_text, DOWN).align_to(disadvan_text, LEFT).shift(LEFT * 1.2)
        self.add(disadvan_list)
        self.wait()

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
        poss_objs = [(Text(str(i)) if i > 0 else Text("?", color=BLACK)) for i in poss_vals]
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
