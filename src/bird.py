import pygame
from settings import BIRD_POS, GRAVITY, BIRD_JUMP, HEIGHT


class Bird(pygame.sprite.Sprite):
    def __init__(self, on_death) -> None:
        super().__init__()
        self.on_death = on_death

        # Import bird graphics
        self.import_graphics()

        # Bird physics
        self.movment = 0

    def import_graphics(self):
        mid = pygame.image.load(
            "../data/assets/bluebird-midflap.png").convert_alpha()
        up = pygame.image.load(
            "../data/assets/bluebird-upflap.png").convert_alpha()
        down = pygame.image.load(
            "../data/assets/bluebird-downflap.png").convert_alpha()

        self.BIRD_IMAGES = [down, mid, up]
        self.BIRD_INDEX = 0

        self.image = self.BIRD_IMAGES[self.BIRD_INDEX]
        self.rect = self.image.get_rect(center=BIRD_POS)

    def animate(self, speed=0.1):
        self.BIRD_INDEX += speed
        if self.BIRD_INDEX >= len(self.BIRD_IMAGES):
            self.BIRD_INDEX = 0
        self.image = self.BIRD_IMAGES[int(self.BIRD_INDEX)]

    def rotate(self, angle):
        self.image = pygame.transform.rotozoom(
            self.BIRD_IMAGES[int(self.BIRD_INDEX)], -angle, 1.8)

        self.rect = self.image.get_rect(
            center=(BIRD_POS[0], self.rect.centery))

    def flap(self):
        self.movment = 0
        self.movment -= BIRD_JUMP

    def check_death(self):
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.on_death()

    def update(self):
        self.animate()
        self.movment += GRAVITY
        self.rect.centery += self.movment
        self.rotate(self.movment * 2)
        self.check_death()
