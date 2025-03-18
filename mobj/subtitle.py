#
# Created by 着火的冰块nya(zhdbk3) on 2025/3/18
#

from typing import Optional
import wave

from manim import *

from .with_background import WithBackground


class Subtitle:
    def __init__(self, scene: Scene):
        """字幕"""
        self.scene = scene
        self.mobj: WithBackground | None = None
        self.duration = 0  # 音频播放所需的时长

    def disappear(self) -> None:
        """字幕消失"""
        if self.mobj is not None:
            self.scene.remove(self.mobj)
            self.mobj = None
            self.duration = 0

    def set_text(self, text: str, sound_path: Optional[str] = None, block: bool = True) -> None:
        """
        更新字幕，播放音频
        :param text: 符合 Tex 语法的字符串
        :param sound_path: 对应音频的路径，应为 .wav 格式
        :param block: 是否阻塞，等待音频播放完
        :return: None
        """
        self.disappear()
        # 字幕为无衬线体
        self.mobj = WithBackground(Tex(r'\textsf{' + text + '}')).to_edge(DOWN)
        # 显示字幕
        if isinstance(self.scene, ThreeDScene):
            self.scene.add_fixed_in_frame_mobjects(self.mobj)
        else:
            self.scene.add(self.mobj)
        self.scene.bring_to_front(self.mobj)
        # 播放音频（如果有）
        if sound_path is not None:
            self.scene.add_sound(sound_path)
        # 计算需要的时间并等待（如果有）
        self.duration = len(text) / 4 if sound_path is None else self.get_duration(sound_path)
        if block:
            self.scene.wait(self.duration, frozen_frame=False)
            self.scene.remove(self.mobj)

    @staticmethod
    def get_duration(sound_path: str) -> float:
        """
        获取一段音频的时长
        :param sound_path: 音频路径
        :return: 时长秒数
        """
        with wave.open(sound_path) as f:
            f: wave.Wave_read
            return f.getnframes() / f.getframerate()
