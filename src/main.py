from typing import Union, Sequence, Any

import pygame
import math
from pygame.sprite import Sprite, AbstractGroup, Group

pygame.init()
window_width, window_height = 1200, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('AsteroidR')
frames_per_second = 60
clock = pygame.time.Clock()

background = pygame.Surface(window.get_size())
background = background.convert()
background.fill((79, 78, 75))

window.blit(background, (0, 0))
pygame.display.flip()


class SinePattern:
    def __init__(self, amplitude, duration, baseline=(window_height/2)):
        self.amplitude = amplitude
        self.duration = duration
        self.baseline = baseline

    def calculate_position(self, item_num, amount):
        x = window_width / (amount + 1) * (item_num + 1)
        y = self.get_sine_for_ms(item_num, amount)
        return (x, y)

    def get_sine_for_ms(self, item_num, amount, factor=1):
        normalized_time = (pygame.time.get_ticks() % self.duration) / self.duration
        offset = normalized_time + ((item_num / amount) * self.duration) * factor
        scaled_to_duration = (2 * math.pi / self.duration)
        t = offset * scaled_to_duration
        n = math.sin(t) * self.amplitude
        return int(n)


class Enemies(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)

    def generate(self, amount, width=32, height=32, pattern=SinePattern(200, 1000)):
        for num in range(amount+1):
            enemy = Enemy(self, pattern=pattern, height=height, width=width, item_num=num, amount=amount)
            self.add(enemy)


class Enemy(Sprite):
    def __init__(self, *groups: Enemies, color=pygame.Color(180, 170, 140), width, height, pattern, item_num, amount):
        super().__init__(*groups)
        self.amount = amount
        self.item_num = item_num
        self.pattern = pattern
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = self.pattern.calculate_position(self.item_num, self.amount)


        # y_pos_movement = self.get_sine_for_ms(self.movement_height, self.loop_duration, self.offset)

        # x_pos_mouse = pygame.mouse.get_pos()[0]
        # x_distance_mouse_center = abs(self.rect.center[0] - x_pos_mouse)
        # x_normalized_modulation_distance = (window_width - x_distance_mouse_center) / window_width
        # y_new = self.baseline + (y_pos_movement * x_normalized_modulation_distance *1.5)
        # self.rect.y = y_new

    # enemy.rect.center = self.pattern.calculate_position(num, amount)

    @staticmethod
    def get_sine_for_ms(amplitude, loop_duration, offset):
        milliseconds_in_loop = (pygame.time.get_ticks() + offset % loop_duration)
        scaled_to_duration = (2 * math.pi / loop_duration)
        t = milliseconds_in_loop * scaled_to_duration
        n = math.sin(t) * amplitude
        return int(n)


def point_dist(point_1, point_2):
    x1, y1 = point_1[0], point_1[1]
    x2, y2 = point_2[0], point_2[1]
    return math.hypot(x2 - x1, y2 - y1)


crashed = False

enemies = Enemies()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    enemies.update()

    window.blit(background, (0, 0))
    enemies.draw(window)
    pygame.display.flip()
    pygame.event.pump()
    # pygame.display.update()
    clock.tick(frames_per_second)
