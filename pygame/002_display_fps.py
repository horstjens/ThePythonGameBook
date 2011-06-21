# -*- coding: utf-8 -*-
"""
002_display_fps.py

Display frame rate

This program does nothing special, just starting an empty pygame screen,
displaying the framerate and making a clean exit if the ESCAPE key is pressed.

URL    : http://thepythongamebook.com/en:part2:pygame:step002
Author : horst.jens@spielend-programmieren.at
License: gpl, see http://www.gnu.org/licenses/gpl.html
"""

import pygame

# Initialize Pygame
pygame.init()
# Set window size
WIDTH = 640
HEIGHT = 480
screen=pygame.display.set_mode((WIDTH, HEIGHT))

# Create a pygame clock object
clock = pygame.time.Clock()
# Desired framerate in frames per second. try out other values !
FPS = 30
# How many seconds the "game" is played
playtime = 0.0 
y = 0
mainloop = True
while mainloop:

    # Update and erase screen
    pygame.display.flip()
    screen.fill((0, 0, 0))
    
    # Do not loop faster than this framerate
    milliseconds = clock.tick(FPS)
    # Add seconds to playtime
    playtime += milliseconds / 1000.0
    
    for event in pygame.event.get():
        # pygame window closed
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
                
    # Print framerate and playtime in window title
    pygame.display.set_caption("Frame Rate: %.2f, Playtime: %.2f seonds"\
                               % (clock.get_fps(), playtime))

    y = (y + 1) % HEIGHT
    pygame.draw.line(screen, (255, 255, 0), (0, y), (WIDTH-1, y))
    
    
print "This 'game' was played for %.2f seconds" % playtime
pygame.quit() 
