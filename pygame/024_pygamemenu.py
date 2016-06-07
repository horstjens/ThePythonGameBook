#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pygamemenu.py

demonstration of a game menu with pygame / EzMenu.
The gamemenu can change resolution, call a pygame 
program (the screensaver), return values (the playtime),
write and display a highscore list
EzMenu from PyMike, see EzMenu.py

Url:        http://ThePythonGameBook.com/en:part2:pygame:start
Author:     Horst JENS, horst.jens@spielend-programmieren.at
License:    GPL see http://www.gnu.org/licenses/gpl.html
Date:       2011/06

TODO: python3
works with pyhton2.7
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

import pygame
import os
import os.path
import time
import webbrowser
from lib import ezmenu
from lib import screensaver


class Config(object):
    #geraet = "Joystick"
    fullscreen = False
    resolution = (640,480)
    menu = None
    menuloop = True
    gamefolder =  os.path.expanduser(os.path.join("~",".screensavertest"))  
    gamefile = os.path.join(gamefolder, "highscorelist.txt")  
    reslist = []
    watched = 0
    result = "no game played yet"

def write(msg="pygame is cool", fontcolor=(255,0,255), fontsize=42, font=None):
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext
  
   
def ask(screen, question):  
    """ from pygame newsgroup
    replacement for raw_input() in pygame
    
    ask(screen, question) -> answer"""
    pygame.font.init()  
    text = ""
    pygame.display.flip()
    line1 = write("please type in your name")
    line2 = write("and press ENTER:")
    while True:
        screen.fill((0,0,0)) #paint background black
        line3 = write(">" + text)
        screen.blit(line1, (20,20))
        screen.blit(line2, (20,50))
        screen.blit(line3, (20,80))
        pygame.time.wait(50)
        #event = pygame.event.poll()
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                sys.exit()   
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_BACKSPACE:
                text = text[0:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return text
            else:
                text += event.unicode.encode("ascii")         
        pygame.display.flip()
               
    
def makemenu(pos=0):
    """pos is the current menuitem"""
    Config.menu = ezmenu.EzMenu(
        ["Run the Screensaver", gameRun],
        ["Change screen resolution: %i x %i" % (Config.resolution[0], Config.resolution[1]), gameNextResolution],
        ["toggle Fullscreen: %s" % Config.fullscreen, gameFullscreen],
        ["view hightscore/logfile ", gameReadFile],
        ["visit ThePythonGameBook homepage", lambda: gameUrl("http://ThePythonGameBook.com")],
        ["Quit Game", gameQuit] )
    
    Config.menu.center_at(320, 240)

    #Set the menu font (default is the pygame font)
    Config.menu.set_font(pygame.font.SysFont("Arial", 32))

    #Set the highlight color to green (default is red)
    Config.menu.set_highlight_color((255, 255, 0))

    #Set the normal color to white (default is black)
    Config.menu.set_normal_color((255, 255, 255))
    Config.menu.option = pos       

#Functions called when an option is selected
def gameRun():
    """play a game/ watch the screensaver"""
    playtime = screensaver.screensaver(Config.resolution, Config.fullscreen, False) # the False avoid the screensaver to do pygame.quit()
    screen, background = repaint()
    
def gameReadFile():
    pass
    
def gameFullscreen():
    Config.fullscreen = not Config.fullscreen
    print( Config.fullscreen)
    makemenu(2) # repaint menu, set active option of item #2 (start counting with 0)

def gameNextResolution():
    """ returns the next possible screen resolution from Config.reslist
    and set it into Config.resolution. If already on the end of reslist,
    start over with first element of reslist.
    reslist is a list of tuples, resolutio is a tuple of 2 integers"""
    myRes = Config.resolution
    if myRes not in Config.reslist:
        print("Error: %s is not part of %s" % ( myRes, Config.reslist))
        exit()
    mypos = Config.reslist.index(myRes)
    if mypos == len(Config.reslist) -1 :
        mypos = 0 # cycle to first element of reslist
    else:
        mypos += 1 
    Config.resolution = Config.reslist[mypos]
    makemenu(1)
    
def gameUrl(url):
    print( "i try to open the webbrowser, please wait a bit...")
    webbrowser.open_new_tab(url)
    # no makemenu, because the webbrowser does not open inside python
    
def gameQuit():
    """quit game"""
    Config.menuloop = False
    


def repaint():
    """set screen and background for game menu"""
    screen = pygame.display.set_mode((640,480))
    background = pygame.image.load(os.path.join("data", "tux.jpg"))
    background = pygame.transform.scale(background, Config.resolution)
    screen.blit(background, (0,0))
    return screen, background

#Main script
def main():

    #Set up pygame
    pygame.init()
    Config.reslist = pygame.display.list_modes()
    pygame.display.set_caption("EzMenu Example")
    screen, background = repaint()
    makemenu(0)
    FPS = 30
    clock = pygame.time.Clock()
    cooldown = 0
    
    # ask for playername
    playername = ask(screen, "Please type in your name and press ENTER")
    print( playername )
    
    while Config.menuloop:
        pygame.display.set_caption("last game result: %s" % Config.result)
        #Get all the events called
        seconds = clock.tick(FPS) / 1000.0 # do not go faster than this frame rate
        if cooldown < 0:
            cooldown = 0
        if cooldown > 0:
            cooldown -= seconds
        events = pygame.event.get()
        
        #...and update the menu which needs access to those events
        Config.menu.update(events)

  
        #Let's quit when the Quit button is pressed
        for e in events:
            if e.type == pygame.QUIT:
                Config.menuloop = False
                
            elif e.type == pygame.KEYDOWN:
                #print "keypress"
                if e.key == pygame.K_ESCAPE:
                     Config.menuloop = False
        
        # mouse to open url's
        if pygame.mouse.get_pressed()[0] == True and cooldown ==0: # left mouse button was pressed
           mousex = pygame.mouse.get_pos()[0] 
           mousey = pygame.mouse.get_pos()[1] 
           if mousey > 95 and mousey < 116: # open game homepage
               webbrowser.open_new_tab("http://thepythongamebook.com/en:resources:games:schwarzweiss")
               cooldown = 1
           elif mousey > 170 and mousey < 274 and mousex < 145:
               webbrowser.open_new_tab("http://thepythongamebook.com")
               cooldown = 1
           elif mousey > 284 and mousey < 457 and mousex < 145:
               webbrowser.open_new_tab("http://flattr.com/thing/163126/schwarzweiss-game")
                     
        #Draw the scene!
        #screen.fill((0, 0, 255))
        screen.blit(background, (0,0))
        Config.menu.draw(screen)
        pygame.display.flip()
    # end of menuloop 
    #pygame.quit()
    #sys.exit()
    return                

#Run the script if executed
if __name__ == "__main__":
    main()
