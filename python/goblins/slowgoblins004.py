# part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins004.py

hitpoints_stinky = 22
hitpoints_grunty = 43
print(" --- The Goblin Dice Duel ---")
print("game_round, Stinky, Grunty")
for game_round in range(22):
    print(game_round, hitpoints_stinky, hitpoints_grunty)
    hitpoints_stinky -= 1
    hitpoints_grunty -= 1
print()  # print an empty line
print("Game Over")
