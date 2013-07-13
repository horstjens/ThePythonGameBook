# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins004.py


hitpointsStinky = 22
hitpointsGrunty = 43
print(" --- The Goblin Dice Duel ---")
print("gameround, Stinky, Grunty")
for gameround in range(22):
     print(gameround, hitpointsStinky, hitpointsGrunty)
     hitpointsStinky -=1
     hitpointsGrunty -=1
print() # print an empty line
print("Game Over")