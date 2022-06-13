import pygame
import logging
from pygame.locals import *

from Screen import *
from player import Player
from plat import Platform
from level import generate

logging.basicConfig(level=logging.INFO)

pygame.init()
pygame.display.set_caption("Game 1")

FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

BottomPlatform = Platform(WIDTH, 20, 0, HEIGHT - 10)
all_sprites.add(BottomPlatform)
platforms.add(BottomPlatform)
generate(platforms, all_sprites)

P1 = Player(platforms)
all_sprites.add(P1)


# TODO figure out how to reinit sprites and platforms since these vars are shadowing outer vars.. wrap in a class?
def shake(sprites, platforms):
    sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    generate(platforms, sprites)
    all_sprites.add(P1)


def game_loop():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_q]:
            done = True
        elif pressed_keys[K_t]:
            shake(all_sprites, platforms)

        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

        displaysurface.fill((0, 0, 0))
        P1.move()
        P1.update()

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)

        if not P1.alive():
            pygame.quit()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
