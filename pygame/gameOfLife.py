# Game of Life (was: Pygame Cheat Sheet)
# This program simulate the classic Conway'S Game of Life
# see http://en.wikipedia.org/wiki/Conway's_Game_of_Life
# pygame cheatsheet by Al Sweigart http://inventwithpython.com
# game by Horst JENS http://ThePythonGameBook
# bug hunting & making thinks work by yipyip
# license: gpl, see http://www.gnu.org/licenses/gpl.html


import pygame
import sys
import random

#from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Conway's Game of Life")

msg = "Conway's Game of Life"
fontObj = pygame.font.Font("freesansbold.ttf", 32)
msg2 = "right click: toggle pause mode. left click while in pause mode: paint"
fontObj2 = pygame.font.Font("freesansbold.ttf", 14)

screen.fill((255,255,255)) # white
ymove = 50 # move playfield down to have room for text



cellA = {} # the playfield
#cellB = {}
#cellC = {}

maxX = 150 # maximum lenght of x dimension
maxY = 100 # maximum lenght of y dimension

# write text on screen
msgSurfaceObj = fontObj.render(msg, False, (0,0,255)) # blue
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.topleft = (10, 10)
screen.blit(msgSurfaceObj, msgRectobj)

helpTextObj = fontObj2.render(msg2, False, (0,0,255))
msgRectobj2 = helpTextObj.get_rect()
msgRectobj2.topleft = (10, ymove + maxY*4 + 10)
screen.blit(helpTextObj, msgRectobj2)

# pxSurfaceObj = pygame.surface.Surface((maxX, maxY))

#create 100 x 100 cells
# with random value
for x in range(maxX):    
    for y in range(maxY):
        cellA[x, y] = 0 # clean all

# make a copy of cellA
#cellB = cellA.copy() # full copy of clean
#cellC = cellA.copy() # a clean copy

for x in range(maxX):
    for x in range(maxX):
        for y in range(maxY):
            cellA[x, y] = random.choice([0,0,0,0,0,0,0,0,1]) # random pattern



# fill some random values in cella

def checkcell(c, x, y, direction):
    """check a neighboring cell and return it's value
       assuming a 100x100 playfield with wrap-around
       borders"""
    dx=0 # delta to calculate next cell
    dy=0 
    if direction == 0: # east
        if x == 0: 
            dx = maxX-1 
        else:
            dx = -1
    elif direction ==4: #west:
        if x == maxX-1:
            dx = -1 * (maxX-1)
        else:
            dx = 1
    elif direction ==2: # north
        if y ==0:
            dy = maxY-1
        else: dy = -1
    elif direction ==6: # south
        if y ==maxY-1:
            dy = -1 * (maxY - 1)
        else:
            dy = 1
    elif direction == 1: # northeast
        if y ==0:
            dy = maxY-1
        else: dy = -1
        if x == 0: 
            dx = maxX-1 
        else:
            dx = -1
    elif direction == 3: # northwest
        if y ==0:
            dy = maxY-1
        else: 
            dy = -1
        if x == maxX-1:
            dx = -1 * (maxX-1)
        else:
            dx = 1
    elif direction == 5: #southwest
        if x == maxX-1:
            dx = -1 * (maxX-1)
        else:
            dx = 1
        if y ==maxY-1:
            dy = -1 * (maxY - 1)
        else:
            dy = 1
    elif direction == 7: # southeast
        if x == 0: 
            dx = maxX-1 
        else:
            dx = -1
        if y ==maxY-1:
            dy = -1 * (maxY - 1)
        else:
            dy = 1
    else:
        print "wtf???"
    return c[x+dx, y+dy]

def paint(cells ):
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    #print "x,y:", x,y
    if ( x < maxX*4 and 
         y < maxY*4 + ymove and
         y > ymove):
       #print x/4, (y-ymove)/4
       cells[x/4, (y-ymove)/4] = 1
    
        
def newvalue(ca, cb, x, y):
    """count the neighbors of a cell (8 directions). If too few or
    too many neighbors, the cell dies., else it become or stay alife.
    rules: 
    0 or 1 neigbors: cell dies because of underpopulation
    2 or 3 neigbors: cell stay alive
    4 or more cells: cell dies because of overpopulation
    3 neignors and cell dead: cell becomes alive.
    Returns 0 for a dead cell, 1 for an alive cell
    also see http://en.wikipedia.org/wiki/Conway's_Game_of_Life"""
    neighbors = 0
    for direction in range(8):
        neighbors += checkcell(ca, x,y,direction)
    # cell is dead and become alive ?
    if ca[x, y] == 0:
        if neighbors == 3:
            cb[x, y] = 1 # born again
            return 1
        else:
            cb[x, y] = 0 # stay dead
            return 0
    else:
        # cell is alive
        if neighbors < 2 or neighbors > 3:
            cb[x, y] = 0 # dead 
            return 0
        else:
            # stay alivie
            cb[x, y] = 1
            return 1
        
       


gameloop = True
old_cells = cellA
new_cells = {}
mousepainting = False
pause = False
while gameloop:

    if not pause:
        cellsum = 0
        # calculate cells birth and dead
        for x in range(maxX):
            for y in range(maxY):
                # cellsum is the number of alive cells in the whole playfield
                # in this frame
                cellsum += newvalue(old_cells, new_cells, x, y) # calculate values of CellB
    
    else:
        if mousepainting:
           paint(old_cells) 
    
    # paint the cells on the screen       
    for x in range(maxX):
        for y in range(maxY):
            color = pygame.Color(old_cells[x, y] * 255,0,0) # red or black
            ## paint 4 x 4 dots instead of 1 dot (fatx, faty) is the size of a dot
            pygame.draw.rect(screen, color, (x*4,ymove+y*4, 4,4), 0)
    
    if not pause:        
        old_cells  = new_cells
        new_cells = {}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameloop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                if pause:
                   mousepainting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button ==3: # right click
                pause = not pause # toggle
            if event.button ==1: # left click 
                if pause:
                   mousepainting = False
    
  
    if not pause:    
        statusmsg =  'Game of Life fps: %.2f cells:%i:%i' % (fpsClock.get_fps(), cellsum, 10000-cellsum)       
    else: 
        statusmsg = " pause mode. right-click to continue"
    pygame.display.set_caption(statusmsg)
    pygame.display.update()
    #pygame.display.flip()
    fpsClock.tick(30) # pause to run the loop at 30 frames per second

pygame.quit()
sys.exit()
