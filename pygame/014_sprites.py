#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
014-sprites.py
real pygame sprites
url: http://thepythongamebook.com/en:part2:pygame:step014
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

Real pygame Sprites moving around. Create more sprites with mouse click.
Shows collision detection
loading images from a subfolder called 'data'
all images files must be in the subfolder 'data'. The subfolder must be inside the
same folder as the program itself. 

works with pyhton3.4 and python2.7
"""
import pygame
import os
import random


pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
screen=pygame.display.set_mode((640,480)) # try out larger values and see what happens !
#winstyle = 0  # |FULLSCREEN # Set the display mode
BIRDSPEED = 50.0

def write(msg="pygame is cool"):
    myfont = pygame.font.SysFont("None", 32)
    mytext = myfont.render(msg, True, (0,0,0))
    mytext = mytext.convert_alpha()
    return mytext

class BirdCatcher(pygame.sprite.Sprite):
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


class Bird(pygame.sprite.Sprite):
    image=[]  # list of all images
    # not necessary:
    birds = {} # a dictionary of all Birds, each Bird has its own number
    number = 0  
    def __init__(self, startpos=(50,50), area=screen.get_rect()):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = startpos[0]*1.0 # float
        self.pos[1] = startpos[1]*1.0 # float
        self.image = Bird.image[0]
        self.rect = self.image.get_rect()
        self.area = area # where the sprite is allowed to move
        self.newspeed()
        self.catched = False
        #--- not necessary:
        self.number = Bird.number # get my personal Birdnumber
        Bird.number+= 1           # increase the number for next Bird
        Bird.birds[self.number] = self # store myself into the Bird dictionary
        #print "my number %i Bird number %i " % (self.number, Bird.number)
    def newspeed(self):
        # new birdspeed, but not 0
        speedrandom = random.choice([-1,1]) # flip a coin
        self.dx = random.random() * BIRDSPEED * speedrandom + speedrandom 
        self.dy = random.random() * BIRDSPEED * speedrandom + speedrandom 
      
    def update(self, seconds):
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        # -- check if out of screen
        if not self.area.contains(self.rect):
            self.image = Bird.image[1] # crash into wall
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
        else:
            if self.catched:
                self.image = Bird.image[2] # blue rectangle
            else:
                self.image = Bird.image[0] # normal bird image
        #--- calculate new position on screen -----
            
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)


    
background = pygame.Surface((screen.get_width(), screen.get_height()))
background.fill((255,255,255))     # fill white
background.blit(write("Press left mouse button for more sprites. Press ESC to quit"),(5,10))
background = background.convert()  # jpg can not have transparency
screen.blit(background, (0,0))     # blit background on screen (overwriting all)
clock = pygame.time.Clock()        # create pygame clock object 
mainloop = True
FPS = 60                           # desired max. framerate in frames per second. 

# load images into classes (class variable !)
try:
    Bird.image.append(pygame.image.load(os.path.join("data","babytux.png")))
    Bird.image.append(pygame.image.load(os.path.join("data","babytux_neg.png")))
except:
    raise( UserWarning, "Unable to find babytux images in the folder 'data' :-( ")
Bird.image.append(Bird.image[0].copy()) # copy of first image
pygame.draw.rect(Bird.image[2], (0,0,255), (0,0,32,36), 1) # blue border
Bird.image[0] = Bird.image[0].convert_alpha()
Bird.image[1] = Bird.image[1].convert_alpha()
Bird.image[2] = Bird.image[2].convert_alpha()

birdgroup = pygame.sprite.Group()
allgroup = pygame.sprite.Group()
        
#assign default groups to each sprite class
Bird.groups = birdgroup, allgroup
BirdCatcher.groups = allgroup
# one single Bird
Bird()
# display the BirdCatcher and name it "hunter"
hunter = BirdCatcher() 

while mainloop:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
    # create new Bird on mouseclick
    if pygame.mouse.get_pressed()[0]:
        Bird(pygame.mouse.get_pos()) # create a new Bird at mousepos
    
    pygame.display.set_caption("[FPS]: %.2f birds: %i" % (clock.get_fps(), len(birdgroup)))
    
    # ------ collision detecttion
    for bird in birdgroup:
        bird.catched = False   # set all Bird sprites to not catched
        
    #pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
    crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, False, pygame.sprite.collide_circle)
    # pygame.sprite.collide_circle works only if one sprite has self.radius
    # you can do without that argument collided and only the self.rects will be checked
    for crashbird in crashgroup:
        crashbird.catched = True # will get a blue border from Bird.update()
        #crashbird.kill()   # this would remove him from all his groups
        
    allgroup.clear(screen, background)
    allgroup.update(seconds)
    allgroup.draw(screen)
    
    pygame.display.flip()          # flip the screen 30 times a second             
