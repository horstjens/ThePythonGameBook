#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
006_time_baed_movement.py
url: http://thepythongamebook.com/en:part2:pygame:step006
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with python3.4 and pyhton2.7
 
bouncing ball. Movement is now time based.
Because at coding, you never know exactly how many milliseconds
will have been passed between two frames, this example use pygame's
clock function to calculate the passed time and move the ballsurface at
constantly the same speed. 
If you toggle the wild circle painting by pressing SPACE, the computer
has more to paint, framerate will drop, more time will pass between 
2 frames and movement of the ball surface will be choppy (less smooth).
However, the movent speed remain unchanged because of the time-based movement.
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import random


def wildPainting():
    """draw random circles to give the cpu some work to do"""
    pygame.draw.circle(background, (random.randint(0,255),
                       random.randint(0,255), random.randint(0,255)),
                       (random.randint(0,screenrect.width),
                       random.randint(0,screenrect.height)),
                       random.randint(50,500))

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
screen=pygame.display.set_mode((640,480)) # try out larger values and see what happens !
screenrect = screen.get_rect()
background = pygame.Surface(screen.get_size()) #create surface for background
background.fill((255,255,255))     #fill the background white (red,green,blue)
background = background.convert()  #convert surface for faster blitting
background2 = background.copy()    # clean background to restore for later 
ballsurface = pygame.Surface((50,50))     #create a new surface (black by default)
ballsurface.set_colorkey((0,0,0))         #make black the transparent color (red,green,blue)
#pygame.draw.circle(Surface, color, pos, radius, width=0)
pygame.draw.circle(ballsurface, (0,0,255), (25,25),25) # paint blue circle
ballsurface = ballsurface.convert_alpha()        # for faster blitting. because transparency, use convert_alpha()
ballrect = ballsurface.get_rect()
ballx, bally = 550,240             # start position for the ball surface (topleft corner)
dx,dy  = 60, 50                    # speed of ball surface in pixel per second !
                  
screen.blit(background, (0,0))     #blit the background on screen (overwriting all)
screen.blit(ballsurface, (ballx, bally))  #blit the ball surface on the screen (on top of background)
 
 
clock = pygame.time.Clock()        #create pygame clock object
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 
playtime = 0
paint_big_circles = False
cleanup = True
 
while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC

            elif event.key == pygame.K_1: 
                FPS = 10
            elif event.key == pygame.K_2:
                FPS = 20
            elif event.key == pygame.K_3:
                FPS = 30
            elif event.key == pygame.K_4:
                FPS = 40
            elif event.key == pygame.K_5:
                FPS = 50
            elif event.key == pygame.K_6:
                FPS = 60
            elif event.key == pygame.K_7:
                FPS = 70
            elif event.key == pygame.K_8:
                FPS = 80
            elif event.key == pygame.K_9:
                FPS = 90
            elif event.key == pygame.K_0:
                FPS = 1000 # absurd high value
            elif event.key == pygame.K_x:
                paint_big_circles =  not paint_big_circles # toggle
            elif event.key == pygame.K_y:
                cleanup = not cleanup # toggle boolean value
            elif event.key == pygame.K_w: # restore old background
                background.blit(background2, (0,0)) # clean the screen

                
               
            
    pygame.display.set_caption("x: paint ({}) y: cleanup ({}) ,"
                               " w: white, 0-9: limit FPS to {}"
                               " (now: {:.2f})".format(
                    paint_big_circles, cleanup, FPS,clock.get_fps()))
    if cleanup:
        screen.blit(background, (0,0))     #draw background on screen (overwriting all)
    if paint_big_circles:
       wildPainting()
    #calculate new center of ball (time-based)
    ballx += dx * seconds # float, since seconds passed since last frame is a decimal value
    bally += dy * seconds 
    # bounce ball if out of screen
    if ballx < 0:
        ballx = 0
        dx *= -1 
    elif ballx + ballrect.width > screenrect.width:
        ballx = screenrect.width - ballrect.width
        dx *= -1
    if bally < 0:
        bally = 0
        dy *= -1
    elif bally + ballrect.height > screenrect.height:
        bally = screenrect.height - ballrect.height
        dy *= -1
    # paint the ball    
    screen.blit(ballsurface, (round(ballx,0), round(bally,0 )))
    pygame.display.flip()          # flip the screen 30 times a second
print("This 'game' was played for {:.2f} seconds".format(playtime))
