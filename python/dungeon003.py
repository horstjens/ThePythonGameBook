"""
dungeon003.py: simple pyhton3 dungeon / adventure game

example of a game dungeon to teach python programming to young students
importing the ask function from dungeon003_utils, diffent import methods

This code is part of ThePythonGameBook project, see http://ThePythonGameBook.com
"""
__author__ = "Horst JENS (horstjens@gmail.com, http://spielend-programmieren.at)"
__license__ = "GPL3, see http://www.gnu.org/licenses/gpl-3.0.html"

import dungeon003_utils  # ALWAYS import WITHOUT the file extension .py
#other forms:
# import dungeon003_utils.*        # import everything, no need for dot notation
# from dungeon003_utils import ask # import only the ask function, no need for dot notation
# import dungeon003_utils as u     # create a custom name so that you have to type less

intro = """
You are thrown into the dreaded dungeon of doom. Try to escape!"""

room1 = """
You see a flooded room with an dangerous monster swimming in it. You need to
cross this room without getting eaten by the monster.
Things on the floor: a bone, a stone"""

actions1 = """
Your possible actions:
a: throw stone at monster
b: throw bone at monster
i: read room description again
q: give up (quit)
"""

loose1 = """You manage to hit the monster with the stone but the effect is bad
for your health: The monster crawls out of the water and eats you.
Game over"""

win1 = """The monster is distracted by the bone, allowing you to cross
the flooded room and advance to the next room. Congratulation!"""

room2 = """You reached a room with an blue glowing lock on a podest. It looks
important.
Things on the floor: a blue glowing key, ancient piece of bread."""

actions2 = """
Your possible actions:
a: open blue lock with the blue key
b: eat ancient piece of brad
i: read room description again
q: give up (quit)
"""

loose2 = """The ancient bread was home to a wide range of toxic fungi and insects.
You die of food poisoning. Game Over!"""

win2 = """You manage to open the blue lock using the blue key. How clever!
A magic light erupts and you are teleported out of the dungeon. You have
won the game! Congratulation!"""

# game
alive = True
print(intro)
print(room1)  # ---- first room -----------
while alive:
    answer = dungeon003_utils.ask(actions1)  # dot notation.
    if answer == "a":
        print(loose1)
        alive = False
    elif answer == "b":
        print(win1)
        break  # proceed to next room
    elif answer == "i":
        print(room1)
    elif answer == "q":
        print("bye-bye")
        alive = False

if alive:
    print(room2)  # ------ second room ----------
while alive:
    answer = dungeon003_utils.ask(actions2)  # when importing as u: u.ask
    if answer == "a":
        print(win2)
        break  # leave the while loop
    elif answer == "b":
        print(loose2)
        alive = False
    elif answer == "i":
        print(room2)
    elif answer == "q":
        print("bye-bye")
        alive = False
# ------- end ----------
print("Thanks for playing")
