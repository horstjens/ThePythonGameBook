#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt


import random 

# this example uses classes to store the propertys of the goblins,
# introduces the __main__ function and handles user-input
# with the raw_input() function

intro = """
---- Introduction -------
Two goblins, Grunty and Stinky, play the traditional game of 
Goblin Dice Duel

The rules a very simple. Each goblin throws a die and is 
allowed to hit the other goblin on the head with a club as often
as the number of eyes on his throwed die. This is called damage.

As each goblins has an individual number of hitpoints (how much damage
he can suffer) the last gobling standing is the winner.

Note that dice in the goblin cave are made out of bones and are not 
six-sided as the dice you may know. 
Each dice has a minimal value (number of eyes) and a maximal value. 

To find out if weak and smart goblins beat dumb and strong goblins more 
often than not, it is necessary to observe thousands of games
"""

class Goblin(object):
	"""goblin with name, and other individual values"""
	def __init__(self):
		"""standard out-of-the-cave goblin, alter values after creation"""
		self.name = "dummy"
		self.hitpoints = 50
		self.wins = 0
		self.min_damage = 1
		self.max_damage = 6
		self.min_speed = 1
		self.max_speed = 6
	

def menu():
    menuitems = [] # empty list
    menuitems.append("read introduction")           # 0
    menuitems.append("view and compare goblins")    # 1
    menuitems.append("modify Stinky")               # 2
    menuitems.append("modify Grunty")               # 3
    menuitems.append("make many fights")            # 4
    menuitems.append("quit")                        # 5
    while True # endless menu loop
		for item in menuitems:
			print menuitems.index(item), item
		while True: # endless user input loop
			wish = raw_input("your choice (and Enter):")  
			if wish.isdigit():
				if int(wish) >= 0 and int(wish) < len(menuitems):
					break # break the endless user input loop
		print "your wish was %i: %s" % (int(wish), menuitems[int(wish)])
		 
		if int(wish) == 0:
			print intro 
		elif int(wish) == 1:
			
		elif int(wish)==5:
			break # break out of the menu loop
    
    

def combat(goblinA, goblinB):
    """a function that takes 2 goblins (class instances)
       let them fight and returns the winning goblin"""
    
    # define Grunty and Stinky. Note that variables are lowercase
    stinky_hitpoints = 50 # Stinky is weak but smart
    grunty_hitpoints = 60 # Srunty is strong but dumb

    stinky_min_damage = 3 # Stinky does better minimal damage
    stinky_max_damage = 5 # but not so much maximal damage

    grunty_min_damage = 1 # Grunty does very low minimal damage
    grunty_max_damage = 6 # but higher maximal damage

    combatround = 0 # the word "round" is a reserved keyword in python

    while stinky_hitpoints > 0 and grunty_hitpoints > 0:
        combatround += 1 # increase the combat round counter
        print " ----- combat round %i -------" % combatround
        
        # Stinky is smarter and always attacks first
        damage = random.randint(stinky_min_damage, stinky_max_damage)
        grunty_hitpoints -= damage # Stinky hits Grunty
        print "Stinky hits Grunty for %i damage. Grunty has %i hp left" % (
               damage, grunty_hitpoints)
        
        if grunty_hitpoints <= 0:
            break # leave the while loop if Grunty has lost
        
        # Grunty strikes back if he is still in the game
        damage = random.randint(grunty_min_damage, grunty_max_damage)
        stinky_hitpoints -= damage # Grunty bashes Stinky
        print "Grunty hits Stinky for %i damage. Stinky has %i hp left" % (
              damage, stinky_hitpoints)
    #----- end of loop ----
    print "=================================="
    #print "The combat ends after %i rounds" % combatround
    print "Stinky has %i hitpoints left" % stinky_hitpoints
    print "Grunty has %i hitpoints left" % grunty_hitpoints
    if grunty_hitpoints > 0:
        print "Grunty is the winner !"
        return "Grunty"
    else:
        print "Stinky is the winner !"
        return "Stinky"
        
def many_games(number_of_fights=1000):
    """calls the combat function 1000 times"""
    stinky_wins = 0
    grunty_wins = 0     
    for fight in range(number_of_fights):
        print "fight number %i" % fight
        winner = combat()
        if winner == "Grunty":
            grunty_wins += 1
        else:
            stinky_wins += 1
    print "==============================="
    print " * * * end results * * * "
    print "==============================="
    print "Grunty wins: %i  vs. Stinky wins: %i" % (grunty_wins, stinky_wins)
    
# start !
#many_games() # enter another number in the parantheses
menu()          
               
        
        
    


