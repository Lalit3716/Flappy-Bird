import pygame, sys, os, pickle
from random import choice

# Init
pygame.init()

# Load High Score
if not os.path.isfile("data/data.bat"):
    with open("data/data.bat", "wb"):
        HIGH_SCORE = 0
else:
    with open("data/data.bat", "rb") as f:
        HIGH_SCORE = int(pickle.load(f))


def draw_floor():
    screen.blit(floor, (floor_x, 500))
    screen.blit(floor, (floor_x + WIDTH, 500))


def rotate_bird():
    new_bird = pygame.transform.rotozoom(
        birds[int(bird_index)], -bird_movement * 2, 1.8
    )
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    screen.blit(new_bird, new_bird_rect)
    return new_bird_rect


def animate_bird(speed=0.1):
    global bird_index
    bird_index += speed
    if bird_index >= len(birds):
        bird_index = 0


def create_pipe():
    height = choice(POSSIBLE__PIPE_HEIGHTS)
    top_rect = pipe_img.get_rect(midbottom=(WIDTH + 100, height - 200))
    bottom_rect = pipe_img.get_rect(midtop=(WIDTH + 100, height))
    return (bottom_rect, top_rect)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_SPEED
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= WIDTH - 300:
            screen.blit(pipe_img, pipe)
        else:
            reversed_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(reversed_pipe, pipe)


def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx <= -100:
            pipes.remove(pipe)


def check_collisions(bird, pipes):
    if bird.bottom >= WIDTH - 250 or bird.top <= 0:
        # death_sound.play()
        hit_sound.play()
        return True
    if not CHEAT_ENABLED:
        for pipe in pipes:
            if bird.colliderect(pipe):
                # death_sound.play()
                hit_sound.play()
                return True
    return False


def calc_score(pipes, bird):
    global SCORE, HIGH_SCORE
    for pipe in pipes:
        if pipe.centerx == bird.centerx:
            SCORE += 1
            point_sound.set_volume(0.1)
            point_sound.play()

    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
    return SCORE


def write_Font(
    pos, message="", size=40, score=None, HighScore=None, color=(255, 255, 255)
):
    font = pygame.font.Font("data/font/04B_19.ttf", size)
    if score != None and score >= 0:
        text = font.render(f"{message}{score}", False, color)
    elif HighScore != None and HighScore >= 0:
        text = font.render(f"{message}{HighScore}", False, color)
    else:
        text = font.render(f"{message}", False, color)
    screen.blit(text, pos)


# Game Variables
WIDTH = 800
HEIGHT = 600
FPS = 120
GRAVITY = 0.25
PIPE_SPEED = 5
GAME_OVER = False
LOADING = True
POSSIBLE__PIPE_HEIGHTS = [250, 350, 300, 390, 420]
SCORE = 0
CHEAT_ENABLED = False
CHECKPOINT = 20

# Configs
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
PIPE_TIMER = pygame.USEREVENT
pygame.time.set_timer(PIPE_TIMER, 1200)
death_sound = pygame.mixer.Sound("data/sound/sfx_die.wav")
flap_sound = pygame.mixer.Sound("data/sound/sfx_wing.wav")
swooshing_sound = pygame.mixer.Sound("data/sound/sfx_swooshing.wav")
hit_sound = pygame.mixer.Sound("data/sound/sfx_hit.wav")
point_sound = pygame.mixer.Sound("data/sound/sfx_point.wav")

# Background-Images
bg_day_image = pygame.image.load("data/assets/background-day.png").convert_alpha()
bg_day_image = pygame.transform.scale(bg_day_image, (WIDTH, HEIGHT))
bg_night_image = pygame.image.load("data/assets/background-night.png").convert_alpha()
bg_night_image = pygame.transform.scale(bg_night_image, (WIDTH, HEIGHT))

# Floor-Image
floor = pygame.image.load("data/assets/base.png")
floor = pygame.transform.scale(floor, (WIDTH, 100))
floor_x = 0

# Game-Over Image
game_over_img = pygame.image.load("data/assets/gameover.png").convert_alpha()
game_over_message = pygame.image.load("data/assets/message.png").convert_alpha()
game_over_message = pygame.transform.scale(game_over_message, (300, 400))

# Bird-Images
birds = []
birds.append(pygame.image.load("data/assets/bluebird-downflap.png").convert_alpha())
birds.append(pygame.image.load("data/assets/bluebird-midflap.png").convert_alpha())
birds.append(pygame.image.load("data/assets/bluebird-upflap.png").convert_alpha())
bird_index = 0
bird_movement = 0
bird_rect = birds[0].get_rect(center=(100, 250))

# Pipes
pipes = []
pipe_green_img = pygame.image.load("data/assets/pipe-green.png")
pipe_red_img = pygame.image.load("data/assets/pipe-red.png")

# Main Loop
while True:
    if SCORE <= CHECKPOINT:
        screen.blit(bg_day_image, (0, 0))
        pipe_img = pipe_green_img

    elif SCORE >= CHECKPOINT:
        screen.blit(bg_night_image, (0, 0))
        pipe_img = pipe_red_img
        if SCORE == CHECKPOINT + 20:
            CHECKPOINT += 40

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/data.bat", "wb") as f:
                pickle.dump(str(HIGH_SCORE), f)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and LOADING:
                LOADING = False

            if event.key == pygame.K_SPACE and not GAME_OVER and not LOADING:
                # flap_sound.play()
                swooshing_sound.play()
                bird_movement = 0
                bird_movement -= 9
            if event.key == pygame.K_SPACE and GAME_OVER:
                bird_rect.center = (100, 250)
                pipes.clear()
                bird_movement = 0
                GAME_OVER = False
                bird_index = 0
                SCORE = 0
                LOADING = True
            if event.key == pygame.K_LCTRL:
                CHEAT_ENABLED = not CHEAT_ENABLED

        if event.type == PIPE_TIMER and not LOADING and not GAME_OVER:
            pipes.extend(create_pipe())

    if not GAME_OVER and not LOADING:
        # Bird
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        rotated_bird_rect = rotate_bird()
        animate_bird(0.08)

        GAME_OVER = check_collisions(rotated_bird_rect, pipes)

        # Pipes
        draw_pipes(pipes)
        move_pipes(pipes)
        remove_pipes(pipes)

        SCORE = calc_score(pipes, rotated_bird_rect)
        write_Font((WIDTH / 2, 100), score=SCORE)
        write_Font((WIDTH / 2 - 100, 50), message="High Score-", HighScore=HIGH_SCORE)

    if LOADING:
        screen.blit(game_over_message, (WIDTH / 2 - 145, HEIGHT / 2 - 250))

    if GAME_OVER:
        screen.blit(game_over_img, (WIDTH / 2 - 100, HEIGHT / 2 - 42))
        write_Font((WIDTH / 2, 100), score=SCORE)
        write_Font((WIDTH / 2 - 100, 50), message="High Score-", HighScore=HIGH_SCORE)

    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -WIDTH:
        floor_x = 0

    pygame.display.update()
    clock.tick(FPS)
