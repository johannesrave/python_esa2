from typing import Union, Sequence, Any

import pygame
import math
from pygame.sprite import Sprite, AbstractGroup, Group

pygame.init()
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('AsteroidR')
frames_per_second = 60
clock = pygame.time.Clock()

background = pygame.Surface(window.get_size())
background = background.convert()
background.fill((79, 78, 75))

window.blit(background, (0, 0))
pygame.display.flip()


class Enemies(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)


class Enemy(Sprite):
    def __init__(self, *groups: AbstractGroup, color=pygame.Color(180, 170, 140), width, height, offset):
        super().__init__(*groups)
        self.color = color
        self.movement_height = 128
        self.baseline = window_height/2
        self.loop_duration = 1000
        self.offset = offset
        self.y_scale = 1.0
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        dist_to_mouse = point_dist(self.rect.center, pygame.mouse.get_pos())
        pattern_pos_y = self.get_sine_for_ms(self.movement_height, self.loop_duration, self.offset)

        mouse_influence = (window_width - dist_to_mouse) * 0.01
        mouse_influence = math.copysign(mouse_influence, pattern_pos_y)
        self.rect.y = pattern_pos_y * mouse_influence + self.baseline

        # self.rect.center = (self.rect.center[0], self.rect.center[1] + (dist_to_mouse/30)**2)

        # if dist_to_mouse < 200:
        #     print('mouse is close to rect!', pygame.mouse.get_pos())
        #     self.y_scale = 4.0
        #
        # else:
        #     self.y_scale = 1.0
        #     self.rect.center = (self.rect.center[0], self.rect.center[1] - 30)

        # center = self.rect.center
        # self.rect.height *= self.y_scale
        # self.rect.center = center
        #
        # self.image = pygame.Surface((self.rect.width, self.rect.height))
        # self.image.fill(self.color)

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
enemies.number = 24
for num in range(enemies.number):
    enemy = Enemy(enemies, height=32, width=16, offset=num * 48)
    enemy.rect.x = num * 32 + 16
    enemy.rect.y = 300
    window.blit(enemy.image, enemy.rect)

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
