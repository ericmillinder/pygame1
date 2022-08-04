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

        self.images = {RIGHT: self.loadPlayerImage("assets/images/Jump__002.png"),
                       LEFT: pygame.transform.flip(self.loadPlayerImage("assets/images/Jump__002.png"), True, False)}
        self.image = self.images[LEFT]
        self.rect = self.image.get_rect()
        # The inflate method inflates around the center of the rectangle
        self.hitbox = self.rect.inflate(-10, -10)
        # self.hitbox = Rect(self.rect.bottomleft, (self.rect.width, 10))

        self.pos = vec(Screen.WIDTH // 2, Screen.HEIGHT // 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0.5)

        self.directionFacing = RIGHT
        self.jumping = False
        self.doubleJumping = False

    def loadPlayerImage(self, path):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        return image

    def update(self):
        self.move()
        # check collision with platforms
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            # logging.info("Velocity {}, Acc {}".format(self.vel, self.acc))
            # logging.info("Hit at {}".format(hits))
            # y > 0 == falling
            if self.vel.y > 0:
                if self.rect.bottom > hits[0].rect.top:
                    self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                self.jumping = False
                self.doubleJumping = False

        if self.directionFacing == LEFT:
            self.image = self.images[LEFT]
        if self.directionFacing == RIGHT:
            self.image = self.images[RIGHT]

        # player_image = self.image
        # if self.directionFacing == LEFT:
        #     player_image = pygame.transform.flip(player_image, True, False)
        #
        # self.display_surface.blit(player_image, self.rect)
        # if (self.jumping):
        #     self.image = pygame.image.load("assets/images/Jump__007.png").convert_alpha()
        #     self.image = pygame.transform.scale(self.image, (64, 64))
        #     self.rect = self.image.get_rect()
        #     # The inflate method inflates around the center of the rectangle
        #     self.hitbox = self.rect.inflate(-10, -10)
        # else:
        #     self.image = pygame.image.load("assets/images/Jump__002.png").convert_alpha()
        #     self.image = pygame.transform.scale(self.image, (64, 64))
        #     self.rect = self.image.get_rect()
        #     # The inflate method inflates around the center of the rectangle
        #     self.hitbox = self.rect.inflate(-10, -10)


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

        self.hitbox.x += self.pos.x * self.vel.x
        self.collision('horizontal')
        self.hitbox.y += self.pos.y * self.vel.y
        self.collision('vertical')
        # self.rect.center = self.hitbox.center
