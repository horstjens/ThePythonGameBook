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

TODO: file writing does not work with pyhton3
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

import pygame
from lib import easygui 
from lib import screensaver 
import os
import os.path
import time
import webbrowser

def createGameDir(gamefolder):
    """create directory for logfile"""
    if os.path.isdir(gamefolder):
        print("directory already exist")
    else:
        print("directory does not exist yet")
        try:
            os.mkdir(gamefolder)
        except:
            raise(UserWarning, "error at creating directory %s" % gamefolder)
            exit()

def createGameFile(gamefile):
    """create logfile inside game directory"""
    if os.path.isfile(gamefile):
        print("highscore file aready exist")
    else:
        try:
            f = file(gamefile, "w") # open for writing
            f.write("--- screensaver logfile ---\n")
            f.close()
        except:
            raise(UserWarning, "error while creating file %s" % gamefile)
            exit()
            
def getPygameModes():
    """open pygame, get a list of valid screen resolutions, close pygame"""
    pygame.init()
    reslist = pygame.display.list_modes()
    pygame.quit()
    return reslist
    
def readGameFile(gamefile):
    try:
        f = file(gamefile, "r") # read
        text = f.read() 
        f.close()
    except:
        raise(UserWarning, "Error while reading higscore file %s" % gamefile)
        exit()
    return text

def writeGameFile(gamefile, line):
    try:
        f = file(gamefile, "a") # append
        f.write(line)
        f.close()
    except:
        #raise(UserWarning, "Error while writing higscore file %s" % gamefile)
        print("error while writing file")
        exit()

def parse(answer):
    """get a string like '(640, 480)'.
       Return integer tuple like (640, 480)"""
    comma = answer.find(",") # position of the comma inside answer
    x = int(answer[1:comma])
    y = int(answer[comma+1:-1])
    resolution = (x,y)
    return resolution

def gamemenu():
    # setting directory for stroing highscorelist / logfile 
    #~ means home on linux . as first char will hide 
    gamefolder =  os.path.expanduser(os.path.join("~",".screensavertest"))  
    gamefile = os.path.join(gamefolder, "highscorelist.txt")                   
    # do not name gamefile "file", that is a reserved word !
    createGameDir(gamefolder)
    createGameFile(gamefile)
    # gamefile should now exist in gamefolder
    resolution = [640,480]
    fullscreen = False
    watched = 0
    title = "please choose wisely:"
    buttons = ["watch screensaver", "change resolution", "toggle fullscreen", "view highscore","visit homepage", "quit"]
    #picture = None # gif file or make sure python-imaging-tk is installed correctly
    picture = "data/tux.gif" 
    # ---- use pygame only to get a list of valid screen resolutions ---
    reslist = getPygameModes()
    # --- ask player name ----
    playername = easygui.enterbox("What is you name?", "please enter you name and press ENTER or click ok", "Mister dunno")

    while True: #endless loop        
        if fullscreen:
            msg2 = "fullscreen mode"
        else:
            msg2 = "window mode"
        msg = "Welcome at screensaver game menu.\nScreensaver will run with %ix%i resolution,\n%s" % (resolution[0], resolution[1], msg2)
        selection = easygui.buttonbox(msg, title, buttons, picture)
        if selection == "quit":
            easygui.msgbox("bye-bye", "such a sad decision...")
            break # leave loop
        elif selection == "visit homepage":
            print("i try to open the webbrowser, please wait a bit...")
            webbrowser.open_new_tab("http://www.thepythongamebook.com")
        elif selection == "toggle fullscreen":
            fullscreen = not fullscreen 
        elif selection == "view highscore":
            text = readGameFile(gamefile)
            easygui.textbox("This is the Screensaver logfile", "displaying highscore", text)
        elif selection == "watch screensaver":
            watched += 1
            # get return value from called pygame program (playtime)
            playtime = screensaver.screensaver(resolution, fullscreen)
            easygui.msgbox("You watched the scrensaver %i x using this game menu \nYour screen was saved for %.2f seconds" % (watched, playtime))
            # writing highscore-list
            line = "date: %s player: %s playtime:  %.2f seconds resolution: %ix%i fullscreen: %s \n" % (time.asctime(), playername, playtime, resolution[0], resolution[1], fullscreen)
            writeGameFile(gamefile, line)
        elif selection == "change resolution":
            answer = easygui.choicebox("Please select one of those screen resolutions", "x,y", reslist)
            # answer gives back a string like '(320, 200)'
            resolution = parse(answer)
            
    return 

if __name__ == '__main__':
    gamemenu()

