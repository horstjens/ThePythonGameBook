#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       screensaver.py
import pygame
import random

def screensaver(screenresolution = (640,480), fullscreen = False):
    # -*- coding: utf-8 -*-
    """very simple test "game" or screensaver.
       all the user have to do is press ESC or SPACE.
       the "game" paint random circles.
       the "game" accept a screen resolution tuple as argument.
       the "game" returns the time passed until the user pressed space"""
    pygame.init()                      #initialize pygame
    if fullscreen:
        screen=pygame.display.set_mode((screenresolution[0],screenresolution[1]), pygame.FULLSCREEN) # set screensize of pygame window
    else:
        screen=pygame.display.set_mode((screenresolution[0],screenresolution[1])) # set screensize of pygame window
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
        # paint random circles
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.draw.circle(screen, color, (random.randint(0,screenresolution[0]),
                                           random.randint(0,screenresolution[1])),
                                           random.randint(1, min(screenresolution[0], screenresolution[1])),
                                           random.randint(0,1))        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                print "event key:", event.key
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                if event.key == pygame.K_SPACE:
                    mainloop = False # user pressed ESC
        pygame.display.set_caption("press ESC to quit. FPS: %.2f (%ix%i), time: %.2f seonds" % (clock.get_fps(), screenresolution[0], screenresolution[1], playtime))
        pygame.display.flip()          # flip the screen like in a flip book
    print "This 'game' was played for %.2f seconds" % playtime
    pygame.quit()
    return playtime # in seconds

if __name__ == '__main__':
    screensaver()
