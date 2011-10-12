#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
easyguimenu.py

demonstration of a game menu with easygui.
The gamemenu can change resolution, call a pygame 
program (the screensaver), return values (the playtime),
write and display a highscore list

Url:        http://ThePythonGameBook.com/en:part2:pygame:start
Author:     Horst JENS, horst.jens@spielend-programmieren.at
License:    GPL see http://www.gnu.org/licenses/gpl.html
Date:       2011/06
"""

import pygame
from lib import easygui 
from lib import screensaver 
import os
import os.path
import time




def gamemenu():
    gamefolder =  os.path.expanduser(os.path.join("~",".screensavertest"))  # ~ means home on linux . as first char will hide 
    gamefile = os.path.join(gamefolder, "highscorelist.txt")                    # do not call it "file", that is a reserved word !
    if os.path.isdir(gamefolder):
        print "directory already exist"
    else:
        print "directory does not exist yet"
        try:
            os.mkdir(gamefolder)
        except:
            raise UserWarning, "error at creating directory %s" % gamefolder
            exit()
    if os.path.isfile(gamefile):
        print "highscore file aready exist"
    else:
        try:
            f = file(gamefile, "w") # open for writing
            f.write("--- screensaver logfile ---\n")
            f.close()
        except:
            raise UserWarning, "error while creating file %s" % gamefile
            exit()
    # gamefile should now exist in gamefolder
    
        
    resolution = [640,480]
    fullscreen = False
    watched = 0
    title = "please choose wisely:"
    buttons = ["watch screensaver", "change resolution", "toggle fullscreen", "view highscore", "quit"]
    #picture = None # gif file or make sure python-imaging-tk is installed correctly
    picture = "data/tux.gif" 
    # ---- use pygame only to get a list of valid screen resolutions ---
    pygame.init()
    reslist = pygame.display.list_modes()
    pygame.quit()
    # ---- end of pygame ----------
    # --- ask player name ----
    playername = easygui.enterbox("What is you name?", "please enter you name and press ENTER or click ok", "Mister dunno")
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
        elif selection == "view highscore":
            try:
                f = file(gamefile, "r") # read
                text = f.read() 
                f.close()
            except:
                raise UserWarning, "Error while reading higscore file %s" % gamefile
                exit()
            easygui.textbox("This is the Screensaver logfile", "displaying highscore", text)
        elif selection == "watch screensaver":
            watched += 1
            playtime = screensaver.screensaver(resolution, fullscreen)
            easygui.msgbox("You watched the scrensaver %i x using this game menu \nYour screen was saved for %.2f seconds" % (watched, playtime))
            # writing highscore-list
            try:
                f = file(gamefile, "a") # append
                f.write("date: %s player: %s playtime:  %.2f seconds resolution: %ix%i fullscreen: %s \n" % (time.asctime(), playername, playtime, resolution[0], resolution[1], fullscreen))
                f.close()
            except:
                raise UserWarning, "Error while writing higscore file %s" % gamefile
                exit()
        elif selection == "change resolution":
            answer = easygui.choicebox("Please select one of those screen resolutions", "x,y", reslist)
            # answer gives back a string like '(320, 200)'
            comma = answer.find(",") # position of the comma inside answer
            x = int(answer[1:comma])
            y = int(answer[comma+1:-1])
            resolution = (x,y)
    return 

if __name__ == '__main__':
    gamemenu()

