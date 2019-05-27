#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
008_animation.py
animation & spritesheet
url: http://thepythongamebook.com/en:part2:pygame:step008
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html


spritesheet from
http://www.flyingyogi.com

using subsurface, this program gets "sprites" from a sprite sheet 
and display them, creating an animation.

works with python3.4 and pyhton2.7
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division
import pygame
import random
import os
pygame.init()
folder = "data" # replace with "." if pictures lay in the same folder as program
try: 
    spritesheet = pygame.image.load(os.path.join(folder, "char9.bmp"))
except: 
    raise(UserWarning, "i'm unable to load 'cahr9.bmp' form the folder 'data'") # error msg and exit

screen=pygame.display.set_mode((800,480)) # try out larger values and see what happens !
spritesheet.convert() # convert only works afteer display_setmode is set.
screenrect = screen.get_rect()
background = pygame.Surface((screen.get_size()))
backgroundrect = background.get_rect()
background.fill((255,0,255)) # fill white
background = background.convert()
screen.blit(background,(0,0))

class LionAnim():
    lions = [] # a list for the lion images
    sz = 128
    cycletime = 0 
    #newnr = 0 # index of the first lionimage to display
    #oldnr = 0 # needed to compare if image has changed
    interval = .15 # how long one single images should be displayed in seconds 
    picnr = 0
    xloc, yloc = 0, 0
    def __init__(self, spritesheet, x0, y0):
        self.xloc = x0
        self.yloc = y0
        # the spritesheet has lions, 128 x 64 pixels
        sz = self.sz
        w, h = 128, 64
        # for nbr in range(1,5,1): # first line contains 4 pictures of lions
        #    lions.append(spritesheet.subsurface((sz*(nbr-1),64,sz,sz)))
        # for nbr in range(5,7,1): # second line contains 2 pictures of lions
        #    lions.append(spritesheet.subsurface((sz*(nbr-5),262-64,sz,sz)))
        for nbr in range(4): # first line contains 4 pictures of lions
            self.lions.append(spritesheet.subsurface((sz*nbr,64,w,h)))
        for nbr in range(2): # second line contains 2 pictures of lions
            self.lions.append(spritesheet.subsurface((sz*nbr,198,w,h)))

        for nbr in range(len(self.lions)):
           self.lions[nbr].set_colorkey((0,0,0)) # black transparent
           self.lions[nbr] = self.lions[nbr].convert_alpha()
           print("converted nbr", nbr)

        print("len:",len(self.lions), self.lions[0].get_size())

    def anim(self, seconds, dx=0, dy=0):
        self.cycletime += seconds
        if self.cycletime > self.interval: # Note that milliseconds is a lot smaller than interval
            #screen.blit(background.subsurface((300,300,128,66)),(300,300)) ##
            # below will cause an error when it goes out of the background image.
            # it is up to you to fix it.
            bg = background.subsurface((self.xloc, self.yloc,128,66))
            screen.blit(bg,(self.xloc, self.yloc)) ##

            self.xloc += dx
            self.yloc += dy
            mypicture = self.lions[self.picnr] ## 
            screen.blit(mypicture, (self.xloc, self.yloc)) 
            self.picnr += 1
            if self.picnr > 5:
                self.picnr = 0
            self.cycletime = 0  # reset cycletime.
        return
#

alion = LionAnim(spritesheet, 200, 150)
lion2 = LionAnim(spritesheet, 20, 300)


for nbr in range(len(alion.lions)):
    screen.blit(alion.lions[nbr], (nbr*(alion.sz+1), 0))  #blit the ball surface on the screen (on top of background)
    print("blitted nbr", nbr)

# 
clock = pygame.time.Clock()        #create pygame clock object
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 
playtime = 0
while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    playtime += seconds

    alion.anim(seconds)
    lion2.anim(seconds, 10, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
 
    pygame.display.set_caption("[FPS]: %.2f picture: %i" % (clock.get_fps(), alion.picnr))
    #this would repaint the whole screen (secure, but slow)
    #screen.blit(background, (0,0))     #draw background on screen (overwriting all)

    pygame.display.flip()          # flip the screen 30 times a second
print("This 'game' was played for {:.2f} seconds".format(playtime))
