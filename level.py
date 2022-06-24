import random
import logging
import pygame.sprite

from plat import Platform
from Screen import *

LEVEL_HEIGHT = 2000
LEVEL_WIDTH = 1000

def generate(platforms, all_sprites: pygame.sprite.Group):
    for x in range(random.randint(13, 35)):
        retry = True
        while retry:
            pl = Platform(random.randint(0, LEVEL_WIDTH - 25), random.randint(30, LEVEL_HEIGHT))
            retry = check(pl, platforms, retry)
        platforms.add(pl)
    platforms.add(Platform(0, 100))

    for p in platforms:
        all_sprites.add(p)

    logging.info("Generated {} platforms".format(x))


def check(pl, platforms, retry):
    if not pygame.sprite.spritecollide(pl, platforms, False):
        retry = False
    else:
        logging.info("Generated an overlapping platform!")
    return retry
