import pygame
from settings import WIDTH


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(
            "../data/assets/base.png").convert_alpha(), (WIDTH, 100))
        self.rect = self.image.get_rect(topleft=(x, 500))
        self.initial_x = x

    def update(self) -> None:
        self.rect.x -= 2
        lim = -WIDTH if self.initial_x == 0 else 0
        if self.rect.x <= lim:
            self.rect.x = self.initial_x
