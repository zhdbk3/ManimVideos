#
# Created by MC着火的冰块(zhdbk3) on 2025/2/4
#

from manim import *

from config import load_config

TEXT_LIST = [
    r'''谨以此作献给：
\qquad 我热烈而灿烂的初中时光
\qquad 我一去不复返的豆蔻年华
\qquad 屏幕前每个热爱仰望星空的你''',

    '''方法原作者：@鬼蝉
\u3000
参考资料：
【从一张星空照片定位出拍摄地是真的还是假的？】 https://www.bilibili.com/video/BV1Dx4y117yM
【照片测星定位法原理简介】 https://www.bilibili.com/opus/871438831332622336
https://github.com/zhdbk3/PhotoAstrologicalPositioning
https://github.com/BengbuGuards/StarLocator/tree/main/prototype/core/positioning''',

    '''相关软件：
1. StarLocator（推荐，最先进、完善、便捷）
【找拍摄地，传统方法难度4星，但测星定位秒了】 https://www.bilibili.com/video/BV1ZcyCYTE5u
https://github.com/BengbuGuards/StarLocator
https://caveallegory.cn/StarLocator
2. PhotoAstrologicalPositioning（up 自己初三时独立完成的，还有很多不足之处，懒得修了）
【[开源]照片测星定位！一张星空照片就能算出你的位置！】 https://www.bilibili.com/video/BV124akeTEEQ
https://github.com/zhdbk3/PhotoAstrologicalPositioning
3. StarPhotoPositioning
https://github.com/cheanus/StarPhotoPositioning''',

    '''感谢 @NcdFT 提供的排版建议与数学支持
感谢 @薛定谔的按钮~对音频处理的建议''',

    r'''本视频使用 Manim 制作
耗时约 20 天，代码量约 2600 行
源码见 https://github.com/zhdbk3/PAP\_Animation
萌新的第一个 Manim 视频，尚存在许多不足或错误之处
欢迎各位大佬来指正或提出建议！
给个三连加关注吧，谢谢喵！''',

    r'''BGM:
Alpha
宇宙尽头的碎片
The truth that you leave
光落下的声音
向着那亲爱的每一天
（碧蓝航线）决意
Cryout'''
]


def manage_tex(s: str) -> Tex:
    s = s.replace('\n', r'\\')
    return Tex(r'\textsf{%s}' % s, tex_environment='flushleft')


class End(Scene):
    def construct(self):
        load_config()

        for s in TEXT_LIST:
            tex = manage_tex(s)
            self.play(FadeIn(tex))
            self.wait(3)
            self.play(FadeOut(tex))

        self.wait()
