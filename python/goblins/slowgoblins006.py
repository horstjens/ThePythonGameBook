"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins006.py"""

import random

hitpoints_stinky = 22
hitpoints_grunty = 43
combat_round = 0
print(" --- Goblin Dice Duel ---")
print("round    hitpoints")

while hitpoints_stinky > 0:
    print("{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(combat_round, hitpoints_stinky, hitpoints_grunty))
    combat_round += 1
    hitpoints_grunty -= random.randint(0, 6)
    if hitpoints_grunty <= 0:
        break
    hitpoints_stinky -= random.randint(0, 6)
print("Game Over")

if hitpoints_stinky > hitpoints_grunty:
    print("Stinky wins")
elif hitpoints_grunty > hitpoints_stinky:
    print("Grunty wins")
else:
    print("Nobody wins ?")

print("thank you for playing Goblin Dice Duel. bye-bye!")
