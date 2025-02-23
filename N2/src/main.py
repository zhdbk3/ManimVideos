#
# Created by 着火的冰块nya(zhdbk3) on 2025/2/23
#

from manim import *


class N2(ThreeDScene):
    def construct(self):
        Tex.set_default(font_size=144)

        # 若直接写在一个 Tex 中，则无法对齐，所以分开来
        lone_pair_1 = Tex(':')
        atom_1 = Tex('N').next_to(lone_pair_1)
        # 用两个 \vdots 模拟三键
        vdots_1 = Tex(r'\vdots').next_to(atom_1)
        vdots_2 = Tex(r'\vdots').next_to(vdots_1)
        atom_2 = Tex('N').next_to(vdots_2)
        lone_pair_2 = Tex(':').next_to(atom_2)

        VGroup(lone_pair_1, atom_1, vdots_1, vdots_2, atom_2, lone_pair_2).center()
        # 将电子式旋转到 xOz 平面上，这样下面旋转相机时仅用调整 theta 即可
        VGroup(atom_1, atom_2).rotate(PI / 2, RIGHT)
        # 但是电子由下面的 add_fixed_orientation_mobjects 保证方向，所以不需要旋转

        self.set_camera_orientation(PI / 2)
        self.add(atom_1, atom_2)
        self.add_fixed_orientation_mobjects(lone_pair_1, lone_pair_2, vdots_1, vdots_2)
        self.add_sound('bgm.wav')

        self.move_camera(theta=-PI, zoom=2, frame_center=lone_pair_1, run_time=3)
        self.move_camera(theta=-3 / 2 * PI, zoom=1, frame_center=ORIGIN, run_time=3)
        self.wait(1)
        self.move_camera(theta=-TAU, zoom=2, frame_center=lone_pair_2, run_time=3)
        self.move_camera(theta=-PI / 2 - TAU, zoom=1, frame_center=ORIGIN, run_time=3)

        # 剪映 bug，不等待后面一段会消失
        self.wait(11)
