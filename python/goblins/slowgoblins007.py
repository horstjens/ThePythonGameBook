"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins007.py"""

import random


#later use output instead of print
def output(c_round, hp_stinky, hp_grunty):
    """printing out three values c_round, hp_stinky and hp_grunty"""
    print("{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(c_round, hp_stinky, hp_grunty))
    # no return necessary because this functions returns nothing (yet)


hitpoints_stinky = 22
hitpoints_grunty = 43
combat_round = 0
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")

while hitpoints_stinky > 0:
    output(combat_round, hitpoints_stinky, hitpoints_grunty)
    combat_round += 1
    hitpoints_grunty -= random.randint(0, 6)
    if hitpoints_grunty <= 0:
        break
    hitpoints_stinky -= random.randint(0, 6)

output(combat_round, hitpoints_stinky, hitpoints_grunty)  # output of final strike
print("Game Over")

if hitpoints_stinky > hitpoints_grunty:
    print("Stinky wins")
elif hitpoints_grunty > hitpoints_stinky:
    print("Grunty wins")
else:
    print("Nobody wins ?")
print("thank you for playing Goblin Dice Duel. bye-bye!")
