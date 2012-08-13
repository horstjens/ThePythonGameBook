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
rawlevel ="""\
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
X....##..m.##....X
X.t..##m...##...mX
XXXXXXXXXXXXXXXXXX\
"""

    



class Level(object):

    def __init__(self, level):
        self.level_map = list(map(list, level.split()))

    def __getitem__(self, xy):
        x, y = xy
        return self.level_map[y][x] # row, col 

    def __setitem__(self, xy, item):
        """ x (col) and y (row) position of item (block) to set. x and y start with 0"""
        x, y = xy
        self.level_map[y][x] = item # row, col

    def __iter__(self):
        return ("".join(row) for row in self.level_map)

    def __str__(self):
        return "\n".join(row for row in self)


def main():
    """ a demo to move the player in an ascii level map"""
    print(' the "raw" level without player and monsters')
    #print(rawlevel)
    print( " now the player comes into the level at pos row 9 col 9")

    firstlevel = Level(rawlevel)
    #screen = firstlevel[:]
    
    # coordinates of player (x,y)
    pcol = 8
    prow = 8
    
    firstlevel[pcol,prow] = "@" # set the player to this coordinate
    # iterating lines over the Level obect
    #for row in firstlevel:
    #    print(row)
    # output with __str__
    while True:
        print(firstlevel)
        i = input("move player [press numpad keys 8426 or nwso or q for quit and ENTER] :")
        i = i.lower()
        if "q" in i:
            break
        elif not i in "8426nwso":
            print("please enter q for quit or 8426 or nwso for directions")
            continue
        elif i == "4" or i =="w":
            pcol -= 1
        elif i  =="6" or i =="e":
            pcol += 1
        elif i == "8" or i =="n":
            prow -= 1 # y goes from top to down
        elif i == "2" or i =="s":
            prow += 1
        print("pcol:",pcol, "prow:",prow)
        firstlevel[pcol, prow] = "@" # set new player positionxy

if __name__ == '__main__':
    main()

