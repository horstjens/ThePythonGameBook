# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins006.py


import random
hitpointsStinky = 22
hitpointsGrunty = 43
combatround = 0
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")
while hitpointsStinky >0:
    print("{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(combatround, hitpointsStinky, hitpointsGrunty))
    combatround += 1
    hitpointsGrunty -= random.randint(0,6)
    if hitpointsGrunty <= 0:
        break
    hitpointsStinky -= random.randint(0,6)
print("Game Over")
if hitpointsStinky > hitpointsGrunty:
    print("Stinky wins")
elif hitpointsGrunty > hitpointsStinky:
    print("Grunty wins")
else:
    print("Nobody wins ?")
print("thank you for playing Goblin Dice Duel. bye-bye!")