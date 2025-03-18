#
# Created by 着火的冰块nya(zhdbk3) on 2025/3/18
#

from manim import *
import numpy as np


class AngleMark(VGroup):
    def __init__(self, vertex: np.ndarray | Mobject, initial_side: Line, terminal_side: Line, label: str,
                 r: float | int = 0.55, always_positive: bool = True, add_tip: bool = False):
        """
        一个角的小圆弧标记和名字标记，当角的大小和位置发生变化时，小圆弧和名字会自动调整
        :param vertex: 角的顶点
                       若传入一个坐标，那它就是定点
                       若传入一个 mobj，那顶点会跟随其移动
        :param initial_side: 始边，应指向角延伸的方向
        :param terminal_side: 终边，应指向角延伸的方向
        :param label: 角的名字，应符合 MathTex 语法
        :param r: 小圆弧的半径
        :param always_positive: 是否永远为正角
        :param add_tip: 是否加上表示方向的小箭头
        """
        self.vertex = vertex
        self.initial_side = initial_side
        self.terminal_side = terminal_side
        self.label = MathTex(label)
        self.r = r
        self.always_positive = always_positive
        self.add_tip = add_tip
        self.arc = Arc()
        self.updater(self)
        super().__init__(self.arc, self.label)

    def updater(self, _: Mobject) -> None:
        """自动调整小圆弧和标签"""
        try:
            # 调整小圆弧
            start_angle = self.initial_side.get_angle()
            end_angle = self.terminal_side.get_angle()
            angle = end_angle - start_angle
            if self.always_positive:
                angle %= TAU
            arc = Arc(self.r, start_angle, angle, arc_center=self.vertex)
            if self.add_tip:
                arc.add_tip(tip_length=0.2, tip_width=0.2 * 2 / 3 * np.sqrt(3))
            self.arc.become(arc)
            # 调整标签
            direction = start_angle + angle / 2
            vec = np.array((np.cos(direction), np.sin(direction), 0))  # 标签相对于圆心的单位方向向量
            self.label.move_to(self.vertex + vec * (self.r + 0.3))
        except ValueError:  # 两线平行时会报此错误
            pass

    def start_updater(self) -> None:
        """开启 updater，较吃性能，及时关闭"""
        self.add_updater(self.updater)

    def stop_updater(self) -> None:
        """关闭 updater"""
        self.remove_updater(self.updater)
