# Import Libraries

import pygame
import time
import random

# Snake Speed
snake_speed = 20

# Window Size
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0,0,0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

# Initialising Pygame
pygame.init()

# Initialising Game Window
pygame.display.set_caption('Totoro Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (Frames Per Second) Controller
fps = pygame.time.Clock()

# Defining Snake Default Position
snake_position = [100,50]

# Defining first 4 block of snake body
snake_body = [[100, 50],[90,50],[80,50],[70,50]]

# Fruit Position
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# Default Snake Direction
direction = 'RIGHT'
change_to = direction

# Initial Score
score = 0

# Display score function
def show_score(choice, color, font, size):
    # Creating Font Object
    score_font = pygame.font.SysFont(font, size)

    # Create Display Surface Object
    score_surface = score_font.render('Score :' + str(score), True, color)

    # Create Background for Score Surface
    score_rect = score_surface.get_rect()

    # Display Text
    game_window.blit(score_surface, score_rect)

# Game Over Function
def game_over():
    # Creating Font Object
    my_font = pygame.font.SysFont('times new roman', 50)

    # Creating Text Surface
    game_over_surface = my_font.render('Your Score Is : ' + str(score), True, red)

    # Creating Rectangular Object for Text Surface
    game_over_rect = game_over_surface.get_rect()

    # Setting Position of Text
    game_over_rect.midtop = (window_x/2, window_y/4)

    # Blit will draw text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # After 2 Sec, Quit the program
    time.sleep(2)

    # Deactivate Pygame Library
    pygame.quit()

    # Quit the program
    quit()


# MAIN FUNCTION
while True:
     # Handling Key Events
     for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'


    # Don't Move in two directions
     if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
     if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
     if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
     if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'



    # Moving Snake
     if direction == 'UP':
        snake_position[1] -= 10
     if direction == 'DOWN':
        snake_position[1] += 10
     if direction == 'LEFT':
        snake_position[0] -= 10
     if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake Body Growing
     snake_body.insert(0, list(snake_position))
     if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
     else:
        snake_body.pop()

     if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10))*10,
                          random.randrange(1, (window_y//10))*10]

     fruit_spawn = True
     game_window.fill(black)

     for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))


        # Game Over Conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y-10:
            game_over()

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        # Displaying Score
        show_score(1, white, 'time new roman', 22)

        # Refresh Game
        pygame.display.update()

        # FPS/Refresh Rate (SNAKE SPEED MAYBE)
        fps.tick(snake_speed)

