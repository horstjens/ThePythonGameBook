# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins004.py

hitpointsStinky = 22
hitpointsGrunty = 43
print(" --- The Goblin Dice Duel ---")
print("game_round, Stinky, Grunty")
for game_round in range(22):
    print(game_round, hitpointsStinky, hitpointsGrunty)
    hitpointsStinky -= 1
    hitpointsGrunty -= 1
print()  # print an empty line
print("Game Over")
