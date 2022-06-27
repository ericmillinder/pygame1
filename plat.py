import pygame


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/platform_main_big.png").convert()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect
