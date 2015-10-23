# pycrawl_walkdemo
# my very own rogulike game
# because i play far too much dungeon crawl stone soup
# 2012 by Horst JENS   horstjens@gmail.com
# license: gpl3 see http://www.gnu.org/copyleft/gpl.html
# this game is a part of http://ThePythonGameBook.com

# this is a demo where the player (@) runs around in some small rooms.
# each tile (block) where the player stands should be saved and drawn again as soon as the player moves away

# 3 x 3 roooms with 8 x 8 tiles

#ROOMROOT = 3
#BLOCKROOT = 6
rawlevel = """\
XXXXXXXXXXXXXXXXXX
X.l..##....dd.m..X
X...m##>...##..m.X
Xtb.m##t..l##...>X
X.<..dd....ddm.t.X
########d#d#######
########d#d#######
X...>##....##....X
X....dd....ddt.<.X
X...mdd...m##....X
X....##.m..##....X
####d#########d###
####d#########d###
X....##..m.##...lX
Xmmb.dd<m..dd...mX
X.s..##..m.##....X
X.t..##m...##...mX
XXXXXXXXXXXXXXXXXX\
"""


class Tile(object):
    """the level or map is made out of ascii tiles. the properties of the tiles are defined here"""
    tiledict = {}  # a dict for all the different tiles

    def __init__(self, char, **kwargs):
        self.char = char
        self.text = ""
        #Tile.tileset.add(char) # put this new Tile into the tileset
        Tile.tiledict[char] = self  # put this new Tile into the tiledict
        self.stepin = True  # can the player step into this tile ? walls, fire etc: False
        #self.interact = False
        self.action = []  # possible actions on this tile
        self.description = ""  # text to be displayed
        self.moveable = False

        for attr in kwargs.keys():
            if attr in self.__dict__:
                self.__dict__[attr] = kwargs[attr]

    def showStats(object):
        """display all stats of an class instance"""
        for key in object.__dict__:
            print(key, ":", object.__dict__[key])


Tile(
    "X",
    text="an outer wall",
    description="an outer wall of the level. You can not go there",
    stepin=False,
    action=["write grafitti"]
)
Tile(
    ".",
    text="an empty space",
    description="an empty boring space. There is really nothing here."
)
Tile("d", text="a door", description="an (open) door", action=["open", "close"])
Tile(
    "m",
    text="an suspicious space",
    description=
    "monster placeholder. You have the feeling this place belongs to a monster, but you can not see it yet"
)
Tile(
    "<",
    text="a stair up",
    description="a stair up to the previous level",
    action=["climb up"]
)
Tile(
    ">",
    text="a stair down",
    description="a stair down to the next deeper level",
    action=["climb down"]
)
Tile(
    "#",
    text="an inner wall",
    description=
    "an inner wall. You may destroy this wall with the right tools or spells",
    stepin=False
)
Tile(
    "t",
    text="a trap",
    description="a dangerous trap !",
    action=["disarm", "destroy", "flag"]
)
Tile(
    "l",
    text="a heap of loot",
    description=
    "a heap of loot. Sadly, not yet programmed. But feel yourself enriched",
    action=["pick up"]
)
Tile(
    "b",
    text="a box",
    description="a box. You wonder what is inside. And if it is trapped",
    action=["force open", "check for traps"]
)
Tile(
    "s",
    text="a shop",
    descriptoin="a shop of a friendly merchant",
    action=["go shopping"]
)

#print(" - - - -  tiles - - - - ")
#for tile in Tile.tiledict.keys():
#    Tile.tiledict[tile].showStats()


class Level(object):
    """the Level object is created with a map string and has elegant methods
    to get an specific tile (at position x,y) or set an specific tile or
    to return the whole level"""

    def __init__(self, level):
        self.level_map = list(map(list, level.split()))

    def __getitem__(self, xy):
        """get the char at position x,y (x,y start with 0)"""
        x, y = xy
        return self.level_map[y][x]  # row, col

    def __setitem__(self, xy, item):
        """ x (col) and y (row) position of char to set. (x and y start with 0)"""
        x, y = xy
        self.level_map[y][x] = item  # row, col

    def __iter__(self):
        """iterating over the lines of the level"""
        return ("".join(row) for row in self.level_map)

    def __str__(self):
        """calling __iter__ (row for row) to produce one big output string"""
        return "\n".join(row for row in self)


def main():
    """ a demo to move the player in an ascii level map"""
    #print(' the "raw" level without player and monsters')
    #print(rawlevel)
    #print( " now the player comes into the level at pos row 9 col 9")
    firstlevel = Level(rawlevel)  # creating the level from raw file
    # coordinates of player (x,y)
    pcol = 8
    prow = 8
    # saving the original tile so that we can draw it again later or the player will become a snake and pollute the level
    original = firstlevel[pcol, prow]  # saving the tile where the player will soon be
    firstlevel[pcol, prow] = "@"  # set the player to this coordinate
    print(firstlevel)  # first time printing
    firstlevel[pcol, prow] = original  # clean up after printing, restore the original tile at player position
    showtext = True  # for inside the while loop
    while True:  # game loop
        # output situation text
        postext = "You (@) are at position %i, %i on %s. press:" % (
            pcol, prow, Tile.tiledict[original].text
        )
        actions = Tile.tiledict[original].action  # get the actionlist for this tile
        if len(actions) == 0:
            actiontext = ""
        else:
            actiontext = "for action: a and ENTER\n"
        # input
        inputtext = "to move: numpad 8426 or nwso and ENTER\n" \
                  "%sto get more a more detailed description: d and ENTER\nto quit: q and ENTER] :" % actiontext
        if showtext:  # avoid printing the whole text again for certain answers (action, description etc.)
            print(postext)
            print(inputtext)
        i = input(">")
        i = i.lower()
        if "q" in i:
            break
        elif i == "4" or i == "w":
            if Tile.tiledict[firstlevel[pcol - 1, prow]].stepin:
                pcol -= 1
            else:
                print(
                    "Bad idea! you can not walk into %s" %
                    Tile.tiledict[firstlevel[pcol - 1, prow]].text
                )
                showtext = False
                continue
        elif i == "6" or i == "e":
            if Tile.tiledict[firstlevel[pcol + 1, prow]].stepin:
                pcol += 1
            else:
                print(
                    "Bad idea! you can not walk into %s" %
                    Tile.tiledict[firstlevel[pcol + 1, prow]].text
                )
                showtext = False
                continue
        elif i == "8" or i == "n":
            if Tile.tiledict[firstlevel[pcol, prow - 1]].stepin:
                prow -= 1  # y goes from top to down
            else:
                print(
                    "Bad idea! you can not walk into %s" %
                    Tile.tiledict[firstlevel[pcol, prow - 1]].text
                )
                showtext = False
                continue
        elif i == "2" or i == "s":
            if Tile.tiledict[firstlevel[pcol, prow + 1]].stepin:
                prow += 1
            else:
                print(
                    "Bad idea! you can not walk into %s" %
                    Tile.tiledict[firstlevel[pcol - 1, prow + 1]].text
                )
                showtext = False
                continue
        elif i == "d":
            showtext = False
            print("--------- more detailed description -------")
            print("This is", Tile.tiledict[original].description)
            print("------ ----- -------- --------- -----------")
            continue  # go to the top of the while loop
        elif len(actions) > 0 and i == "a":
            showtext = False
            print(
                "Those are the possible actions (not yet coded, you can only look at it:)"
            )
            print("------ list of possible actions -------")
            for action in actions:
                print(actions.index(action), action)
            print("------ ----- -------- --------- -------")
            continue  # go to the top of the while loop
        else:
            print("please enter q for quit or 8426 or nwso for directions")
            continue
        showtext = True
        original = firstlevel[pcol, prow]  # saving the original tile ( __getitem__ )
        #print("original:", original)
        firstlevel[pcol, prow] = "@"  # set new player positionxy ( __setitem__ )
        # output level
        print(firstlevel)
        # replace player position with the original tile
        firstlevel[pcol, prow] = original


if __name__ == '__main__':
    main()
