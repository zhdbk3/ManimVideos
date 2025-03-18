#
# Created by 着火的冰块nya(zhdbk3) on 2025/3/18
#

from manim import *


class WithBackground(VGroup):
    def __init__(self, mobj: Mobject):
        """
        给对象添加一个黑色半透明的背景
        :param mobj: Mobject 对象
        """
        self.mobj = mobj
        self.background = Rectangle(BLACK, mobj.height, mobj.width, fill_opacity=0.5, stroke_width=0).move_to(mobj)
        super().__init__(self.background, self.mobj)
