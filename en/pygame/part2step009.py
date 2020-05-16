# -*- coding: utf-8 -*-
"""
part2step009-loading-image-from-subfolder.py

loading 2 images from a subfolder called 'data'
Both images files must be in the subfolder 'data'. The subfolder must be inside the
same folder as the program itself. 
"""
import pygame
import os
import sys
try:
    # load from subfolder 'data'
    background = pygame.image.load(os.path.join("data","background640x480_a.jpg"))
    ball = pygame.image.load(os.path.join("data","snake.gif"))
except:
    sys.exit("Unable to find the images in the folder 'data' :-( ")  
#finally:
pygame.init()
screen=pygame.display.set_mode((640,480)) # try out larger values and see what happens !
background = background.convert()  # jpg can not have transparency
ball = ball.convert_alpha()        # png image has transparent color 
ballx, bally = 250, 240            # start position of ball surface
dx, dy  = 60, 60                   # ball speed in pixel per second !
screen.blit(background, (0,0))     # blit background on screen (overwriting all)
screen.blit(ball, (ballx, bally))  # blit the ball shape 
clock = pygame.time.Clock()        # create pygame clock object 
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 
while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
    pygame.display.set_caption("[FPS]: %.2f X:%.1f Y:%.1f Speed"
    " [pixel/sec] dx:%.2f dy:%.2f" % (clock.get_fps(), ballx, bally, dx, dy))
    # only blit the part of the background where the ball was (cleanrect)
    dirtyrect = background.subsurface((round(ballx,0), 
                round(bally,0), ball.get_width(), ball.get_height()))
    # comment out the next line for a funny effect !
    screen.blit(dirtyrect, (round(ballx,0), round(bally,0))) 
    #calculate new center of ball 
    ballx += dx * seconds # time based movement
    bally += dy * seconds
    # bounce ball if out of screen
    if ballx < 0:
        ballx = 0
        dx *= -1 
    elif ballx + ball.get_width() > screen.get_width():
        ballx = screen.get_width() - ball.get_width()
        dx *= -1
    if bally < 0:
        bally = 0
        dy *= -1
    elif bally + ball.get_height() > screen.get_height():
        bally = screen.get_height() - ball.get_height()
        dy *= -1
    # paint the ball    
    screen.blit(ball, (round(ballx,0), round(bally,0)))    
    pygame.display.flip()          # flip the screen 30 times a second                # flip the screen 30 (or FPS) times a second
