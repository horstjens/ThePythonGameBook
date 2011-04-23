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
            "o":"Spock"
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
    for thingy in wintext.keys():
        question += thingy + ": " + keys[thingy] + "\n"
        validstring += thingy
    validstring += "q" # add "q" to quit
    question += "\n please press one of the keys listed above and ENTER \n or press q and ENTER to quit \n>" 
    mainloop = True
    #playerpoints = 0
    #computerpoints = 0
    rounds = 0
    print "*** Welcome to a game of rock, paper, scissors, lizard, Spock ! ***"
    print " see http://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-spock\n for game rules"
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
                while not (playerthing in validstring) or playerthing == "" or playerthing == None:
                    print "******** player %s, it is your turn ! *******" % player
                    playerthing = raw_input(question)
                if playerthing == "q":
                    print "i'm sad that you want to quit the game"
                    mainloop = False
                    break # exit loop
                else:
                    players[player]["thing"] = playerthing # adding answer to dict
            else: # computer player
                players[player]["thing"] = random.choice(wintext.keys()) # computerthing
        rounds += 1
        
        # --- output ----
        for player in players.keys():
            playerthing = players[player]["thing"]
            print "The coice of player %s is: %s " % (player, playerthing)
        #print "The computer choice is %s " % keys[computerthing]
        # ---- calculate winner
        for player in players.keys():
            print "calculating points for player %s" % player
            playerthing = players[player]["thing"]
            for enemy in players.keys():
                if player != enemy:
                    enemything = players[enemy]["thing"]
                    print "%s of %s versus %s of %s" % (keys[playerthing], player, keys[enemything], enemy)                        
                    if playerthing == enemything:
                        print "this is a draw (0 points)"
                    elif enemything in wintext[playerthing].keys():
                        players[player]["points"] += 1
                        print wintext[playerthing][enemything],"(+1 point)"
                    else:
                        print wintext[enemything][playerthing],"(0 points)"
        #------ summary -------
        print "====== result ======="
        for player in players.keys():
            print "points: %i for %s" %( players[player]["points"], player)
        print "------ next round -------"
        delay = raw_input("press ENTER to continue, q and ENTER to quit")
        if delay == "q":
            mainloop = False
        print "\n\n\n" # three empty lines
    print "bye-bye"
    return 0 # (computerpoints, playerpoints)

if __name__ == '__main__':
    main()

