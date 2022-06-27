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
        self.image = pygame.image.load("assets/images/sonic.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(0, -26)

        self.pos = vec(Screen.WIDTH // 2, Screen.HEIGHT // 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0.5)

        self.directionFacing = RIGHT
        self.jumping = False
        self.doubleJumping = False

    def update(self):
        self.move()
        # check collision with platforms
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            logging.info("Velocity {}, Acc {}".format(self.vel, self.acc))
            logging.info("Hit at {}".format(hits))
            # y > 0 == falling
            if self.vel.y > 0:
                if self.rect.bottom > hits[0].rect.top:
                    self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                self.jumping = False
                self.doubleJumping = False

        # player_image = self.image
        # if self.directionFacing == LEFT:
        #     player_image = pygame.transform.flip(player_image, True, False)
        #
        # self.display_surface.blit(player_image, self.rect)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.platforms:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.vel.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.vel.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.platforms:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.vel.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.vel.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def jump(self):
        # Ensure we are currently in contact with something
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

        # self.hitbox.x += self.pos.x * self.vel.x
        # self.collision('horizontal')
        # self.hitbox.y += self.pos.y * self.vel.y
        # self.collision('vertical')
        # self.rect.center = self.hitbox.center
