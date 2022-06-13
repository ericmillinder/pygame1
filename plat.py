import pygame

class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=(x, y))