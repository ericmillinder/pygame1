import pygame
import logging
from constants import *
from Screen import *

pygame.init()
if not pygame.font.init():
    logging.error("Pygame Font not initialized!")


class Debug():
    def __init__(self):
        pass

    def update(self):
        pass
