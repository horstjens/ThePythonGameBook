"""
dungeon004.py: simple pyhton3 dungeon / adventure game

example of a game dungeon to teach python programming to young students
data structure with list

This code is part of ThePythonGameBook project, see http://ThePythonGameBook.com
"""
__author__ = "Horst JENS (horstjens@gmail.com, http://spielend-programmieren.at)"
__license__ = "GPL3, see http://www.gnu.org/licenses/gpl-3.0.html"

#import dungeon003_utils as u

# for reason of simplifying the code examples i do NOT import the ask function,
# but instead code it again here:


def ask(prompt, allowed=["a", "b", "i", "q"]):
    """force the player to choose one of the allowed answers and returns it"""
    while True:
        print(prompt)
        answer = input("Please type corresponding key and ENTER>")
        if answer in allowed:
            return answer
        print("Wrong answer. Possible answers are:", allowed)

# the same strings as usual
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

# data structure: lists [], beginning with the first room
rooms = [room1, room2]
actions = [actions1, actions2]
wins = [win1, win2]
losses = [loose1, loose2]
wrong_answers = ["a", "b"]  # in first room, answer "a" is bad, in second room, "b" is bad
right_answers = ["b", "a"]  # in first room, answer "b" is good, in second room, "a" is good

# game data
room_index = 0  # python always start counting elements in a list with 0. So
# the first room becomes rooms[0], the second room becomes rooms[1]
history = []  # list of visited rooms

# game
alive = True
print(intro)
while alive and room_index < 2:
    if room_index not in history:
        print(rooms[room_index])  # show room description only once
        history.append(room_index)  # modify history
    answer = ask(actions[room_index])
    if answer == "i":
        print(rooms[room_index])
    elif answer == "q":
        print("bye-bye")
        alive = False
    elif answer == wrong_answers[room_index]:
        print(losses[room_index])
        alive = False
    elif answer == right_answers[room_index]:
        print(wins[room_index])
        room_index += 1  # increase room_index. also: room_index = room_index +1
# ------- end ----------
print("Thanks for playing")
