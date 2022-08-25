import pygame
import logging
from pygame.locals import *

import Screen
from constants import *
from Screen import *

vec = pygame.math.Vector2
LEFT = 0
RIGHT = 1

IDLE = 0
RUNNING = 1
JUMPING = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms: pygame.sprite.Group):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.platforms = platforms

        self.images = {RIGHT: self.loadPlayerImage("assets/images/Jump__002.png"),
                       LEFT: pygame.transform.flip(self.loadPlayerImage("assets/images/Jump__002.png"), True, False)}
        self.jump_cycle = [self.loadPlayerImage(f"assets/images/Jump__00{i}.png") for i in range(1, 9)]
        self.run_cycle = [self.loadPlayerImage(f"assets/images/Run__00{i}.png") for i in range(1, 9)]
        self.idle_cycle = [self.loadPlayerImage(f"assets/images/Idle__00{i}.png") for i in range(1, 9)]

        self.image = self.images[LEFT]
        self.rect = self.image.get_rect()
        # The inflate method inflates around the center of the rectangle
        self.hitbox = self.rect.inflate(-10, -10)
        self.feetbox = Rect((self.rect.bottomleft), (self.rect.width - 12, 10))
        # self.hitbox = Rect(self.rect.bottomleft, (self.rect.width, 10))

        self.pos = vec(Screen.WIDTH // 2, Screen.HEIGHT // 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0.5)

        self.directionFacing = RIGHT
        self.jumping = False
        self.doubleJumping = False

        self.state = IDLE
        self.animation_index = 0

    def loadPlayerImage(self, path):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() / 8, image.get_height() / 8))
        return image

    def animate(self, cycle, rate, hold=False):
        self.image = cycle[int(self.animation_index)]
        if self.directionFacing == LEFT:
            self.image = pygame.transform.flip(self.image, True, False)

        max_cycle_index = len(cycle) - 1
        if self.animation_index < max_cycle_index:
            self.animation_index += rate
        else:
            if hold:
                self.animation_index = max_cycle_index
            else:
                self.animation_index = 0

    def update(self):
        self.move()

        if self.directionFacing == LEFT:
            self.image = self.images[LEFT]
        if self.directionFacing == RIGHT:
            self.image = self.images[RIGHT]

        if self.state == JUMPING:
            self.animate(self.jump_cycle, 0.6, hold=True)
        elif int(self.vel.x) != 0:
            self.animate(self.run_cycle, 0.5)
        else:
            self.animate(self.idle_cycle, 0.2)

    def stateTo(self, state):
        if self.state == state:
            return

        self.state = state
        self.animation_index = 0

    def collision_with_platform(self, box, direction):
        if direction == 'horizontal':
            for sprite in self.platforms:
                if sprite.hitbox.colliderect(box):
                    if self.vel.x > 0:  # moving right
                        logging.info("Box {} hit {}".format(box, sprite.hitbox))
                    if self.vel.x < 0:  # moving left
                        logging.info("Box {} hit {}".format(box, sprite.hitbox))

        if direction == 'vertical':
            for sprite in self.platforms:
                if sprite.hitbox.colliderect(box):
                    if self.vel.y > 0:  # moving down
                        logging.info("Moving downwards at {} and hit {}".format(box, sprite.hitbox))
                        self.pos.y = sprite.rect.y + 1
                        self.vel.y = 0
                        self.jumping = False
                        self.doubleJumping = False
                        self.stateTo(IDLE)
                    if self.vel.y < 0:  # moving up
                        logging.info("Box {} hit {}".format(box, sprite.hitbox))

    def jump(self):
        # Ensure we are currently in contact with something
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            self.stateTo(JUMPING)
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

        self.feetbox.x = self.pos.x - (self.rect.width / 2)
        self.feetbox.y = self.pos.y - (self.feetbox.height) - 2

        # self.hitbox.x += self.pos.x * self.vel.x
        # self.collision(self.feetbox, 'horizontal')
        # self.hitbox.y += self.pos.y * self.vel.y
        # self.collision(self.feetbox, 'vertical')
        # self.rect.center = self.hitbox.center

        # check collision with platforms
        hit_platform = None
        for platform in self.platforms:
            hits = self.feetbox.colliderect(platform.rect)
            if hits:
                hit_platform = platform
                platform.collided = True

        self.collision_with_platform(self.feetbox, 'vertical')

        self.feetbox.x = self.pos.x - (self.rect.width / 2)
        self.feetbox.y = self.pos.y - (self.feetbox.height) - 1

        #
        # if hit_platform:
        #     if self.vel.y > 0:
        #         if self.feetbox.bottom > hit_platform.rect.top:
        #             self.pos.y = hit_platform.rect.top
        #         self.vel.y = 0
        #         self.jumping = False
        #         self.doubleJumping = False
        #         self.stateTo(IDLE)


        self.rect.midbottom = self.pos


    def draw(self, offset, surface):
        feetbox = self.feetbox.copy()
        feetbox.topleft = self.feetbox.topleft - offset
        # logging.info("feetbox: {}".format(feetbox))
        pygame.draw.rect(surface, "red", feetbox, 1)
