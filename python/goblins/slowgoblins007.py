"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins007.py"""

import random


#later use output instead of print
def output(c_round, hp_stinky, hp_grunty):
    """printing out three values c_round, hp_stinky and hp_grunty"""
    # please note that hp_stinky is a local variable, only existing inside this output function
    # hp_stinky is an PARAMETER, it's NOT the same as hitpointsStinky !
    print("{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(c_round, hp_stinky, hp_grunty))
    # no return necessary because this functions returns nothing (yet)


hitpointsStinky = 22
hitpointsGrunty = 43
combat_round = 0
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")

while hitpointsStinky > 0:
    output(combat_round, hitpointsStinky, hitpointsGrunty)
    combat_round += 1
    hitpointsGrunty -= random.randint(0, 6)
    if hitpointsGrunty <= 0:
        break
    hitpointsStinky -= random.randint(0, 6)

output(combat_round, hitpointsStinky, hitpointsGrunty)  # output of final strike
print("Game Over")

if hitpoints_stinky > hitpoints_grunty:
    print("Stinky wins")
elif hitpoints_grunty > hitpoints_stinky:
    print("Grunty wins")
else:
    print("Nobody wins ?")
print("thank you for playing Goblin Dice Duel. bye-bye!")
