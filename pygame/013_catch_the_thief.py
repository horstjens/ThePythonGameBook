# -*- coding: utf-8 -*-
"""
part2step013-catch-the-thief.py

Loading  images and sounds from a subfolder called 'data'
The subfolder must be inside the same folder as the program itself. 
The player(s) can control the Pygame snake (with cursor keys) and the
Tux bird (with the mouse). A blue police icon moves toward the middle
distance between snake and bird (indicated by a cross).
Your task is to catch the thief (red triangle) with the blue police circle.
The thief moves by random. You have only a short period of time. For each 
millisecond where the police circle touches the thief triangle, you get points.

cleanrect function seems to be not perfect. 
"""
def play_the_game():
    import pygame
    import os
    import sys
    import random

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
        sys.exit("Unable to find or play the files in the folder 'data' :-( ")  
    # ------- some functions for later use ----------
    def write(msg="pygame is cool", colour=(0,0,0), fontsize=24):
        """returns a surface with text"""
        myfont = pygame.font.SysFont("None", fontsize)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext
    def cleanblit(sprite,x,y):
        """clean a sprite from the screen, restoring the background"""
        dirtyrect = background.subsurface((round(x - sprite.get_width()/2, 0),
                                           round(y - sprite.get_height()/2,0),
                                           sprite.get_width(), sprite.get_height()))
        screen.blit(dirtyrect, ((round(x - sprite.get_width()/2, 0),
                                round(y - sprite.get_height()/2,0)))) 
    def cleanrect(x1,y1,x2,y2):
        """clean a rect from the screen, restoring the background"""
        startx = max(0,min(x1,x2) -5)
        starty = max(0,min(y1,y2) -5)
        width = min(screen.get_width(), 5 +max(x1,x2) - min(x1,x2))
        height =min(screen.get_height(), 5+ max(y1,y2) - min(y1,y2)) 
        dirtyrect = background.subsurface((startx, starty, width, height))
        screen.blit(dirtyrect, (startx, starty))
    def draw(sprite, x, y):
        """blit a sprite"""
        screen.blit(sprite, (round(x,0) - sprite.get_width()/2,
                             round(y,0) - sprite.get_height()/2)) 
    def bounce(sprite, x, y, dx, dy):
        """bounce sprite if it touches the screen borders"""
        if x - sprite.get_width()/2 < 0:
            x =  sprite.get_width()/2
            dx *= -1 
        elif x + sprite.get_width()/2 > screen.get_width():
            x = screen.get_width() - sprite.get_width()/2
            dx *= -1
        if y - sprite.get_height()/2 < 0:
            y = sprite.get_height()/2
            dy *= -1
        elif y + sprite.get_height()/2 > screen.get_height():
            y = screen.get_height() - sprite.get_height()/2
            dy *= -1
        return x,y,dx,dy
    def randomcolour():
        """returns a random colour tuple (red,green,blue)"""
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    # ----------- start ---------

    screen=pygame.display.set_mode((1024,600)) # try out larger values and see what happens !
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    background = background.convert()  # jpg can not have transparency
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
    thiefx, thiefy = 50,50
    thiefdx, thiefdy = random.randint(-150,150), random.randint(-150,150)
    thiefmaxspeed = 200
    erratic = 3                            # possible change +/- of thief speed
    policex, policey = 250, 240            # start position of police surface
    policedx, policedy  = 0, 0                   # police speed in pixel per second !
    birdx, birdy = 100,100
    birddx, birddy = 0,0
    snakex, snakey = 200,200
    snakedx, snakedy = 0,0
    crossx, crossy = 150,150
    catch_in_last_frame = False
    catch_in_this_frame = False
    pygame.draw.rect(background, (200,200,200), ((0,0), (470,110)))
    pygame.draw.rect(background, (200,200,200), ((screen.get_width()-360, 
                     screen.get_height()-25), (360,25)))
    background.blit(write("control the snake with the cursor keys (Enter to stop)"),(10,10))
    background.blit(write("control the bird with the mouse (left button to stop)"), (10,30))
    background.blit(write("the cross is always in the middle between snake and bird"), (10,50))
    background.blit(write("the blue circle (police) moves toward the cross"),(10,70))
    background.blit(write("catch the red triangle with the blue circle to win points"),(10,90))
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
                                   (clock.get_fps(), snakedx, snakedy,
                                    birddx, birddy, policedx, policedy ))
        if playtime < 0:
            gameOver = True
        if gameOver:
            #background.fill((255,255,255)) # white b
            screen.blit(background,(0,0))
            if gameOverSound:
                over.play()
                gameOverSound = False # play the sound only once
            screen.blit(write("Game Over. %.2f points. Press ESCAPE" % points, (128,0,128), 64), (20,250))
        else:
            #screen.blit(background, (0,0))  # not GameOver
            #-------- clean -----------
            cleanblit(police, policex, policey)
            cleanblit(bird, birdx, birdy)
            cleanblit(snake, snakex, snakey)
            cleanblit(cross, crossx, crossy)
            cleanblit(thief, thiefx, thiefy)
            pygame.draw.rect(screen, (200,200,200), (screen.get_width()-360, 
                     screen.get_height()-25, 360,25))
            cleanrect(policex, policey,crossx,crossy)
            cleanrect(snakex, snakey, birdx, birdy)
            screen.blit(write("points: %.2f time left: %.2f seconds" % (points, playtime)), 
                       (screen.get_width()-350,screen.get_height()-20))
            
            # ----- compute movement ----
            # ---- mouse ---
            #(birdx, birdy) = pygame.mouse.get_pos()
            (mousex, mousey) = pygame.mouse.get_pos()
            if mousex < birdx:
                birddx -= 1
            elif mousex > birdx:
                birddx += 1
            if mousey < birdy:
                birddy -= 1
            elif mousey > birdy:
                birddy += 1
            if pygame.mouse.get_pressed()[0] == True:
                birddx = 0 # stop movement by mouseclick (left button)
                birddy = 0
            # ---- keyboard ------
            pressedkeys = pygame.key.get_pressed() # all keys that are pressed now
            if pressedkeys[pygame.K_LEFT]:
                snakedx -= 1
            if pressedkeys[pygame.K_RIGHT]:
                snakedx += 1
            if pressedkeys[pygame.K_UP]:
                snakedy -= 1
            if pressedkeys[pygame.K_DOWN]:
                snakedy += 1
            if pressedkeys[pygame.K_RETURN]:
                snakedx = 0 # stop movement by pressing the 's' key
                snakedy = 0
            # ------------ AI ----------------
            crossx = min(birdx,snakex) + ( max(birdx, snakex) -  # cross is in the middle of bird and snake 
                     min(birdx,snakex)) / 2.0 -cross.get_width()/2
            crossy = min(birdy,snakey) + ( max(birdy, snakey) - 
                     min(birdy,snakey)) / 2.0 - cross.get_height()/2
            if crossx < policex:
                policedx -= 1        # police moves toward cross
            elif crossx > policex:
                policedx += 1
            if crossy > policey:
                policedy += 1
            elif crossy < policey:
                policedy -= 1
            thiefdx += random.randint( -erratic,erratic )  # thief is erratic
            thiefdy += random.randint( -erratic,erratic )
            thiefdx = max(thiefdx, -thiefmaxspeed)         # limit speed of thief
            thiefdx = min(thiefdx, thiefmaxspeed)
            thiefdy = max(thiefdy, -thiefmaxspeed)
            thiefdy = min(thiefdy, thiefmaxspeed)
            # ---- friction... sprites get slower ----
            policedx *= 0.995
            policedy *= 0.995
            snakedx *= 0.995
            snakedy *= 0.995
            birddx *= 0.995
            birddy *= 0.995
            # --------- new position -----------
            policex += policedx * seconds 
            policey += policedy * seconds
            birdx += birddx * seconds
            birdy += birddy * seconds
            snakex += snakedx * seconds
            snakey += snakedy * seconds
            thiefx += thiefdx * seconds
            thiefy += thiefdy * seconds
            # ----------- bounce ----------
            policex, policey, policedx, policedy = bounce(police, policex, policey, policedx, policedy)
            birdx, birdy, birddx, birddy = bounce(bird, birdx, birdy, birddx, birddy)
            snakex, snakey, snakedx, snakedy = bounce(snake, snakex, snakey, snakedx, snakedy)
            thiefx, thiefy, thiefdx, thiefdy = bounce(thief, thiefx, thiefy, thiefdx, thiefdy)
            # --- police got thief ? -----
            distx =  max(policex + police.get_width()/2 , thiefx + 
                     thief.get_width()/2) - min(policex + 
                     police.get_width()/2, thiefx + thief.get_width()/2)
            disty =  max(policey + police.get_height()/2 , thiefy + 
                     thief.get_height()/2) - min(policey + police.get_width()/2,
                     thiefy + thief.get_width()/2)
            catch_in_last_frame = catch_in_this_frame # save old catch info
            catch_in_this_frame = False
            if (distx < police.get_width() /2) and (disty < police.get_height()/2):
                catch_in_this_frame = True
                points += seconds
                screen.fill(randomcolour()) 
                if not pygame.mixer.get_busy():
                    spring.play() # only play this sound if mixer is silent at the moment
            else:
                # no catch this time
                if catch_in_last_frame:
                    screen.blit(background, (0,0)) # restore background
            # ---------- blit ----------------
            draw(bird, birdx, birdy)
            draw(snake, snakex, snakey)
            pygame.draw.line(screen, randomcolour(), (snakex,snakey), (birdx, birdy), 1)
            pygame.draw.line(screen, randomcolour(), (crossx,crossy), (policex, policey) ,1)
            draw(police, policex, policey)
            draw(cross, crossx, crossy)
            draw(thief, thiefx, thiefy)
        pygame.display.flip()          # flip the screen FPS times a second                
# check if the program is imported. if not, start it directly
if __name__ == "__main__":
    play_the_game()
