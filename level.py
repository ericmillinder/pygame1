import random
import logging
import pygame.sprite

from plat import Platform
from Screen import *

LEVEL_HEIGHT = 2000
LEVEL_WIDTH = 1000

logger = logging.getLogger("platforms")
logger.setLevel(level=logging.DEBUG)


def generate(platforms, all_sprites: pygame.sprite.Group):
    for x in range(random.randint(10, 20)):
        retry = True
        while retry:
            pl = Platform(random.randint(65, WIDTH - 65), random.randint(100, HEIGHT - 50))
            retry = check(pl, platforms, retry)
        logger.info("Platform at {}".format(pl.rect))
        platforms.add(pl)
    platforms.add(Platform(0, HEIGHT - 20, width=WIDTH))  # full floor

    for p in platforms:
        all_sprites.add(p)

    logging.info("Generated {} platforms".format(x))


def check(pl, platforms, retry):
    if not pygame.sprite.spritecollide(pl, platforms, False):
        retry = False
    else:
        logging.info("Generated an overlapping platform!")
    return retry
