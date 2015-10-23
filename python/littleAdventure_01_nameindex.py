# part of http://ThePythonGameBook.com
# (c) 2013 by Horst JENS ( horst.jens@spielend-programmieren.at )
# license: gpl3, see http://www.gnu.org/copyleft/gpl.html
# written for python3
# little adventure game with different rooms
# you can walk between the rooms.
#
# changes:
# using roomnames as index instead of room numbers
# introducing enumerate to create a menu

import random


class Game(object):
    """
    holds all information for a game. Later it may be
    possible to run several game instances at once
    """
    number = 0

    def __init__(self):
        self.number = Game.number
        Game.number += 1
        #self.rooms = {} # dictionary of rooms, index is room number
        self.roomnames = {}  # key is roomname, value is room instance
        self.items = {}  # dictionary of items
        self.monsters = {}  # dictionary of monsters


class Item(object):
    number = 0

    def __init__(self, game, description=""):
        self.number = Item.number
        Item.number += 1
        if description == "":
            description = random.choice(
                (
                    "ring", "beer", "flowerpot", "stone", "bottle"
                )
            )
        self.description = description
        game.items[self.number] = self  # add item into game dict

    def info(self):
        txt = "Item Number {}: ".format(self.number)
        txt += self.description + "\n"
        return txt


class Monster(object):
    number = 0

    def __init__(self, game, description=""):
        self.number = Monster.number
        Monster.number += 1
        game.monsters[self.number] = self  # add monster into game dict
        self.description = description
        if description == "":
            self.description = random.choice(
                (
                    "goblin", "ork", "troll", "mice", "rat", "dwarf", "dragon"
                )
            )
        self.hitpoints = random.randint(5, 15)

    def info(self):
        txt = "Monster number {}: {} with {} hitpoints\n".format(self.number, self.description, self.hitpoints)
        return txt


class Effect(object):
    pass


class Room(object):
    number = 0

    def __init__(self, game, description="", connections=[], itemchances=[0.5, 0.25, 0.1], monsterchances=[0.3, 0.2, 0.1, 0.05]):
        """need game instance"""
        self.number = Room.number
        #game.rooms[self.number] = self # add room into game dict
        Room.number += 1
        # testing if room description is unique
        while description in game.roomnames:
            description += str(self.number)
        self.description = description
        game.roomnames[self.description] = self
        self.connections = connections
        self.itemchances = itemchances
        self.monsterchances = monsterchances
        self.effect = random.randint(1, 100)
        # create items
        self.itemnumbers = []  # list of indexes of items in this room
        for chance in self.itemchances:
            if random.random() < chance:
                newItem = Item(game)
                self.itemnumbers.append(newItem.number)  # add reference
        self.monsternumbers = []  # list of indexes of monsters in this room
        for chance in self.monsterchances:
            if random.random() < chance:
                newMonster = Monster(game)
                self.monsternumbers.append(newMonster.number)  # add reference

    def info(self, game):
        """return string with all information about this room"""
        txt = "Room number {}: ".format(self.number)
        txt += self.description + "\n"
        if len(self.itemnumbers) > 0:
            txt += "You see {} itmes here: \n".format(len(self.itemnumbers))
            for i in self.itemnumbers:
                txt += game.items[i].info()
        else:
            txt += "This room has no items\n"
        if len(self.monsternumbers) > 0:
            txt += "You see {} monster(s) here:\n".format(len(self.monsternumbers))
            for m in self.monsternumbers:
                txt += game.monsters[m].info()
        else:
            txt += "No monsters in this room, fortunately.\n"
        txt += "You see {} door(s).\n".format(len(self.connections))
        txt += "\n"
        return txt


# this function use print, replace later with gui commands
def output(txt):
    """can be later replaced by gui or graphical output"""
    print(txt)


# this funciton use input, replace later with gui command
def nextMove(game, where):
    """ask the user to select only one of many options"""
    output("Where do you want to go today ?")
    connections = game.roomnames[where].connections
    # create list of tuples with (number, roomname), starting with 1:
    for c in enumerate(connections, 1):
        output("{}.........{}".format(c[0], c[1]))
    answer = ""
    while (
        (not answer.isdecimal()) or (int(answer) < 1) or
        (int(answer) > len(connections))
    ):
        answer = input("please type in valid room number:>")
    return connections[int(answer) - 1]  # return room name

    # create a game instance


g = Game()

# add rooms with  description and connections.
# Each room will have a unique number and add himself to game
# make sure each room name is unique and spelled correctly !
Room(g, "starting lobby", ["first room", "end of the world"])  # 0
Room(g, "first room", ["starting lobby", "storage room", "boss chamber"])  # 1
Room(g, "storage room", ["first room"])  # 2
Room(g, "boss chamber", ["first room", "storage room"])  # 3
Room(g, "end of the world", [])  # 4

# start player in lobby (room 0)
where = "starting lobby"  # the actual room number

print(g.roomnames[where])
print(g.roomnames[where].connections)

# main loop
while len(g.roomnames[where].connections) > 0:
    output("You are now here:\n{}".format(g.roomnames[where].info(g)))
    where = nextMove(g, where)
    output("\n" * 15)
output("\n" * 5)
output("Thank you for playing. Have a nice real life")
