#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
018_pefect_collision_detection.py
pixel perfect collision detection for pygame sprites
url: http://thepythongamebook.com/en:part2:pygame:step018
author: horst.jens@spielend-programmieren.at
physic by Leonard Michlmayr
licence: gpl, see http://www.gnu.org/licenses/gpl.html
 
this code demonstrate the difference between
colliderect, collidecircle and collidemask
 
move the small babytux around with the keys w,a,s,d  and q and e
fire with space, toggle gravity with g
toggle collision detection with c
Shoot on the giant monsters and watch the yellow impact "wounds"

works with python3.4 and python2.7
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

def game(folder = "data"):
    import pygame
    import os
    import random
    import math 
    #------ starting pygame -------------
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    screen=pygame.display.set_mode((640,480)) # try out larger values and see what happens !
    #winstyle = 0  # |FULLSCREEN # Set the display mode
    print("pygame version", pygame.ver )
    # ------- game constants ----------------------
    #BIRDSPEEDMIN = 10
    FRAGMENTMAXSPEED = 200
    FRICTION =.991  # between 1 and 0. 1 means no friction at all (deep space)
    FORCE_OF_GRAVITY = 2.81 # pixel per second square. Earth: 9.81 m/s²
    GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad
    # ----------- functions -----------
    def write(msg="pygame is cool", color=(0,0,0)):
        """write text into pygame surfaces"""
        myfont = pygame.font.SysFont("None", 32)
        mytext = myfont.render(msg, True, color)
        mytext = mytext.convert_alpha()
        return mytext
    def getclassname(class_instance):
        """this function extract the class name of a class instance.
        For an instance of a XWing class, it will return 'Wing'."""
        text = str(class_instance.__class__) # like "<class '__main__.XWing'>"
        parts = text.split(".") # like ["<class '__main__","XWing'>"]
        return parts[-1][0:-2] # from the last (-1) part, take all but the last 2 chars
    # ----------- classes ------------------------
    class Text(pygame.sprite.Sprite):
        """a pygame Sprite displaying text"""
        def __init__(self, msg="The Python Game Book", pos = (0,0), color=(0,0,0)):
            self.groups = allgroup, textgroup
            self.pos = pos
            self._layer = 1
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.newmsg(msg,color)
            self.rect.topleft = self.pos
            
        def update(self, time):
            pass # allgroup sprites need update method that accept time
        
        def newmsg(self, msg, color=(0,0,0)):
            self.image =  write(msg,color)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
            #self.rect.center = (screen.get_width()/2,10)

    class Lifebar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Bird sprite
           with a given bossnumber, the Lifebar class can 
           identify the boos (Bird sprite) with this codeline:
           Bird.birds[bossnumber] """
        def __init__(self, boss):
            self.groups = allgroup, bargroup
            self.boss = boss
            self._layer = self.boss._layer
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.oldpercent = 0
            self.paint()
            
        def paint(self):
            self.image = pygame.Surface((self.boss.rect.width,7))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,7),1)
            self.rect = self.image.get_rect()
 
        def update(self, time):
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                self.paint() # important ! boss.rect.width may have changed (because rotating)
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                                 int(self.boss.rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
            if self.boss.hitpoints < 1:   #check if boss is still alive
                self.kill() # kill the hitbar
       
    class Bird(pygame.sprite.Sprite):
        """generic Bird class, to be called from SmallBird and BigBird"""
        image=[]  # list of all images
        birds = {} # a dictionary of all Birds, each Bird has its own number
        number = 0  
        waittime = 1.0 # seconds
        def __init__(self, layer = 4 ):
            if getclassname(self) == "Monster":
                self.groups = birdgroup, allgroup  # assign groups 
            else:
                self.groups = birdgroup, allgroup, gravitygroup
            self._layer = layer                   # assign level
            #self.layer = layer
            pygame.sprite.Sprite.__init__(self,  self.groups  ) #call parent class. NEVER FORGET !
            self.pos = [random.randint(50,screen.get_width()-50),
                        random.randint(25,screen.get_height()-25)] 
            self.area = screen.get_rect()
            self.rect = self.image.get_rect()
            #small radius from center to midleft
            self.radius = self.rect.width / 2
            #big radius from center to corner:
            #self.radius = ((self.rect.width/2) **2 + (self.rect.height/2) **2) ** .5
            self.dx = 0   # wait at the beginning
            self.dy = 0            
            self.frags = 25 # number of framgents if Bird is killed
            self.number = Bird.number # get my personal Birdnumber
            Bird.number+= 1           # increase the number for next Bird
            Bird.birds[self.number] = self # store myself into the Bird dictionary
            print("my number %i Bird number %i and i am a %s " % (self.number, Bird.number, getclassname(self)))
            self.mass = 100.0
            
      
        def kill(self):
            # a shower of red fragments, exploding outward
            for _ in range(self.frags):
                RedFragment(self.pos)
            pygame.sprite.Sprite.kill(self) # kill the actual Bird 
            
        def speedcheck(self):
            #if abs(self.dx) > BIRDSPEEDMAX:
            #   self.dx = BIRDSPEEDMAX * (self.dx/abs(self.dx)) # dx/abs(dx) is 1 or -1
            #if abs(self.dy) > BIRDSPEEDMAX:
            #   self.dy = BIRDSPEEDMAX * (self.dy/abs(self.dy))
            if abs(self.dx) > 0 : 
                self.dx *= FRICTION  # make the Sprite slower over time
            if abs(self.dy) > 0 :
                self.dy *= FRICTION

        def areacheck(self):
            if not self.area.contains(self.rect):
                #self.crashing = True # change colour later
                # --- compare self.rect and area.rect
                if self.pos[0] + self.rect.width/2 > self.area.right:
                    self.pos[0] = self.area.right - self.rect.width/2
                    self.dx *= -0.5 # bouncing off but loosing speed
                if self.pos[0] - self.rect.width/2 < self.area.left:
                    self.pos[0] = self.area.left + self.rect.width/2
                    self.dx *= -0.5 # bouncing off the side but loosing speed
                if self.pos[1] + self.rect.height/2 > self.area.bottom:
                    self.pos[1] = self.area.bottom - self.rect.height/2
                    self.dy *= -0.5
                if self.pos[1] - self.rect.height/2 < self.area.top:
                    self.pos[1] = self.area.top + self.rect.height/2
                    self.dy *= -0.5 # stop when reaching the sky
                    
        def update(self, seconds):
            self.speedcheck()    
            # ------------- movement
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            # -------------- check if Bird out of screen
            self.areacheck()
            # ------ rotating
            if self.dx != 0 and self.dy!=0:
                ratio = self.dy / self.dx
                if self.dx > 0:
                    self.angle = -90-math.atan(ratio)/math.pi*180.0 # in grad
                else:
                    self.angle = 90-math.atan(ratio)/math.pi*180.0 # in grad
            #self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
            #--- calculate new position on screen -----
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            if self.hitpoints <= 0:
                self.kill()
    
    class Monster(Bird):
        """a very big bird for target practising"""
        def __init__(self, image):
            self.image = image
            Bird.__init__(self)
            #self.rect = self.image.get_rect()
            #self.radius = self.rect.width / 2 # for collision detection
            self.mask = pygame.mask.from_surface(self.image) # pixelmask
            self.hitpoints = float(1000)
            self.hitpointsfull = float(1000)
            #self.image = Bird.image[2] # big bird image
            Lifebar(self)
            
        def update(self, time):
            if random.randint(1,60) == 1:
                self.dx = random.randint(-100,100)
                self.dy = random.randint(-50,50)
            Bird.update(self,time)
            
        
    
    class BigBird(Bird):
        """A big bird controlled by the player"""
        
        def __init__(self):
            self.image = Bird.image[0] # big bird image
            self.image0 = Bird.image[0]
            #self.big = 2 # smallsprites have the value 0 for this attribute (.big) -> important for Bird.image
            Bird.__init__(self,5) # create a "little" Bird but do more than that
            self.hitpoints = float(100)
            self.hitpointsfull = float(100)
            self.pos = [screen.get_width()/2, screen.get_height()/2]
            #print "my BigBirdNumber is", self.number # i have a number in the Bird class !
            self.angle = 0
            self.speed = 20.0 # base movement speed factor
            self.rotatespeed = 1.0 # rotating speed
            self.frags = 100
            Lifebar(self)
            self.cooldowntime = 0.08 #seconds
            self.cooldown = 0.0
            self.damage = 5 # how many damage one bullet inflict
            self.shots = 0
            #self.radius = self.image.get_width() / 2.0
            self.mass = 400.0
        
        def kill(self):
            bombsound.play()
            Bird.kill(self)
            
        def update(self, time):
            """BigBird has its own update method, overwriting the 
               update method from the Bird class"""
             
            #--- calculate actual image: crasing, bigbird, both, nothing ?
            #self.image = Bird.image[self.crashing+self.big] # 0 for not crashing, 2 for big
            pressedkeys = pygame.key.get_pressed()
            self.ddx = 0.0
            self.ddy = 0.0
            if pressedkeys[pygame.K_w]: # forward
                     self.ddx = -math.sin(self.angle*GRAD) 
                     self.ddy = -math.cos(self.angle*GRAD) 
                     Smoke(self.rect.center, -self.ddx , -self.ddy )
            if pressedkeys[pygame.K_s]: # backward
                     self.ddx = +math.sin(self.angle*GRAD) 
                     self.ddy = +math.cos(self.angle*GRAD) 
                     Smoke(self.rect.center, -self.ddx, -self.ddy )
            if pressedkeys[pygame.K_e]: # right side
                     self.ddx = +math.cos(self.angle*GRAD)
                     self.ddy = -math.sin(self.angle*GRAD)
                     Smoke(self.rect.center, -self.ddx , -self.ddy )
            if pressedkeys[pygame.K_q]: # left side
                     self.ddx = -math.cos(self.angle*GRAD) 
                     self.ddy = +math.sin(self.angle*GRAD) 
                     Smoke(self.rect.center, -self.ddx , -self.ddy )
            # ------------shoot-----------------
            if self.cooldown > 0:
                self.cooldown -= time 
            else:
                if pressedkeys[pygame.K_SPACE]: # shoot forward
                    lasersound.play() # play sound
                    self.shots += 1
                    Bullet(self, -math.sin(self.angle*GRAD) ,
                           -math.cos(self.angle*GRAD) )
                self.cooldown = self.cooldowntime
            # ------------move------------------
            self.dx += self.ddx * self.speed
            self.dy += self.ddy * self.speed
            #self.speedcheck()   # friction, maxspeed             
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            # -- check if Bird out of screen
            self.areacheck()
            # ------------- rotate ------------------
            if pressedkeys[pygame.K_a]: # left turn , counterclockwise
                self.angle += self.rotatespeed
            if pressedkeys[pygame.K_d]: # right turn, clockwise
                self.angle -= self.rotatespeed
            self.oldcenter = self.rect.center
            self.image = pygame.transform.rotate(self.image0, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.oldcenter
            #--- calculate new position on screen -----
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            if self.hitpoints <= 0: # ----- alive---- 
                self.kill()
            
    class Fragment(pygame.sprite.Sprite):
        """generic Fragment class. Inherits to blue Fragment (implosion),
           red Fragment (explosion), smoke (black) and shots (purple)"""
        def __init__(self, pos, layer = 9):
            self._layer = layer
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [0.0,0.0]
            self.fragmentmaxspeed = FRAGMENTMAXSPEED# try out other factors !

        def init2(self):  # split the init method into 2 parts for better access from subclasses
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, self.color, (5,5), random.randint(2,5))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
            self.time = 0.0
            
        def update(self, seconds):
            self.time += seconds
            if self.time > self.lifetime:
                self.kill() 
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
    
    class RedFragment(Fragment):
        """explodes outward from (killed) Bird"""
        def __init__(self,pos):
            self.groups = allgroup, stuffgroup, fragmentgroup, gravitygroup
            Fragment.__init__(self,pos)
            #red-only part -----------------------------
            self.color = (random.randint(25,255),0,0) # red            
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.lifetime = 1 + random.random()*3 # max 3 seconds
            self.init2() # continue with generic Fragment class
            self.mass = 48.0
            
   
    class Smoke(Fragment):
        """black exhaust indicating that the BigBird sprite is moved by
           the player. Exhaust direction is inverse of players movement direction"""
        def __init__(self, pos, dx, dy):
           self.color = ( random.randint(1,50), random.randint(1,50), random.randint(1,50) )
           self.groups = allgroup, stuffgroup
           Fragment.__init__(self,pos, 3) # give startpos and layer 
           self.pos[0] = pos[0]
           self.pos[1] = pos[1]
           self.lifetime = 1 + random.random()*2 # max 3 seconds
           Fragment.init2(self)
           self.smokespeed = 120.0 # how fast the smoke leaves the Bird
           self.smokearc = .3 # 0 = thin smoke stream, 1 = 180 Degrees
           arc = self.smokespeed * self.smokearc
           self.dx = dx * self.smokespeed + random.random()*2*arc - arc
           self.dy = dy * self.smokespeed + random.random()*2*arc - arc
           
    class Wound(Fragment):
        """yellow impact wound that shows the exact location of the hit"""
        def __init__(self, pos, victim):
            self.color = ( random.randint(200,255), random.randint(200,255), random.randint(0,50))
            self.groups = allgroup, stuffgroup
            Fragment.__init__(self, pos, 7) # layer
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.lifetime = 1 + random.random()*2 # max 3 seconds
            Fragment.init2(self)
            self.victim = victim
        
        def update(self,time):
            self.dx = self.victim.dx
            self.dy = self.victim.dy
            Fragment.update(self, time)
           
    class Bullet(Fragment):
        """a bullet flying in the direction of the BigBird's heading. May 
           be subject to gravity"""
        def __init__(self, boss, dx, dy):
            self.color = (200,0,200)
            self.boss = boss
            self.groups = allgroup, bulletgroup, gravitygroup
            Fragment.__init__(self, self.boss.rect.center, 3) # layer behind Bird
            self.pos[0] = self.boss.pos[0]
            self.pos[1] = self.boss.pos[1]
            self.lifetime = 5 # 5 seconds
            self.image = pygame.Surface((4,20))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,4,20) )
            pygame.draw.rect(self.image, (10,0,0), (0,0,4,4)) # point
            self.image = self.image.convert_alpha()
            self.image0 = self.image.copy()
            self.rect = self.image.get_rect()
            self.rect.center = self.boss.rect.center
            self.image = pygame.transform.rotate(self.image, self.boss.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.boss.rect.center
            self.time = 0.0
            self.bulletspeed = 250.0 # pixel per second ?
            self.bulletarc = 0.05 # perfect shot has 0.0
            arc = self.bulletspeed * self.bulletarc
            self.dx = dx * self.bulletspeed + random.random()*2*arc -arc
            self.dy = dy * self.bulletspeed + random.random()*2*arc -arc
            self.mass = 25.0
            self.angle = self.boss.angle
            
        def update(self, time):
            Fragment.update(self,time)
            #--------- rotate into direction of movement ------------
            if self.dx != 0 and self.dy!=0:
                ratio = self.dy / self.dx
                if self.dx > 0:
                    self.angle = -90-math.atan(ratio)/math.pi*180.0 # in grad
                else:
                    self.angle = 90-math.atan(ratio)/math.pi*180.0 # in grad
            self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
            
    # ----------------- end of definitions ------------  
    # ----------------- background artwork -------------  
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white
    background.blit(write("navigate with w,a,s,d and q and e "),(50,40))
    background.blit(write("press SPACE to fire bullets"),(50,70))
    background.blit(write("press g to toggle gravity"), (50, 100))
    background.blit(write("press c to toggle collision detection."),(50,130))
    background.blit(write("Press ESC to quit "), (50,160))
    background = background.convert()  # jpg can not have transparency
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)
    #-----------------define sprite groups------------------------
    birdgroup = pygame.sprite.Group() 
    textgroup = pygame.sprite.Group()
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    fragmentgroup = pygame.sprite.Group()
    gravitygroup = pygame.sprite.Group()
    # only the allgroup draws the sprite, so i use LayeredUpdates() instead Group()
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated, can draw sprites in layers 

    #-------------loading files from data subdirectory -------------------------------
    try: # load images into classes (class variable !). if not possible, draw ugly images
        Bird.image.append(pygame.image.load(os.path.join(folder,"babytux.png")))
        Bird.image.append(pygame.image.load(os.path.join(folder,"crossmonster.png")))
        Bird.image.append(pygame.image.load(os.path.join(folder,"xmonster.png")))
    except:
        raise(UserWarning, "could not load images from folder %s" % folder)
        # ------------
    Bird.image[0] = Bird.image[0].convert_alpha()
    Bird.image[1] = Bird.image[1].convert_alpha()
    Bird.image[2] = Bird.image[2].convert_alpha()
    
    try: # ------- load sound -------
        crysound = pygame.mixer.Sound(os.path.join(folder,'claws.ogg'))  #load sound
        bombsound = pygame.mixer.Sound(os.path.join(folder,'bomb.ogg'))
        lasersound = pygame.mixer.Sound(os.path.join(folder,'shoot.ogg'))
        hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))
    except:
        print( "could not load one of the sound files from folder %s. no sound, sorry" %folder)
    # ------------- before the main loop ----------------------
    collision = "rect"
    screentext = Text()
    screentext2 = Text("collsion detection: %s" % collision, (200,0))
    othergroup =  [] # important for good collision detection
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 
    amount = 7 # how many small birds should always be present on the screen
    #for _ in range(amount):     # start with some small Birds
    #    SmallBird()  # some small Birds
    player = BigBird() # big Bird
    dummy = Monster(Bird.image[1])
    dummy2 = Monster(Bird.image[2])  # add more giant birds at will
    overtime = 15 # time in seconds to admire the explosion of player before the game ends
    gameOver = False
    hits = 0  # how often the player was hitting a small Bird
    quota = 0 # hit/miss quota
    gametime = 60 # how long to play (seconds)
    playtime = 0  # how long the game was played
    gravity = True
        
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        playtime += seconds # keep track of playtime
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                elif event.key == pygame.K_x:
                    player.hitpoints -= 1
                    print( player.hitpoints)
                elif event.key == pygame.K_y:
                    player.hitpoints += 1
                    print(player.hitpoints)
                elif event.key == pygame.K_g:
                    gravity = not gravity # toggle gravity
                elif event.key == pygame.K_p: # get sprites at mouse position, print info
                    print("=========================")
                    print( "-----Spritelist---------")
                    spritelist = allgroup.get_sprites_at(pygame.mouse.get_pos())
                    for sprite in spritelist:
                        print(sprite, "Layer:",allgroup.get_layer_of_sprite(sprite))
                    print("------------------------")
                elif event.key == pygame.K_c:
                    if collision == "rect":
                        collision = "circle"
                    elif collision == "circle":
                        collision = "mask"
                    elif collision == "mask":
                        collision = "rect"
                    screentext2.newmsg("collsion detection: %s" % collision)
         
   
        if player.shots > 0:
            quota = (float(hits)/player.shots )* 100
        pygame.display.set_caption("fps: %.2f gravity: %s hits:%i shots:%i quota:%.2f%%"  % (clock.get_fps(), 
                                     gravity, hits, player.shots, quota))
        # ------ collision detection
        for bird in birdgroup:

            if collision == "rect":
                crashgroup = pygame.sprite.spritecollide(bird, bulletgroup, False, pygame.sprite.collide_rect)
            elif collision == "circle":
                crashgroup = pygame.sprite.spritecollide(bird, bulletgroup, False, pygame.sprite.collide_circle)
            elif collision == "mask":
                crashgroup = pygame.sprite.spritecollide(bird, bulletgroup, False, pygame.sprite.collide_mask)
            else:
                raise( SystemExit, "wrong/missing collisoin method")
            for ball in crashgroup:  # test for collision with bullet
                if ball.boss.number != bird.number:
                    hitsound.play()
                    hits +=1
                    bird.hitpoints -= ball.boss.damage
                    #factor =  (ball.mass / bird.mass)
                    #bird.dx += ball.dx * factor
                    #bird.dy += ball.dy * factor
                    Wound(ball.rect.center, bird)
                    ball.kill()
                    
            crashgroup = pygame.sprite.spritecollide(bird, fragmentgroup, False)
            for frag in crashgroup: # test for red fragments
                bird.hitpoints -=1
                factor =  frag.mass / bird.mass
                bird.dx += frag.dx * factor
                bird.dy += frag.dy * factor
                frag.kill()
                    
        if gravity: # ---- gravity check ---
            for thing in gravitygroup:
                thing.dy += FORCE_OF_GRAVITY # gravity suck down all kind of things
                    
        #if len(birdgroup) < amount: # create enough SmallBirds
        #    for _ in range(random.randint(1,3)):
        #        SmallBird()
        
        # ------game Over ? -------------
        if (player.hitpoints < 1 or playtime > gametime) and not gameOver:
            gameOver = True # do those things once when the game ends
            screentext2.newmsg("")
            screentext.newmsg("Game Over. hits/shots: %i/%i quota: %.2f%%" % (hits, player.shots, quota), (255,0,0))
            player.hitpoints = 0 # kill the player into a big explosion
        if gameOver: # overtime to watch score, explosion etc
            overtime -= seconds
            if overtime < 0:
                mainloop = False
        else: # not yet gameOver
            screentext.newmsg("Time left: %.2f" % (gametime - playtime))
        
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
