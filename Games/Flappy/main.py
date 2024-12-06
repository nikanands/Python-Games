import pygame, sys, random
from pygame.locals import *

def terminate():
    pygame.quit()
    sys.exit()

def draw_floor():
    screen.blit(floor_surf, (floor_x_pos, 800))
    screen.blit(floor_surf, (floor_x_pos + 576, 800))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop=(800, random_pipe_pos))
    top_pipe = pipe_surf.get_rect(midbottom=(800, random_pipe_pos - 250))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_surf, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf,False,True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 800:
        death_sound.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surf = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surf.get_rect(center=(288,100))
        screen.blit(score_surf, score_rect)
    if game_state == 'game_over':
        score_surf = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(288, 100))
        screen.blit(score_surf, score_rect)

        high_score_surf = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surf.get_rect(center=(288, 750))
        screen.blit(high_score_surf, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# INITIALIZE THE MIXER AND PYGAME
pygame.mixer.pre_init(frequency=44100, size= 16, channels=1, buffer=512)
pygame.init()

# CREATING SCREEN AND TITLE
screen = pygame.display.set_mode((576,900))
pygame.display.set_caption('Flappy Bird')

# CREATE CLOCK
clock = pygame.time.Clock()

# CREATING BACKGROUND
bg_surf = pygame.image.load('image/background-day.png').convert()
bg_surf = pygame.transform.scale2x(bg_surf)

# CREATING FLOOR
floor_surf = pygame.image.load('image/base.png').convert()
floor_surf = pygame.transform.scale2x(floor_surf)
floor_x_pos = 0

# CREATING BIRDS
bird_downflap = pygame.transform.scale2x(pygame.image.load('image/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('image/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('image/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surf = bird_frames[bird_index]
bird_rect = bird_surf.get_rect(center=(100,400))

# CREATING PIPE
pipe_surf = pygame.image.load('image/pipe-green.png')
pipe_surf = pygame.transform.scale2x(pipe_surf)
pipe_list = []
pipe_height = [300,500,600]

# CREATING GAME OVER SCREEN
game_over_surf = pygame.transform.scale2x(pygame.image.load('image/message.png').convert_alpha())
game_over_rect = game_over_surf.get_rect(center = (288,450))

# CREATING GAME FONT
game_font = pygame.font.Font('04B_19.ttf',40)

# CREATING CUSTOM EVENT
## BIRD FLAP
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

## PIPE
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)

# CREATING SOUND
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# VARIABLES
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0
game_active = True
score_sound_countdown = 100

# MAIN LOOP
while True:
    # EVENT TRIGGER
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

            if event.key == K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,400)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surf, bird_rect =  bird_animation()

    # SHOWING MAIN SCREEN
    screen.blit(bg_surf, (0,0))

    # MAIN CONDITIONS
    if game_active:
        # BIRD
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surf)
        bird_rect.centery += bird_movement
        screen.blit(bird_surf,bird_rect)

        # PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # CHECK COLLISION
        game_active = check_collision(pipe_list)

        # SCORE
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        # HIGH SCORE
        high_score = update_score(score,high_score)
        score_display('game_over')
        screen.blit(game_over_surf,game_over_rect)

    # DRAW FLOOR
    draw_floor()

    # CREATING ENDLESS FLOOR
    floor_x_pos -= 1
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # UPDATING THE GAME
    pygame.display.update()
    clock.tick(120)
