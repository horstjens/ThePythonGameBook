#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
022_minimap.py
demo of tank game with rotating turrets and minimap
url: http://thepythongamebook.com/en:part2:pygame:step022
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

the minimap displays tanks, traces and bullets even for elements
currently not visible on the playfield.

works with python3.4 and python2.7
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

import pygame
import random
import math
GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad

class Config(object):
    """ a class to hold all game constants that may be modded by the user"""
    fullscreen = False
    width = 640
    height = 480
    bigmapwidth = 1024
    bigmapheight = 800
    fps = 60
    xtiles = 15 # how many grid tiles for x axis
    ytiles = 15 # how many grid tiles for y axis
    title = "Esc: quit"
    scrollstepx = 3 # how many pixels to scroll when pressing cursor key
    scrollstepy = 3 # how many pixels to scroll when pressing cursor key
    cornerpoint = [0,0] # left upper edge of visible screen rect inside bigmap
    radarmapwidth = 200
    radarmapheight = 150

class Text(pygame.sprite.Sprite):
    """ a helper class to write text on the screen """
    number = 0 
    book = {}
    def __init__(self, pos, msg):
        self.number = Text.number # get a unique number
        Text.number += 1 # prepare number for next Textsprite
        Text.book[self.number] = self # store myself into the book
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.msg = msg
        self.changemsg(msg)
        
    def update(self, seconds):        
        pass
        
    def changemsg(self,msg):
        self.msg = msg
        self.image = write(self.msg)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0] 
        self.rect.centery = self.pos[1]
        
class Bullet(pygame.sprite.Sprite):
    """ a big projectile fired by the tank's main cannon"""
    side = 7 # small side of bullet rectangle
    vel = 180 # velocity
    mass = 50
    maxlifetime = 10.0 # seconds
    book = {}
    number = 0
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.number = Bullet.number 
        Bullet.number += 1
        Bullet.book[self.number] = self # add myself into the bulletbook
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.tracer = False # the tracer class will have self.tracer = True
        self.lifetime = 0.0
        self.color = self.boss.color
        self.calculate_heading() # !!!!!!!!!!!!!!!!!!!
        self.dx += self.boss.dx
        self.dy += self.boss.dy # add boss movement
        self.pos = self.boss.pos[:] # copy (!!!) of boss position 
        #self.pos = self.boss.pos   # uncomment this linefor fun effect
        self.calculate_origin()
        self.update() # to avoid ghost sprite in upper left corner,  force position calculation.
                      
    def calculate_heading(self):
        """ drawing the bullet and rotating it according to it's launcher"""
        self.radius = Bullet.side # for collision detection
        self.angle += self.boss.turretAngle
        self.mass = Bullet.mass
        self.vel = Bullet.vel
        image = pygame.Surface((Bullet.side * 2, Bullet.side)) # rect 2 x 1
        image.fill((128,128,128)) # fill grey
        pygame.draw.rect(image, self.color, (0,0,int(Bullet.side * 1.5), Bullet.side)) # rectangle 1.5 length
        pygame.draw.circle(image, self.color, (int(self.side *1.5) ,self.side//2), self.side//2) #  circle
        pygame.draw.circle(image, (0,0,0), (int(Bullet.side * 1.5) , Bullet.side // 2) , 2) # point circle
        image.set_colorkey((128,128,128)) # grey transparent
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        self.dx = math.cos(degrees_to_radians(self.boss.turretAngle)) * self.vel
        self.dy = math.sin(degrees_to_radians(-self.boss.turretAngle)) * self.vel
        
    def calculate_origin(self):
        # - spawn bullet at end of turret barrel instead tank center -
        # cannon is around Tank.side long, calculatet from Tank center
        # later subtracted 20 pixel from this distance
        # so that bullet spawns closer to tank muzzle
        self.pos[0] +=  math.cos(degrees_to_radians(self.boss.turretAngle)) * (Tank.side-20)
        self.pos[1] +=  math.sin(degrees_to_radians(-self.boss.turretAngle)) * (Tank.side-20)
 
    def kill(self):
        # overwriting this function to kill myself out of the bullet book correctly
        del Bullet.book[self.number] # delete myself out of the book
        pygame.sprite.Sprite.kill(self) # call the kill function
 
    def update(self, seconds=0.0):
        # ---- kill if too old ---
        self.lifetime += seconds
        if self.lifetime > Bullet.maxlifetime:
            self.kill()
        # ------ calculate movement --------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        # ----- kill if out of screen
        if self.pos[0] < 0:
            self.kill()
        elif self.pos[0] > Config.bigmapwidth:
            self.kill()
        if self.pos[1] < 0:
            self.kill()
        elif self.pos[1] > Config.bigmapheight:
            self.kill()
        #------- move -------
        self.rect.centerx = round(self.pos[0] - Config.cornerpoint[0],0)
        self.rect.centery = round(self.pos[1] - Config.cornerpoint[1],0)
        
class Tracer(Bullet):
    """Tracer is nearly the same as Bullet, but smaller
       and with another origin (bow MG rect instead cannon.
       Tracer inherits all methods of Bullet, but i overwrite
       calculate_heading and calculate_origin"""
    side = 15 # long side of bullet rectangle
    vel = 200 # velocity
    mass = 10
    color = (200,0,100)
    maxlifetime = 10.0 # seconds
    def __init__(self, boss, turret=False):
        self.turret = turret
        Bullet.__init__(self,boss ) # this line is important 
        self.tracer = True
        
    def calculate_heading(self):
        """overwriting the method because there are some differences 
           between a tracer and a main gun bullet"""
        self.radius = Tracer.side # for collision detection
        self.angle = 0
        self.angle += self.boss.tankAngle
        if self.turret:
            self.angle = self.boss.turretAngle
        self.mass = Tracer.mass
        self.vel = Tracer.vel
        image = pygame.Surface((Tracer.side, Tracer.side // 4)) # a line 
        image.fill(self.boss.color) # fill yellow ? 
        pygame.draw.rect(image, (0,0,0), (Tracer.side * .75, 0, Tracer.side, Tracer.side // 4)) # red dot at front
        image.set_colorkey((128,128,128)) # grey transparent
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        if self.turret:
            # turret mg
            self.dx = math.cos(degrees_to_radians(self.boss.turretAngle)) * self.vel
            self.dy = math.sin(degrees_to_radians(-self.boss.turretAngle)) * self.vel
        else:
            # bow mg
            self.dx = math.cos(degrees_to_radians(self.boss.tankAngle)) * self.vel
            self.dy = math.sin(degrees_to_radians(-self.boss.tankAngle)) * self.vel

    def calculate_origin(self):
        """overwriting because another point of origin is needed"""
        # - spawn bullet at end of machine gun muzzle (bow or turret)
        if self.turret:
            self.pos[0] +=  math.cos(degrees_to_radians(-90+self.boss.turretAngle)) * 15
            self.pos[1] +=  math.sin(degrees_to_radians(90-self.boss.turretAngle)) * 15
        else:
            self.pos[0] +=  math.cos(degrees_to_radians(30+self.boss.tankAngle)) * (Tank.side/2)
            self.pos[1] +=  math.sin(degrees_to_radians(-30-self.boss.tankAngle)) * (Tank.side/2)
        
class Radarmap(pygame.sprite.Sprite):
    """a classic radarmap of the bigmap, 
    to be displayed alsways in the upper right corner 
    of the screen. With colored dots for the tanks
    and a rect for the visible screen area"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.image = pygame.Surface((Config.radarmapwidth, Config.radarmapheight))
        self.paintmap() # self image's color is not defined, therfore it remains black
        self.rect = self.image.get_rect()
        self.rect.topleft = (Config.width - Config.radarmapwidth, 0) # topleft is a pygame variable
        self.factorx = Config.radarmapwidth  * 1.0 / Config.bigmapwidth # 1.0 to force decimapl point calculation 
        self.factory = Config.radarmapheight *1.0 / Config.bigmapheight
        
    def paintmap(self):
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image, (150,0,0), (0,0, Config.radarmapwidth, Config.radarmapheight),1)    
    
    def update(self, seconds):
        self.paintmap() # redraw black map # outcomment for funny painting effect
        # draw a withe rect to show the visible area of the bigmap
        pygame.draw.rect(self.image, (255,255,255), (round(Config.cornerpoint[0] * self.factorx,0),
                                                     round(Config.cornerpoint[1] * self.factory,0),
                                                     round(Config.width * self.factorx, 0),
                                                     round(Config.height * self.factory, 0)),1)
        for tanknumber in Tank.book: # tank are circles with radius 4
            pos = Tank.book[tanknumber].pos
            color = Tank.book[tanknumber].color
            pygame.draw.circle(self.image,color, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)), 4 )
        for bulletnumber in Bullet.book:
            if Bullet.book[bulletnumber].tracer:
                dotlength = 2 # bullets are rectangles with sidelength 4 (bullets) or 2 (tracer)
            else:
                dotlength = 4 # rect with length 1 is not visible
            pos = Bullet.book[bulletnumber].pos
            color = Bullet.book[bulletnumber].color
            pygame.draw.rect(self.image, color,(int(pos[0] * self.factorx),
                                                int(pos[1] * self.factory),
                                                dotlength, dotlength))
    
class Tank(pygame.sprite.Sprite):
    """ A Tank, controlled by the Player with Keyboard commands.
    This Tank draw it's own Turret (including the main gun) 
    and it's bow rectangle (slit for Tracer Machine Gun"""
    side = 100 # side of the quadratic tank sprite
    recoiltime = 0.75 # how many seconds  the cannon is busy after firing one time
    mgrecoiltime = 0.2 # how many seconds the bow mg (machine gun) is idle
    turretTurnSpeed = 50 # turret
    tankTurnSpeed = 80 # tank
    movespeed = 80
    #maxrotate = 360 # maximum amount of degree the turret is allowed to rotate
    book = {} # a book of tanks to store all tanks
    number = 0 # each tank gets his own number
    # keys for tank control, expand if you need more tanks
    #          player1,        player2    etc
    firekey = (pygame.K_k, pygame.K_KP0)
    mgfirekey = (pygame.K_LCTRL, pygame.K_KP_ENTER)
    mg2firekey = (pygame.K_i, pygame.K_KP_PLUS)
    turretLeftkey = (pygame.K_j, pygame.K_KP7)
    turretRightkey = (pygame.K_l, pygame.K_KP9)
    forwardkey = (pygame.K_w, pygame.K_KP8)
    backwardkey = (pygame.K_s, pygame.K_KP5)
    tankLeftkey = (pygame.K_a, pygame.K_KP4)
    tankRightkey = (pygame.K_d, pygame.K_KP6)
    color = ((200,200,0), (100,100,255))
    #msg = ["wasd LCTRL, ijkl", "Keypad: 4852, ENTER, cursor"]
          
    def __init__(self, startpos = (150,150), angle=0):
        self.number = Tank.number # now i have a unique tank number
        Tank.number += 1 # prepare number for next tank
        Tank.book[self.number] = self # store myself into the tank book
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.pos = [startpos[0], startpos[1]] # x,y
        self.dx = 0
        self.dy = 0
        self.ammo = 30 # main gun
        self.mgammo = 500 # machinge gun
        self.color = Tank.color[self.number]
        self.turretAngle = angle #turret facing
        self.tankAngle = angle # tank facing
        self.msg =  "tank%i: x:%i y:%i facing: turret:%i tank:%i"  % (self.number, self.pos[0], self.pos[1], self.turretAngle, self.tankAngle )
        #Text((Config.width/2, 30+20*self.number), self.msg) # create status line text sprite
        self.firekey = Tank.firekey[self.number] # main gun
        self.mgfirekey = Tank.mgfirekey[self.number] # bow mg
        self.mg2firekey = Tank.mg2firekey[self.number] # turret mg
        self.turretLeftkey = Tank.turretLeftkey[self.number] # turret
        self.turretRightkey = Tank.turretRightkey[self.number] # turret
        self.forwardkey = Tank.forwardkey[self.number] # move tank
        self.backwardkey = Tank.backwardkey[self.number] # reverse tank
        self.tankLeftkey = Tank.tankLeftkey[self.number] # rotate tank
        self.tankRightkey = Tank.tankRightkey[self.number] # rotat tank
        # painting facing north, have to rotate 90° later
        image = pygame.Surface((Tank.side,Tank.side)) # created on the fly
        image.fill((128,128,128)) # fill grey
        if self.side > 10:
             pygame.draw.rect(image, self.color, (5,5,self.side-10, self.side-10)) #tank body, margin 5
             pygame.draw.rect(image, (90,90,90), (0,0,self.side//6, self.side)) # track left
             pygame.draw.rect(image, (90,90,90), (self.side-self.side//6, 0, self.side,self.side)) # right track
             pygame.draw.rect(image, (255,0,0), (self.side//6+5 , 10, 10, 5)) # red bow rect left
             #pygame.draw.rect(image, (255,0,0), (self.side/2 - 5, 10, 10, 5)) # red bow rect middle
        pygame.draw.circle(image, (255,0,0), (self.side//2,self.side//2), self.side//3 , 2) # red circle for turret
        image = pygame.transform.rotate(image,-90) # rotate so to look east
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        #---------- turret ------------------
        self.firestatus = 0.0 # time left until cannon can fire again
        self.mgfirestatus = 0.0 # time until mg can fire again
        self.mg2firestatus = 0.0 # time until turret mg can fire again
        self.turndirection = 0    # for turret
        self.tankturndirection = 0
        self.movespeed = Tank.movespeed
        self.turretTurnSpeed = Tank.turretTurnSpeed
        self.tankTurnSpeed = Tank.tankTurnSpeed
        Turret(self) # create a Turret for this tank
        
    def update(self, seconds):  # no need for seconds but the other sprites need it
        #-------- reloading, firestatus----------
        if self.firestatus > 0:
            self.firestatus -= seconds # cannon will soon be ready again
            if self.firestatus <0:
                self.firestatus = 0 #avoid negative numbers
        if self.mgfirestatus > 0:
            self.mgfirestatus -= seconds # bow mg will soon be ready again
            if self.mgfirestatus <0:
                self.mgfirestatus = 0 #avoid negative numbers
        if self.mg2firestatus > 0:
            self.mg2firestatus -= seconds # turret mg will soon be ready again
            if self.mg2firestatus <0:
                self.mg2firestatus = 0 #avoid negative numbers
        
        # ------------ keyboard --------------
        pressedkeys = pygame.key.get_pressed()
        # -------- turret manual rotate ----------
        self.turndirection = 0    #  left / right turret rotation
        if self.number == 1:   # only for tank2
            self.aim_at_player()       # default aim at player0
        else:
            if pressedkeys[self.turretLeftkey]:
                self.turndirection += 1
            if pressedkeys[self.turretRightkey]:
                self.turndirection -= 1
           
        #---------- tank rotation ---------
        self.tankturndirection = 0 # reset left/right rotation
        if pressedkeys[self.tankLeftkey]:
            self.tankturndirection += 1
        if pressedkeys[self.tankRightkey]:
            self.tankturndirection -= 1
        
        # ---------------- rotate tank ---------------
        self.tankAngle += self.tankturndirection * self.tankTurnSpeed * seconds # time-based turning of tank
        # angle etc from Tank (boss)
        oldcenter = self.rect.center
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image0, self.tankAngle) 
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter 
        # if tank is rotating, turret is also rotating with tank !
        # -------- turret autorotate ----------
        self.turretAngle += self.tankturndirection * self.tankTurnSpeed * seconds  + self.turndirection * self.turretTurnSpeed * seconds # time-based turning
        # ---------- fire cannon -----------
        if (self.firestatus ==0) and (self.ammo > 0):
            if pressedkeys[self.firekey]:
                self.firestatus = Tank.recoiltime # seconds until tank can fire again
                Bullet(self)    
                self.ammo -= 1
                #self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.mgammo, Tank.msg[self.number])
                #Text.book[self.number].changemsg(self.msg)
        # -------- fire bow mg ---------------
        if (self.mgfirestatus ==0) and (self.mgammo >0):
            if pressedkeys[self.mgfirekey]:
                self.mgfirestatus = Tank.mgrecoiltime
                Tracer(self, False) # turret mg = False
                self.mgammo -= 1
                #self.msg = "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.mgammo, Tank.msg[self.number])
                #Text.book[self.number].changemsg(self.msg)
        # -------- fire turret mg ---------------
        if (self.mg2firestatus ==0) and (self.mgammo >0):
            if pressedkeys[self.mg2firekey]:
                self.mg2firestatus = Tank.mgrecoiltime # same recoiltime for both mg's
                Tracer(self, True) # turret mg = True
                self.mgammo -= 1
                #self.msg =  "player%i: ammo: %i/%i keys: %s" % (self.number+1, self.ammo, self.mgammo, Tank.msg[self.number])
                #Text.book[self.number].changemsg(self.msg)
        # ---------- movement ------------
        self.dx = 0
        self.dy = 0
        self.forward = 0 # movement calculator
        if pressedkeys[self.forwardkey]:
            self.forward += 1
        if pressedkeys[self.backwardkey]:
            self.forward -= 1
        # if both are pressed togehter, self.forward becomes 0
        if self.forward == 1:
            self.dx =  math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy =  -math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        if self.forward == -1:
            self.dx =  -math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy =  math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        # ------------- check border collision ---------------------
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        if self.pos[0] + self.side/2 >= Config.bigmapwidth:
            self.pos[0] = Config.bigmawidth - self.side/2
            self.dx = 0 # crash into border
        elif self.pos[0] -self.side/2 <= 0:
            self.pos[0] = 0 + self.side/2
            self.dx = 0
        if self.pos[1] + self.side/2 >= Config.bigmapheight:
            self.pos[1] = Config.bigmapheight - self.side/2
            self.dy = 0 # crash into border
        elif self.pos[1] -self.side/2 <= 0:
            self.pos[1] = 0 + self.side/2
            self.dy = 0    
        
        self.rect.centerx = round(self.pos[0] - Config.cornerpoint[0], 0) #x
        self.rect.centery = round(self.pos[1] - Config.cornerpoint[1], 0) #y    
        #self.msg =  "tank%i: x:%i y:%i facing: turret:%i tank:%i"  % (self.number, self.pos[0], self.pos[1], self.turretAngle, self.tankAngle )
                    
    def aim_at_player(self, targetnumber=0):
        deltax = Tank.book[targetnumber].pos[0] - self.pos[0]
        deltay = Tank.book[targetnumber].pos[1] - self.pos[1]
        angle =   math.atan2(-deltax, -deltay)/math.pi*180.0    
        
        diff = (angle - self.turretAngle - 90) %360 #reset at 360
        diff -= 180
        # to avoid a jittering canon introduce a tolerance range of 4 degrees
        if abs(diff) < 2:
            self.turndirection = 0
        elif diff > 0:
            self.turndirection = 1
        else:
            self.turndirection = -1
        # return diff
     
     
class Turret(pygame.sprite.Sprite):
    """turret on top of tank"""
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups) # THE most important line !
        self.boss = boss
        self.side = self.boss.side
        self.images = {} # how much recoil after shooting, reverse order of apperance
        self.images[0] = self.draw_cannon(0)  # idle position
        self.images[1] = self.draw_cannon(1)
        self.images[2] = self.draw_cannon(2)
        self.images[3] = self.draw_cannon(3)
        self.images[4] = self.draw_cannon(4)
        self.images[5] = self.draw_cannon(5)
        self.images[6] = self.draw_cannon(6)
        self.images[7] = self.draw_cannon(7)
        self.images[8] = self.draw_cannon(8)  # position of max recoil
        self.images[9] = self.draw_cannon(4)
        self.images[10] = self.draw_cannon(0) # idle position
         
    def update(self, seconds):        
        # painting the correct image of cannon
        if self.boss.firestatus > 0:
            self.image = self.images[int(self.boss.firestatus // (Tank.recoiltime / 10.0))]
        else:
            self.image = self.images[0]
        # --------- rotating -------------
        # angle etc from Tank (boss)
        oldrect = self.image.get_rect() # store current surface rect
        self.image  = pygame.transform.rotate(self.image, self.boss.turretAngle) 
        self.rect = self.image.get_rect()
        # ---------- move with boss ---------
        self.rect = self.image.get_rect()
        self.rect.center = self.boss.rect.center
    
    def draw_cannon(self, offset):
         # painting facing right, offset is the recoil
         image = pygame.Surface((self.boss.side * 2,self.boss.side * 2)) # created on the fly
         image.fill((128,128,128)) # fill grey
         pygame.draw.circle(image, (255,0,0), (self.side,self.side), 22, 0) # red circle
         pygame.draw.circle(image, (0,255,0), (self.side,self.side), 18, 0) # green circle
         pygame.draw.rect(image, (255,0,0), (self.side-10, self.side + 10, 15,2)) # turret mg rectangle
         pygame.draw.rect(image, (0,255,0), (self.side-20 - offset,self.side - 5, self.side - offset,10)) # green cannon
         pygame.draw.rect(image, (255,0,0), (self.side-20 - offset,self.side - 5, self.side - offset,10),1) # red rect 
         image.set_colorkey((128,128,128))
         return image
# ---------------- End of classes --------------------

#------------ defs ------------------
def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0

def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)

def write(msg="pygame is cool"):
    """helper function for the Text sprite"""
    myfont = pygame.font.SysFont("None", 28)
    mytext = myfont.render(msg, True, (255,255,255))
    mytext = mytext.convert_alpha()
    return mytext        

def main():
    """the game itself"""
    pygame.init()
    screen=pygame.display.set_mode((Config.width,Config.height)) 
    # note that "map" is an pygame function and can not be used as a name for a variable
    bigmap = pygame.Surface((Config.bigmapwidth, Config.bigmapheight))
    # ----------------- create bigmap -------------------
    bigmap.fill((128,128,128)) # fill grey 
    # paint a grid of dark lines
    for x in range(0,Config.bigmapwidth,Config.bigmapwidth//Config.xtiles): #start, stop, step
        pygame.draw.line(bigmap, (64,64,64), (x,0), (x,Config.bigmapheight))
    for y in range(0,Config.bigmapheight,Config.bigmapheight//Config.ytiles): #start, stop, step
        pygame.draw.line(bigmap, (64,64,64), (0,y), (Config.bigmapwidth,y))
    pygame.draw.rect(bigmap, (255,0,0), (0,0,Config.bigmapwidth, Config.bigmapheight), 25) # red bigmap edge
    # paint thin red cross in the middle of the map
    pygame.draw.line(bigmap, (200,0,0), (Config.bigmapwidth /2, 0),( Config.bigmapwidth / 2, Config.bigmapheight),1)
    pygame.draw.line(bigmap, (200,0,0), (0, Config.bigmapheight/2),( Config.bigmapwidth , Config.bigmapheight/2),1)
    bigmap = bigmap.convert()
    # ------- background is a subsurface of bigmap ----------
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background = bigmap.subsurface((Config.cornerpoint[0],
                                    Config.cornerpoint[1],
                                    Config.width,
                                    Config.height)) # take snapshot of bigmap
    # -----------------------------------
    background = background.convert()
    screen.blit(background, (0,0)) # delete all
    clock = pygame.time.Clock()    # create pygame clock object
    FPS = Config.fps               # desired max. framerate 
    playtime = 0
    
    tankgroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    allgroup = pygame.sprite.LayeredUpdates()
    
    Tank._layer = 4   # base layer
    Bullet._layer = 7 # to prove that Bullet is in top-layer
    Tracer._layer = 5 # above Tank, but below Turret
    Turret._layer = 6 # above Tank & Tracer
    Text._layer = 3   # below Tank
    Radarmap._layer = 3  # below Tank # better 9 ?
 
    #assign default groups to each sprite class
    Tank.groups = tankgroup, allgroup
    Turret.groups = allgroup 
    Bullet.groups = bulletgroup, allgroup
    Text.groups = allgroup # text does not move with map !
    Radarmap.groups = allgroup # radar does not move with map
    
    player1 = Tank((150,250), 90) # create  first tank, looking north
    player2 = Tank((450,250), 90) # create second tank, looking south
    Radarmap() # there is only one radarmap, so no variable assigned to it
     
    status3 = Text((155, 25), "cursor keys to scroll the map,")
    status3 = Text((155, 45), "tanks: keypad, wasd, ijkl, lctrl")
    mainloop = True           
    while mainloop:
        milliseconds = clock.tick(Config.fps)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # exit game
            # teleport player1 tank if left mousebutton is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    #left mousebutton was pressed
                    player1.pos[0]=pygame.mouse.get_pos()[0] + Config.cornerpoint[0]
                    player1.pos[1]=pygame.mouse.get_pos()[1] + Config.cornerpoint[1]
                    
        # -------- scroll the big map ----------
        scrollx = 0
        scrolly = 0
        pressedkeys = pygame.key.get_pressed()
        # --- handle Cursor keys to scroll map ----
        if pressedkeys[pygame.K_LEFT]:
             scrollx -= Config.scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
             scrollx += Config.scrollstepx
        if pressedkeys[pygame.K_UP]:
             scrolly -= Config.scrollstepy
        if pressedkeys[pygame.K_DOWN]:
             scrolly += Config.scrollstepy
        # -------- scroll the visible part of the map ------
        Config.cornerpoint[0] += scrollx
        Config.cornerpoint[1] += scrolly
        #--------- do not scroll out of bigmap edge -----
        if Config.cornerpoint[0] < 0:
            Config.cornerpoint[0] = 0
            scrollx = 0
        elif Config.cornerpoint[0] > Config.bigmapwidth - Config.width:
            Config.cornerpoint[0] = Config.bigmapwidth - Config.width
            scrollx = 0
        if Config.cornerpoint[1] < 0:
            Config.cornerpoint[1] = 0
            scrolly = 0
        elif Config.cornerpoint[1] > Config.bigmapheight - Config.height:
            Config.cornerpoint[1] = Config.bigmapheight - Config.height
            scrolly = 0
        
        pygame.display.set_caption("%s FPS: %.2f playtime: %.1f " % ( Config.title,clock.get_fps(), playtime))
        #screen.blit(background, (0,0)) # delete all
        if scrollx == 0 and scrolly == 0:    # only necessery if there was no scrolling
            allgroup.clear(screen, background) # funny effect if you outcomment this line
        else:
            background = bigmap.subsurface((Config.cornerpoint[0],
                                            Config.cornerpoint[1],
                                            Config.width,
                                            Config.height)) # take snapshot of bigmap
            screen.blit(background, (0,0))
        allgroup.update(seconds) 
        allgroup.draw(screen)
        pygame.display.flip() # flip the screen 30 times a second
    return 0

if __name__ == '__main__':
    main()
