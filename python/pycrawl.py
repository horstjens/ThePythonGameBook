# pycrawl
# my very own rogulike game
# because i play far too much dungeon crawl stone soup
# 2012 by Horst JENS   horstjens@gmail.com
# license: gpl3 see http://www.gnu.org/copyleft/gpl.html
# this game is a part of http://ThePythonGameBook.com

# short description:
# like dungeon crawl stone soup ( see http://crawl.develz.org/wordpress/ )
# this game shall create random levels. Each level has several rooms.
# Each room is made out of tiles (blocks).
# the player start in level one and has to find the ultimate quest item
# in the deepest level (and maybe return to level one)
# each level has 3 stairs down and 3 stairs up

import random

#class Config(object):
#    """all user-changable constants for the game. ideal for modding"""

# a level consist of 8 x 8 rooms, so ROOMROOT = 8
ROOMROOT = 3  # warning, you can get an maximum recursion error if this number is too large
# a room consist of 8 x 8 blocks, so BLOCKROOT = 8
BLOCKROOT = 6
# all propabilities are roughly how much monsters , traps etc. you want per room
# values must be a bit higher because the edge of a room is made out of walls
# i want on average 4 monsters per room
P_MONSTER = 4 / BLOCKROOT**2  # chance that an (non-wall) block is a monster
# i want on average 3 traps per room
P_TRAP = 3 / BLOCKROOT**2  #  it is a trap
P_BOX = 0.5 / BLOCKROOT**2  # it is a box
P_LOOT = 0.3 / BLOCKROOT**2  # it is a loot
P_SHOP = 0.015 / BLOCKROOT**2  # it is a shop
# create a lookup table to see what an individual block should become
# the idea is to create a random number bewteen 0 and 1 and use the table
# to look up what the block is
BLOCKDICT = {
    P_MONSTER: "m",
    P_MONSTER + P_TRAP: "t",
    P_MONSTER + P_TRAP + P_BOX: "b",
    P_MONSTER + P_TRAP + P_BOX + P_LOOT: "l",
    P_MONSTER + P_TRAP + P_BOX + P_LOOT + P_SHOP: "s"
}
# be careful when using floats as keys for a dict, see http://floating-point-gui.de/

BLOCKSORT = sorted(BLOCKDICT.keys())  # sorted() generates a new sorted list

P_DOOR = 0.5  # probaility that a wall has a door
P_NOWALL = 0.05  # probability that a wall is removed to create a big hall
STAIRS = 3  # number of stairs up as well as number of stairs down per level
DEEPEST_LEVEL = 10  # the number of the deepest level, where the ultimate questitem is hidden
DOORCHARS = [".", "d"]  # chars for empty space and door. both allow connection between rooms
CARDINALS = ["north", "south", "east", "west"]  # the 4 possible directions for connecting rooms
# a dict for each cardinal direction: (counter-direction, dy, dx)
CARDINALSDICT = {
    "north": ("south", -1, 0),
    "south": ("north", 1, 0),
    "east": ("west", 0, 1),
    "west": ("east", 0, -1)
}
LEGEND = {
    "X": "granite wall",
    "#": "wall",
    "d": "door",
    "t": "trap",
    "m": "monster",
    "b": "box",
    "l": "loot",
    "s": "shop",
    "w": "water",
    "f": "fire",
    ".": "emtpy",
    "<": "stair up",
    ">": "stair down",
    "p": "player",
    "q": "questitem"
}


class Room(object):
    """room, made out of BLOCKROOT x BLOCKROOT blocks (or fields).
    startpoint (1,1) is always topleft, going each line from left to right and from top to down
    cols and row start with 1, not with zero. (very un-pythonic!)
    to avoid headache when hand-editing levels.
    And it's always row first, column second.
    """
    # some classvariables:
    roomnumber = 0  # total amount of rooms. unique number for each room
    book = {}  # dict to store all rooms. will maybe transferred into Level class in the future

    def __init__(self, level, row, col):
        """ a room in a level. row and col start with 1, not with 0 """
        self.level = level
        self.row = row
        self.col = col
        Room.roomnumber += 1
        self.roomnumber = Room.roomnumber
        #self.totalnumber = Room.totalnumber # unique number
        Room.book[(self.level, self.row, self.col)] = self  # store class instance into class dict
        self.edge = False  # possibly unnecessary..
        self.edgewest = False
        self.edgeeast = False
        self.edgenorth = False
        self.edgesouth = False
        # is this a edge room ?
        if self.row == 1:
            self.edgenorth = True
        elif self.row == ROOMROOT:
            self.edgesouth = True
        if self.roomnumber % ROOMROOT == 0:
            self.edgeeast = True
        elif self.roomnumber % ROOMROOT == 1:
            self.edgewest = True
        if self.edgewest or self.edgeeast or self.edgesouth or self.edgenorth:
            self.edge = True
        # possible directions for path. If there is a connection (door) to the next room, change to True
        self.north = False  # may be also unnecessary, see Level.doors[]
        self.south = False
        self.west = False
        self.east = False
        # create outer wall
        ##self.blocks = ""
        self.blocks = {}
        for row in list(range(1, BLOCKROOT + 1)):
            if row == 1 or row == BLOCKROOT:
                #upper or lower edge
                for col in list(range(1, BLOCKROOT + 1)):
                    if (row == 1 and self.edgenorth) or (row == BLOCKROOT and self.edgesouth):
                        self.blocks[row, col] = "X"  # granit
                    else:
                        self.blocks[row, col] = "#"  # mortar
            else:
                # middle rows
                for col in list(range(1, BLOCKROOT + 1)):
                    if col == 1 or col == BLOCKROOT:
                        # generate wall left and right
                        if (col == 1 and self.edgewest) or (col == BLOCKROOT and self.edgeeast):
                            self.blocks[row, col] = "X"  # granit
                        else:
                            self.blocks[row, col] = "#"  # mortar
                    else:
                        # generate  empty space or loot, traps and monsters in the middle
                        block = "."  # default is the empty space
                        blockroll = random.random()  # number between 0.0 and 1.0
                        for fate in BLOCKSORT:
                            # fate is sorted from 0.0 upwards. if blockroll < fate than we know the type of the block
                            if blockroll < fate:
                                block = BLOCKDICT[fate]
                                break  # we found our block, do not compare fate again
                        self.blocks[row, col] = block

    def make_door(self, direction):
        """create a door from one room into another room,
        the door facing direction north, south, west or east.
        also makes a corresponding door in the other room.
        return True if door was made, otherwise False
        a door can be made only vertical to a wall"""
        #check if direction is meaningful or forbidden because edge
        if self.edge:
            if direction == "west" and self.edgewest:
                return False
            elif direction == "east" and self.edgeeast:
                return False
            elif direction == "north" and self.edgenorth:
                return False
            elif direction == "south" and self.edgesouth:
                return False
        # ok, let us make the door !
        if direction == "west":
            row = random.randint(2, BLOCKROOT - 1)
            #only make a door if there is a wall
            if self.blocks[row, 1] != ".":
                self.blocks[row, 1] = "d"
                self.west = True
                # corresponding door in other room
                Room.book[(self.level, self.row, self.col - 1)].blocks[row, BLOCKROOT ] = "d"
                Room.book[(self.level, self.row, self.col - 1)].east = True
        elif direction == "east":
            row = random.randint(2, BLOCKROOT - 1)
            if self.blocks[row, BLOCKROOT] != ".":
                self.blocks[row, BLOCKROOT] = "d"
                self.east = True
                Room.book[(self.level, self.row, self.col + 1)].blocks[row, 1] = "d"
                Room.book[(self.level, self.row, self.col + 1)].west = True
        elif direction == "north":
            col = random.randint(2, BLOCKROOT - 1)
            if self.blocks[1, col] != ".":
                self.blocks[1, col] = "d"
                self.north = True
                Room.book[(self.level, self.row - 1, self.col)].blocks[BLOCKROOT, col] = "d"
                Room.book[(self.level, self.row - 1, self.col)].south = True
        elif direction == "south":
            col = random.randint(2, BLOCKROOT - 1)
            if self.blocks[BLOCKROOT, col] != ".":
                self.blocks[BLOCKROOT, col] = "d"
                self.south = True
                Room.book[(self.level, self.row + 1, self.col)].blocks[1, col] = "d"
                Room.book[(self.level, self.row + 1, self.col)].north = True
        return True

    def destroy_wall(self, direction):
        """destroys a whole wall of a room (the corner stones are excluded)
        and the corresponding wall of the other room to create giant halls
        return True if wall was destroyed and False otherwise"""
        if self.edge:
            if direction == "west" and self.edgewest:
                return False
            elif direction == "east" and self.edgeeast:
                return False
            elif direction == "north" and self.edgenorth:
                return False
            elif direction == "south" and self.edgesouth:
                return False
        # ok, let us destroy some walls !
        if direction == "west":
            for row in list(range(2, BLOCKROOT)):
                self.blocks[row, 1] = "."
                self.west = True
                # corresponding wall in other room
                Room.book[(self.level, self.row, self.col - 1)].blocks[row, BLOCKROOT] = "."
                Room.book[(self.level, self.row, self.col - 1)].east = True
        elif direction == "east":
            for row in list(range(2, BLOCKROOT)):
                self.blocks[row, BLOCKROOT] = "."
                self.east = True
                # corresponding wall in other room
                Room.book[(self.level, self.row, self.col + 1)].blocks[row, 1] = "."
                Room.book[(self.level, self.row, self.col + 1)].west = True
        elif direction == "north":
            for col in list(range(2, BLOCKROOT)):
                self.blocks[1, col] = "."
                self.north = True
                # corresponding wall in other room
                Room.book[(self.level, self.row - 1, self.col)].blocks[BLOCKROOT, col] = "."
                Room.book[(self.level, self.row - 1, self.col)].south = True
        elif direction == "south":
            for col in list(range(2, BLOCKROOT)):
                self.blocks[BLOCKROOT, col] = "."
                self.south = True
                # corresponding door in other room
                Room.book[(self.level, self.row + 1, self.col)].blocks[
                    1, col
                ] = "."
                Room.book[(self.level, self.row + 1, self.col)].north = True
        return True

    def printroom(self, verbose=True):
        """print and return a single room as string"""
        lines = ""
        for blockrow in list(range(1, BLOCKROOT + 1)):
            line = ""
            for blockcol in list(range(1, BLOCKROOT + 1)):
                line += self.blocks[blockrow, blockcol]
                #screen[(row, col, blockrow, blockcol)] = actualroom.blocks[blockrow, blockcol]
            lines += line + "\n"
        if verbose:
            print(lines)
        return lines


class Level(object):
    book = {}

    #levelnumber = 0
    def __init__(self, number=1):
        """create level with random rooms.
        set player_position if levelnumber is 1
        set questitem if levelnumber is DEEPEST_LEVEL"""
        self.level = number
        Level.book[number] = self  # store the whole class instance into a class dict
        for row in list(range(1, ROOMROOT + 1)):
            for col in list(range(1, ROOMROOT + 1)):
                # create rooms
                actualroom = Room(self.level, row, col)
        self.stairsup = []  # this level: row, col, blockrow, blockcol, connect to: row, col, blockrow, blockcol
        self.stairsdown = []
        #self.dirtyrooms = set() # used for pathfinding. A set has only unique items, no doublets
        #self.used_doors = 0 # check how long pathfinding is running, break if necessary
        self.doors = {}
        self.unused_doors = {}
        # create stairs
        while len(self.stairsup) < STAIRS:
            row, col, blockrow, blockcol = self.placeme()
            Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = "<"
            #self.stairsup += 1
            self.stairsup.append((row, col, blockrow, blockcol))
        if self.level < DEEPEST_LEVEL:  # the deepest level has no stairs down
            while len(self.stairsdown) < STAIRS:
                row, col, blockrow, blockcol = self.placeme()
                Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = ">"
                #self.stairsdown += 1
                self.stairsdown.append((row, col, blockrow, blockcol))
            # some function to test that there is a valid path from stairup to stairdown
            # TODO FIXME

            # remove walls and create doors between rooms
        for row in list(range(1, ROOMROOT + 1)):
            for col in list(range(1, ROOMROOT + 1)):
                self.doors[(row, col)] = []
                for wall in ["north", "south", "west", "east"]:
                    if random.random() < P_NOWALL:
                        Room.book[(self.level, row, col)].destroy_wall(wall)
                    elif random.random() < P_DOOR:  # if there is a wall, make door at a random position in this wall
                        #print("making door:", wall, "row",row, "col",col)
                        Room.book[(self.level, row, col)].make_door(wall)

        # recalculate directions now, because we have doors !
        self.recalculate_directions()
        # set player in level 1
        if self.level == 1:
            row, col, blockrow, blockcol = self.placeme()
            Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = "p"
        # --------------- level validation -----------------
        # test if player can reach a stairdown
        #self.dirtyrooms.clear() # clear the set
        self.unused_doors = self.doors.copy()  # have a fresh dict of unused doors

        print("initiating pathfinding...")
        if self.findpath(row, col, ">"):
            print("player can reach stair down")
            #pass
        else:
            print("player has no path to stair down")
            #raise Exception("this level is invalid. please create another one").with_traceback(tracebackobj)
            # fix this level !
            target = random.choice(self.stairsdown)  # select one of the stairdowns in this level and create a path to it
            targetrow = target[0]
            targetcol = target[1]
            print("creating tunnel....")
            self.create_tunnel(row, col, targetrow, targetcol)  # create a tunnel to the target room, by making doors

        # set questitem in DEEPEST_LEVEL
        if self.level == DEEPEST_LEVEL:
            row, col, blockrow, blockcol = self.placeme()
            Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = "q"

    def create_tunnel(self, startrow, startcol, targetrow, targetcol):
        """to make walking from startroom to targetroom possible,
        this method will create some necessary doors"""
        deltax = targetcol - startcol
        deltay = targetrow - startrow
        dx = 0
        dy = 0
        if deltax != 0:
            dx = deltax / abs(deltax)  # if negative, makes -1, else, makes 1
        if deltay != 0:
            dy = deltay / abs(deltay)
        #print("I start tunneling in rwo %i col %i"%(startrow, startcol))
        for x in list(range(abs(deltax))):
            if dx == -1:
                Room.book[(self.level, startrow, startcol + x * dx)].make_door("west")
                #print('tunneling west')
            elif dx == 1:
                Room.book[(self.level, startrow, startcol + x * dx)].make_door("east")
                #print('tunneling east')
        for y in list(range(abs(deltay))):
            print("y::::row: %i col %i ynow: %i xnow: %i" % (startrow, startcol, startrow + y * dy, startcol + x * dx))
            if dy == -1:
                # i am not sure but i feel the (x+1) is because i want to be in this room, not just
                # make a door into this room.
                Room.book[(self.level, startrow + y * dy, startcol + (x + 1) * dx) ].make_door("north")
                #print('tunneling north')
            elif dy == 1:
                Room.book[(self.level, startrow + y * dy, startcol + (x + 1) * dx) ].make_door("south")
                #print('tunneling south')
        self.recalculate_directions()  # update level map

    def recalculate_directions(self):
        """after importing a level from textfile,
        after generating a level, or after creating doors,
        this method is necessary to find out
        for each room if this room is connected (doors, no wall)
        to other rooms. Also find out if a room is an edge room"""
        # stuff that normally Level.__init__() does
        #self.dirtyrooms = set() # used for pathfinding. A set has only unique items, no doublets
        self.doors = {}
        # recalculate all rooms of this level
        for row in list(range(1, ROOMROOT + 1)):
            for col in list(range(1, ROOMROOT + 1)):
                self.doors[(row, col)] = []
                if row == 1:  # north edge
                    Room.book[(self.level, row, col)].edge = True
                    Room.book[(self.level, row, col)].edgenorth = True
                elif row == ROOMROOT:  # south edge
                    Room.book[(self.level, row, col)].edge = True
                    Room.book[(self.level, row, col)].edgesouth = True
                if col == 1:  # west edge
                    Room.book[(self.level, row, col)].edge = True
                    Room.book[(self.level, row, col)].edgewest = True
                elif col == ROOMROOT:  # east edge
                    Room.book[(self.level, row, col)].edge = True
                    Room.book[(self.level, row, col)].edgeeast = True
                for wall in ["north", "south", "west", "east"]:
                    if Room.book[(self.level, row, col)].edge:
                        if wall == "north" and Room.book[(self.level, row, col)].edgenorth:
                            continue
                        if wall == "south" and Room.book[(self.level, row, col)].edgesouth:
                            continue
                        if wall == "west" and Room.book[(self.level, row, col)].edgewest:
                            continue
                        if wall == "east" and Room.book[(self.level, row, col)].edgeeast:
                            continue
                    # check wall for doors or empty space
                    #DOORCHARS = [".","d"]
                    if wall == "north":
                        for blockcol in list(range(1, BLOCKROOT + 1)):
                            if Room.book[(self.level, row, col)].blocks[(1, blockcol)] in DOORCHARS:
                                Room.book[(self.level, row, col)].north = True
                                self.doors[(row, col)].append("north")
                                break
                    elif wall == "south":
                        for blockcol in list(range(1, BLOCKROOT + 1)):
                            if Room.book[(self.level, row, col)].blocks[(BLOCKROOT, blockcol)] in DOORCHARS:
                                Room.book[(self.level, row, col)].south = True
                                self.doors[(row, col)].append("south")
                                break
                    elif wall == "west":
                        for blockrow in list(range(1, BLOCKROOT + 1)):
                            if Room.book[(self.level, row, col)].blocks[(blockrow, 1)] in DOORCHARS:
                                Room.book[(self.level, row, col)].west = True
                                self.doors[(row, col)].append("west")
                                break
                    elif wall == "east":
                        for blockrow in list(range(1, BLOCKROOT + 1)):
                            if Room.book[(self.level, row, col)].blocks[(blockrow, BLOCKROOT)] in DOORCHARS:
                                Room.book[(self.level, row, col)].east = True
                                self.doors[(row, col)].append("east")
                                break

    def findpath(self, row, col, target=">"):
        """returns True if there exist a path from row/col toward a target block"""
        print("finding path from %s %s to %s" % (row, col, target))
        if self.testroom(row, col, target):
            return True
        else:
            if len(self.unused_doors[(row, col)]) > 0:
                for direction in CARDINALS:
                    if direction in self.unused_doors[(row, col)]:
                        self.unused_doors[(row, col)].remove(direction)
                        # cardinalsdict is {dir:(counterdir, dy, dx)}
                        dx = CARDINALSDICT[direction][2]
                        dy = CARDINALSDICT[direction][1]
                        if self.findpath(row + dy, col + dx, target):
                            return True
            else:
                #self.dirtyrooms.add((row, col)) # this room is searched
                return False

    def testroom(self, row, col, target=">"):
        """returns True if the target ist in the room"""
        teststring = Room.book[(self.level, row, col)].printroom(False)
        if target in teststring:
            return True  # valid path in same room
        else:
            return False

    def placeme(self):
        """returns an empty random position to place stuff"""
        target = "x"  # set invalid target
        while target != ".":  # as long as target is not empty space
            row = random.randint(1, ROOMROOT)
            col = random.randint(1, ROOMROOT)
            blockrow = random.randint(1, BLOCKROOT)
            blockcol = random.randint(1, BLOCKROOT)
            target = Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)]
        return row, col, blockrow, blockcol

    def printlevel(self, verbose=True):
        """print and return the whole level as string"""
        lines = ""
        for row in list(range(1, ROOMROOT + 1)):
            for blockrow in list(range(1, BLOCKROOT + 1)):
                line = ""
                for col in list(range(1, ROOMROOT + 1)):
                    for blockcol in list(range(1, BLOCKROOT + 1)):
                        line += Room.book[(self.level, row, col)].blocks[
                            blockrow, blockcol
                        ]
                lines += line + "\n"
        if verbose:
            print(lines)
        return lines

    def exportlevel(self, filename="level.txt"):
        """dump level into an txt file"""
        f = open(filename, "w")  # create file object f for writing
        f.write(self.printlevel(False))
        f.close()

    def importlevel(self, filename="level.txt"):
        """import a single level from file"""
        self.stairsdown = []  # stuff that __init__ does normally
        self.stairsup = []
        f = open(filename, "r")  # create file object f for reading
        row = 1
        blockrow = 1
        for textline in f.readlines():
            #for row in list(range(1,ROOMROOT+1)):
            #for blockrow in list(range(1,BLOCKROOT+1)):
            start = 0
            for col in list(range(1, ROOMROOT + 1)):
                for blockcol in list(range(1, BLOCKROOT + 1)):
                    end = start + 1
                    mychar = textline[start:end]
                    #print("mychar:",mychar)
                    Room.book[(self.level, row, col)].blocks[
                        blockrow, blockcol
                    ] = mychar
                    start += 1  # next char
                    if mychar == ">":
                        #self.stairsdown += 1
                        self.stairsdown.append((row, col, blockrow, blockcol))
                    elif mychar == "<":
                        #self.stairsup += 1
                        self.stairsup.append((row, col, blockrow, blockcol))
            blockrow += 1
            if blockrow > BLOCKROOT:
                blockrow = 1
                row += 1
        f.close()


if __name__ == '__main__':
    Level(1)  # create first level
    Level.book[1].printlevel()

    Level.book[1].exportlevel()
    #Level.book[1].importlevel()
    #Level.book[1].recalculate_directions()
    #Level.book[1].printlevel()
    #Room.book[(1,3,3)].printroom()

    #print(Level.book[1].doors)
