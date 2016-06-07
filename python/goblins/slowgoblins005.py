# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins005.py

import random
hitpoints_stinky = 22
hitpoints_grunty = 43
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")
for combat_round in range(22):
    print("{0:2d} Stinky: {1:3d} Grunty: {2:3d}".format(combat_round, hitpoints_stinky, hitpoints_grunty))
    hitpoints_grunty -= random.randint(1, 6)
    hitpoints_stinky -= random.randint(1, 6)
print("Game Over")
