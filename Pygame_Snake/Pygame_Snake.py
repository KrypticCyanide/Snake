## Imports for future defined variables
from sys import exit
import sys
import pygame
import random, pygame, sys
from pygame.locals import *

## FPS = Snake Speed
FPS = 12.5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

bkrnd_img = "Images/Black.png"

## Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 20, 75)
DARKSOULSRED = (185, 35, 35)
DARKPURPLE = (100, 0, 200)
PURPLE = (155, 50, 255)
GREEN = (35, 140, 35)
DARKGREEN = (0, 100, 0)
DARKGRAY = (40, 50, 70)
DARKSLATEGRAY = (45, 80, 80)
DARKOLIVEGREEN = (100, 105, 45)
DARKEROLIVEGREEN = (85 ,150, 45)
BLUE = (30, 180, 170)
ALICEBLUE = (240, 250, 255)
LIGHTBLUE = (155, 185, 250)
LIGHTSKYBLUE = (115, 195, 250)
ROYALBLUE = (65, 105, 225)
STEELBLUE = (70, 130, 180)
MEDIUMBLUE = (0, 0, 205)
NAVYBLUE = (0, 0, 130)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

## Index of snake's head
HEAD = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Slippery Snaek Schlurps Snaccs')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    ## Sets a random start point (how nice...)
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakeCoords =[{'x':startx - 1, 'y':starty},
                  {'x':startx - 2, 'y':starty}]
    direction = RIGHT

    ## Start the apple in a random place
    apple = getRandomLocation()
    ## Main game loop
    while True:
        ## Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif(event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif(event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif(event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                        terminate()
        ## Check if the snaek has hit itself or the edge; Rad, dudes !
        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
            ## Game over! Oof
            return
        for snakeBody in snakeCoords[1:]:
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                ## Game over! Oof x2
                return
        ## Check if snaek has eaten an apple
        if snakeCoords[HEAD]['x'] == apple['x'] and snakeCoords[HEAD]['y'] == apple['y']:
            file = 'Sound_Effects/AppleCrunch2.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            ## Don't remove the snaek's tail segment, that'd be goodn't
            ## Set a new apple somewhere random
            apple = getRandomLocation()
        else:
            ## Remove snake's tail segment, ah hek
            del snakeCoords[-1]
## Moving the snaek; heck yeah!
## Add segment in the direction it is Moving
        if direction == UP:
            newHead = {'x':snakeCoords[HEAD]['x'],'y': snakeCoords[HEAD]['y']-1}
        elif direction == DOWN:
            newHead = {'x':snakeCoords[HEAD]['x'],'y': snakeCoords[HEAD]['y']+1}
        elif direction == LEFT:
            newHead = {'x':snakeCoords[HEAD]['x']-1,'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x':snakeCoords[HEAD]['x']+1,'y': snakeCoords[HEAD]['y']}
        snakeCoords.insert(0, newHead)

## HOLY HECK THE REALM IS REAL
# (Drawing the screen)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawSnake(snakeCoords)
        drawApple(apple)
        drawScore(len(snakeCoords) - 2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

## You know, you gotta do the thing to play the game...
## (Function for start message)
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play . . .', True, BLUE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT -30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 110)
    titleSurf1 = titleFont.render('§naek!', True, NAVYBLUE, ROYALBLUE)
    titleSurf2 = titleFont.render('§naek!', True, MEDIUMBLUE)

    degrees1 = 0
    degrees2 = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            ## Clear event queue
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        ## Rotates by 3 degrees each frame
        degrees1 += 3
        ## Rotates by 6 degrees each frame
        degrees2 += 6

def terminate():
    pygame.quit()
    sys.exit()

## Hey, where's that hek'n apple ?
def getRandomLocation():
    return{'x': random.randint(0, CELLWIDTH - 1), 'y':random.randint(0, CELLHEIGHT - 1)}

## Well, you hek' up (GAME OVER SCREEN)
def showGameOverScreen():
    gameOverFont = pygame.font.Font('C:\Windows\Fonts\OptimusPrincepsSemiBold.ttf', 120)
    gameSurf = gameOverFont.render('', True, DARKSOULSRED)
    overSurf = gameOverFont.render('YOU DIED', True, DARKSOULSRED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    file = 'Sound_Effects/YouDied.wav'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    screen = pygame.display.set_mode((640, 480), 0, 16)
    background = pygame.image.load(bkrnd_img).convert()

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    ## Clear out any key presses in the event queue
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            ## Clear event queue
            pygame.event.get()
            return

## Score
def drawScore(score):
    scoreFont = pygame.font.Font('C:\Windows\Fonts\ArDestine.ttf', 24)
    scoreSurf = scoreFont.render('Score: %s' % (score), True, ALICEBLUE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH -120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

## Squares for snake (Y33T)
def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKOLIVEGREEN, snakeInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrid():
    ## Draws vertical lines
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    ## Draws Horizontal lines
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
         pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

## Let us being, shall we?
if __name__== '__main__':
    main()
