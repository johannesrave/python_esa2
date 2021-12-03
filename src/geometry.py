import math
from typing import Tuple


class Modulation:
    def modulate(self, position: Tuple[float, float], reference_position):
        return position


class Pattern:
    def __init__(self, dimensions, time, modulation: Modulation):
        self.modulation = modulation
        self.dimensions_width = dimensions[0]
        self.dimensions_height = dimensions[1]
        self.time = time

    def place(self, index, amount):
        raise NotImplementedError


class SinePattern(Pattern):
    def __init__(self, amplitude, duration, dimensions, time, modulation: Modulation):
        super().__init__(dimensions, time, modulation)
        self.amplitude = amplitude
        self.duration = duration
        self.baseline = self.dimensions_height / 2

    def place(self, index, amount):
        x = self.dimensions_width / (amount + 1) * (index + 1)
        y = self.baseline + self.get_sine_for_ms(index, amount, 3)
        position = (x, y)
        reference_position = (x, self.baseline)
        modulated_position = self.modulation.modulate(position, reference_position)
        return modulated_position

    def get_sine_for_ms(self, item_num, amount, factor=4):
        normalized_offset = ((item_num / amount) * self.duration)
        normalized_moment = ((self.time.get_ticks() + normalized_offset) % self.duration) / self.duration
        t = (normalized_moment * (2 * 3.14159)) * factor
        n = math.sin(t) * self.amplitude
        return n


class MouseBased(Modulation):
    def __init__(self, max_distance, axis, mouse):
        self.mouse = mouse
        self.max_distance = max_distance
        self.axis = axis

    def modulate(self, position: Tuple[float, float], reference_position):
        (x_pos, y_pos) = position
        (x_ref, y_ref) = reference_position
        (x_mouse, y_mouse) = self.mouse.get_pos()
        mouse_x_distance = abs(x_pos - x_mouse)
        modulation_amount = (self.max_distance - mouse_x_distance) / self.max_distance
        y_new = (y_ref) + ((y_pos - y_ref) * modulation_amount)
        return (x_pos, y_new)
