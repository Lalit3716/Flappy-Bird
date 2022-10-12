import pygame
from game import Game
from settings import *

# Initialize pygame
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game loop
Game().run()
