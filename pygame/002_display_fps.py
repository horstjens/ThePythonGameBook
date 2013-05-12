#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
002_display_fps.py

<<<<<<< HEAD
Open a Pygame window and display framerate.
Program terminates by pressing the ESCAPE-Key.
 
Tested with Python 2.7 and 3.3. 

URL    : http://thepythongamebook.com/en:part2:pygame:step002
Aauthor: horst.jens@spielend-programmieren.at
License: GPL, see http://www.gnu.org/licenses/gpl.html
=======
Display frame rate

This program does nothing special, just starting an empty pygame screen,
displaying the framerate and making a clean exit.

URL    : http://thepythongamebook.com/en:part2:pygame:step002
Author : horst.jens@spielend-programmieren.at
License: gpl, see http://www.gnu.org/licenses/gpl.html
>>>>>>> pretty
"""

import pygame

<<<<<<< HEAD
# Initialize Pygame.
pygame.init()
# Set size of pygame window.
screen=pygame.display.set_mode((640,480))
# Create empty pygame surface.
background = pygame.Surface(screen.get_size())
# Fill the background white color.
background.fill((255, 255, 255))
# Convert Surface object to make blitting faster.
background = background.convert()
# Copy background to screen (position (0, 0) is upper left corner).
screen.blit(background, (0,0))
# Create Pygame clock object.  
clock = pygame.time.Clock()

mainloop = True
# Desired framerate in frames per second. Try out other values.              
FPS = 30
# How many seconds the "game" is played.
playtime = 0.0

while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0 
    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0 # add seconds to playtime

    for event in pygame.event.get():
        # User presses QUIT-button.
=======
# Initialize Pygame
pygame.init()
# Set window size
WIDTH = 640
HEIGHT = 480
screen=pygame.display.set_mode((WIDTH, HEIGHT))

# Create a pygame clock object
clock = pygame.time.Clock()
# Desired framerate in frames per second. Try out other values!
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
>>>>>>> pretty
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
                
<<<<<<< HEAD
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))

=======
    # Print framerate and playtime in window title
    pygame.display.set_caption("Frame Rate: %.2f, Playtime: %.2f seonds"\
                               % (clock.get_fps(), playtime))

    y = (y + 1) % HEIGHT
    pygame.draw.line(screen, (255, 255, 0), (0, y), (WIDTH-1, y))
    
    
print "This game was played for %.2f seconds." % playtime
pygame.quit() 
>>>>>>> pretty
