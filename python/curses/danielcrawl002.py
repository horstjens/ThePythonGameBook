#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import curses


class Level(object):
    def __init__(self, txt):
        self.lines = len(txt.splitlines())
        self.colls = len(txt.splitlines()[1])
        self.txt = txt

    def check(self, x, y):
        #check if  position x/y is a valid space
        char = self.txt.splitlines()[y][x]
        return char


levels = []

#level0
levels.append(
    Level(
        """
#########nnnnnnnnnnnn#########################################
##########            ################  8    MMM             #
###########            ###############  7     MMM            #
############             ############# MMMMMMMMM             #
#############                 ############################   #
##############                ############################   #
###############       O       #######################        #
################              #######################        #
#################                                            #
##################                                           #
##################                                           #
##################                                           #
##################                  B             s          #
||||||||||||||||||                                           #
##################                                           #
##################          l                                #
#                                              D             #
#         T                                                  #
#                            G                               #
#                                                            #
##############################################################
"""
    )
)
#T=Troll / G=Goblin / D=DarkElv / B=Bat / O=Ork / M=Mice
#|=breakable wall / #=unbreakable wall
#8=full health potion / 7=super big backpack / s=sword / l=leather helmet

#level1
levels.append(
    Level(
        """
#########pppppppppppp#########################################
#                                                            #
#   ###################                    ######            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #    #            #
#   #                 #                    #   ##            #
#   #                 #                    #   ##            #
#   #                 #                    #   ##            #
#   #                 #                    #   ##            #
#   #                 #                    #                 #
#   #    #####        #                    #                 #
#   #        #        #                    #                 #
#   ##########        #                    #                 #
#                     #                    #                 #
##########################nnnnnnnnnnnnn#######################
"""
    )
)

#level 2
levels.append(
    Level(
        """
##############################################################
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
##########################ppppppppppppp#######################
"""
    )
)

#start
stdscr = curses.initscr()
# Keine Anzeige gedrückter Tasten
curses.noecho()
# Kein line-buffer
curses.cbreak()
# Escape-Sequenzen aktivieren
stdscr.keypad(1)

# Farben
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

# Fenster und Hintergrundfarben
stdscr.bkgd(curses.color_pair(1))
stdscr.refresh()

windowheight = 10
windowwidth = 20
windowx = 5
windowy = 5

win = curses.newwin(windowheight, windowwidth, windowy, windowx)  # (höhe, breite, y, x)
win.bkgd(curses.color_pair(2))
win.box()

# Warten auf Tastendruck
c = stdscr.getch()

line_start = 1
col_start = 1

monsterx = 7
monstery = 7
monsterdx = 1
monsterdy = 0


def crash():
    for x in range(10):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        win.refresh()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        win.refresh()


while True:
    # Teile des Pads aufs Display bringen
    win.clear()
    win.addstr(line_start, col_start, "x")
    win.addstr(monstery, monsterx, "M")
    win.refresh()
    c = stdscr.getch()
    #if c == ord('x'):
    #  break
    if c == curses.KEY_DOWN:
        if line_start < windowheight - 2:
            line_start += 1
        else:
            crash()
    elif c == curses.KEY_UP:
        if line_start > 1:
            line_start -= 1
        else:
            crash()
    elif c == curses.KEY_LEFT:
        if col_start > 1:
            col_start -= 1
        else:
            crash()
    elif c == curses.KEY_RIGHT:
        if col_start < windowwidth - 3:
            col_start += 1
        else:
            crash()
    elif c == ord(' '):
        pass
    elif c == ord('q'):
        break

    #move monster

    if monsterx >= windowwidth - 3:
        monsterdx = -1
    if monsterx <= 1:
        monsterdx = 1
    monsterx += monsterdx
# Ende
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
