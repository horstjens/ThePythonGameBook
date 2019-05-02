# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins005.py

import random
hitpointsStinky = 22
hitpointsGrunty = 43
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")
for combat_round in range(22):
    print("{0:2d} Stinky: {1:3d} Grunty: {2:3d}".format(combat_round, hitpointsStinky, hitpointsGrunty))
    hitpointsGrunty -= random.randint(1, 6)
    hitpointsStinky -= random.randint(1, 6)
print("Game Over")
