#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt


import random 

# this is a very simple program, packed into a function to call
# thousands of times, teaching about functions, parameters and
# return values. New: for-loop and range


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

def combat():
	"""a function that let 2 goblins fight and return the winners name"""
    
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
		print(" ----- combat round {0} -------".format(combatround))
		
		# Stinky is smarter and always attacks first
		damage = random.randint(stinky_min_damage, stinky_max_damage)
		grunty_hitpoints -= damage # Stinky hits Grunty
		print("Stinky hits Grunty for {0} damage. Grunty has {1} hp left".format(
			   damage, grunty_hitpoints))
		
		if grunty_hitpoints <= 0:
			break # leave the while loop if Grunty has lost
		
		# Grunty strikes back if he is still in the game
		damage = random.randint(grunty_min_damage, grunty_max_damage)
		stinky_hitpoints -= damage # Grunty bashes Stinky
		print("Grunty hits Stinky for {0} damage. Stinky has {1} hp left".format(
			  damage, stinky_hitpoints))
	#----- end of loop ----
	print("==================================")
	#print("The combat ends after %i rounds" % combatround)
	print("Stinky has {0} hitpoints left".format(stinky_hitpoints))
	print("Grunty has {0} hitpoints left".format(grunty_hitpoints))
	if grunty_hitpoints > 0:
		print("Grunty is the winner !")
		return "Grunty"
	else:
		print("Stinky is the winner !")
		return "Stinky"
		
def many_games(number_of_fights=100):
	"""calls the combat function 100 times"""
	stinky_wins = 0
	grunty_wins = 0		
	for fight in range(number_of_fights):
		print("fight number {}".format(fight))
		winner = combat()
		if winner == "Grunty":
			grunty_wins += 1
		else:
			stinky_wins += 1
	print( "=========================")
	print( " * * * end results * * * ")
	print( "=========================")
	print( "      victories of       ")
	print( "   Grunty vs. Stinky     ")
	print( "  {0:>7} vs. {1}".format(grunty_wins, stinky_wins))
	
# start !
many_games() # enter another number in the parantheses
			
			   
		
		
	


