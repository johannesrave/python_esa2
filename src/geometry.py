import math
from typing import Tuple


class Pattern:
    def __init__(self, dimensions, time):
        self.dimensions_width = dimensions[0]
        self.dimensions_height = dimensions[1]
        self.time = time

    def place(self, index, amount):
        raise NotImplementedError


class SinePattern(Pattern):
    def __init__(self, amplitude, duration, dimensions, time):
        super().__init__(dimensions, time)
        self.amplitude = amplitude
        self.duration = duration
        self.baseline = self.dimensions_height / 2

    def place(self, index, amount):
        x = self.dimensions_width / (amount + 1) * (index + 1)
        y = self.baseline + self.get_sine_for_ms(index, amount, 3)
        return (x, y)

    def get_sine_for_ms(self, item_num, amount, factor=4):
        normalized_offset = ((item_num / amount) * self.duration)
        normalized_moment = ((self.time.get_ticks() + normalized_offset) % self.duration) / self.duration
        t = (normalized_moment * (2 * 3.14159)) * factor
        n = math.sin(t) * self.amplitude
        return n


class Modulation:
    def modulate(self, position: Tuple[int]):
        return position


class MouseBased(Modulation):
    def __init__(self, strength, axis):
        self.strength = strength
        self.axis = axis

    def modulate(self, position: Tuple[int]):
        return position
