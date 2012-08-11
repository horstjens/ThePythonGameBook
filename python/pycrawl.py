# pycrawl
# my very own rogulike game
# because i play far too much dungeon crawl stone soup
# 2012 by Horst JENS   horstjens@gmail.com
# license: gpl3
# part of http://ThePythonGameBook.com

import random

#class Config(object):
#    """all user-changable constants for the game. ideal for modding"""

# a room consist of 8 x 8 blocks
ROOMROOT = 4
# a level consist of 8 x 8 rooms
BLOCKROOT = 8
# all propabilities are roughly how much monsters , traps etc. you want per room
# values must be a bit higher because the edge of a room is made out of walls
# i want on average 4 monsters per room
P_MONSTER = 4 /  BLOCKROOT **2 # chance that an (non-wall) block is a monster
# i want on aberage 3 traps per room
P_TRAP = 3 /  BLOCKROOT **2 #  it is a trap
P_BOX = 0.5 / BLOCKROOT ** 2 # it is a box
P_LOOT = 0.3 / BLOCKROOT ** 2 # it is a loot
P_SHOP = 0.015 / BLOCKROOT ** 2 # it is a shop
# create a lookup table to see what an individual block should become
# the idea is to create a random number bewteen 0 and 1 and use the table
# to look up what the block is
BLOCKDICT = { P_MONSTER:"m",
              P_MONSTER+P_TRAP:"t",
              P_MONSTER+P_TRAP+P_BOX:"b",
              P_MONSTER+P_TRAP+P_BOX+P_LOOT:"l",
              P_MONSTER+P_TRAP+P_BOX+P_LOOT+P_SHOP:"s"
              }
BLOCKSORT = list(BLOCKDICT.keys()) # it is not possible to sort here directly
BLOCKSORT.sort()                   # now we can sort
P_DOOR = 0.7 # probaility that a wall has a door
P_NOWALL = 0.04 # probability that a wall is removed to create a big hall
STAIRS = 3 # number of stairs up as well as number of stairs down per level
DEEPEST_LEVEL = 10 # the number of the deepest level, where the ultimate questitem is hidden

class Room(object):
    """room, made out of BLOCKROOT x BLOCKROOT blocks (or fields).
    legend:
    # = wall
    d = door
    t = trap
    m = monster
    b = box
    l = loot
    s = shop
    w = water
    f = fire
    . = emtpy
    < = stair up
    > = stair down
    p = player
    q = questitem
    startpoint (1,1) is always topleft, goint each line from left to right and from top to down
    cols and row start with 1, not with zero
    """
    # some classvariables:
    roomnumber = 0
    book = {}
    def __init__(self, level, row, col):
        """ a room in a level. row and col should start with 1, not with 0 """
        self.level = level
        self.row = row
        self.col = col
        Room.roomnumber +=1
        self.roomnumber = Room.roomnumber
        #self.totalnumber = Room.totalnumber # unique number
        Room.book[(self.level, self.row, self.col)] = self  # store class instance into class dict
        self.edge = False
        self.edgeleft = False
        self.edgeright = False
        self.edgetop = False
        self.edgebottom = False
        # is this a edge room ?
        if self.row ==1:
            self.edgetop = True
        elif self.row == ROOMROOT:
            self.edgebottom = True
        if self.roomnumber % ROOMROOT == 0:
            self.edgeright = True
        elif self.roomnumber % ROOMROOT == 1:
            self.edgeleft = True
        if self.edgeleft or self.edgeright or self.edgebottom or self.edgetop:
            self.edge = True
        # possible directions for path
        self.north = False
        self.south = False
        self.west = False
        self.easyt = False
        # create outer wall
        ##self.blocks = ""
        self.blocks = {}
        for row in list(range(1,BLOCKROOT+1)):
            if row == 1 or row == BLOCKROOT :
                #upper or lower edge
                for col in list(range(1,BLOCKROOT+1)):
                    self.blocks[row,col]="#"
            else:
                # middle rows
                for col in list(range(1,BLOCKROOT+1)):
                    if col == 1 or col == BLOCKROOT:
                        # generate wall left and right
                        self.blocks[row,col] = "#" 
                    else:
                        # generate  empty space or loot, traps and monsters in the middle
                        block = "." # default is the empty space
                        blockroll = random.random() # number between 0.0 and 1.0
                        for fate in BLOCKSORT:
                            # fate is sorted from 0.0 upwards. if blockroll < fate than we know the type of the block
                            if blockroll < fate:
                                block = BLOCKDICT[fate]
                                break # we found our block, do not compare fate again
                        self.blocks[row, col] = block
                                
        
        
    def make_door(self, direction):
        """create a door from one room into another room,
        the door facing direction north, south, west or east.
        also makes a corresponding door in the other room.
        return True if door was made, otherwise False
        a door can be made only vertical to a wall"""
        #check if direction is meaningful or forbidden because edge
        if self.edge:
            if direction == "west" and self.edgeleft:
                return False
            elif direction == "east" and self.edgeright:
                return False
            elif direction =="north" and self.edgetop:
                return False
            elif direction == "south" and self.edgebottom:
                return False
        # ok, let us make the door !
        if direction == "west":
            row = random.randint(2, BLOCKROOT-1)
            #only make a door if there is a wall
            if self.blocks[row,1] != ".":
                self.blocks[row,1] = "d"
                # corresponding door in other room
                Room.book[(self.level, self.row, self.col -1)].blocks[row, BLOCKROOT] = "d"
        elif direction == "east":
            row = random.randint(2, BLOCKROOT-1)
            if self.blocks[row, BLOCKROOT] != ".":
                self.blocks[row, BLOCKROOT] = "d"
                Room.book[(self.level, self.row, self.col +1)].blocks[row, 1] = "d"
        elif direction == "north":
            col = random.randint(2, BLOCKROOT-1)
            if self.blocks[1,col] != ".":
                self.blocks[1,col] = "d"
                Room.book[(self.level, self.row-1, self.col)].blocks[BLOCKROOT, col] = "d"
        elif direction == "south":
            col = random.randint(2, BLOCKROOT-1)
            if self.blocks[BLOCKROOT,col] != ".":
                self.blocks[BLOCKROOT,col] = "d"
                Room.book[(self.level, self.row+1,self.col)].blocks[1,col] = "d"
        return True
    
    
    def destroy_wall(self, direction):
        """destroys a whole wall of a room (the corner stones are excluded)
        and the corresponding wall of the other room to create giant halls
        return True if wall was destroyed and False otherwise"""
        if self.edge:
            if direction == "west" and self.edgeleft:
                return False
            elif direction == "east" and self.edgeright:
                return False
            elif direction =="north" and self.edgetop:
                return False
            elif direction == "south" and self.edgebottom:
                return False
         # ok, let us destroy some walls !
        if direction == "west":
            for row in list(range(2, BLOCKROOT)):
                self.blocks[row,1] = "."
                self.west = True
                # corresponding wall in other room
                Room.book[(self.level, self.row, self.col -1)].blocks[row, BLOCKROOT] = "."
                Room.book[(self.level, self.row, self.col -1)].east = True
        elif direction == "east":
            for row in list(range(2, BLOCKROOT)):
                self.blocks[row, BLOCKROOT] = "."
                self.east = True
                # corresponding wall in other room
                Room.book[(self.level, self.row, self.col +1)].blocks[row, 1] = "."
                Room.book[(self.level, self.row, self.col +1)].west = True
        elif direction == "north":
            for col in list(range(2, BLOCKROOT)):
                self.blocks[1,col] = "."
                self.north = True
                # corresponding wall in other room
                Room.book[(self.level, self.row-1, self.col)].blocks[BLOCKROOT, col] = "."
                Room.book[(self.level, self.row-1, self.col)].south = True
        elif direction == "south":
            for col in list(range(2, BLOCKROOT)):
                self.blocks[BLOCKROOT,col] = "."
                self.south = True
                # corresponding door in other room
                Room.book[(self.level, self.row+1,self.col)].blocks[1,col] = "."
                Room.book[(self.level, self.row+1,self.col)].north = True
        return True
    
    def printroom(self, verbose=True):
        """print and return a single room as string"""
        lines = ""
        for blockrow in list(range(1,BLOCKROOT+1)):
            line = ""
            for blockcol in list(range(1,BLOCKROOT+1)):
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
        Level.book[number] = self # store the whole class instance into a class dict
        for row in list(range(1,ROOMROOT+1)):
            for col in list(range(1,ROOMROOT+1)):
                # create rooms
                actualroom = Room(self.level, row, col)
        self.stairsup = 0
        self.stairsdown = 0
        # create stairs
        while self.stairsup < STAIRS:
            row, col, blockrow, blockcol = self.placeme()
            Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = "<"
            self.stairsup += 1
        if self.level < DEEPEST_LEVEL: # the deepest level has no stairs down
            while self.stairsdown < STAIRS:
                row, col, blockrow, blockcol = self.placeme()
                Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = ">"
                self.stairsdown += 1
            # some function to test that there is a valid path from stairup to stairdown
            # TODO FIXME    
            
        # remove walls and create doors between rooms
        for row in list(range(1,ROOMROOT+1)):
            for col in list(range(1,ROOMROOT+1)):
                for wall in ["north","south","west","east"]:
                    if random.random() < P_NOWALL:
                        Room.book[(self.level, row, col)].destroy_wall(wall)
                    elif random.random() < P_DOOR: # if there is a wall, make door at a random position in this wall
                        #print("making door:", wall, "row",row, "col",col)
                        Room.book[(self.level, row, col)].make_door(wall)
        # set player in level 1
        if self.level == 1:
            row, col, blockrow, blockcol = self.placeme()
            Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = "p"
        # test if player can reach a stairdown
            
        # set questitem in DEEPEST_LEVEL
        if self.level == DEEPEST_LEVEL:
            row, col, blockrow, blockcol = self.placeme()
            Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] = "q"
        
    def findpath(self, row, col, target=">" ):
        """returns True if there exist a path from row/col toward a target block"""
        rooms = 0
        dx = 1 # search direction
        dy = 0 # search direction
        while rooms < ROOMROOT**2:
            teststring = ROOM.book[(self.level, row, col)].printroom(False)
            if target in teststring:
                return True # valid path in same room
            else:
                col += dx
                if col > 
                
            
            
    def placeme(self):
        """returns an empty random position to place stuff"""
        target = "x" # set invalid target
        while target != ".":
            row = random.randint(1, ROOMROOT)
            col = random.randint(1, ROOMROOT)
            blockrow = random.randint(1, BLOCKROOT)
            blockcol = random.randint(1, BLOCKROOT)
            target = Room.book[(self.level, row, col)].blocks[(blockrow, blockcol)] 
        return row, col, blockrow, blockcol
    
    def printlevel(self, verbose=True):
        """print and return the whole level as string"""
        lines = ""
        for row in list(range(1,ROOMROOT+1)):
            for blockrow in list(range(1,BLOCKROOT+1)):
                line = ""
                for col in list(range(1,ROOMROOT+1)):
                    for blockcol in list(range(1,BLOCKROOT+1)):
                        line += Room.book[(self.level,row,col)].blocks[blockrow, blockcol]
                lines += line + "\n"
        if verbose:
            print(lines)
        return lines
            

if __name__ == '__main__':
    Level(1) # create first level
    Level.book[1].printlevel()
    Room.book[(1,3,3)].printroom()
