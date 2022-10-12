from random import choice
import pygame
import sys
from settings import *
from floor import Floor
from pipe import Pipe
from bird import Bird


class Game:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        # Timer
        self.pipe_timer = pygame.USEREVENT
        pygame.time.set_timer(self.pipe_timer, 1200)

        # Import bg graphics
        self.import_graphics()
        self.current_bg = self.BG_DAY

        # Sprite groups
        self.floor_sprites = pygame.sprite.Group()
        self.pipe_sprites = pygame.sprite.Group()
        self.bird_sprite = pygame.sprite.GroupSingle()

        # Floor
        Floor(0, self.floor_sprites)
        Floor(WIDTH, self.floor_sprites)

        # Pipes
        self.pipe_color = "green"

        # Bird
        self.bird = Bird(self.on_death)
        self.bird_sprite.add(self.bird)

        # Score
        self.score = 0

        # Game variables
        self.game_started = False
        self.game_over = False

    def import_graphics(self):
        self.BG_DAY = pygame.transform.scale(pygame.image.load(
            "../data/assets/background-day.png").convert_alpha(), (WIDTH, HEIGHT))

        self.BG_NIGHT = pygame.transform.scale(pygame.image.load(
            "../data/assets/background-night.png").convert_alpha(), (WIDTH, HEIGHT))

        self.GAME_OVER_BG = pygame.image.load(
            "../data/assets/gameover.png").convert_alpha()
        self.START_BG = pygame.transform.scale(pygame.image.load(
            "../data/assets/message.png").convert_alpha(), (300, 400))

    def create_pipe(self):
        x = WIDTH + 100
        y = choice(POSSIBLE_PIPE_HEIGHTS)
        Pipe((x, y), self.pipe_color, "bottom", self.pipe_sprites)
        Pipe((x, y - PIPE_DISTANCE), self.pipe_color, "top", self.pipe_sprites)

    def on_death(self):
        self.game_over = True

    def start_screen(self):
        self.display.blit(self.START_BG, (WIDTH / 2 - 145, HEIGHT / 2 - 250))

    def game_over_screen(self):
        self.display.blit(self.GAME_OVER_BG,
                          (WIDTH / 2 - 100, HEIGHT / 2 - 42))

    def main_screen(self):
        # Draw bird
        self.bird_sprite.update()
        self.bird_sprite.draw(self.display)

        # Draw pipes
        self.pipe_sprites.update()
        self.pipe_sprites.draw(self.display)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.pipe_timer:
                    self.create_pipe()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.game_started:
                            self.game_started = True
                        if not self.game_over:
                            self.bird.flap()
                        if self.game_over:
                            self.__init__()

            # Draw background
            self.display.blit(self.current_bg, (0, 0))

            # Screen
            if self.game_over:
                self.game_over_screen()
            elif self.game_started:
                self.main_screen()
            else:
                self.start_screen()

            # Draw floor
            self.floor_sprites.update()
            self.floor_sprites.draw(self.display)

            pygame.display.update()
            self.clock.tick(FPS)
