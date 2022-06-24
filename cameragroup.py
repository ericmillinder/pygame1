from typing import List

import pygame
from Screen import *


# This sprite group functions as a camera
# The sprites are Y sorted
from pygame.rect import Rect
from pygame.surface import Surface


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            full_surface.blit(sprite.surf, sprite.rect)

    def draw(self, surface: Surface) -> List[Rect]:
        return super().draw(surface)

