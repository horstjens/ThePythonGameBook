# pycrawl_walkdemo
# my very own rogulike game
# because i play far too much dungeon crawl stone soup
# 2012 by Horst JENS   horstjens@gmail.com
# license: gpl3 see http://www.gnu.org/copyleft/gpl.html
# this game is a part of http://ThePythonGameBook.com

# this is a demo where the player (p) runs around in some small rooms.
# each tile (block) where the player stands is saved and drawn again as soon as the player moves away

# 3 x 3 roooms with 8 x 8 tiles
ROOMROOT = 3
BLOCKROOT = 6
level = "XXXXXXXXXXXXXXXXXX"+ \
        "X.l..##....dd.m..X"+ \
        "X...m##>...##..m.X"+ \
        "Xtb.m##t..l##...>X"+ \
        "X.<..dd....ddm.t.X"+ \
        "########d#d#######"+ \
        "########d#d#######"+ \
        "X...>##....##....X"+ \
        "X....dd....ddt.<.X"+ \
        "X...mdd...m##....X"+ \
        "X....##.m..##....X"+ \
        "####d#########d###"+ \
        "####d#########d###"+ \
        "X....##..m.##...lX"+ \
        "Xmmb.dd<m..dd...mX"+ \
        "X....##..m.##....X"+ \
        "X.t..##m...##...mX"+ \
        "XXXXXXXXXXXXXXXXXX"


#level = 18 x 18
# i assume the player (p) is standing on an empty block (.)
#playerpos = [10,9] # row, col
prow = 9 # start with 0 !
pcol = 8

# make a xy matrix out of level
blocks={}
for y in list(range(18)):
    for x in list(range(18)):
        blocks[(y,x)] = level[18*y+x:18*y+x+1]
        print(y,x,blocks[y,x])
#print(blocks)

#tmpblock = blocks[(prow,pcol)]

#create screenstring
def calcscreen(paintplayer=True):
    screen = ""
    for y in list(range(18)):
        for x in list(range(18)):
            if x == pcol and y == prow:
                if paintplayer:
                    screen += "p"
                else:
                    screen += blocks[(y,x)]
            else:
                screen += blocks[(y,x)]
        screen+= "\n"
    return screen



# ---------- play 10 moves -----------
print(calcscreen())
moves = 0
while moves < 10:
    print("----------move: %i---------------" % moves)
    
    dx = input("delta x (-1,0,1):")
    dy = input("delta y (-1,0,1):")
    
    prow += int(dy)
    pcol += int(dx)
    screen = calcscreen()
    
    print(screen)
    moves += 1
    
    
#-------------yipyip-----------

"""
How to manage an ascii level map.

Tested with Python 2.6, 3.2.
"""


raw_level =\
"""\
######
#....#
#....#
######\
"""

class Level(object):

    def __init__(self, level):
        self.level_map = list(map(list, level.split()))


    def __getitem__(self, xy):
        x, y = xy
        return self.level_map[y][x]


    def __setitem__(self, xy, item):
        x, y = xy
        self.level_map[y][x] = item


    def __iter__(self):
        return ("".join(row) for row in self.level_map)


    def __str__(self):
        return "\n".join(row for row in self)


def main():

    print('___')
    print(raw_level)
    print( '~~~')

    alevel = Level(raw_level)
    print("alevel")
    print(alevel)
    print()
    print("alevel rows and setitem")
    alevel[1,2] = "?"
    for row in alevel:
        print(row)

if __name__ == '__main__':
    main()

