__author__ = 'Horst JENS'
# see http://ThePythonGameBook.com

import random
hitpointsStinky = 22
hitpointsGrunty = 43
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")
for combatround in range(22):
    print("{0:2d} Stinky: {1:3d} Grunty: {2:3d}".format(combatround, hitpointsStinky, hitpointsGrunty))
    hitpointsGrunty -= random.randint(1,6)
    hitpointsStinky -= random.randint(1,6)
print("Game Over")
