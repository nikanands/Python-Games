import pygame
import random
import math
from pygame import mixer


# Initialize the PyGame
pygame.init()

# Creating the Screen
screen = pygame.display.set_mode((800,600))

# Background Sound
mixer.music.load('/Users/nik/Downloads/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load("/Users/nik/Downloads/spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("/Users/nik/Downloads/spaceship.png")
playerX = 370
playerY = 500
playerX_change=0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("/Users/nik/Downloads/enemy.png"))
    enemyX.append(random.randint(0,760))
    enemyY.append(random.randint(50,200))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("/Users/nik/Downloads/bullet.png")
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

def showScore(x,y):
    score_val = font.render("Score: " + str(score), True, (0,0,0))
    screen.blit(score_val, (x,y))

def gameOver():
    game_over_font = pygame.font.Font('freesansbold.ttf', 100)
    game_over = game_over_font.render("GAME OVER", True, (0,0,0))
    screen.blit(game_over, (80, 250))

def drawPlayer(x,y):
    screen.blit(playerImg,(x, y))

def drawEnemy(x,y, i):
    screen.blit(enemyImg[i],(x, y))

def fireBullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Main Loop
running=True

while running:
    screen.fill((255, 250, 200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 0.5
            if event.key == pygame.K_RIGHT:
                playerX_change += 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('/Users/nik/Downloads/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change

    if playerX <= 0:
        playerX=0
    elif playerX >= 768:
        playerX=768


    # ENEMY BOUNDARY
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] =0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] =-0.3
            enemyY[i] += enemyY_change[i]

        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 760)
            enemyY[i] = random.randint(50, 200)
            explosion_sound = mixer.Sound('/Users/nik/Downloads/explosion.wav')
            explosion_sound.play()

        drawEnemy(enemyX[i], enemyY[i], i)

    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change


    drawPlayer(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()