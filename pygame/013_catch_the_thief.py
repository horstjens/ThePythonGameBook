#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
013_catch_the_thief.py
a game without pygame sprites
url: http://thepythongamebook.com/en:part2:pygame:step013
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

The player(s) can control the Pygame snake (with cursor keys) and the
Tux bird (with the mouse). A blue police icon moves toward the middle
distance between snake and bird (indicated by a cross).
Your task is to catch the thief (red triangle) with the blue police circle.
The thief moves by random. You have only a short period of time. For each 
millisecond where the police circle touches the thief triangle, you get points.

Loading  images and sounds from a subfolder called 'data'
The subfolder must be inside the same folder as the program itself. 

works with pyhton3.4 and python2.7
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

import pygame
import os
import random

# ------ a class to store global variables
class Config(object):
    """place to store some variables so that every function can access them
       also a good place to start modding the game"""
    # some class attributes:
    screenwidth = 1024                    # screen resolution
    screenheight = 600
    thiefx, thiefy = 50,50                # start position of thief
    thiefdx = random.randint(-150,150)    # speed of thief
    thiefdy = random.randint(-150,150)
    thiefmaxspeed = 200                   # max speed of thief
    erratic = 1                           # possible change +/- of thief speed
    policex, policey = 250, 240           # start position of police 
    policedx, policedy  = 0, 0            # police speed in pixel per second !
    birdx, birdy = 100,100                # start position of bird
    birddx, birddy = 0,0                  # start speed of bird
    snakex, snakey = 200,200              # start position of snake
    snakedx, snakedy = 0,0                # start speed of snake
    crossx, crossy = 150,150              # start position of cross

# ------- some functions for later use ----------

def intro(screen):
    """draw game instructions and wait for mouseclick"""
    screen.fill((255,255,255))
    #pygame.draw.rect(background, (200,200,200), ((0,0), (470,110)))
    #pygame.draw.rect(background, (200,200,200), ((screen.get_width()-360, 
    #                 screen.get_height()-25), (360,25)))
    
    screen.blit(write("Catch the hief - INSTRUCTIONS", (0,0,255), 64), (80, 15))    
    screen.blit(write("control the snake with the cursor keys or WASD (Enter or LCTRLto stop)"),(10,70))
    screen.blit(write("control the bird with the mouse (left button to stop)"), (10,90))
    screen.blit(write("the cross is always in the middle between snake and bird"), (10,110))
    screen.blit(write("the blue circle (police) moves toward the cross"),(10,130))
    screen.blit(write("catch the red triangle (the thief) with the blue circle to win points"),(10,150))
    screen.blit(write("click the left mouse button to start"),(50,290))
    pygame.display.flip()
        
    while True:
        for event in pygame.event.get():
            pass # do nothing but pull all events
        if pygame.mouse.get_pressed()[0]: # mouse button pressed
                return  # escape this function
            
    
def write(msg="pygame is cool", colour=(0,0,0), fontsize=24):
    """returns a surface with text"""
    myfont = pygame.font.SysFont("None", fontsize)
    mytext = myfont.render(msg, True, colour)
    mytext = mytext.convert_alpha()
    return mytext


def draw(sprite, x, y):
    """blit a sprite at position x, y"""
    Config.screen.blit(sprite, (round(x,0) - sprite.get_width()/2,
                         round(y,0) - sprite.get_height()/2)) 
def bounce(sprite, x, y, dx, dy):
    """bounce sprite if it touches the screen borders"""
    if x - sprite.get_width()/2 < 0:
        x =  sprite.get_width()/2
        dx *= -1 
    elif x + sprite.get_width()/2 > Config.screenwidth:
        x = Config.screenwidth - sprite.get_width()/2
        dx *= -1
    if y - sprite.get_height()/2 < 0:
        y = sprite.get_height()/2
        dy *= -1
    elif y + sprite.get_height()/2 > Config.screenheight:
        y = Config.screenheight - sprite.get_height()/2
        dy *= -1
    return x,y,dx,dy
    
def randomcolour():
    """returns a random colour tuple (red,green,blue)"""
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def arrow(sprite, dx, dy):
    midx = sprite.get_width() /2
    midy = sprite.get_height() /2
    
    return sprite


def play_the_game():


    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    try:
        # load graphic files from subfolder 'data'
        background = pygame.image.load(os.path.join("data","wien.jpg"))
        snake = pygame.image.load(os.path.join("data","snake.gif"))
        bird = pygame.image.load(os.path.join("data","babytux.png"))
        # load sound files 
        over = pygame.mixer.Sound(os.path.join('data','time_is_up_game_over.ogg'))
        spring = pygame.mixer.Sound(os.path.join('data', 'spring.wav'))

    except:
        raise(UserWarning, "Unable to find or play the files in the folder 'data' :-( ")


    # ----------- start ---------

    screen=pygame.display.set_mode((1024,600)) # try out larger values and see what happens !
    Config.screen = screen # copy screen into the Config class so that functions can access screen
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    background = background.convert()  # jpg can not have transparency
    Config.background = background # copy background in the Config class so that functions can access background
    snake = snake.convert_alpha()
    bird = bird.convert_alpha()
    police = pygame.Surface((50,50)) 
    pygame.draw.circle(police, (0,0,255), (25,25),25) # blue police
    police.set_colorkey((0,0,0)) # black transparent colour 
    police.blit(write("P", (255,255,255), 48), ((12,10))) # white "P"
    police = police.convert_alpha()        # png image has transparent color 
    cross = pygame.Surface((10,10))
    cross.fill((255,255,255)) # fill white
    pygame.draw.line(cross, (0,0,0), (0,0), (10,10)) # black lines
    pygame.draw.line(cross, (0,0,0), (0,10), (10,0))
    cross.set_colorkey((255,255,255))
    cross = cross.convert_alpha()
    thief = pygame.Surface((26,26))
    thief.set_colorkey((0,0,0))
    pygame.draw.polygon(thief, (255,0,0), [(0,0),(25,0),(12,25)])
    thief.blit(write("T", (0,0,0), 32), ((6,3))) # transparent "T"
    thief = thief.convert_alpha()

    catch_in_last_frame = False
    catch_in_this_frame = False
    intro(screen)
    #pygame.draw.rect(background, (200,200,200), ((0,0), (470,110)))
    pygame.draw.rect(background, (200,200,200), ((screen.get_width()-360, 
                     screen.get_height()-25), (360,25)))

    screen.blit(background, (0,0))     # blit background on screen (overwriting all)
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                     # desired max. framerate in frames per second.       
    playtime = 60.0              # seconds of playtime left
    points = 0.0
    gameOver = False
    gameOverSound = True
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        playtime -= seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
        pygame.display.set_caption("[FPS]: %.2f Snake: dx %i dy %i Bird:"
                                   " dx %i dy %i police: dx %.2f dy %.2f " % 
                                   (clock.get_fps(), Config.snakedx, Config.snakedy,
                                    Config.birddx, Config.birddy, Config.policedx, Config.policedy ))
        if playtime < 0:
            gameOver = True
        # ---------------- clean screen ----------
        screen.blit(background,(0,0)) 
        # --------  detect game over ------------
        if gameOver:
            if gameOverSound:
                over.play()
                gameOverSound = False # play the sound only once
            screen.blit(write("Game Over. %.2f points. Press ESCAPE" % points, (128,0,128), 64), (20,250))
        else:
            screen.blit(write("points: %.2f time left: %.2f seconds" % (points, playtime)), 
                       (screen.get_width()-350,screen.get_height()-20))
            # ----- compute movement ----
            # ---- mouse ---
            #(Config.birdx, Config.birdy) = pygame.mouse.get_pos()
            (mousex, mousey) = pygame.mouse.get_pos()
            if mousex < Config.birdx:
                Config.birddx -= 1
            elif mousex > Config.birdx:
                Config.birddx += 1
            if mousey < Config.birdy:
                Config.birddy -= 1
            elif mousey > Config.birdy:
                Config.birddy += 1
            if pygame.mouse.get_pressed()[0] == True:
                Config.birddx = 0 # stop movement by mouseclick (left button)
                Config.birddy = 0
            # ---- keyboard ------
            # cursor keys or wasd
            pressedkeys = pygame.key.get_pressed() # all keys that are pressed now
            if pressedkeys[pygame.K_LEFT] or pressedkeys[pygame.K_a]:
                Config.snakedx -= 1
            if pressedkeys[pygame.K_RIGHT] or pressedkeys[pygame.K_d]:
                Config.snakedx += 1
            if pressedkeys[pygame.K_UP] or pressedkeys[pygame.K_w]:
                Config.snakedy -= 1
            if pressedkeys[pygame.K_DOWN] or pressedkeys[pygame.K_s]:
                Config.snakedy += 1
            if pressedkeys[pygame.K_RETURN] or pressedkeys[pygame.K_LCTRL]:
                Config.snakedx = 0 # stop movement by pressing the 's' key
                Config.snakedy = 0
            # ------------ compute movement ----------------
            Config.crossx = min(Config.birdx,Config.snakex) + ( max(Config.birdx, Config.snakex) -  # cross is in the middle of bird and snake 
                     min(Config.birdx,Config.snakex)) / 2.0 -cross.get_width()/2
            Config.crossy = min(Config.birdy,Config.snakey) + ( max(Config.birdy, Config.snakey) - 
                     min(Config.birdy,Config.snakey)) / 2.0 - cross.get_height()/2
            if Config.crossx < Config.policex:
                Config.policedx -= 1        # police moves toward cross
            elif Config.crossx > Config.policex:
                Config.policedx += 1
            if Config.crossy > Config.policey:
                Config.policedy += 1
            elif Config.crossy < Config.policey:
                Config.policedy -= 1
            Config.thiefdx += random.randint( -Config.erratic,Config.erratic )  # thief is erratic
            Config.thiefdy += random.randint( -Config.erratic,Config.erratic )
            Config.thiefdx = max(Config.thiefdx, -Config.thiefmaxspeed)         # limit speed of thief
            Config.thiefdx = min(Config.thiefdx, Config.thiefmaxspeed)
            Config.thiefdy = max(Config.thiefdy, -Config.thiefmaxspeed)
            Config.thiefdy = min(Config.thiefdy, Config.thiefmaxspeed)
            # ---- friction... sprites get slower ----
            Config.policedx *= 0.995
            Config.policedy *= 0.995
            Config.snakedx *= 0.995
            Config.snakedy *= 0.995
            Config.birddx *= 0.995
            Config.birddy *= 0.995
            # --------- new position -----------
            Config.policex += Config.policedx * seconds 
            Config.policey += Config.policedy * seconds
            Config.birdx += Config.birddx * seconds
            Config.birdy += Config.birddy * seconds
            Config.snakex += Config.snakedx * seconds
            Config.snakey += Config.snakedy * seconds
            Config.thiefx += Config.thiefdx * seconds
            Config.thiefy += Config.thiefdy * seconds
            # ----------- bounce ----------
            Config.policex, Config.policey, Config.policedx, Config.policedy = bounce(police, Config.policex, Config.policey, Config.policedx, Config.policedy)
            Config.birdx, Config.birdy, Config.birddx, Config.birddy = bounce(bird, Config.birdx, Config.birdy, Config.birddx, Config.birddy)
            Config.snakex, Config.snakey, Config.snakedx, Config.snakedy = bounce(snake, Config.snakex, Config.snakey, Config.snakedx, Config.snakedy)
            Config.thiefx, Config.thiefy, Config.thiefdx, Config.thiefdy = bounce(thief, Config.thiefx, Config.thiefy, Config.thiefdx, Config.thiefdy)
            # --- police got thief ? collision detection -----
            distx =  max(Config.policex + police.get_width()/2 , Config.thiefx + 
                     thief.get_width()/2) - min(Config.policex + 
                     police.get_width()/2, Config.thiefx + thief.get_width()/2)
            disty =  max(Config.policey + police.get_height()/2 , Config.thiefy + 
                     thief.get_height()/2) - min(Config.policey + police.get_width()/2,
                     Config.thiefy + thief.get_width()/2)
            catch_in_last_frame = catch_in_this_frame # save old catch info
            catch_in_this_frame = False
            if (distx < police.get_width() /2) and (disty < police.get_height()/2):
                catch_in_this_frame = True
                points += seconds
                screen.fill(randomcolour()) 
                if not pygame.mixer.get_busy():
                    spring.play() # only play this sound if mixer is silent at the moment
            else:   # no catch this time
                if catch_in_last_frame:
                    screen.blit(background, (0,0)) # restore background
            # ---------- blit ----------------
            draw(bird, Config.birdx, Config.birdy)
            draw(snake, Config.snakex, Config.snakey)
            pygame.draw.line(screen, randomcolour(), (Config.snakex,Config.snakey), (Config.birdx, Config.birdy), 1)
            pygame.draw.line(screen, randomcolour(), (Config.crossx,Config.crossy), (Config.policex, Config.policey) ,1)
            draw(police, Config.policex, Config.policey)
            draw(cross, Config.crossx, Config.crossy)
            draw(thief, Config.thiefx, Config.thiefy)
        pygame.display.flip()          # flip the screen FPS times a second    
    pygame.quit()
# check if the program is imported. if not, start it directly
if __name__ == "__main__":
    play_the_game()
