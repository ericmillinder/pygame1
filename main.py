from pygame.locals import *

from level import *
from player import Player
from cameragroup import YSortCameraGroup

logging.basicConfig(level=logging.DEBUG)

pygame.init()
pygame.display.set_caption("Game 1")

FramePerSec = pygame.time.Clock()

all_sprites = YSortCameraGroup()
platforms = pygame.sprite.Group()

generate(platforms, all_sprites)

P1 = Player(platforms)
all_sprites.add(P1)

background = pygame.image.load("assets/images/training.png").convert_alpha()


def game_loop():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_q]:
            done = True

        displaysurface.fill('#000000')
        displaysurface.blit(background, (0,0))

        all_sprites.update()
        all_sprites.custom_draw(P1)

        pygame.display.update()
        FramePerSec.tick(FPS)


        if P1.pos.y > 1000:
            done = True

    pygame.quit()


if __name__ == "__main__":
    game_loop()
