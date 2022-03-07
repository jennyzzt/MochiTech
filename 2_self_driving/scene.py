from manim import *
import cv2
import numpy as np


class VideoScene(Scene):
    def construct(self):
        self.next_section(skip_animations=False)
        intro_text = Text("How do self-driving cars work?")
        self.play(Write(intro_text))
        self.wait()
        self.clear()

        self.next_section("overall architecture", skip_animations=False)
        # add car cameras view video
        cap = cv2.VideoCapture("./scene_images/car_cameras_view.mp4")
        # TODO: add start counter
        progress_length = 2  # seconds
        progress = 0  # seconds
        frame_length = 0.1  # seconds
        frame_img = None
        flag = True
        while flag and progress < progress_length:
            flag, frame = cap.read()
            if flag:
                if frame_img:
                    self.remove(frame_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_img = ImageMobject(frame)
                self.add(frame_img)
                self.wait(frame_length)
                progress += frame_length
        cap.release()
        # vision network
        self.play(frame_img.animate.scale(0.3).to_edge(LEFT).shift(UP * 2))
        vision_net_text = Text("Vision \nNetwork").scale(0.5).next_to(frame_img, DOWN).shift(DOWN)
        vision_net_box = SurroundingRectangle(vision_net_text, color=BLUE, buff=MED_LARGE_BUFF)
        cameraview_to_visionnet_arrow = Arrow(start=frame_img.get_edge_center(DOWN), end=vision_net_box.get_edge_center(UP), buff=0.0)
        self.play(Create(cameraview_to_visionnet_arrow), run_time=0.5)
        self.play(Create(vision_net_box))
        self.play(Write(vision_net_text))
        # vision network output
        vector_space_img = ImageMobject("./scene_images/vector_space.png").scale(0.5).next_to(vision_net_box, RIGHT).shift(RIGHT * 0.1 + UP * 0.7)
        vector_space_text = Text("Vector \nSpace").scale(0.4).next_to(vector_space_img, UP).align_to(vector_space_img, LEFT)
        features_img = ImageMobject("./scene_images/intermediate_features.png").scale(0.6).next_to(vision_net_box, RIGHT).shift(RIGHT * 0.1 + DOWN * 1.3)
        features_text = Text("Intermediate \nFeatures").scale(0.4).next_to(features_img, UP).align_to(features_img, LEFT)
        self.add(vector_space_img, vector_space_text)
        self.wait()
        self.add(features_img, features_text)
        self.wait()
        # neural network planner
        nn_planner_text = Text("Neural Net \nPlanner").scale(0.5).next_to(vision_net_box, RIGHT).shift(RIGHT * 3)
        nn_planner_box = SurroundingRectangle(nn_planner_text, color=GREEN, buff=MED_LARGE_BUFF)
        visionnet_to_nnplanner_arrow = Arrow(start=vision_net_box.get_edge_center(RIGHT), end=nn_planner_box.get_edge_center(LEFT), buff=0.0)
        self.play(Create(visionnet_to_nnplanner_arrow), run_time=0.5)
        self.play(Create(nn_planner_box))
        self.play(Write(nn_planner_text))
        # control system
        control_text = Text("Control \nSystem").scale(0.5).next_to(nn_planner_box, RIGHT).shift(RIGHT * 2)
        control_box = SurroundingRectangle(control_text, color=RED, buff=MED_LARGE_BUFF)
        nnplanner_to_control_arrow = Arrow(start=nn_planner_box.get_edge_center(RIGHT), end=control_box.get_edge_center(LEFT), buff=0.0)
        trajectory_text = Text("Trajectory").scale(0.4).next_to(nnplanner_to_control_arrow, UP)
        self.add(trajectory_text)
        self.play(Create(nnplanner_to_control_arrow), run_time=0.5)
        self.play(Create(control_box))
        self.play(Write(control_text))
        # control car
        car_img = ImageMobject("./scene_images/car.png").scale(0.2).next_to(control_box, UP).shift(UP)
        control_to_car_arrow = Arrow(start=control_box.get_edge_center(UP), end=car_img.get_edge_center(DOWN), buff=0.0)
        steer_text = Text("Steering \n& Acceleration").scale(0.4).next_to(control_to_car_arrow, RIGHT)
        self.play(Create(control_to_car_arrow), run_time=0.5)
        self.add(steer_text)
        self.add(car_img)
        self.wait()

        self.next_section("data from simulation", skip_animations=False)
        # animate car moving
        self.play(car_img.animate.shift(LEFT * 8), run_time=1.5)
        self.remove(
            frame_img,
            vision_net_text, vision_net_box, cameraview_to_visionnet_arrow,
            vector_space_img, vector_space_text, features_img, features_text,
            nn_planner_text, nn_planner_box, visionnet_to_nnplanner_arrow,
            control_text, control_box, nnplanner_to_control_arrow, trajectory_text,
            control_to_car_arrow, steer_text,
        )
        self.wait()
        # many road pictures
        road_imgs = [ImageMobject(f"./scene_images/road{i}.png").scale(0.2) for i in range(6)]
        added_road_imgs = []
        for i in range(20):
            x_adjust = (np.random.rand()-0.5) * 9
            y_adjust = (np.random.rand()-0.7) * 5
            img = road_imgs[i % 6].copy().shift(RIGHT * x_adjust + UP * y_adjust)
            added_road_imgs.append(img)
            self.add(img)
            self.wait(0.2)
        added_road_imgs_grp = Group(*added_road_imgs)
        # create dataset title
        create_text = Title("Create the Data!")
        self.play(Create(create_text), FadeOut(car_img))
        self.wait()
        # rare scene video
        self.play(FadeOut(added_road_imgs_grp))
        cap = cv2.VideoCapture("./scene_images/rare_scene.mp4")
        # TODO: change the parameters
        progress_length = 2  # seconds
        progress = 0  # seconds
        frame_length = 0.5  # seconds
        frame_img = None
        flag = True
        while flag and progress < progress_length:
            flag, frame = cap.read()
            if flag:
                if frame_img:
                    self.remove(frame_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_img = ImageMobject(frame)
                self.add(frame_img)
                self.wait(frame_length)
                progress += frame_length
        cap.release()
        rare_scene_text = Text("Prepare for the most unexpected situations").scale(0.5).next_to(frame_img, DOWN)
        self.play(Write(rare_scene_text))

        self.next_section("creation of simulation", skip_animations=False)
        create_sim_title = Title("High-Quality Representaiton of the Real World")
        self.play(ReplacementTransform(create_text, create_sim_title), FadeOut(rare_scene_text))
        self.remove(frame_img)
        # list of simulation creation notes
        point1_text = Text("1. Accurate sensor simulation").scale(0.5).next_to(create_sim_title, DOWN).to_edge(LEFT).shift(RIGHT + DOWN * 0.5)
        point2_text = Text("2. Diverse actors and locations").scale(0.5).next_to(point1_text, DOWN).align_to(point1_text, LEFT).shift(DOWN * 0.5)
        point3_text = Text("3. Scalable scenario generation").scale(0.5).next_to(point2_text, DOWN).align_to(point2_text, LEFT).shift(DOWN * 0.5)
        point4_text = Text("4: Scenario reconstruction (of failures)").scale(0.5).next_to(point3_text, DOWN).align_to(point3_text, LEFT).shift(DOWN * 0.5)
        # point 1 animations
        self.play(Write(point1_text))
        self.wait(2.0)
        view_img = ImageMobject("./scene_images/road0.png").scale(0.5).shift(RIGHT * 2 + DOWN * 2)
        self.play(GrowFromCenter(view_img))
        self.wait(2.0)
        camera_img = ImageMobject("./scene_images/spy-camera.png").scale(0.5).shift(RIGHT * 4 + UP)
        self.play(SpinInFromNothing(camera_img))
        self.wait()
        camera_view_line1 = Line(camera_img.get_edge_center(LEFT), view_img.get_corner(UP + LEFT))
        camera_view_line2 = Line(camera_img.get_edge_center(RIGHT), view_img.get_corner(UP + RIGHT))
        self.play(Create(camera_view_line1), Create(camera_view_line2))
        self.wait(2.0)
        # clear point 1 animations
        self.remove(view_img, camera_img, camera_view_line1, camera_view_line2)
        self.wait()
        # point 2 animations
        self.play(Write(point2_text))
        self.wait()
        car_imgs = Group(*[ImageMobject(f"./scene_images/car{i}.png").scale(0.45) for i in range(3)]).arrange(DOWN, buff=0.1)
        people_imgs = Group(*[ImageMobject(f"./scene_images/people{i}.png").scale(0.35) for i in range(3)]).arrange(DOWN, buff=0.2)
        scene_imgs = Group(*[ImageMobject(f"./scene_images/road{i}.png").scale(0.2) for i in range(3)]).arrange(DOWN, buff=0.2)
        diverse_imgs = Group(car_imgs, people_imgs, scene_imgs).arrange(RIGHT, buff=0.3).next_to(create_sim_title, DOWN).to_edge(RIGHT)
        self.play(ShowIncreasingSubsets(car_imgs))
        self.wait()
        self.play(ShowIncreasingSubsets(people_imgs))
        self.wait()
        self.play(ShowIncreasingSubsets(scene_imgs))
        self.wait(2.0)
        # clear point 2 animations
        self.remove(*car_imgs, *people_imgs, *scene_imgs)
        self.wait()
        # point 3 animations
        self.play(Write(point3_text))
        algo_img = ImageMobject("./scene_images/algorithm.png").scale(0.6).shift(RIGHT * 2)
        artist_img = ImageMobject("./scene_images/paint.png").scale(0.6).next_to(algo_img, RIGHT)
        cross = Cross(color=RED, stroke_width=10.0).move_to(artist_img.get_center())
        self.play(GrowFromCenter(algo_img), GrowFromCenter(artist_img))
        self.play(SpinInFromNothing(cross))
        self.wait(2.0)
        # clear point 3 animations
        self.remove(algo_img, artist_img, cross)
        self.wait()
        # point 4 animations
        self.play(Write(point4_text))
        road_img = ImageMobject("./scene_images/road0.png").scale(0.3).next_to(create_sim_title, DOWN).to_edge(RIGHT).shift(LEFT)
        accident_img = ImageMobject("./scene_images/accident.png").scale(0.3).move_to(road_img.get_center())
        self.play(GrowFromCenter(road_img))
        self.wait()
        self.add(accident_img)
        road_img1 = road_img.copy().next_to(road_img, DOWN)
        road_img2 = road_img.copy().next_to(road_img1, DOWN)
        self.play(GrowFromCenter(road_img1))
        self.play(GrowFromCenter(road_img2))
        self.wait()
        accident1_img = ImageMobject("./scene_images/accident1.png").scale(0.3).move_to(road_img1.get_center())
        accident2_img = ImageMobject("./scene_images/accident2.png").scale(0.3).move_to(road_img2.get_center())
        self.add(accident1_img)
        self.wait()
        self.add(accident2_img)
        self.wait(2.0)
