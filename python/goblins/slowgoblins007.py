# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins007.py

def output(combatround,hitpointsStinky,hitpointsGrunty):
    """printing out three values"""
    print("{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(combatround, hitpointsStinky, hitpointsGrunty))
    # no return necessary because this functions returns nothing (yet)

import random
hitpointsStinky = 22
hitpointsGrunty = 43
combatround = 0
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")
while hitpointsStinky >0:
    output(combatround, hitpointsStinky, hitpointsGrunty)
    combatround += 1
    hitpointsGrunty -= random.randint(0,6)
    if hitpointsGrunty <= 0:
        break
    hitpointsStinky -= random.randint(0,6)
output(combatround, hitpointsStinky, hitpointsGrunty) # output of final strike
print("Game Over")
if hitpointsStinky > hitpointsGrunty:
    print("Stinky wins")
elif hitpointsGrunty > hitpointsStinky:
    print("Grunty wins")
else:
    print("Nobody wins ?")
print("thank you for playing Goblin Dice Duel. bye-bye!")