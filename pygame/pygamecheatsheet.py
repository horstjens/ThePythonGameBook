# Pygame Cheat Sheet
# This program should show you the basics of using the Pygame library.
# by Al Sweigart http://inventwithpython.com
# modification by Horst JENS http://ThePythonGameBook

# Download files from:
#     http://inventwithpython.com/cat.png
#     http://inventwithpython.com/bounce.wav

import pygame, sys, os
#from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Cheat Sheet')

redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
mousex, mousey = 0, 0
msg = 'Hello world!'
try:
    cat = os.path.join("data",'babytux.png')
    font = os.path.join("data", 'freesansbold.ttf')
    sound = os.path.join("data",'beep.ogg')
except:
    # does not raise alert if file does not exist ! TODO: fix
    raise UserWarning, "could not found files inside subfolder data"
catSurfaceObj = pygame.image.load(cat)
fontObj = pygame.font.Font(font, 32)
soundObj = pygame.mixer.Sound(sound)

while True:
    screen.fill(whiteColor)

    pygame.draw.polygon(screen, greenColor, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    pygame.draw.circle(screen, blueColor, (300, 50), 20, 0)
    pygame.draw.ellipse(screen, redColor, (300, 250, 40, 80), 1)
    pygame.draw.rect(screen, redColor, (10, 10, 50, 100))
    pygame.draw.line(screen, blueColor, (60, 160), (120, 60), 4)

    pixArr = pygame.PixelArray(screen)
    for x in range(100, 200, 4):
        for y in range(100, 200, 4):
            pixArr[x][y] = blueColor
    del pixArr


    screen.blit(catSurfaceObj, (mousex, mousey))

    msgSurfaceObj = fontObj.render(msg, False, blueColor)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (10, 20)
    screen.blit(msgSurfaceObj, msgRectobj)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = event.pos
            soundObj.play()
            if event.button in (1, 2, 3):
                msg = 'left, middle, or right mouse click'
            elif event.button in (4, 5):
                msg = 'mouse scrolled up or down'

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, 
                             pygame.K_UP, pygame.K_DOWN):
                msg = 'Arrow key pressed.'
            if event.key == pygame.K_a:
                msg = '"A" key pressed'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    pygame.display.update()
    fpsClock.tick(30) # pause to run the loop at 30 frames per second
