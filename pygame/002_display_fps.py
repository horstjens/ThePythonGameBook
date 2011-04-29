# -*- coding: utf-8 -*-
"""
002_display_fps.py
display fps and clean exit
url: http://thepythongamebook.com/en:part2:pygame:step002
author: horst.jens@spielend-programmieren.at
licence: gpl

This program does nothing special,
just starting an empty pygame screen,
displaying the framerate and
making a clean exit if the ESCAPE key is pressed 
or the pygame window is closed."""
import pygame
pygame.init()                      #initialize pygame
screen=pygame.display.set_mode((640,480)) # set screensize of pygame window
background = pygame.Surface(screen.get_size())  #create empty pygame surface
background.fill((255,255,255))     #fill the background white color (red,green,blue)
background = background.convert()  #convert Surface object to make blitting faster
screen.blit(background, (0,0))     #draw the background on screen
clock = pygame.time.Clock()        #create a pygame clock object
mainloop = True                    
FPS = 30 # desired framerate in frames per second. try out other values !
playtime = 0.0 # how many seconds the "game" is played
while mainloop:
    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0 # add seconds to playtime
    print ("%i milliseconds passed since last frame" % milliseconds ) # brackets for python3.x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
    # print the framerate and playtime into the pygame window title
    pygame.display.set_caption("frame rate: %.2f frames per second, playtime: %.2f seonds" % (clock.get_fps(), playtime))
    pygame.display.flip()          # flip the screen like in a flip book
print "This 'game' was played for %.2f seconds" % playtime
pygame.quit() # idle-friendly quit method
