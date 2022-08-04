import logging

import pygame.draw

from Screen import *


# This sprite group functions as a camera
# The sprites are Y sorted


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(0, 0)

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.center_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            if sprite == player:
                logging.info("Drawing player's hitbox {}".format(sprite.hitbox))
                pygame.draw.rect(self.display_surface, "#ff3333", sprite.hitbox, 1)

            elif sprite.hitbox:
                hitbox = sprite.hitbox.copy()
                hitbox.topleft = sprite.hitbox.topleft - self.offset
                pygame.draw.rect(self.display_surface, "#ff3333", hitbox, 1)
