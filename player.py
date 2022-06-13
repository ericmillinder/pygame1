import pygame
import logging
from pygame.locals import *

import Screen
from constants import *
from Screen import *

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.platforms = platforms
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec(20, Screen.HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
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
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
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
