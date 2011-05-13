# -*- coding: utf-8 -*-
"""
part2step012-coding.py

This program demonstrate how to render and blit text into a surface"""

import pygame
import random

def flytext(msg="hello world", duration=5):

    def newcolour():
        # any colour but black or white 
        return (random.randint(10,250), random.randint(10,250), random.randint(10,250))

    def write(msg="pygame is cool"):
        myfont = pygame.font.SysFont("None", random.randint(34,128))
        mytext = myfont.render(msg, True, newcolour())
        mytext = mytext.convert_alpha()
        return mytext
        
    pygame.init()
    x = 60
    y = 60
    dx = 5
    dy = 5

    screen = pygame.display.set_mode((640,400))
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255)) # white
    background = background.convert()
    screen.blit(background, (0,0)) # clean whole screen
    clock = pygame.time.Clock()
    mainloop = True
    FPS = 60 # desired framerate in frames per second.
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
        textsurface = write("hello world")
        #screen.blit(background, (0,0)) # clean whole screen
        x += dx
        y += dy
        if x < 0:
           x = 0
           dx *= -1
           screen.blit(background, (0,0)) # clean whole screen
        elif x + textsurface.get_width() > screen.get_width():
            x = screen.get_width() - textsurface.get_width()
            dx *= -1
        if y < 0:
            y = 0
            dy *= -1
        elif y + textsurface.get_height() > screen.get_height():
            y = screen.get_height() - textsurface.get_height()
            dy *= -1
            
        screen.blit(textsurface, (x,y))
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__":
    flytext()
