import pygame
import logging
from pygame.locals import *

import Screen
from constants import *
from Screen import *

vec = pygame.math.Vector2
LEFT = 0
RIGHT = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.platforms = platforms
        self.surf = pygame.image.load("assets/images/sonic.png").convert_alpha()
        self.rect = self.surf.get_rect()

        self.pos = vec(20, Screen.HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.directionFacing = RIGHT
        self.jumping = False
        self.doubleJumping = False

    def update(self):

        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            if self.vel.y > 0:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                self.jumping = False
                self.doubleJumping = False
        player_image = self.surf
        if self.directionFacing == LEFT:
            player_image = pygame.transform.flip(player_image, True, False)

        self.display_surface.blit(player_image,self.rect)

    def jump(self):
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            self.jumping = True
            self.vel.y = -10
        elif not self.doubleJumping and self.vel.y > 0:
            self.vel.y = -9
            self.doubleJumping = True

    def cancelJump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            self.directionFacing = LEFT
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.directionFacing = RIGHT
        if pressed_keys[K_f]:
            self.jump()
        else:
            self.cancelJump()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + ACC * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos
