#!/usr/bin/env python3

"""
dungeon001.py: simple pyhton3 dungeon game for adventure games

example of a game dungeon to teach python programming to young students
This code is used to teach the use of lists, dictionaries and enumeration

This code is part of ThePythonGameBook project, see http://ThePythonGameBook.com
"""
__author__ = "Horst JENS (horstjens@gmail.com, http://spielend-programmieren.at)"
__license__ = "GPL3, see http://www.gnu.org/licenses/gpl-3.0.html"

import random


def select(origin_list, target_list, verb):
    """ask the user to select one item of a list of items.
       removes the selected item from origin_list and adds it to targetlist.
       returns the item, the altered origin_list and the altered target_list"""
    if len(origin_list) < 1:
        print("There is nothing to select")
        return None, origin_list, target_list
    pairs = enumerate(origin_list) # create iterable object
    print("please select one item to {}:".format(verb))
    for number, item in pairs:
        print(number, item)
    y = input("please press the corresponding number and ENTER\n>")
    if not y.isdigit():
        print("that was no number")
        return None, origin_list, target_list
    else:
        y = int(y)
        if y < 0 or y >= len(origin_list):
            print("invalid number")
            return None, origin_list, target_list
        else:
            item = origin_list[y]
            print("you selected ", item)
            target_list.append(item)
            origin_list.remove(item)
            return item, origin_list, target_list



#some variables with text messages for later use
intro = """
You are thrown into a pre-defined dungeon by an untalented programmer. Survive
and exit the dungeon by solving the riddle!"""

room1 = """
You are in the dry first room of the dungeon. Beside dust, stones, and the
remains of unlucky explorers you see an overflooded room (second room) and
behind the water a blue lock on a podest in the (dry) third room.
Waves in the overflooded room indicate that some kind of animal or monster
is living in the water.
"""

room2 = """
You swim through the ice cold water of the overflooded second room. You are
aware that you are not the only living being in this room. Some creature is
swimming toward you!"""

room3 = """
You are in the dry third room of the dungeon. On a podest you see a blue
glowing lock."""

room4= """
You leave the dungeon and enjoy the sunlight and your freedom.
Congratulation, you have won!"""

# game over messages
msg_give_up = """This dungeon had only one riddle to solve but your mind was
to weak for this challenge. As you are unable to leave the dungeon you die of
shame. Game over!"""

msg_poison = """
The bread was laying on the floor for ages, cultivating some yet undiscovered
forms of fungus and mildew. As you eat the bread you discover that it tastes
really bad and is also toxic. You die by food poisoning. Game over!"""

msg_stone = """
It looks like swimming trough the flooded room is no difficult task,
but the ice cold water makes swimming very strenuous. Strange currents, possibly
caused by some kind of monster pull you underwater. The additional weight
of the stone makes you sinking faster and faster.
You are drowned. Game over!"""

msg_fish = """Swimming in the ice cold water without drowning is taking all
your concentration so you register the attack of the unseen swimming creature
only as it is already too late. The creature bites and eates you. You die as
fish fodder."""

# some good messages
msg_unlock = """You manage to unlock the blue lock with the blue key. You hear
some noise from the first room and by the rush of fresh air in the dungeon you
are sure that an exit to the surface was opened by your action. It is maybe a
good idea to go back and examine the first room!"""

msg_busy = """
You feel by the movement of water below you that some kind of monster is busy
devouring the items you dropped here. Lucky for you, the monster has found
something tasty and ignores you....this time."""


#lists for items on the floor and items carried by the player
items1 = ["glowing blue key","small bone", "old bone","very old bread","fossil bread",
          "large stone", "small stone"]
items2 = []
items3 = ["giant stone"]
inventory = []
# variables
room = 1 # where the player is now
history = [] # rooms the player has visited (to not show the description every time)
# data structure: a dict with room number as key and room test as value
rooms={1:room1, 2:room2,3:room3,4:room4}
room_nicknames = {1:"first room", 2:"flooded room", 3:"podest room", 4: "surface"}
# another dict with room number as key and list_of_items as value
items={1:items1, 2:items2, 3:items3}
# another dict with room number as key and list of reachable rooms as value
doors = {1:[2],2:[1,3], 3:[2]}

endmsg = ""
print(intro)
while endmsg == "":
    print("You are currently in room {} ({})".format(room, room_nicknames[room]))
    if not room in history:
        print(rooms[room]) # first time visit
        history.append(room)
    print("On the floor you see: {}".format(items[room]))
    print("You carry those items: {}".format(inventory))
    print("From here you can go to those rooms: {}".format(doors[room]))
    print("What do you want to do now:")
    print("i .... look (read room info)")
    print("p .... pick up some item")
    print("d .... drop some item")
    print("e .... eat an item")
    print("u .... use an item")
    print("m .... move to another room")
    print("q .... quit")
    x = input("press the corresponding char and ENTER\n>")
    if x == "q":
        endmsg = msg_give_up
    elif x == "i":
        print(rooms[room]) # detailed room description
    elif x == "p":
        item, items[room], inventory  = select(items[room],inventory,"pick up")
    elif x == "d":
        item, inventory, items[room] = select(inventory, items[room], "drop")
    elif x == "e":
        belly = [] # create temporary target list (players stomach)
        item, inventory, belly = select(inventory, belly, "eat")
        if item != None:
            if "bread" in item:
                endmsg = msg_poison
            elif "bone" in item:
                print("The {} tastes bad and has no nutrition but you manage to eat all of it".format(item))
            else:
                print("After the first bite you recognize that this {} is not edible and throw it away".format(item))
                items[room].append(item) # throw it on the floor
    elif x == "u":
        item, inventory, items[room] = select(inventory, items[room],"use") # throw item on the floor after using
        if item == "glowing blue key" and room == 3:
            print(msg_unlock)
            doors[1].append(4) # create exit
            rooms[1] +="\nYou see sunlight filtering through an newly created exit to the surface!"
        else:
            print("You can not figure out how to use {} meaningful and throw it frustrated on the floor".format(item))
    elif x == "m":
        print("Please select the room you want to move into:")
        for door in doors[room]:
            print(door, room_nicknames[door])
        y = input("press the corresponding char and ENTER\n>")
        if not y.isdigit():
            print("invalid choice")
        else:
            y = int(y)
            if y in doors[room]:
                # test if player is trying to swim through the flooded room
                # with stone?
                if room == 2:
                    sinking = False
                    for stuff in inventory:
                        if "stone" in stuff:
                            sinking = True
                    monster_busy = False
                    for stuff in items[2]: # check the water (floor of room2)
                        if "bread" or "bone" in stuff:
                            monster_busy = True
                    if sinking:
                        endmsg = msg_stone
                    elif not monster_busy:
                        endmsg = msg_fish
                    else:
                        print(msg_busy)
                        items[2] = [] # the monster eats everything
                        room = y      # swim away
                elif room == 1 and y == 4:
                        endmsg = room4 # game won
                else:
                    room = y # move into new room
print(endmsg)
print("Thanks for playing")















