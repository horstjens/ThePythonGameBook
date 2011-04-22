# -*- coding: utf-8 -*-
"""
step005.py

bouncing ball and pulsating circle
url: http://thepythongamebook.com/en:part2:pygame:step005
author: horst.jens@spielend-programmieren.at


bouncing ball. each frame the complete screen is filled with the background,
making this example simple to code but possible slow on larger resolutions.
Each frame, a random-coloured circle is drawn with randomized radius directly on the screen.
Try to manipulate the display.set_mode values to change the resolution."""
import pygame
import random
pygame.init()
screen=pygame.display.set_mode((1000,480)) # try out larger values and see what happens !
screenrect = screen.get_rect()
background = pygame.Surface(screen.get_size())
background.fill((255,155,155))     #fill the background white (red,green,blue)
background = background.convert()
ballsurface = pygame.Surface((50,50))     #create a new surface (black by default)
ballsurface.set_colorkey((0,0,0))         #make black the transparent color (red,green,blue)
#pygame.draw.circle(Surface, color, pos, radius, width=0)
pygame.draw.circle(ballsurface, (100,175,81), (25,25),25) # paint blue circle
ballsurface = ballsurface.convert_alpha()       # if you use tranparent colors you need convert_alpha()
ballrect = ballsurface.get_rect() # the rectangle of the ball surface, for collision detection
ballx, bally = 550, 240           # start position of the ball (x,y)
dx = 10                 # x speed vector of the ball in pixel per frame            
dy = 10                 # y speed vector of the ball in pixel per frame
screen.blit(background, (0,0))     #draw background on screen (overwriting all)
screen.blit(ballsurface, (ballx, bally))  #draw the topleft corner of ball surface at pos (ballx, bally)
clock = pygame.time.Clock()
mainloop = True
FPS = 30 # desired framerate in frames per second. 
playtime = 0
radius = 50 # for pulsating circle
dr = 1  # change of radius in pixel per frame
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
    screen.blit(background, (0,0))     #draw background on screen (overwriting all)
    # ----- pulsating circle -----------
    colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    if radius >100 or radius < 5:
        dr *= -1
    radius += dr
    pygame.draw.circle(screen, colour , (100,100), radius, 2) # draw pulsating circle
    # -------- end of pulsating circle -------
    #calculate new center of ball 
    ballx += dx
    bally += dy
    # bounce ball if out of screen
    if ballx < 0:
        ballx = 0
        dx *= -1 
    #elif ballx + ball.get_width() > screen.get_width():
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
    screen.blit(ballsurface, (round(ballx,0), round(bally,0)))    
    pygame.display.flip()          # flip the screen FPS times a second
print "This 'game' was played for %.2f seconds." % playtime
