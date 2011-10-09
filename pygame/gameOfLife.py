# Game of Life (was: Pygame Cheat Sheet)
# This program simulate the classic Conway'S Game of Life
# see http://en.wikipedia.org/wiki/Conway's_Game_of_Life
# cheatsheet by Al Sweigart http://inventwithpython.com
# game by Horst JENS http://ThePythonGameBook
# license: gpl


import pygame
import sys
import random

#from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Game of Life')

redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
mousex, mousey = 0, 0
msg = "Conway's Game of Life"
#try:
    #cat = os.path.join("data",'babytux.png')
    #font = os.path.join("data", 'freesansbold.ttf')
    #sound = os.path.join("data",'beep.ogg')
#except:
    # does not raise alert if file does not exist ! TODO: fix
#    raise UserWarning, "could not found files inside subfolder data"
    
#catSurfaceObj = pygame.image.load(cat)
fontObj = pygame.font.Font("freesansbold.ttf", 32)
#soundObj = pygame.mixer.Sound(sound)

screen.fill(whiteColor)

msgSurfaceObj = fontObj.render(msg, False, blueColor)
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.topleft = (10, 10)
screen.blit(msgSurfaceObj, msgRectobj)


cell = {} # the playfield

#create 100 x 100 cells
# with random value
for x in range(100):
    cell[x] = {}    
    for y in range(100):
        cell[x][y] = random.choice([0,1])


def checkcell(x,y, direction):
    """check a neighboring cell and return it's value
       assuming a 100x100 playfield with wrap-around
       borders"""
    dx=0 # delta to calculate next cell
    dy=0 
    if direction == 0: # east
        if x == 0: 
            dx = 99 
        else:
            dx = -1
    elif direction ==4: #west:
        if x == 99:
            dx = -99
        else:
            dx = 1
    elif direction ==2: # north
        if y ==0:
            dy = 99
        else: dy = -1
    elif direction ==6: # south
        if y ==99:
            dy = -99
        else:
            dy = 1
    elif direction == 1: # northeast
        if y ==0:
            dy = 99
        else: dy = -1
        if x == 0: 
            dx = 99 
        else:
            dx = -1
    elif direction == 3: # northwest
        if y ==0:
            dy = 99
        else:
            dy = -1
        if x == 99:
            dx = -99
        else:
            dx = 1
    elif direction == 5: #southwest
        if x == 99:
            dx = -99
        else:
            dx = 1
        if y ==99:
            dy = -99
        else:
            dy = 1
    elif direction == 7: # southeast
        if x == 0: 
            dx = 99 
        else:
            dx = -1
        if y ==99:
            dy = -99
        else:
            dy = 1
    else:
        print "wtf???"
    return cell[x+dx][y+dy]
        
def newvalue(x,y):
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
        neighbors += checkcell(x,y,direction)
    # cell is dead and become alive ?
    if cell[x][y] == 0:
        if neighbors == 3:
            cell[x][y] = 1 # born again
            return 1
        else:
            return 0
    else:
        if neighbors < 2 or neighbors > 3:
            cell[x][y] = 0 # dead 
            return 0
        else:
            # stay alivie
            return 1
        
       
ymove = 50

gameloop = True
while gameloop:

    cellsum = 0
    # calculate cells birth and dead
    for x in range(100):
        for y in range(100):
            cellsum += newvalue(x,y)

    # paint cells (each a 4x4 dot) on the screen
    pixArr = pygame.PixelArray(screen)
    
    for x in range(100):
        for y in range(100):
            color = pygame.Color(cell[x][y] * 255,0,0)
            # paint 4 x 4 dots instead of 1 dot (fatx, faty) is the size of a dot
            for fatx in range(4):
                for faty in range(4):
                    pixArr[x*4+fatx][ymove+y*4+faty] = color # left0 upper0
    del pixArr # you must delete the pixarry object to unlock the surface
    


    #screen.blit(catSurfaceObj, (mousex, mousey))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameloop = False
    pygame.display.set_caption('Game of Life fps: %.2f cells:%i:%i' % (fpsClock.get_fps(), cellsum, 10000-cellsum))
    pygame.display.update()
    #pygame.display.flip()
    fpsClock.tick(30) # pause to run the loop at 30 frames per second
# quit the game
#pygame.event.post(pygame.event.Event(pygame.QUIT))
pygame.quit()
sys.exit()
