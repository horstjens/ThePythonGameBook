#!/usr/bin/env python
"""
005_bouncing_ball_frame_based.py
bouncing ball and pulsating circle
url: http://thepythongamebook.com/en:part2:pygame:step005
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with python3.4 and python2.7

bouncing ball. each frame the complete screen is filled with the background,
making this example simple to code but possible slow on larger resolutions.
Each frame, a random-coloured circle is drawn with randomized radius directly on the screen.
Try to manipulate the display.set_mode values to change the resolution."""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import random
pygame.init()
screen=pygame.display.set_mode((640,480),) # try out larger values and see what happens !
screenrect = screen.get_rect()
# ------ constants ------------
clock = pygame.time.Clock()
mainloop = True
FPS = 30 # desired framerate in frames per second. 
playtime = 0
radius = 50 # for pulsating circle
dr = 1  # change of radius in pixel per frame
# ------- background ---------
background = pygame.Surface(screen.get_size())
background.fill((255,155,155))     #fill the background white (red,green,blue)
background = background.convert()
screen.blit(background, (0,0))     #draw background on screen (overwriting all)
# -------- bouncing ball surface ---------
ballsurface = pygame.Surface((50,50))     #create a new surface (black by default)
ballsurface.set_colorkey((0,0,0))         #make black the transparent color (red,green,blue)
#pygame.draw.circle(Surface, color, pos, radius, width=0)
pygame.draw.circle(ballsurface, (100,175,81), (25,25),25) # paint blue circle
ballsurface = ballsurface.convert_alpha()       # if you use tranparent colors you need convert_alpha()
ballrect = ballsurface.get_rect() # the rectangle of the ball surface, for collision detection
ballx, bally = 550, 240           # start position of the ball (x,y)
dx = 10                 # x speed vector of the ball in pixel per frame            
dy = 0                 # y speed vector of the ball in pixel per frame
# ----------- bouncing ball (drawing) ------
x1 = 50
y1 = 200
dx1 = 7
dy1 = 0
radius1 = 40
# --------- static big blue ball -----------
pygame.draw.circle(background, (0,0,200), (screenrect.width//2, screenrect.height//2), screenrect.width//3)
# --------- mainloop ----------
while mainloop:
    # do all this each frame
    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
    pygame.display.set_caption("FPS: %.2f X: %.2f Y: %.2f dx: %.2f dy:"
                               " %.2f" % (clock.get_fps(), ballx, bally, dx, dy))
    # ----- clean screen ----------
    screen.blit(background, (0,0))     #draw background on screen (overwriting all)
    # ------- bouncing ball (drawing) ---------
    x1 += dx1
    if x1 + radius1 >= screenrect.width:
        x1 = screenrect.width - radius1
        dx1 *= -1
    elif x1 - radius1 <= 0:
        x1 =  radius1
        dx1 *= -1
    pygame.draw.circle(screen, (255,255,0), (x1,y1), radius1)
    # -------- bouncing ball surface ----------
    ballx += dx
    bally += dy 
    if ballx < 0: # bounce ball if out of screen
        ballx = 0
        dx *= -1 
    elif ballx + ballrect.width > screenrect.width:
        ballx = screenrect.width - ballrect.width
        dx *= -1
    screen.blit(ballsurface, (round(ballx,0), round(bally,0)))    
    # ----- pulsating circle -----------
    colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    if radius >100 or radius < 5:
        dr *= -1
    radius += dr
    pygame.draw.circle(screen, colour , (100,100), radius, 2) # draw pulsating circle
    # --------- flip screen ------------------
    pygame.display.flip()          # flip the screen FPS times a second
print("This 'game' was played for {:.2f} seconds.".format(playtime))
