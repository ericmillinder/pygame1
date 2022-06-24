import pygame
import logging
import random
from pygame.locals import *

from Screen import *
from player import Player
from plat import Platform
from level import generate
from debug import Debug

logging.basicConfig(level=logging.INFO)

pygame.init()
pygame.display.set_caption("Game 1")

FramePerSec = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

BottomPlatform = Platform(0, HEIGHT - 10)
all_sprites.add(BottomPlatform)
platforms.add(BottomPlatform)
generate(platforms, all_sprites)

P1 = Player(platforms)
# all_sprites.add(P1)

debug = Debug()


# TODO figure out how to reinit sprites and platforms since these vars are shadowing outer vars.. wrap in a class?
def shake(sprites, platforms):
    sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    generate(platforms, sprites)
    all_sprites.add(P1)


def game_loop():
    done = False
    while not done:
        debug.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_q]:
            done = True
        elif pressed_keys[K_t]:
            shake(all_sprites, platforms)

        # if P1.rect.top <= HEIGHT / 3:
        #     P1.pos.y += abs(P1.vel.y)
        #     # because the player is moved up on sprite collision with a platform, the y
        #     # pos stays low and platforms keep generating. Not good.
        #     # platform = Platform(random.randint(0, WIDTH - 25), random.randint(30, int(HEIGHT / 3)))
        #     # platforms.add(platform)
        #     # all_sprites.add(platform)
        #     for plat in platforms:
        #         plat.rect.y += abs(P1.vel.y)
        #         if plat.rect.top >= HEIGHT:
        #             plat.kill()  # removes the sprite from ALL groups it is in

        displaysurface.fill((0, 0, 0))
        full_surface.fill((0, 0, 0))
        P1.move()
        P1.update()

        for entity in all_sprites:
            full_surface.blit(entity.surf, entity.rect)

        display_rect = ((WIDTH - P1.pos.x) / 2, (HEIGHT - P1.pos.y) / 2, WIDTH, HEIGHT)
        displaysurface.blit(full_surface, display_rect)
        pygame.display.update()
        FramePerSec.tick(FPS)

        logging.getLogger("main").warning("Pos: {}".format(P1.pos))

        if P1.pos.y > 1000:
            done = True

    pygame.quit()


if __name__ == "__main__":
    game_loop()
