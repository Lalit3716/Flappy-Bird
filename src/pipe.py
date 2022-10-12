import pygame
from settings import PIPE_SPEED, HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, pos, color, type, *groups):
        super().__init__(*groups)
        self.pipe_green = pygame.image.load(
            "../data/assets/pipe-green.png").convert_alpha()
        self.pipe_red = pygame.image.load(
            "../data/assets/pipe-red.png").convert_alpha()

        self.image = self.pipe_green if color == "green" else self.pipe_red

        if type == "top":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midbottom=pos)
        else:
            self.rect = self.image.get_rect(midtop=pos)

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()
