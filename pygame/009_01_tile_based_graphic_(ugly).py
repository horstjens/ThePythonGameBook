#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
009_01_tile_based_graphic_(ugly).py
tile based graphic 
url: http://thepythongamebook.com/en:part2:pygame:step009
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html
 
maze game without pygame sprites and tile-based graphic,
no external files necessary
 
escape the maze by pressing the cursor keys
this program has some bugs, like that the ball can move throug a block sometimes
"""   
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

def mazegame():
 
    import pygame
    import random
 
    pygame.init()
    screen=pygame.display.set_mode((640,480)) 
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((255,255,255)) # fill white
    background = background.convert()
    background0 = background.copy()
    screen.blit(background,(0,0))
 
    ballsurface = pygame.Surface((10,10))
    ballsurface.set_colorkey((0,0,0)) # black transparent
    pygame.draw.circle(ballsurface,(255,0,0),(5,5),5) # red ball
    ballsurface = ballsurface.convert_alpha()
    ballrect = ballsurface.get_rect()
 
    dx = 0 # delta x ... x moving vector of ball surface
    dy = 0 # delta y ... y moving vector of ball surface
 
    # -------------------- maze ----------------
    # s...startposition of ball
    # n...next level
    # p...previous level
    # r...random level
    # e...end (game won)
    # x...wall 
 
    #syntax: levelname = ["firstline", "secondline",..]
 
    #startlevel: 24 x 15
    startlevel = ["xxx.xxxxxxxxxxxxxxxxxx",
                  ".s.....x..............",
                  "xxxx.........xx......x",
                  "x......x....x.x......x",
                  "x......x......x......x",
                  "x......x......x......x",
                  "x...xxxxxx....x......x",
                  "x......x.............x",
                  "x......x......xxxxxxxx",
                  "xxxxxx.x.............x",
                  "x......x.............x",
                  "x......x.............x",
                  "x..........xxxx...xxxx",
                  "x..........x.........x",
                  "xxxxxxxxxxxxxxxxx.xxnx"]
    # middlelevel = 15 x 16
    middlelevel =  ["xxxxxxxxxxxxxxx",
                    "xs............x",
                    "x.........x...x",
                    "x.........x...x",
                    "x......x..x...x",
                    "x.....x...x...x",
                    "x..p.xxxxxx...x",
                    "x.....x.......x",
                    "x.x....x......x",
                    "x.x...........x",                   
                    "x.x...x.......x",
                    "x.x....x......x",
                    "x.xxxxxxx..n..x",
                    "x......x......x",
                    "x.....x.......x",
                    "xxxxxxxxxxxxxxx"]
    # smilelevel: 32 x 18
    winlevel = ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "xs.............................x",
                "x..............................x",
                "x..............................x",
                "x............xxx....xxx........x",
                "x...........xx.xx..xx.xx.......x",
                "x............xxx....xxx........x",
                "x..............................x",
                "x................x.............x",
                "x................x.............x",
                "x................x.............x",
                "x..............................x",
                "x................r.............x",
                "x............xx....xxx.........x",
                "x.............xxxxxxx..........x",
                "x..............................x",
                "x..............................x",
                "xxxxxxpxxxxxxxxxxxnxxxxxxxxxxxex"]
 
 
    def createblock(length, height, color):
        tmpblock = pygame.Surface((length, height))
        tmpblock.fill(color)
        tmpblock.convert()
        return tmpblock
 
    def addlevel(level):
        """this function read the layout of the level dictionary
           and blit it to the screen.
           recalculate and return variables like block, height etc.
           usage:
 
           length, height, block, goal, ballx, bally, background = addlevel(newlevel)
        """
 
        lines = len(level)
        columns = len(level[0])
 
        length = screenrect.width / columns
        height = screenrect.height / lines
 
        wallblock = createblock(length, height,(20,0,50))
        nextblock = createblock(length, height,(255,50,50))
        prevblock = createblock(length, height,(255,50,255))
        endblock  = createblock(length, height,(100,100,100))
        randomblock = createblock(length, height,(0,0,200))
 
        background = background0.copy()
 
        for y in range(lines):
            for x in range(columns):
                if level[y][x] == "x": # wall
                    background.blit(wallblock, (length * x, height * y))
                elif level[y][x] == "n": # next level
                    background.blit(nextblock, (length * x, height * y))
                elif level[y][x] == "p": # previous level
                    background.blit(prevblock, (length * x, height * y))
                elif level[y][x] == "r": # random level
                    background.blit(randomblock, (length*x, height * y))
                elif level[y][x] == "e": # end block
                    background.blit(endblock,  (length * x, height * y))
                elif level[y][x] == "s": #start
                    ballx = length * x
                    bally = height * y
        screen.blit(background0, (0,0))
 
        return length, height, ballx, bally , lines, columns, background
 
    # a list holding all levels
    all_levels = [startlevel, middlelevel, winlevel]  
    max_levels = len(all_levels)        
    my_maze = all_levels[0] # start with the first level
    length, height,  ballx, bally, lines, columns, background = addlevel(my_maze)
    # ------------------- maze --------------------------
 
 
    clock = pygame.time.Clock() #create pygame clock object
    mainloop = True
    FPS = 60         # desired max. framerate in frames per second. 
    playtime = 0
 
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False 
                if event.key == pygame.K_UP:
                    dy -= 1 
                if event.key == pygame.K_DOWN:
                    dy += 1
                if event.key == pygame.K_RIGHT:
                    dx += 1
                if event.key == pygame.K_LEFT:
                    dx -= 1
        pygame.display.set_caption("[FPS]: %.2f dx: %i dy %i press cursor keys to move ball" % (clock.get_fps(), dx, dy))
        screen.blit(background, (0,0)) # delete all
        # ---------find out probing point of ball surface
        if dx > 0:
            pointx = ballx + ballrect.width
        else:
            pointx = ballx
        if dy > 0:
            pointy = bally + ballrect.height
        else:
            pointy = bally
        # ------- find out if ball want to leave screen
        if pointx + dx < 0:
            ballx = 0
            pointx = 0
            dx = 0
        elif pointx + dx > screenrect.width:
            ballx = screenrect.width - ballrect.width
            pointx = screenrect.width - ballrect.width
            dx = 0
        if pointy + dy < 0:
            bally = 0
            pointy = 0
            dy = 0
        elif pointy + dy > screenrect.height:
            bally = screenrect.height - ballrect.height
            pointy = screenrect.height - ballrect.height
            dy = 0
        # ------- find out if probing point is inside wall
        # make sure proing point does not produce out of index error
        y1 = int(pointy/height)
        y1 = max(0,y1) # be never smaller than 0
        y1 = min(y1,lines-1) # be never bigger than lines
        x1 = int((pointx + dx)/length)
        x1 = max(0,x1) # be never smaller than 0
        x1 = min(x1,columns-1) 
        y2 = int((pointy+dy)/height)
        y2 = max(0,y2)
        y2 = min(y2,lines-1)
        # -------------- check the type of tile where the ball is ------
        if my_maze[y1][x1] == "x":
            dx = 0
        else:
            ballx += dx
        if my_maze[y2][x1] == "x":
            dy = 0
        else:
            bally += dy
        # ---------------move ball surface
        screen.blit(ballsurface, (ballx, bally))
        # -------------- check special tile
        bline = int(bally / height) # a line where ball is currently
        bcolumn = int(ballx / length) # column where ball is currently
        if my_maze[bline][bcolumn] == "n":
           actual = all_levels.index(my_maze)
           # cycle forward
           my_maze = all_levels[(actual + 1) % max_levels]
           length, height,  ballx, bally,  lines, columns,background = addlevel(my_maze)
        elif my_maze[bline][bcolumn] == "p":           
            actual = all_levels.index(my_maze)
            # cycle backward
            my_maze = all_levels[(max_levels + actual - 1) % max_levels]
            length, height,  ballx, bally,  lines, columns,background = addlevel(my_maze)
        elif my_maze[bline][bcolumn] == "r":
            my_maze = random.choice(all_levels)
            length, height,  ballx, bally,  lines, columns,background = addlevel(my_maze)
        elif my_maze[bline][bcolumn] == "e":
            # game won, exit mainloop
            print("---*** congratulation, you escaped the maze ! ***-------")
            mainloop = False
        pygame.display.flip() # flip the screen 30 times a second
    print("This maze game was played for {:.2f} seconds".format(playtime))
if __name__ == "__main__":
    mazegame()
