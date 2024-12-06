import pygame, sys
from pygame.locals import *

pygame.init()

WINDOWWIDTH, WINDOWHEIGHT = 310,310
DISPLAYSCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
FONT = pygame.font.Font('freesansbold.ttf',16)
p1 = (350,200)
board = [[None,None,None],[None,None,None],[None,None,None]]
xo = 'x'

def terminate():
    pygame.quit()
    sys.exit()

def drawKeyPressMsg():
    msgSurf = FONT.render('Press Enter to start game', True, (0,0,0))
    msgRect = msgSurf.get_rect()
    msgRect.topleft = (WINDOWWIDTH-200, WINDOWHEIGHT-30)
    DISPLAYSCREEN.blit(msgSurf,msgRect)

def checkKeyPress():
    if pygame.event.get(QUIT):
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) <= 0:
        return None
    elif keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key == K_RETURN

def startScreen():
    DISPLAYSCREEN.fill((0,250,0))
    start_font = pygame.font.Font('freesansbold.ttf', 50)
    start_game = start_font.render('Start Game', True, (255,255,255), (0,250,0))
    while True:
        DISPLAYSCREEN.blit(start_game, (50,150))

        drawKeyPressMsg()

        if checkKeyPress():
            pygame.event.get()
            return
        pygame.display.update()

def drawBoard():
    # for x in range(120, 360, 120):
    #     pygame.draw.line(DISPLAYSCREEN, (0, 0, 0), (x, 0), (x, 360),2)
    # for y in range(120, 360, 120):
    #     pygame.draw.line(DISPLAYSCREEN, (0, 0, 0), (0, y), (360, y),2)

    # tile = pygame.draw.rect(DISPLAYSCREEN, (255, 255, 255), (x, y, 100, 100))
    drawTile(0,0)
    drawTile(105, 0)
    drawTile(210, 0)
    drawTile(0, 105)
    drawTile(105, 105)
    drawTile(210, 105)
    drawTile(0, 210)
    drawTile(105, 210)
    drawTile(210, 210)

def drawXO(a):
    x = pygame.image.load('cross.png')
    o = pygame.image.load('circle.png')
    if a == 'x':
        DISPLAYSCREEN.blit(x,(80,50))
    elif a == 'o':
        DISPLAYSCREEN.blit(o, (80, 50))

def drawTile(x,y):
    pygame.draw.rect(DISPLAYSCREEN, (255,255,255),(x,y,100,100))

startScreen()
while True:
    DISPLAYSCREEN.fill((255,0,0))
    # drawXO()

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
        if event.type == MOUSEBUTTONDOWN:
            print('x')
            DISPLAYSCREEN.blit(pygame.image.load('cross.png'), (80,50))
            # drawXO(xo)
            xo = 'o'


    drawBoard()


    pygame.display.update()