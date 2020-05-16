#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
016_layers.py
pygame sprites with different layers and parallax scrolling
url: http://thepythongamebook.com/en:part2:pygame:step016
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html


change the sprite layer by clicking with left or right mouse button
the birdsprites will appear before or behind the blocks

point on a sprite and pres "p" to print out more information about that sprite
part of www.pythongamebook.com by Horst JENS


works with python3.4 and python2.7
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

def game():
        
    import pygame
    import os
    import random


    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    screen=pygame.display.set_mode((640,480)) # try out larger values and see what happens !
    #winstyle = 0  # |FULLSCREEN # Set the display mode
    print("pygame version", pygame.ver)

    BIRDSPEEDMAX = 200
    BIRDSPEEDMIN = 10
    FRICTION =.999
    FORCE_OF_GRAVITY = 9.81
    
    
    def write(msg="pygame is cool"):
        """write text into pygame surfaces"""
        myfont = pygame.font.SysFont("None", 32)
        mytext = myfont.render(msg, True, (0,0,0))
        mytext = mytext.convert_alpha()
        return mytext
    
    class Text(pygame.sprite.Sprite):
        """ display a text"""
        def __init__(self, msg ):
            self.groups = allgroup, textgroup
            self._layer = 99
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.newmsg(msg)

            
        def update(self, time):
            pass
        
        def newmsg(self, msg="i have nothing to say"):
            self.image =  write(msg)
            self.rect = self.image.get_rect()
            self.rect.center = (screen.get_width()/2,10)

    class Mountain(pygame.sprite.Sprite):
        """generate a mountain sprite for the background, to 
           demonstrate parallax scrolling. Like in the classic
           'moonbuggy' game. Mountains slide from right to left"""
        def __init__(self, type):
            self.type = type
            if self.type == 1:
                self._layer = -1
                self.dx = -100
                self.color = (0,0,255) # blue mountains, close
            elif self.type == 2:
                self._layer = -2
                self.color = (200,0,255) # pink mountains, middle
                self.dx = -75
            else:
                self._layer = -3
                self.dx = -35
                self.color = (255,0,0) # red mountains, far away
            self.groups = allgroup, mountaingroup
            pygame.sprite.Sprite.__init__(self, self.groups) # THE Line
            self.dy = 0
            x = 100 * self.type * 1.5
            y = screen.get_height() / 2 + 50 * (self.type -1)
            self.image = pygame.Surface((x,y))
            #self.image.fill((0,0,0)) # fill with black
            self.image.set_colorkey((0,0,0)) # black is transparent
            pygame.draw.polygon(self.image, self.color,
               ((0,y),
                (0,y-10*self.type), 
                (x/2, int(random.random()*y/2)),
                (x,y-10*self.type),
                (x,y),
                (9,y)),0) # width=0 fills the polygon
            self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.pos = [0.0,0.0]
            # start right side from visible screen
            self.pos[0] = screen.get_width()+self.rect.width/2
            self.pos[1] = screen.get_height()-self.rect.height/2
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            self.parent = False
            
        def update(self, time):
            self.pos[0] += self.dx * time
            self.pos[1] += self.dy * time
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            # kill mountains too far to the left
            if self.rect.centerx + self.rect.width/2+10 < 0:
                self.kill()
            # create new mountains if necessary
            if not self.parent:
                if self.rect.centerx  < screen.get_width():
                    self.parent = True
                    Mountain(self.type) # new Mountain coming from the right side
            
           
    
    class Block(pygame.sprite.Sprite):
        """a block with a number indicating it's layer.
           Blocks move horizontal and bounce on screen edges"""
        def __init__(self, blocknumber=1):
            self.blocknumber = blocknumber
            self.color = (random.randint(10,255),
                          random.randint(10,255),
                          random.randint(10,255))
            self._layer = self.blocknumber
            self.groups = allgroup, blockgroup
            pygame.sprite.Sprite.__init__(self, self.groups) # THE line
            self.area = screen.get_rect()
            self.image = pygame.Surface((100,100))
            self.image.fill(self.color)
            self.image.blit(write(str(self.blocknumber)),(40,40))
            self.image = self.image.convert()
            self.rect = self.image.get_rect()
            self.rect.centery = screen.get_height() / 2
            self.rect.centerx = 100 * self.blocknumber + 50
            #self.rect.centery = (screen.get_height() / 10.0) * self.blocknumber + self.image.get_height() / 2
            self.pos = [0.0,0.0]
            self.pos[0] = self.rect.centerx
            self.pos[1] = self.rect.centery
            self.dy = random.randint(50,100) * random.choice((-1,1))
            self.dx = 0
            
        def newspeed(self):
            self.dy *= -1
            
        def update(self, time):
            if not self.area.contains(self.rect):
                # --- compare self.rect and area.rect
                if self.pos[1]  < self.area.top:
                    self.pos[1] = self.area.top
                    self.newspeed() # calculate a new direction
                elif self.pos[1] > self.area.bottom:
                    self.pos[1] = self.area.bottom
                    self.newspeed() # calculate a new direction
            self.pos[0] += self.dx * time
            self.pos[1] += self.dy * time
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            
    class BirdCatcher(pygame.sprite.Sprite):
        """circle around the mouse pointer. Left button create new sprite, right button kill sprite"""
        def __init__(self):
            self._layer = 9
            self.groups = allgroup, stuffgroup
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.image = pygame.Surface((100,100)) # created on the fly
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (255,0,0), (50,50), 50, 2) # red circle
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.radius = 50 # for collide check

        def update(self, seconds):
            # no need for seconds but the other sprites need it
            self.rect.center = pygame.mouse.get_pos()

    class Lifebar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Bird sprite
           with a given bossnumber, the Lifebar class can 
           identify the boos (Bird sprite) with this codeline:
           Bird.birds[bossnumber] """
        def __init__(self, bossnumber):
            self.groups = allgroup, bargroup
            self.bossnumber = bossnumber
            self._layer = Bird.birds[self.bossnumber]._layer
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.image = pygame.Surface((Bird.birds[self.bossnumber].rect.width,7))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, (0,255,0), (0,0,Bird.birds[self.bossnumber].rect.width,7),1)
            self.rect = self.image.get_rect()
            self.oldpercent = 0
            
        def update(self, time):
            self.percent = Bird.birds[self.bossnumber].hitpoints / Bird.birds[self.bossnumber].hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                pygame.draw.rect(self.image, (0,0,0), (1,1,Bird.birds[self.bossnumber].rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                                 int(Bird.birds[self.bossnumber].rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = Bird.birds[self.bossnumber].rect.centerx
            self.rect.centery = Bird.birds[self.bossnumber].rect.centery - Bird.birds[self.bossnumber].rect.height /2 - 10
            #check if boss is still alive
            if Bird.birds[self.bossnumber].hitpoints < 1:
                self.kill() # kill the hitbar
      
    class Bird(pygame.sprite.Sprite):
        """a nice little sprite that bounce off walls and other sprites"""
        image=[]  # list of all images
        birds = {} # a dictionary of all Birds, each Bird has its own number
        number = 0  
        waittime = 1.0 # seconds
        def __init__(self, layer = 4 ):
            self.groups = birdgroup, allgroup # assign groups 
            self._layer = layer                   # assign level
            #self.layer = layer
            pygame.sprite.Sprite.__init__(self,  self.groups  ) #call parent class. NEVER FORGET !
            #pygame.sprite.Sprite.__init__(self,  *args ) #call parent class. NEVER FORGET !
            self.pos = [random.randint(50,screen.get_width()-50),
                        random.randint(25,screen.get_height()-25)] 
            self.area = screen.get_rect()
            self.image = Bird.image[0]
            self.hitpointsfull = float(100) # maximal hitpoints
            self.hitpoints = float(100) # actual hitpoints
            self.rect = self.image.get_rect()
            self.radius = max(self.rect.width, self.rect.height) / 2.0
            self.dx = 0   # wait at the beginning
            self.dy = 0            
            self.waittime = Bird.waittime # 1.0 # one second
            #self.newspeed()
            self.lifetime = 0.0
            self.waiting = True
            self.rect.center = (-100,-100) # out of visible screen
            self.cleanstatus()
            self.catched = False
            self.crashing = False
            #--- not necessary:
            self.number = Bird.number # get my personal Birdnumber
            Bird.number+= 1           # increase the number for next Bird
            Bird.birds[self.number] = self # store myself into the Bird dictionary
            #print "my number %i Bird number %i " % (self.number, Bird.number)
            Lifebar(self.number) #create a Lifebar for this Bird. 
            # starting implosion of blue fragments
            for _ in range(8):
                Fragment(self.pos, True)
            
        def newspeed(self):
            # new birdspeed, but not 0
            speedrandom = random.choice([-1,1]) # flip a coin
            self.dx = random.randint(BIRDSPEEDMIN,BIRDSPEEDMAX) * speedrandom 
            self.dy = random.randint(BIRDSPEEDMIN,BIRDSPEEDMAX) * speedrandom 

        def cleanstatus(self):
            self.catched = False   # set all Bird sprites to not catched
            self.crashing = False
        
        def kill(self):
            # a shower of red fragments, exploding outward
            for _ in range(15):
                Fragment(self.pos)
            pygame.sprite.Sprite.kill(self) # kill the actual Bird 
            
        
        def update(self, seconds):
            #---make Bird only visible after waiting time
            self.lifetime += seconds
            if self.lifetime > (self.waittime) and self.waiting:
                self.newspeed()
                self.waiting = False
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
            if self.waiting:
                self.rect.center = (-100,-100)
            else:
                # speedcheck
                # friction make birds slower
                if abs(self.dx) > BIRDSPEEDMIN and abs(self.dy) > BIRDSPEEDMIN:
                    self.dx *= FRICTION
                    self.dy *= FRICTION
                # spped limit
                if abs(self.dx) > BIRDSPEEDMAX:
                    self.dx = BIRDSPEEDMAX * self.dx / self.dx
                if abs(self.dy) > BIRDSPEEDMAX:
                    self.dy = BIRDSPEEDMAX * self.dy / self.dy
                # movement
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                # -- check if Bird out of screen
                if not self.area.contains(self.rect):
                    self.crashing = True # change colour later
                    # --- compare self.rect and area.rect
                    if self.pos[0] + self.rect.width/2 > self.area.right:
                        self.pos[0] = self.area.right - self.rect.width/2
                    if self.pos[0] - self.rect.width/2 < self.area.left:
                        self.pos[0] = self.area.left + self.rect.width/2
                    if self.pos[1] + self.rect.height/2 > self.area.bottom:
                        self.pos[1] = self.area.bottom - self.rect.height/2
                    if self.pos[1] - self.rect.height/2 < self.area.top:
                        self.pos[1] = self.area.top + self.rect.height/2
                    self.newspeed() # calculate a new direction
                #--- calculate actual image: crasing, catched, both, nothing ?
                self.image = Bird.image[self.crashing + self.catched*2]
                #--- calculate new position on screen -----
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                #--- loose hitpoins
                if self.crashing:
                    self.hitpoints -=1
                #--- check if still alive
                if self.hitpoints <= 0:
                    self.kill()
            
    class Fragment(pygame.sprite.Sprite):
        """a fragment of an exploding Bird"""
        gravity = False # fragments fall down ?
        def __init__(self, pos, bluefrag = False):
            self._layer = 9
            self.groups = allgroup, stuffgroup
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.bluefrag = bluefrag
            self.pos = [0.0,0.0]
            self.target = pos
            self.fragmentmaxspeed = BIRDSPEEDMAX * 2 # try out other factors !
            if self.bluefrag:
                # blue frament implodes from screen edge toward Bird
                self.color = (0,0,random.randint(25,255)) # blue
                self.side = random.randint(1,4)
                if self.side == 1:  # left side
                    self.pos[0] = 0   
                    self.pos[1] = random.randint(0,screen.get_height())
                elif self.side == 2: # top
                    self.pos[0] = random.randint(0,screen.get_width()) 
                    self.pos[1] = 0
                elif self.side == 3: #right
                    self.pos[0] = screen.get_width() 
                    self.pos[1] = random.randint(0,screen.get_height())
                else: #bottom
                    self.pos[0] = random.randint(0,screen.get_width()) 
                    self.pos[1] = screen.get_height()
                # calculating flytime for one second.. Bird.waittime should be 1.0
                self.dx = (self.target[0] - self.pos[0]) * 1.0 / Bird.waittime
                self.dy = (self.target[1] - self.pos[1]) * 1.0 / Bird.waittime
                self.lifetime = Bird.waittime + random.random() * .5 # a bit more livetime after the Bird appears
            else: # red fragment explodes from the bird toward screen edge
                self.color = (random.randint(25,255),0,0) # red            
                self.pos[0] = pos[0]
                self.pos[1] = pos[1]
                self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
                self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
                self.lifetime = 1 + random.random()*3 # max 3 seconds
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
            if Fragment.gravity and not self.bluefrag:
                self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
    
        
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white
    background.blit(write("press left mouse button to increase Bird's layer"),(50,40))
    background.blit(write("press right mouse button to decrease Bird's layer."),(50,65))
    background.blit(write("layer of mountains are: -1 (blue), -2 (pink), -3 (red)"),(50,90))
    background.blit(write("Press ESC to quit, p to print info at mousepos"), (50,115))
    # secret keys: g (gravity), p (print layers)
    
    background = background.convert()  # jpg can not have transparency
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)

    #define sprite groups. Do this before creating sprites 
    blockgroup = pygame.sprite.LayeredUpdates()
    birdgroup = pygame.sprite.Group() 
    textgroup = pygame.sprite.Group()
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    mountaingroup = pygame.sprite.Group()
    # only the allgroup draws the sprite, so i use LayeredUpdates() instead Group()
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated, can draw sprites in layers 



    
    try: # load images into classes (class variable !). if not possible, draw ugly images
        Bird.image.append(pygame.image.load(os.path.join("data","babytux.png")))
        Bird.image.append(pygame.image.load(os.path.join("data","babytux_neg.png")))
    except:
        print("no image files 'babytux.png' and 'babytux_neg.png' in subfolder 'data'")
        print("therfore drawing ugly sprites instead")
        image = pygame.Surface((32,36))
        image.fill((255,255,255))
        pygame.draw.circle(image, (0,0,0), (16,18), 15,2)
        image.set_colorkey((255,255,255))
        Bird.image.append(image) # alternative ugly image
        image2 = image.copy()
        pygame.draw.circle(image2, (0,0,255), (16,18), 13,0)
        Bird.image.append(image2)
    Bird.image.append(Bird.image[0].copy()) # copy of first image
    pygame.draw.rect(Bird.image[2], (0,0,255), (0,0,32,36), 1) # blue border
    Bird.image.append(Bird.image[1].copy()) # copy second image
    pygame.draw.rect(Bird.image[3], (0,0,255), (0,0,32,36), 1) # blue border
    Bird.image[0] = Bird.image[0].convert_alpha()
    Bird.image[1] = Bird.image[1].convert_alpha()
    Bird.image[2] = Bird.image[2].convert_alpha()
    Bird.image[3] = Bird.image[3].convert_alpha()

    
    try: # ------- load sound -------
        cry = pygame.mixer.Sound(os.path.join('data','claws.ogg'))  #load sound
    except:
        raise(SystemExit, "could not load sound claws.ogg from 'data'")
        #print"could not load sound file claws.ogg from folder data. no sound, sorry"


    #create Sprites
    hunter = BirdCatcher() # display the BirdCatcher and name it "hunter"

    for x in range(screen.get_width()//100):
        Block(x) # add more Blocks if you y screen resolution is bigger
    
    othergroup =  [] # important for good collision detection
    badcoding = False
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 
   
    birdlayer = 4
    birdtext = Text("current Bird _layer = %i" % birdlayer) # create Text sprite
    cooldowntime = 0 #sec
    
    # start with some Birds
    for _ in range(15):
        Bird(birdlayer)  # one single Bird
    
    # create the first parallax scrolling mountains
    Mountain(1) # blue
    Mountain(2) # pink
    Mountain(3) # red

    while mainloop: # ----------------- mainloop ----------------------
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                #elif event.key == pygame.K_g:
                    #Fragment.gravity = not Fragment.gravity # toggle gravity class variable
                elif event.key == pygame.K_p: # get sprites at mouse position, print info
                    print("=========================")
                    print("-----Spritelist---------")
                    spritelist = allgroup.get_sprites_at(pygame.mouse.get_pos())
                    for sprite in spritelist:
                        print(sprite, "Layer:",allgroup.get_layer_of_sprite(sprite))
                    print("------------------------")
                    print("toplayer:", allgroup.get_top_layer())
                    print("bottomlayer:", allgroup.get_bottom_layer())
                    print("layers;", allgroup.layers())
                    print("=========================")
                    
                elif event.key == pygame.K_g:
                    Fragment.gravity = not Fragment.gravity # toggle gravity class variable
   

        # change birdlayer on mouseclick
        if cooldowntime <= 0: # to 
            if pygame.mouse.get_pressed()[0]:
                if birdlayer < 10:
                    birdlayer += 1
                    cooldowntime = .5 # seconds
                    cry.play()
                    for bird in birdgroup:
                        allgroup.change_layer(bird, birdlayer) # allgroup draws the sprite 
                    for bar in bargroup:
                        allgroup.change_layer(bar, birdlayer) # allgroup draws the sprite 
            if pygame.mouse.get_pressed()[2]:
                if birdlayer > -4:
                    birdlayer -= 1
                    cooldowntime = .5
                    cry.play()
                    for bird in birdgroup:
                        allgroup.change_layer(bird, birdlayer) # allgroup draws the sprite !
                    for bar in bargroup:
                        allgroup.change_layer(bar, birdlayer) # allgroup draws the sprite 
        else:
            cooldowntime -= seconds # to avoid speedclicking

        pygame.display.set_caption("fps: %.2f birds: %i grav: %s" % (clock.get_fps(), len(birdgroup), Fragment.gravity))
        

        birdtext.newmsg("current Bird _layer = %i" % birdlayer) # update text for birdlayer
    
        # ------ collision detection
        for bird in birdgroup:
            bird.cleanstatus() 
            
        #pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
        crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, False, pygame.sprite.collide_circle)
        # pygame.sprite.collide_circle works only if one sprite has self.radius
        # you can do without that argument collided and only the self.rects will be checked
        for crashbird in crashgroup:
            crashbird.catched = True # will get a blue border from Bird.update()
        
        for bird in birdgroup:  # test if a bird collides with another bird
            # check the Bird.number to make sure the bird is not crashing with himself
            crashgroup = pygame.sprite.spritecollide(bird, birdgroup, False )
            for crashbird in crashgroup:
                if crashbird.number != bird.number: #different number means different birds
                    bird.crashing = True
                    if not bird.waiting:
                        bird.dx -= crashbird.pos[0] - bird.pos[0]
                        bird.dy -= crashbird.pos[1] - bird.pos[1]
        
        # create 10 new Birds if fewer than 11 birds alive
        if len(birdgroup) < 10:
            for _ in range(random.randint(1,5)):
                Bird(birdlayer)
                    
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
else:
    print("i was imported by", __name__)
