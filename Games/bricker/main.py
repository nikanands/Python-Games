import pygame, sys, asyncio
from pygame.locals import *

def draw_wall(bricks):
    for i in bricks:
        pygame.draw.rect(screen, 'Gray', i, border_radius=1)

# INITIALIZE PYGAME
pygame.init()

# MAIN SCREEN
screen = pygame.display.set_mode((600, 500))

# SCREEN TITLE
pygame.display.set_caption('BRICKER')

# BRICKS
r1 = [pygame.Rect(1+i*100, 60, 98, 18) for i in range(6)]
r2 = [pygame.Rect(1+i*100, 80, 98, 18) for i in range(6)]
r3 = [pygame.Rect(1+i*100, 100, 98, 18) for i in range(6)]
r4 = [pygame.Rect(1+i*100, 120, 98, 18) for i in range(6)]

# FLOOR
floor = pygame.Rect(250,450,100,10)

# BALL
ball = pygame.Rect(285,440,10,10)

# FONT
basic_font = pygame.font.Font('freesansbold.ttf', 20)
large_font = pygame.font.Font('freesansbold.ttf', 74)

# SCORE
score = 0


# GAME ACTIVE
game_active = True
move = [1,1]
heldKeys = []
clock = pygame.time.Clock()

async def main():
    global score, game_active, move, heldKeys, clock
    while game_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_active = False
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_active = False
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT:
                    heldKeys.append('Left_Down')
                if event.key == K_RIGHT:
                    heldKeys.append('Right_Down')

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    heldKeys.remove('Left_Down')
                if event.key == K_RIGHT:
                    heldKeys.remove('Right_Down')

        if 'Left_Down' in heldKeys:
            if floor.x > 5:
                floor.x -= 1
        if 'Right_Down' in  heldKeys:
            if floor.x < 495:
                floor.x += 1

        screen.fill('Purple')
        for i in r4:
            if i.collidepoint(ball.x, ball.y):
                r4.remove(i)
                move[0] = -move[0]
                move[1] = -move[1]
                score += 1

        for i in r3:
            if i.collidepoint(ball.x, ball.y):
                r3.remove(i)
                move[0] = -move[0]
                move[1] = -move[1]
                score += 1

        for i in r2:
            if i.collidepoint(ball.x, ball.y):
                r2.remove(i)
                move[0] = -move[0]
                move[1] = -move[1]
                score += 1

        for i in r1:
            if i.collidepoint(ball.x, ball.y):
                r1.remove(i)
                move[0] = -move[0]
                move[1] = -move[1]
                score += 1


        draw_wall(r1)
        draw_wall(r2)
        draw_wall(r3)
        draw_wall(r4)
        pygame.draw.rect(screen,'Red', ball)
        pygame.draw.rect(screen,'Green', floor)

        ball.x = ball.x + move[0]
        ball.y = ball.y + move[1]

        if (ball.x > 590) or (ball.x < 0):
            move[0] = -move[0]
        if ball.y <= 3:
            move[1] = -move[1]
        if floor.collidepoint(ball.x, ball.y):
            move[1] = -move[1]

        # SCORE
        if ball.y < 550:
            score_surf = basic_font.render(f'Score: {score}', True, 'White')
            screen.blit(score_surf,(230,20))
        else:
            score_surf = basic_font.render(f'Your Final Score is: {score}', True, 'White')
            screen.blit(score_surf, (200, 300))

        # GAME OVER
        game_over = large_font.render('GAME OVER', True, 'White')
        game_over_rect = game_over.get_rect(center=(300,250))
        if ball.y > 550:
            screen.blit(game_over, game_over_rect)
            ball.x = 610
            floor.x = 610
            heldKeys = []



        pygame.display.update()
        clock.tick(150)
        await asyncio.sleep(0)

asyncio.run(main())