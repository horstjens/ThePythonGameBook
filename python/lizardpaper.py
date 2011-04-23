#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       lizardpaper.py 
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.      
# 
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.       
#
#       This source code is licensed under the 
#       GNU General Public License, Free Software Foundation
#       http://creativecommons.org/licenses/GPL/2.0/
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       
#       MA 02110-1301, USA.

def main():
    """rock paper scissor lizard spock"""
    # things beat things, equal things are a draw
    import random
    # key and meaning of this key
    keys = {"r":"rock", 
            "s":"scissors",
            "p":"paper",
            "l":"lizard",
            "o":"spock"
            }
    # dictionary of things and things that get beaten by this thing 
    thing = {
             "r":"sl",
             "s":"pl",
             "p":"or",
             "o":"sr",
             "l":"po"
             }
    #  victor victim victorytext
    wintext = {
              "r": { "s": "rock crushes scissors",
                     "l": "rock crushes lizard"},
              "s": { "p": "scissors cut paper",
                     "l": "scissors decapitate lizard"},
              "p": { "o": "paper disproves Spock",
                     "r": "paper covers rock" },
              "o": { "s": "Spock smashes scissors",
                     "r": "Spock vaporizes rock" },
              "l": { "p": "lizard eats paper",
                     "o": "lizard poisons spock" } 
              }
    import random
    question = "What do you play ? \n"
    validstring = ""
    for thingy in thing.keys():
        question += thingy + ": " + keys[thingy] + "\n"
        validstring += thingy
    validstring += "q" # add "q" to quit
    question += "\n please press one of the keys listed above andd ENTER \n or press q and ENTER to quit \n>" 
    mainloop = True
    playerpoints = 0
    computerpoints = 0
    rounds = 0
    print " see http://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-spock for game rules"
    while mainloop:
        playerthing = "xxxx"
        print " ---- round played: %i ----- " % rounds
        while not playerthing in validstring:
            playerthing = raw_input(question)
        if playerthing == "q":
            print "i'm sad that you want to quit the game"
            mainloop = False
            break # exit loop
        rounds += 1
        computerthing = random.choice(thing.keys())
        # --- output ----
        print "Your choice is: %s " % keys[playerthing]
        print "The computer choice is %s " % keys[computerthing]
        # ---- calculate winner
        if playerthing == computerthing:
            print "this is a draw"
        elif computerthing in thing[playerthing]:
            playerpoints += 1
            print wintext[playerthing][computerthing]
            print "YOU win !"
        else:
            computerpoints += 1
            print wintext[computerthing][playerthing]
            print "You loose....."
        print "-------------------------"
        print "points for computer: %i" % computerpoints
        print "points for human player: %i" % playerpoints
        print "------ next round -------"
        delay = raw_input("press ENTER to continue")
        print "\n\n\n" # three empty lines
    print "bye-bye"
    return 0 # (computerpoints, playerpoints)

if __name__ == '__main__':
    main()

