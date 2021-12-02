from typing import Any, Sequence, Union

import pygame
from pygame.sprite import Group, Sprite
from src.geometry import Pattern, Modulation


class Markers(Group):
    def __init__(self,
                 *sprites: Union[Sprite, Sequence[Sprite]],
                 modulation: Modulation,
                 pattern: Pattern):
        super().__init__(*sprites)
        self.modulation = modulation
        self.pattern = pattern

    def update(self):
        for index, marker in enumerate(self):
            raw_position = self.pattern.place(index, len(self))
            modulated_position = self.modulation.modulate(raw_position)
            marker.rect.center = modulated_position


class Marker(Sprite):
    def __init__(self, *groups: Markers,
                 color=pygame.Color(180, 170, 140),
                 width=32, height=32):
        super().__init__(*groups)
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

