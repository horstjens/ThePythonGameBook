#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       lizardpaper.py 
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       This program is part of ThePythonGameBook , 
#       see http://ThePythonGameBook.com for more information.
#       Check the newest version of this file:
#       https://github.com/horstjens/ThePythonGameBook/blob/master/python/lizardpaper.py
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

def startmenu():
    print "*** Welcome !***"
    print "please choose between a classic game of 'rock, paper, scissors'"
    print "or a game of the newer variant 'rock, paper, scissors, lizard, Spock' "
    print 
    print "see Wikipedia for game rules and more information:"
    print "http://en.wikipedia.org/wiki/Rock_paper_scissors"
    print "http://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-spock"
    print
    mode = "x"
    while mode != "c" and mode != "n": 
        print "please press either c for classic or n for newer variant"
        print "and press ENTER to start"
        mode = raw_input("Your choice: \n>")
    if mode == "c":
        game("classic")
    elif mode == "n":
        game("new")
    else:
        return "game variant error"

def game(mode="classic"):
    """rock paper scissor lizard spock
    mode can be new or classic"""
    import random
    if mode != "new" and mode != "classic":
        return "unknow parameter. please start game with either 'classic' or 'new'"
    # { key: human-readable key description }
    things = {"r":"rock", 
            "s":"scissors",
            "p":"paper"}
    if mode == "new": # expand only for new version
        things["l"] = "lizard"
        things["o"] = "Spock"
        
    # { victor : { victim : (victorytext loosertext) }}
    wintext = {
              "r": { "s": ("rock crushes scissors", "scissors is crushed by rock"),
                     "l": ("rock crushes lizard", "lizard is crushed by rock")},
              "s": { "p": ("scissors cut paper", "paper is cut by scissors"),
                     "l": ("scissors decapitate lizard", "lizard is decapitated by scissors")},
              "p": { "o": ("paper disproves Spock", "Spock is disproved by paper"),
                     "r": ("paper covers rock", "rock is enveloped by paper") },
              "o": { "s": ("Spock smashes scissors", "scissors are smashed by Spock"),
                     "r": ("Spock vaporizes rock", "rock is vaporized by Spock") },
              "l": { "p": ("lizard eats paper", "paper is eaten by lizard"),
                     "o": ("lizard poisons Spock", "Spock is poisoned by lizard") } 
              }
    import random
    question = "What do you play ? \n"
    for thingy in things.keys():
        question += thingy + ": " + things[thingy] + "\n"
    question += "\n please press one of the keys listed above and ENTER \n" 
    mainloop = True
    rounds = 0
    # ------ generating players --------
    players = {} # name, nature, thing, points
    answer = ""
    while answer == "":
        print "At the moment, this game has %i players. Minimum to start a game is 2 players." % len(players)
        if len(players.keys()) > 0:
            print "-- list of players in the game --"
            for player in players.keys():
                print "name: %s  type: %s" % (player, players[player]["nature"])
        print "----"
        playername = raw_input("please type in the name of a new player and press ENTER \n"
                               "press only ENTER to start the game \n>")
        if playername == "":
            break # exit
        natureOfPlayer = "x"
        while (natureOfPlayer not in "hc") or (natureOfPlayer == "") or (natureOfPlayer == None):
            natureOfPlayer = raw_input("is this player a (h)uman or a (c)omputer ? press h or c and ENTER")
        players[playername] = {"nature": natureOfPlayer , "thing": "xxx", "points":0 }# add player do dictionary
    if len(players) < 2:
        print "you need at least 2 players to start a game. Bye !"
        return "too few players"
        
    while mainloop: # ----------- the game loop ------------    
        print " ---- rounds played: %i ----- " % rounds
        for player in players.keys():
            if players[player]["nature"] == "h": # human                
                playerthing = ""
                while not (playerthing in things.keys()) or playerthing == "" or playerthing == None:
                    print "******** player %s, it is your turn ! *******" % player
                    playerthing = raw_input(question)
                players[player]["thing"] = playerthing # adding answer to dict
            else: # computer player
                players[player]["thing"] = random.choice(things.keys()) # computerthing
        rounds += 1
        
        for player in players.keys(): # --- output ----
            playerthing = players[player]["thing"]
            print "The coice of player %s is: %s " % (player, playerthing)
        for player in players.keys():         # ---- calculate winner
            print "...calculating points for player %s..." % player
            playerthing = players[player]["thing"]
            for enemy in players.keys():
                if player != enemy:
                    enemything = players[enemy]["thing"]
                    print "%s of %s versus %s of %s" % (things[playerthing], player, things[enemything], enemy)                        
                    if playerthing == enemything:
                        print "this is a draw (0 points)"
                    elif enemything in wintext[playerthing].keys():
                        players[player]["points"] += 1
                        print wintext[playerthing][enemything][0],"(+1 point)" # victory
                    else:
                        print wintext[enemything][playerthing][1],"(0 points)" # loose
        print "====== result (round %i) =======" % rounds     #------ summary -------
        for player in players.keys():
            print "points: %i for %s" %( players[player]["points"], player)
        print "------ next round -------"
        playMore = raw_input("press ENTER to continue, q and ENTER to quit")
        if playMore == "q":
            mainloop = False
        print "\n\n\n" # three empty lines
    print "bye-bye"
    return 0 # (computerpoints, playerpoints)

if __name__ == '__main__':
    startmenu()

