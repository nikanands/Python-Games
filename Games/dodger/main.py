import pygame, sys
from pygame.locals import *
from random import randint

def game_over():
    game_over_font = largeFont.render('Game Over', True, 'Purple')
    game_over_rect = game_over_font.get_rect(center=(200,300))
    screen.blit(game_over_font,game_over_rect)

def terminate():
    pygame.quit()
    sys.exit()

# INITIALIZE GAME
pygame.init()

# CREATE SCREEN
screen = pygame.display.set_mode((400,600))

# SCREEN TITLE
pygame.display.set_caption('Dodger')

# CLOCK
clock = pygame.time.Clock()

# FONT
largeFont = pygame.font.Font('freesansbold.ttf', 60)
basicFont = pygame.font.Font('freesansbold.ttf', 20)

# VARIABLES
game_active = True
heldKeys = []
stoneY = 0
playerX = 180
score = 0

# OBSTACLE
obstacle_img = pygame.image.load('stone.png').convert_alpha()
obstacle_rect = obstacle_img.get_rect(midbottom=(randint(20,350), 0))

# PLAYER
player_img = pygame.image.load('../halloween.png')
player_rect = player_img.get_rect(midtop=(playerX, 540))

# MAIN FUNCTION
def main():
    # SETTING THE VARIABLES GLOBAL
    global game_active, stoneY, playerX, heldKeys, score
    # MAIN LOOP
    while game_active:
        # SCREEN COLOR
        screen.fill('Gray')

        # EVENT CONDITIONS
        for event in pygame.event.get():
            # TO QUIT
            if event.type == QUIT:
                terminate()

            # KEYDOWN EVENT
            if event.type == KEYDOWN:
                # QUIT
                if event.key == K_ESCAPE:
                    terminate()
                # LEFT AND RIGHT ARROW MOVEMENT
                if event.key == K_LEFT:
                    heldKeys.append('Left Down')
                if event.key == K_RIGHT:
                    heldKeys.append('Right Down')
            # KEYUP EVENT
            if event.type == KEYUP:
                # LEFT AND RIGHT ARROW MOVEMENT
                if event.key == K_LEFT:
                    heldKeys.remove('Left Down')
                if event.key == K_RIGHT:
                    heldKeys.remove('Right Down')

        # PLAYER MOVEMENT
        if 'Left Down' in heldKeys:
            if player_rect.x > 0:
                player_rect.x -= 5
        if 'Right Down' in heldKeys:
            if player_rect.x < 350:
                player_rect.x += 5

        # PLACING THE OBSTACLES
        screen.blit(obstacle_img, obstacle_rect)

        # PLACING THE PLAYER
        screen.blit(player_img, player_rect)

        # OBSTACLES MOVEMENT
        if stoneY == 0:
            obstacle_rect.y += randint(5,15)
            score_text = basicFont.render('Score: ' + str(score), True, 'Blue')
            score_rect = score_text.get_rect(topleft=(10, 20))
            screen.blit(score_text, score_rect)

        if obstacle_rect.y > 650:
            obstacle_rect.y = 0
            obstacle_rect.x = randint(0, 350)
            score += 1

        # COLLISION
        if obstacle_rect.colliderect(player_rect):
            player_rect.x = -5000
            player_rect.y = 5000
            obstacle_rect.y = -100
            stoneY = -100

        if stoneY == -100:
            game_over()
            score_text = basicFont.render('Your Final Score is: ' + str(score), True, 'Blue')
            score_rect = score_text.get_rect(center=(180, 350))
            screen.blit(score_text, score_rect)

        # DISPLAY UPDATION
        pygame.display.update()
        clock.tick(60)

main()