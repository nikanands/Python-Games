import pygame, sys, random, math
from pygame.locals import *

# Initialize PyGame
pygame.init()

# Creating Screen
screen = pygame.display.set_mode((800,600))

# Background Sound
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption('Zombie Runner')
logo = pygame.image.load('halloween.png')
pygame.display.set_icon(logo)

playerX = 370
playerY = 500
playerX_change = 0


# ZOMBIE
zombieImg = []
zombieX = []
zombieY = []
zombieX_change = []
zombieY_change = []
num_of_zombies = 20
for i in range(num_of_zombies):
    zombieImg.append(pygame.image.load("halloween.png"))
    zombieX.append(random.randint(0,760))
    zombieY.append(random.randint(50,200))
    zombieX_change.append(0.3)
    zombieY_change.append(40)

# BULLET
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change=0
bulletY_change=1
bullet_state = 'ready'

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def terminate():
    pygame.quit()
    sys.exit()

def drawZombie(x,y,i):
    screen.blit(zombieImg[i], (x,y))

def drawPlayer(x,y):
    player = pygame.image.load('spaceship.png')
    screen.blit(player, (x,y))

def fireBullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))

def showScore(x,y):
    score_val = font.render("Score: " + str(score), True, (0,0,0))
    screen.blit(score_val, (x,y))

def isCollision(zombieX,zombieY,bulletX,bulletY):
    distance = math.sqrt((math.pow(zombieX-bulletX,2)) + (math.pow(zombieY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def gameOver():
    game_over_font = pygame.font.Font('freesansbold.ttf', 80)
    game_over = game_over_font.render("GAME OVER", True, (0,0,0))
    screen.blit(game_over, (170, 200))

    play_again_font = pygame.font.Font('freesansbold.ttf', 60)
    play_again = play_again_font.render("Play Again", True, (0,0,0))
    screen.blit(play_again, (250,300))



# Main Loop

while True:
    screen.fill((255,250,200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()


        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
            # MOVEMENT of PLAYER
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.5
            if event.key == pygame.K_RIGHT:
                playerX_change += 0.5

            # BULLET
            if event.key == K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        if event.type == MOUSEMOTION:
            # print(pygame.mouse.get_pos())
            if pygame.mouse.get_pos() == (403,549):
                    print(pygame.mouse.get_pos())


    # BOUNDARY of PLAYER
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX=736

    # MOVEMENT OF ZOMBIE
    for i in range(num_of_zombies):

        # GAME OVER
        if zombieY[i] > 400: # CHANGE IT LATER TO 400
            for j in range(num_of_zombies):
                zombieY[j] = 2000
            gameOver()
            break

        zombieX[i] += zombieX_change[i]
        if zombieX[i] <= 0:
            zombieX_change[i] =0.3
            zombieY[i] += zombieY_change[i]
        elif zombieX[i] >= 768:
            zombieX_change[i] =-0.3
            zombieY[i] += zombieY_change[i]

        # COLLISION
        collision = isCollision(zombieX[i], zombieY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            zombieX[i] = random.randint(0, 760)
            zombieY[i] = random.randint(50, 200)
            explosion_sound = pygame.mixer.Sound('/Users/nik/Downloads/explosion.wav')
            explosion_sound.play()

        drawZombie(zombieX[i], zombieY[i], i)


    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerX += playerX_change


    drawPlayer(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update()