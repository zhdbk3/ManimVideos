#
# Created by 着火的冰块nya(zhdbk3) on 2025/3/18
#

import sys

from manim import *
from manim.typing import Point2DLike, Point3DLike, Point3D
import numpy as np

sys.path.append('../..')  # 为了可以找到位于项目根目录的 mobj 模块
from mobj import AngleMark

F2M_ORIGIN = np.array((-5.5, -1.5, 0))
F2M_ZOOM_RATIO = 0.5


def coord_f2m(f: Point2DLike | Point3DLike) -> Point3D:
    """
    f: figure
    m: Manim
    将图上的坐标转化为 Manim 坐标
    :param f: 图上坐标，可以直接传入二维的
    :return: 转换后的 Manim 坐标
    """
    # 统一转换为 np.ndarray
    f = np.array(f)
    # 若为二维坐标，添加 z = 0
    if f.size == 2:
        f = np.array((*f, 0))

    m = F2M_ORIGIN + f * F2M_ZOOM_RATIO
    return m  # type: ignore


def length_f2m(f: float) -> float:
    """将图上的长度转化为 Manim 中长度"""
    return f * F2M_ZOOM_RATIO


def align_baseline(left: MathTex, right: MathTex) -> None:
    """
    对齐两个 MathTex 的基线，会竖直移动 right，而 left 不变
    传入的 MathTex，应把等号用双大括号括起来，像这样：{{=}}
    为什么选用等号来对齐基线：因为它永远处在基线上
    """
    right.shift(UP * (left.get_part_by_tex('=').get_y() - right.get_part_by_tex('=').get_y()))


class SpreadAngle(Scene):
    def construct(self):
        Tex.set_default(font_size=36, tex_template=TexTemplateLibrary.ctex)

        condition = Tex(r'如图，$AB=3$，$BC=2$，$AC \perp CD$，$P$为射线$CD$上一点').to_corner(UL)
        question = Tex(r'当$CP$的长度为多少时，$\angle APB$取得最大值？').next_to(condition, DOWN, aligned_edge=LEFT)

        p_x = 10 ** 0.5

        a = coord_f2m((0, 5))
        b = coord_f2m((0, 2))
        c = coord_f2m((0, 0))
        d = coord_f2m((7, 0))
        p = Dot(coord_f2m((p_x, 0)), radius=0)
        ac = Line(a, c)
        cd = Line(c, d)
        pa = Line(p, a)
        pb = Line(p, b)
        a_label = MathTex('A').next_to(a, LEFT)
        b_label = MathTex('B').next_to(b, LEFT)
        c_label = MathTex('C').next_to(c, DL)
        d_label = MathTex('D').next_to(d, DOWN)
        p_label = MathTex('P').next_to(p, DOWN)
        data_2 = MathTex('2').next_to(coord_f2m((0, 1)), LEFT)
        data_3 = MathTex('3').next_to(coord_f2m((0, 3.5)), LEFT)
        theta = AngleMark(p, pa, pb, r'\theta')

        def updater(_: Mobject) -> None:
            p_label.next_to(p, DOWN)
            pa.become(Line(p, a))
            pb.become(Line(p, b))
            theta.updater(theta)

        self.play(
            Write(condition, run_time=2),
            Succession(
                AnimationGroup(
                    Create(VGroup(ac, cd)),
                    Write(VGroup(a_label, b_label, c_label, d_label))
                ),
                Write(VGroup(data_2, data_3)),
                AnimationGroup(
                    Create(VGroup(pa, pb, theta)),
                    Write(p_label)
                )
            )
        )
        self.wait(2)
        theta.add_updater(updater)
        self.play(
            Write(question, run_time=2),
            Succession(
                AnimationGroup(p.animate.move_to(coord_f2m((p_x - 3, 0)))),
                AnimationGroup(p.animate.move_to(coord_f2m((p_x + 3, 0)))),
                AnimationGroup(p.animate.move_to(coord_f2m((p_x, 0))))
                # 关于此 Succession 的奇怪写法
                # 1. 为什么不直接 shift？
                # 直接 shift 终点位置会有 bug
                # 它是以 Succession 开始前的位置为初位置计算的末位置，而不是以上一个 shift 完成后的位置为初位置
                # 2. 为什么要套一层 AnimationGroup？
                # Succession 在处理由 animate 创建的动画时会有 bug，只会播放第一个动画
                # 套一层 AnimationGroup 可以先把 _AnimationBuilder 转化为真正的 Animation，这样就能正常播放了
            )
        )
        theta.remove_updater(updater)
        self.wait(5)

        title_1 = Tex('1. 几何法（米勒圆）').next_to(question, DOWN).set_x(-1.2, LEFT)
        text_draw_circle = Tex(r'过点$A$、$B$作$\odot O$与$CD$相切与$P$').next_to(title_1, DOWN, aligned_edge=LEFT)
        text_angle_min_1 = Tex(r"那么在$CD$上任取一点$P'$\\都有$\angle APB \le \angle AP'B$",
                               tex_environment='flushleft').next_to(text_draw_circle, DOWN, aligned_edge=LEFT)
        text_angle_min_2 = (Tex(r"此时$\angle APB$取到最大")
                            .next_to(text_draw_circle, DOWN, aligned_edge=LEFT))
        text_connect_r = Tex('连接半径').next_to(text_angle_min_2, DOWN, aligned_edge=LEFT)
        text_draw_oh = Tex(r'过点$O$作$OH \perp AB$于$H$').next_to(text_connect_r)
        text_length = (Tex(r'$\displaystyle HB=\frac{3}{2}$，半径$\displaystyle r=\frac{7}{2}$')
                       .next_to(text_connect_r, DOWN, aligned_edge=LEFT))
        # “勾股”没有英文名么？“毕达哥拉斯”也太长了
        text_pythagorean = Tex('$OH^2+HB^2=r^2$').next_to(text_length, DOWN, aligned_edge=LEFT)
        text_answer = Tex(r'$\therefore CP=OH=\sqrt{10}$').next_to(text_pythagorean, DOWN, aligned_edge=LEFT)

        o = Dot(coord_f2m((p_x, 3.5)))
        p_prime = coord_f2m((5, 0))
        h = coord_f2m((0, 3.5))
        o_label = MathTex('O').next_to(o)
        p_prime_label = MathTex("P'").next_to(p_prime, DOWN)
        h_label = MathTex('H').next_to(h, UR, 0.1)
        circle = Circle(length_f2m(3.5), WHITE).move_to(coord_f2m((p_x, 3.5)))
        p_prime_a = Line(p_prime, a)
        p_prime_b = Line(p_prime, b)
        oa = DashedLine(o, a)
        ob = DashedLine(o, b)
        op = DashedLine(o, p)
        oh = DashedLine(o, h)
        rt_triangle = VGroup(Line(p1, p2, color=YELLOW) for p1, p2 in [(o, h), (h, b), (o, b)])

        self.play(Write(title_1))
        self.wait(2)
        self.play(Write(text_draw_circle, run_time=2), Create(VGroup(o, circle)), Write(o_label))
        self.wait(2)
        self.play(Write(text_angle_min_1, run_time=2), FadeIn(p_prime_label, p_prime_a, p_prime_b))
        self.wait(3)
        self.play(FadeOut(p_prime_label, p_prime_a, p_prime_b),
                  ReplacementTransform(text_angle_min_1, text_angle_min_2))
        self.wait(2)
        self.play(Write(text_connect_r), *[Create(r) for r in [oa, ob, op]])
        self.wait(2)
        self.play(Write(text_draw_oh, run_time=2), Create(oh), Write(h_label))
        self.wait(2)
        self.play(Write(text_length, run_time=2))
        self.wait(2)
        self.play(FadeIn(rt_triangle))
        self.wait()
        self.play(Write(text_pythagorean, run_time=2))
        self.wait(2)
        self.play(Write(text_answer, run_time=2))
        self.wait(5)
        self.play(FadeOut(text_draw_circle, text_angle_min_2, text_connect_r, text_draw_oh, text_length,
                          text_pythagorean, text_answer, rt_triangle, oa, ob, op, oh, h_label))
        self.wait(2)

        text_know_tan_sec = Tex('如果您知道切割线定理的话，这里还可以更快！').next_to(title_1, DOWN, aligned_edge=LEFT)
        text_tan_sec_eq = Tex(r'$CP^2=AB \cdot AC$').next_to(text_know_tan_sec, DOWN, aligned_edge=LEFT)
        text_answer = Tex(r'$\therefore CP=\sqrt{10}$').next_to(text_tan_sec_eq, DOWN, aligned_edge=LEFT)

        self.play(Write(text_know_tan_sec, run_time=2))
        self.wait(2)
        self.play(Write(text_tan_sec_eq, run_time=2))
        self.wait(2)
        self.play(Write(text_answer))
        self.wait(5)
        self.play(FadeOut(text_know_tan_sec, text_tan_sec_eq, text_answer, circle, o, o_label))
        self.wait(2)

        title_2 = Tex('2. 向量法').move_to(title_1, UL)
        text_establish_sys = Tex('以$C$为原点，建立如图所示的直角坐标系').next_to(title_2, DOWN, aligned_edge=LEFT)
        text_known_points = Tex('则$A(0,5)$，$B(0,2)$').next_to(text_establish_sys, DOWN, aligned_edge=LEFT)
        text_let_p = Tex('设$P(t,0)$，$t>0$').next_to(text_known_points, DOWN, aligned_edge=LEFT)
        text_vec = (Tex(r'则$\overrightarrow{PA}=(-t,5)$，$\overrightarrow{PB}=(-t,2)$')
                    .next_to(text_let_p, DOWN, aligned_edge=LEFT))

        axes = Axes((-2, 9), (-2, 7), 11, 9, axis_config={'tick_size': 0})
        axes.shift(F2M_ORIGIN - axes.get_origin()).scale(F2M_ZOOM_RATIO, about_point=F2M_ORIGIN)

        self.play(ReplacementTransform(title_1, title_2))
        self.wait(2)
        self.play(Write(text_establish_sys, run_time=2), Create(axes), Write(axes.get_axis_labels()))
        self.wait(2)
        self.play(Write(text_known_points, run_time=2))
        self.wait(2)
        self.play(Write(text_let_p, run_time=2))
        self.wait(2)
        self.play(Write(text_vec, run_time=2))
        self.wait(3)

        hidden_question = VGroup(condition, question, a_label, b_label, c_label, d_label, p_label,
                                 ac, cd, pa, pb, theta, data_2, data_3, title_2)
        hidden_process = VGroup(axes, axes.axis_labels, text_establish_sys, text_known_points, text_let_p)

        self.play(FadeOut(hidden_question, hidden_process), text_vec.animate.to_corner(UL))
        self.wait()

        text_let_theta = (Tex(r'设$\displaystyle\angle APB=\theta\in\left(0,\frac{\pi}{2}\right)$')
                          .next_to(text_vec, DOWN, aligned_edge=LEFT))
        MathTex.set_default(font_size=40)
        eq_1 = (MathTex(r'\cos\theta=\frac{\overrightarrow{PA}\cdot\overrightarrow{PB}}'
                        r'{\left|\overrightarrow{PA}\right|\left|\overrightarrow{PB}\right|}'
                        r'=\frac{t^2+10}{\sqrt{t^2+4}\sqrt{t^2+25}}')
                .next_to(text_let_theta, DOWN).set_x(0))
        eqs = [
            r'\cos^2\theta=\frac{\left(t^2+10\right)^2}{\left(t^2+4\right)\left(t^2+25\right)}',
            r'\cos^2\theta=\frac{t^4+20t^2+100}{t^4+29t^2+100}',
            r'\cos^2\theta=\frac{t^4+29t^2+100-9t}{t^4+29t^2+100}',
            r'\cos^2\theta=1-\frac{9t^2}{t^4+29t^2+100}',
            r'\cos^2\theta{{=}}1-\frac{9}{t^2+29+\frac{100}{t^2}}'
        ]

        self.play(Write(text_let_theta))
        self.wait(2)
        self.play(Write(eq_1, run_time=3))
        self.wait(3)

        last = eq_1
        for eq in eqs:
            current = MathTex(eq).move_to(eq_1, UP)
            self.play(ReplacementTransform(last, current))
            self.wait(3)
            last = current

        # 暂时透明度设为 0，否则下面移动 ineq 的时候它会跳出来
        # 不知道为啥直接在实例化时设置 opacity=0 是无效的
        right = (MathTex(r'\ge 1-\frac{9}{2\sqrt{t^2+\frac{100}{t^2}}+29}{{=}}\frac{40}{49}')
                 .next_to(last).set_opacity(0))
        align_baseline(last, right)
        ineq = VGroup(last, right)
        text_when = (Tex(r'当且仅当$\displaystyle t^2=\frac{100}{t^2}$即$t=\sqrt{10}$时取等号')
                     .next_to(ineq, DOWN).to_edge(LEFT))
        text_now = Tex(r'此时$\cos^2\theta$最小，即$\theta$最大').next_to(text_when, DOWN, aligned_edge=LEFT)
        text_answer = Tex(r'$\therefore CP=t=\sqrt{10}$').next_to(text_now, DOWN, aligned_edge=LEFT)

        self.play(ineq.animate.set_x(0))
        self.wait()
        right.set_opacity(1)
        self.play(Write(right, run_time=3))
        self.wait(3)
        self.play(Write(text_when, run_time=2))
        self.wait(2)
        self.play(Write(text_now, run_time=2))
        self.wait(2)
        self.play(Write(text_answer, run_time=2))
        self.wait(5)
        self.play(FadeOut(text_vec, text_let_theta, ineq, text_when, text_now, text_answer))
        self.wait()

        text_3d = Tex('该方法是计算量最大的，但可以解决三维空间中的张角问题').to_corner(UL)
        text_url = Tex(r'\mbox{\textsf{演示视频：【[Manim]照片测星定位数学原理动画详解！初中生也能看懂！】BV1WhPyeNEYP}}',
                       font_size=24).to_corner(DL)

        self.play(Write(text_3d, run_time=2), FadeIn(text_url))
        self.wait(10)
        self.play(FadeOut(text_3d, text_url))

        MathTex.set_default(font_size=DEFAULT_FONT_SIZE)
        title_3 = Tex('3. 三角函数法').move_to(title_2, UL)
        text_let_alpha_beta = (Tex(r'设$CP=t$，$\angle APC=\alpha$，$\angle BPC=\beta$')
                               .next_to(title_3, DOWN, aligned_edge=LEFT))
        text_tan_val = Tex(
            r'则$\displaystyle\tan\alpha=\frac{5}{t}$，$\displaystyle\tan\beta=\frac{2}{t}$'
        ).next_to(text_let_alpha_beta, DOWN, aligned_edge=LEFT)

        pc = Line(p, c)
        alpha = AngleMark(p, pa, pc, r'\alpha', 1.05, colour=YELLOW)
        beta = AngleMark(p, pb, pc, r'\beta', colour=YELLOW)

        self.play(FadeIn(hidden_question))
        self.wait()
        self.play(ReplacementTransform(title_2, title_3))
        self.wait(2)
        self.play(Write(text_let_alpha_beta, run_time=2), Create(VGroup(alpha, beta)))
        self.wait(2)
        self.play(Write(text_tan_val, run_time=2))
        self.wait(2)

        MathTex.set_default(font_size=40)
        eq_1 = MathTex(r'\tan\angle APB=\tan(\alpha-\beta)').next_to(text_tan_val, DOWN, aligned_edge=LEFT)
        eqs = [
            r'\tan\angle APB=\frac{\tan\alpha-\tan\beta}{1+\tan\alpha\tan\beta}',
            r'\tan\angle APB=\frac{\frac{5}{t}-\frac{2}{t}}{1+\frac{5}{t}\cdot\frac{2}{t}}',
            r'\tan\angle APB{{=}}\frac{3}{t+\frac{10}{t}}'
        ]

        self.play(Write(eq_1, run_time=2))
        self.wait(2)
        last = eq_1
        for eq in eqs:
            current = MathTex(eq).move_to(last, UL)
            self.play(ReplacementTransform(last, current))
            self.wait(3)
            last = current

        right = MathTex(r'\le\frac{3}{\sqrt{t\cdot\frac{10}{t}}}{{=}}\frac{3}{10}\sqrt{3}').next_to(last)
        align_baseline(last, right)
        text_when = (Tex(r'当且仅当$\displaystyle t=\frac{10}{t}$即$t=\sqrt{10}$时取等号')
                     .next_to(VGroup(last, right), DOWN, aligned_edge=LEFT))
        text_answer = Tex(r'$\therefore CP=t=\sqrt{10}$').next_to(text_when, DOWN, aligned_edge=LEFT)

        self.play(Write(right, run_time=2))
        self.wait(3)
        self.play(Write(text_when, run_time=2))
        self.wait(2)
        self.play(Write(text_answer, run_time=2))
        self.wait(5)
