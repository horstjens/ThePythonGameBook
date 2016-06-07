#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
004_colorkey.py
dynamic blitting and colorkey
url: http://thepythongamebook.com/en:part2:pygame:step004
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

Blitting one surface on 2 static positions, once before the
mainloop and once inside the mainloop.
using colorkey to make a part of the surfaces tranparent
blitting lines on the screen to create a colourful pattern
like in a screensaver
"""
 
import pygame
import random
pygame.init()
screen=pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((255,255,255))     # fill the background white (red,green,blue)
background = background.convert()  # faster blitting
ballsurface = pygame.Surface((50,50))     # create a new surface (black by default)
ballsurface.set_colorkey((0,0,0))         # make black the transparent color (red,green,blue)
#pygame.draw.circle(Surface, color, pos, radius, width=0)
pygame.draw.circle(ballsurface, (0,0,255), (25,25),25) # paint blue circle
ballsurface = ballsurface.convert_alpha()        # faster blitting, convert_alpha() because transparency
screen.blit(background, (0,0))     #draw background on screen (overwriting all)
ballx = 20   # left ball position
bally = 240
screen.blit(ballsurface, (ballx, bally))  #draw the ball surface (lines will draw over this ball)
ballx2 = 400  # right ball position
bally2 = 380
clock = pygame.time.Clock()
mainloop = True
FPS = 30 # desired framerate in frames per second. try out other values !
playtime = 0.0
t = 0 # variable used to draw a pattern
color1 = 0
color2 = 0
while mainloop:
    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
    # ------- draw cute pattern ------------------
    pygame.draw.line(screen, (color1,255-color1,color2), (32*t,0), (0,480-24*t))
    pygame.draw.line(screen, (255-color2,color2,color1), (32*t,480), (640,480-24*t))
    screen.blit(ballsurface, (ballx2, bally2))  #draw the ball over the lines 
    t += 1   # increase t
    if t > 20:
        t = 0 # reset t
        color1 = random.randint(0,255) # new color
        color2 = random.randint(0,255)
    # --------- end of cute pattern drawing code ----------
    pygame.display.set_caption("Frame rate %.2f frames per second. Playtime: %.2f seconds" % (clock.get_fps(),playtime))  
    pygame.display.flip()          # flip the screen 30 times a second
print "This 'game' was played for %.2f seconds." % playtime
