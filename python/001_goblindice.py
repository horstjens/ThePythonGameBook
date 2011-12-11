#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt


import random 

# this is a very simple program, showing random.randint, a loop
# and some primitive combat mechanic"""


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

The game did never become popular outside goblin cave societys and is 
rumored to be one of the main reasons why goblins are extinct today."""


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
else:
	print "Stinky is the winner !"
	      
	
	
	       
	
	
	


