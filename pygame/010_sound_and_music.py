#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
010_sound_and_music.py
plays music and sound effects
url: http://thepythongamebook.com/en:part2:pygame:step010
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

This program plays music and 
plays a sound effect whenever the a of b  key is pressed and released
All files must be in a 'data' subfolder.
The 'data' subfolder must be in the same folder as the program.

works with python3.4 and python2.7
"""
import pygame
import os


pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()                      #initialize pygame

try:
    pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
    jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
    fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound
except:
    raise(UserWarning, "could not load or play soundfiles in 'data' folder :-(")

pygame.mixer.music.play(-1)                           # play music non-stop

screen=pygame.display.set_mode((640,480)) # set screensize of pygame window
background = pygame.Surface(screen.get_size())  #create empty pygame surface
background.fill((255,255,255))     #fill the background white color (red,green,blue)
background = background.convert()  #convert Surface object to make blitting faster
screen.blit(background, (0,0))     #draw the background on screen
clock = pygame.time.Clock()        #create a pygame clock object
mainloop = True                    
FPS = 30 # desired framerate in frames per second. try out other values !
while mainloop:
    milliseconds = clock.tick(FPS) # do not go faster than this framerate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
            if event.key == pygame.K_a:
                fail.play()                  # play sound effect
            if event.key == pygame.K_b:
                jump.play()                  # play sound effect
    # print the framerate into the pygame window title
    pygame.display.set_caption("FPS: {:.2f} Press [a] or [b] to play sound effects".format(clock.get_fps()))
    pygame.display.flip()          # flip the screen
