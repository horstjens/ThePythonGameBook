#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
015_more_sprites.py
pygame sprites with hitbars and exploding fragments
url: http://thepythongamebook.com/en:part2:pygame:step015
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

pygame sprites moving araound and exploding into little fragments 
(on mouseclick). Effect of gravity on the fragments can be toggled.
Differnt coding style and its outcome on performance (framerate)
can be toggled and is displayed by green bars. a long bar indicates
a slow performance.

works with pyhton3.4 and python2.7
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
    BIRDSPEEDMAX = 200
    BIRDSPEEDMIN = 10
    FRICTION =.999
    HITPOINTS = 100.0 
    FORCE_OF_GRAVITY = 9.81 # in pixel per second² .See http://en.wikipedia.org/wiki/Gravitational_acceleration
    print(pygame.ver)
    def write(msg="pygame is cool"):
        """write text into pygame surfaces"""
        myfont = pygame.font.SysFont("None", 32)
        mytext = myfont.render(msg, True, (0,0,0))
        mytext = mytext.convert_alpha()
        return mytext
    
    #define sprite groups
    birdgroup = pygame.sprite.LayeredUpdates()   
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    fragmentgroup = pygame.sprite.Group()
    # LayeredUpdates instead of group to draw in correct order
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group

    class BirdCatcher(pygame.sprite.Sprite):
        """circle around the mouse pointer. Left button create new sprite, right button kill sprite"""
        def __init__(self):
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

    class Fragment(pygame.sprite.Sprite):
        """a fragment of an exploding Bird"""
        gravity = True # fragments fall down ?
        def __init__(self, pos):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [0.0,0.0]
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (random.randint(1,64),0,0), (5,5), 
                                            random.randint(2,5))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
            self.lifetime = 1 + random.random()*5 # max 6 seconds
            self.time = 0.0
            self.fragmentmaxspeed = BIRDSPEEDMAX * 2 # try out other factors !
            self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            
        def update(self, seconds):
            self.time += seconds
            if self.time > self.lifetime:
                self.kill() 
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            if Fragment.gravity:
                self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            
    class Timebar(pygame.sprite.Sprite):
        """shows a bar as long as how much milliseconds are passed between two frames"""
        def __init__(self, long):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.long = long   * 2
            self.image = pygame.Surface((self.long,5))
            self.image.fill((128,255,0))
            self.image.convert()
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (0,screen.get_height())
        
        def update(self, time):
            self.rect.centery = self.rect.centery - 7
            if self.rect.centery < 0:
                self.kill()

    class Livebar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Bird sprite"""
        def __init__(self, boss):
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.boss = boss
            self.image = pygame.Surface((self.boss.rect.width,7))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,7),1)
            self.rect = self.image.get_rect()
            self.oldpercent = 0
            self.bossnumber = self.boss.number # the unique number (name) of my boss
            
        def update(self, time):
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                    int(self.boss.rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
            #check if boss is still alive
            if not Bird.birds[self.bossnumber]:
                self.kill() # kill the hitbar

    class Bird(pygame.sprite.Sprite):
        """a nice little sprite that bounce off walls and other sprites"""
        image=[]  # list of all images
        # not necessary:
        birds = {} # a dictionary of all Birds, each Bird has its own number
        number = 0  
        def __init__(self, startpos=screen.get_rect().center):
            pygame.sprite.Sprite.__init__(self,  self.groups ) #call parent class. NEVER FORGET !
            self.pos = [0,0] # dummy values to create a list
            self.pos[0] = float(startpos[0]) # float for more precise calculation
            self.pos[1] = float(startpos[1])
            self.area = screen.get_rect()
            self.image = Bird.image[0]
            self.hitpointsfull = float(HITPOINTS) # maximal hitpoints , float makes decimal
            self.hitpoints = float(HITPOINTS) # actual hitpoints
            self.rect = self.image.get_rect()
            self.radius = max(self.rect.width, self.rect.height) / 2.0
                        
            self.newspeed()
            self.cleanstatus()
            self.catched = False
            self.crashing = False
            #--- not necessary:
            self.number = Bird.number # get my personal Birdnumber
            Bird.number+= 1           # increase the number for next Bird
            Bird.birds[self.number] = self # store myself into the Bird dictionary
            #print "my number %i Bird number %i " % (self.number, Bird.number)
            Livebar(self) #create a Livebar for this Bird. 
            
        def newspeed(self):
            # new birdspeed, but not 0
            speedrandom = random.choice([-1,1]) # flip a coin
            self.dx = random.random() * BIRDSPEEDMAX * speedrandom + speedrandom 
            self.dy = random.random() * BIRDSPEEDMAX * speedrandom + speedrandom 
            
        def kill(self):
            """because i want to do some special effects (sound, dictionary etc.)
            before killing the Bird sprite i have to write my own kill(self)
            function and finally call pygame.sprite.Sprite.kill(self) 
            to do the 'real' killing"""
            cry.play()
            #print Bird.birds, "..."
            for _ in range(random.randint(3,15)):
                Fragment(self.pos)
            Bird.birds[self.number] = None # kill Bird in sprite dictionary
            pygame.sprite.Sprite.kill(self) # kill the actual Bird 

        def cleanstatus(self):
            self.catched = False   # set all Bird sprites to not catched
            self.crashing = False

        def update(self, seconds):
            # friction make birds slower
            if abs(self.dx) > BIRDSPEEDMIN and abs(self.dy) > BIRDSPEEDMIN:
                self.dx *= FRICTION
                self.dy *= FRICTION
            # spped limit
            if abs(self.dx) > BIRDSPEEDMAX:
                self.dx = BIRDSPEEDMAX * self.dx / self.dx
            if abs(self.dy) > BIRDSPEEDMAX:
                self.dy = BIRDSPEEDMAX * self.dy / self.dy
            # new position
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
    
    #---------------  no class -----------
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white
    background.blit(write("press left mouse button for more sprites."),(150,10))
    background.blit(write("press right mouse button to kill sprites."),(150,40))
    background.blit(write("press g to toggle gravity"),(150,70))
    background.blit(write("press b to toggle bad coding"),(150,100))
    background.blit(write("press c to toggle clever coding"), (150,130))
    background.blit(write("Press ESC to quit"), (150,160))

    # paint vertical lines to measure passed time (Timebar)
    #for x in range(0,screen.get_width()+1,20):
    for x in range(0,140,20):
        pygame.draw.line(background, (255,0,255), (x,0) ,(x,screen.get_height()), 1)
    background = background.convert()  # jpg can not have transparency
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)


    #assign default groups to each sprite class
    # (only allgroup is useful at the moment)
    Livebar.groups =  bargroup, allgroup 
    Timebar.groups = bargroup, allgroup
    Bird.groups =  birdgroup, allgroup
    Fragment.groups = fragmentgroup, allgroup
    BirdCatcher.groups = stuffgroup, allgroup
    #assign default layer for each sprite (lower numer is background)
    BirdCatcher._layer = 5 # top foreground
    Fragment._layer = 4
    Timebar._layer = 3
    Bird._layer = 2
    Livebar._layer = 1




    # load images into classes (class variable !)
    try:
        Bird.image.append(pygame.image.load(os.path.join("data","babytux.png")))
        Bird.image.append(pygame.image.load(os.path.join("data","babytux_neg.png")))
    except:
        raise(UserWarning, "no image files 'babytux.png' and 'babytux_neg.png' in subfolder 'data'")
    Bird.image.append(Bird.image[0].copy()) # copy of first image
    pygame.draw.rect(Bird.image[2], (0,0,255), (0,0,32,36), 1) # blue border
    Bird.image.append(Bird.image[1].copy()) # copy second image
    pygame.draw.rect(Bird.image[3], (0,0,255), (0,0,32,36), 1) # blue border
    Bird.image[0] = Bird.image[0].convert_alpha()
    Bird.image[1] = Bird.image[1].convert_alpha()
    Bird.image[2] = Bird.image[2].convert_alpha()
    Bird.image[3] = Bird.image[3].convert_alpha()

    try:
        cry = pygame.mixer.Sound(os.path.join('data','claws.ogg'))  #load sound
    except:
        raise(UserWarning, "could not load sound claws.ogg from 'data'")


   

    # at game start create a Bird and one BirdCatcher
    Bird()  # one single Bird
    hunter = BirdCatcher() # display the BirdCatcher and name it "hunter"

    # set 
    millimax = 0
    othergroup =  [] # important for good collision detection
    badcoding = False
    clevercoding = False
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 


    while mainloop:
        
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        Timebar(milliseconds)
        if milliseconds > millimax:
            millimax = milliseconds
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                elif event.key == pygame.K_g:
                    Fragment.gravity = not Fragment.gravity # toggle gravity class variable
                elif event.key == pygame.K_b:
                    if badcoding:
                        othergroup =  [] # 
                    badcoding = not badcoding
                    if badcoding: 
                        clevercoding = False
                elif event.key == pygame.K_c:
                    clevercoding = not clevercoding
                    if clevercoding:
                        badcoding = False
                elif event.key == pygame.K_p:
                    print("----------")
                    print("toplayer:", allgroup.get_top_layer())
                    print("bottomlayer:", allgroup.get_bottom_layer())
                    print("layers;", allgroup.layers())
                    

        # create new Bird on mouseclick
        if pygame.mouse.get_pressed()[0]:
            #if not pygame.sprite.spritecollideany(hunter, birdgroup): 
                Bird(pygame.mouse.get_pos()) # create a new Bird at mousepos
        if pygame.mouse.get_pressed()[2]:
            # kill sprites
            crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, True, pygame.sprite.collide_circle)
        pygame.display.set_caption("ms: %i max(ms): %i fps: %.2f birds: %i gravity: %s bad:%s clever:%s"% (milliseconds, 
                                    millimax, clock.get_fps(), len(birdgroup), Fragment.gravity, badcoding, clevercoding))
        
        # ------ collision detecttion
        for bird in birdgroup:
            bird.cleanstatus()
            
        #pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
        crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, False, pygame.sprite.collide_circle)
        # pygame.sprite.collide_circle works only if one sprite has self.radius
        # you can do without that argument collided and only the self.rects will be checked
        for crashbird in crashgroup:
            crashbird.catched = True # will get a blue border from Bird.update()
            #crashbird.kill()   # this would remove him from all his groups
        
        # test if a bird collides with another bird
        for bird in birdgroup:
            if not clevercoding:
                if badcoding:
                    othergroup = birdgroup.copy() # WRONG ! THIS CODE MAKES UGLY TIME-CONSUMING GARBAGE COLLECTION !
                else:
                    othergroup[:] = birdgroup.sprites() # correct. no garbage collection
                othergroup.remove(bird) # remove the actual bird, only all other birds remain
                if pygame.sprite.spritecollideany(bird, othergroup): 
                    
                    crashgroup = pygame.sprite.spritecollide(bird, othergroup, False )
                    for crashbird in crashgroup:
                        bird.crashing = True
                        bird.dx -= crashbird.pos[0] - bird.pos[0]
                        bird.dy -= crashbird.pos[1] - bird.pos[1]
            else:
                # very clever coding
                crashgroup = pygame.sprite.spritecollide(bird, birdgroup, False)
                for crashbird in crashgroup:
                    if crashbird.number != bird.number: #avoid collision with itself
                        bird.crashing = True # make bird blue
                        bird.dx -= crashbird.pos[0] - bird.pos[0] # move bird away from other bird
                        bird.dy -= crashbird.pos[1] - bird.pos[1]
                    
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
