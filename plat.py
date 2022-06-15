import pygame


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("assets/images/platform_main_big.png").convert()
        self.rect = self.surf.get_rect(topleft=(x, y))
