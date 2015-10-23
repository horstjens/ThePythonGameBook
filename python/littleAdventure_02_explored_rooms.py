# part of http://ThePythonGameBook.com
# (c) 2013 by Horst JENS ( horst.jens@spielend-programmieren.at )
# license: gpl3, see http://www.gnu.org/copyleft/gpl.html
# written for python3
# little adventure game with different rooms
# you can walk between the rooms
# changes:
# menu with room descriptions and enumerate,
# each room get an "explored" flag, reflected in the menu as
# "unknown room"
# room index changed back to numbers
# added boss monsters into boss chamber

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
        self.rooms = {}  # dictionary of rooms, key is room number
        self.items = {}  # dictionary of items, key is item number
        self.monsters = {}  # dictionary of monsters, key is m. number


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

    def __init__(self, game, description="", boss=False):
        self.number = Monster.number
        Monster.number += 1
        game.monsters[self.number] = self  # add monster into game dict
        self.description = description
        self.hitpoints = random.randint(5, 15)
        if description == "":
            if boss:
                self.description = random.choice(
                    (
                        "dragon", "giant", "arch wizard", "ghost king",
                        "vampire lord"
                    )
                )
                self.hitpoints *= 5
            else:
                self.description = random.choice(
                    (
                        "goblin", "ork", "troll", "mice", "rat", "dwarf",
                        "cave drake"
                    )
                )

    def info(self):
        txt = "Monster number {}: {} with {} hitpoints\n".format(self.number, self.description, self.hitpoints)
        return txt


class Effect(object):
    pass


class Room(object):
    number = 0

    def __init__(self, game, description="", connections=[], itemchances=[0.5, 0.25, 0.1], monsterchances=[0.3, 0.2, 0.1, 0.05], bosschances=[0.0], explored=False):
        """need game instance"""
        self.number = Room.number
        game.rooms[self.number] = self  # add room into game dict
        Room.number += 1
        self.explored = explored  # True or False
        self.description = description
        self.connections = connections
        self.itemchances = itemchances
        self.monsterchances = monsterchances
        self.bosschances = bosschances
        self.effect = random.randint(1, 100)
        # create items
        self.itemnumbers = []  # list of indexes of items in this room
        #self.game = game
        for chance in self.itemchances:
            if random.random() < chance:
                newItem = Item(game)
                self.itemnumbers.append(newItem.number)  # add reference
        self.monsternumbers = []  # list of indexes of monsters in this room
        for chance in self.monsterchances:
            if random.random() < chance:
                newMonster = Monster(game)
                self.monsternumbers.append(newMonster.number)  # add reference
        for chance in self.bosschances:
            if random.random() < chance:
                newMonster = Monster(game, boss=True)
                self.monsternumbers.append(newMonster.number)  # add reference

    def info(self, game):
        """return string with all information about this room"""
        txt = "Room number {}: ".format(self.number)
        txt += self.description + "\n"
        # itmes ?
        if len(self.itemnumbers) > 0:
            txt += "You see {} itmes here: \n".format(len(self.itemnumbers))
            for i in self.itemnumbers:
                txt += game.items[i].info()
        else:
            txt += "This room has no items\n"
        # monsters ?
        if len(self.monsternumbers) > 0:
            txt += "You see {} monster(s) here:\n".format(len(self.monsternumbers))
            for m in self.monsternumbers:
                txt += game.monsters[m].info()
        else:
            txt += "No monsters in this room, fortunately.\n"
        # doors
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
    connections = game.rooms[where].connections
    names = []  # temp list of room names
    for c in connections:
        if game.rooms[c].explored:
            names.append(game.rooms[c].description)
        else:
            names.append("unknown room")
    for d in enumerate(names, 1):  # make list of tuples, start with 1
        output("{}.........{}".format(d[0], d[1]))
    answer = ""
    while (
        (not answer.isdecimal()) or (int(answer) < 1) or
        (int(answer) > len(connections))
    ):
        answer = input("please type in valid room number:>")
    return connections[int(answer) - 1]  # return correct room number

    # create a game instance


g = Game()

# add rooms with  description and connections.
# Each room will have a unique number and add himself to game
# room number 0
Room(g, "starting lobby", [1, 4], explored=True)
# room number 1
Room(g, "fist room", [0, 2, 3])
# room number 2
Room(g, "storage room", [1])
# room number 3
# the boss room has 1 to 6 minions and 1 to 3 bosses
Room(
    g,
    "boss chamber",
    [1, 2],
    monsterchances=[1.0, 0.9, 0.8, 0.5, 0.5, 0.5],
    bosschances=[1.0, 0.15, 0.05]
)
# room number 4
Room(g, "end of the world (game over)", [], explored=True)
# start player in lobby (room 0)
where = 0  # the actual room number

# main loop
while len(g.rooms[where].connections) > 0:
    if not g.rooms[where].explored:
        output("You explore a new room!")
        g.rooms[where].explored = True  # explore this room
    output("You are now here:\n{}".format(g.rooms[where].info(g)))
    where = nextMove(g, where)
    output("\n" * 15)
output("\n" * 5)
output("Thank you for playing. Have a nice real life")
