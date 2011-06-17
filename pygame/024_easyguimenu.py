#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       easyguimenu.py
#       
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       license: gpl
#       part of http://ThePythonGameBook.com
#       needs easygui from http://easygui.sourceforge.net/ to work

# both easygui.py and screensaver.py must be located in a 
# subdirectory 'data'. In this subdirectory there have to exist an
# empty file with the name '__init__.py'

import pygame
from data import easygui 
from data import screensaver 

def gamemenu():
    resolution = [640,480]
    fullscreen = False
    watched = 0
    title = "please choose wisely:"
    buttons = ["watch screensaver", "change resolution", "toggle fullscreen", "quit"]
    #picture = None # gif file or make sure python-imaging-tk is installed correctly
    picture = "data/tux.gif"
    # ---- use pygame only to get a list of valid screen resolutions ---
    pygame.init()
    reslist = pygame.display.list_modes()
    pygame.quit()
    # ---- end of pygame ----------
    while True: #endless loop
        
        if fullscreen:
            msg = "Welcome at screensaver game menu.\nScreensaver will run with %ix%i resolution,\nfullscreen mode" % (resolution[0], resolution[1])
        else:
            msg = "Welcome at screensaver game menu.\nScreensave will run with %ix%i resolution,\nwindow mode" % (resolution[0], resolution[1])
        selection = easygui.buttonbox(msg, title, buttons, picture)
        if selection == "quit":
            easygui.msgbox("bye-bye", "such a sad decision...")
            break # leave loop
        elif selection == "toggle fullscreen":
            fullscreen = not fullscreen 
        elif selection == "watch screensaver":
            watched += 1
            playtime = screensaver.screensaver(resolution, fullscreen)
            easygui.msgbox("You watched the scrensaver %i x \nlast time, you watched the screensaver for %.2f seconds" % (watched, playtime))
        elif selection == "change resolution":
            #resolution[0] = easygui.integerbox("Please enter the new value for the x resolution:", 
            #                                   title, resolution[0], 0, 4000)
            #resolution[1] = easygui.integerbox("Please enter the new value for the y resolution:", 
            #                                   title, resolution[1], 0, 2000)
            answer = easygui.choicebox("Please select one of those screen resolutions", "x,y", reslist)
            # answer gives back a string like '(320, 200)'
            comma = answer.find(",") # position of the comma inside answer
            x = int(answer[1:comma])
            y = int(answer[comma+1:-1])
            resolution = (x,y)
    return watched # returns how many times the screensaver was watched (if anybody ask)

if __name__ == '__main__':
    gamemenu()

