#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name:    010_sound_only_no_graphic.py
Purpose: demonstrate use of pygame for playing sound & music
URL:     http://ThePythonGameBook.com 
Author:  Horst.Jens@spielend-programmieren.at
Licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with pyhton3.4 and python2.7
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

import pygame
import os
import sys

# if using python2, the get_input command needs to act like raw_input:
if sys.version_info[:2] <= (2, 7):
    get_input = raw_input
else:
    get_input = input # python3
        

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()                              #initialize pygame

# look for sound & music files in subfolder 'data'
pygame.mixer.music.load(os.path.join('data', 'an-turr.ogg'))#load music
jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound

# play music non-stop
pygame.mixer.music.play(-1)                           

# game loop
gameloop = True

while gameloop:
    # indicate if music is playing
    if pygame.mixer.music.get_busy():
        print(" ... music is playing")
    else: 
        print(" ... music is not playing")
    # print menu 
    print("please press key:")
    print("[a] to play 'jump.wav' sound")
    print("[b] to play 'fail.wav' sound")
    print("[m] to toggle music on/off")
    print("[q] to quit")
    answer = get_input("press key [a] or [b] or [m] or [q], followed by [ENTER]")
    answer = answer.lower() # force lower case
    if "a" in answer:
        jump.play()
        print("playing jump.wav once")
    elif "b" in answer:
        fail.play()
        print("playing fail.wav once")
    elif "m" in answer:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play()
    elif "q" in answer:
        #break from gameloop
        gameloop = False
    else:
        print("please press either [a], [b], [m] or [q] and [ENTER]")


print("bye-bye")
pygame.quit() # clean exit 
