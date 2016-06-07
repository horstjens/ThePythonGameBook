#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
019_homing_missiles.py
2-player game with homing missiles
url: http://thepythongamebook.com/en:part2:pygame:step019
author: horst.jens@spielend-programmieren.at
physic by Leonard Michlmayr
licence: gpl, see http://www.gnu.org/licenses/gpl.html

2 player can shoot at each other and/or at monster(s).
2 types of homing missiles (can also be shot down)
create new monsters with key m

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
    screen=pygame.display.set_mode((1800,1000)) # try out larger values and see what happens !
    screenrect = screen.get_rect()
    #winstyle = 0  # |FULLSCREEN # Set the display mode
    #print "pygame version", pygame.ver 
    # ------- game constants ----------------------
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
        For an instance of a XWing class, it will return 'XWing'."""
        text = str(class_instance.__class__) # like "<class '__main__.XWing'>"
        parts = text.split(".") # like ["<class '__main__","XWing'>"]
        return parts[-1][0:-2] # from the last (-1) part, take all but the last 2 chars
    
    def radians_to_degrees(radians):
        return (radians / math.pi) * 180.0
    
    def degrees_to_radians(degrees):
        return degrees * (math.pi / 180.0)
    
    def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .pos[0], .pos[1], .dx, dy
           pos[0] is the x postion, pos[1] the y position"""
        # here we do some physics: the elastic
        # collision
        # first we get the direction of the push.
        # Let's assume that the sprites are disk
        # shaped, so the direction of the force is
        # the direction of the distance.
        dirx = sprite1.pos[0] - sprite2.pos[0]
        diry = sprite1.pos[1] - sprite2.pos[1]
        # the velocity of the centre of mass
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        # if we sutract the velocity of the centre
        # of mass from the velocity of the sprite,
        # we get it's velocity relative to the
        # centre of mass. And relative to the
        # centre of mass, it looks just like the
        # sprite is hitting a mirror.
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        # (dirx,diry) is perpendicular to the mirror
        # surface. We use the dot product to
        # project to that direction.
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            # no distance? this should not happen,
            # but just in case, we choose a random
            # direction
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        # We are done. (dirx * dp, diry * dp) is
        # the projection of the velocity
        # perpendicular to the virtual mirror
        # surface. Subtract it twice to get the
        # new direction.
        # Only collide if the sprites are moving
        # towards each other: dp > 0
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp
    
    # ----------- classes ------------------------

    class Text(pygame.sprite.Sprite):
        """a pygame Sprite displaying text"""
        def __init__(self, msg="The Python Game Book", color=(0,0,0), topleft=(0,0)):
            self.groups = allgroup
            self.topleft = topleft
            self._layer = 1
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.newmsg(msg,color)
            
        def update(self, time):
            pass # allgroup sprites need update method that accept time
        
        def newmsg(self, msg, color=(0,0,0)):
            self.image =  write(msg,color)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.topleft

    class Lifebar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a GameObject sprite
           with a given bossnumber, the Lifebar class can 
           identify the boss (GameObject sprite) with this codeline:
           GameObject.gameobjects[self.bossnumber] """
        def __init__(self, boss):
            self.groups = allgroup
            self.boss = boss
            self._layer = self.boss._layer
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.oldpercent = 0
            self.color = (0,255,0)
            self.distance = 10
            self.paint()
            self.oldangle = self.boss.angle # store angle of boss to redraw bar if boss is rotating
            
        def paint(self):
            self.image = pygame.Surface((self.boss.rect.width,7))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,self.boss.rect.width,7),1)
            self.rect = self.image.get_rect()
 
        def recalc(self):
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
 
        def update(self, time):
            self.recalc()
            #self.paint()
            if (self.percent != self.oldpercent) or (self.oldangle != self.boss.angle):
                self.oldangle = self.boss.angle # store angle of boss
                self.paint() # important ! boss.rect.width may have changed (because rotating)
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,5)) # fill black
                pygame.draw.rect(self.image, self.color, (1,1,
                                 int(self.boss.rect.width * self.percent),5),0) # fill green
            self.oldpercent = self.percent
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - self.distance
            if GameObject.gameobjects[self.boss.number] == None:
                self.kill() # kill the hitbar
    
    class Rocketbar(Lifebar):
        """shows a bar to indicate the stock of rockets."""
        def __init__(self, boss):
            Lifebar.__init__(self,boss)
            self.color = (0,0,128)
            self.distance = 16
        
        def recalc(self):
            if self.boss.rockets > self.boss.rocketsmax / 2:
                self.color = (0,0,255)
            else:
                self.color = (0,0,128)
            self.percent = self.boss.rockets / self.boss.rocketsmax * 1.0
        
    class GameObject(pygame.sprite.Sprite):
        """generic Game Object Sprite class, to be called from every Sprite
           with a physic collision (Player, Rocket, Monster, Bullet)
           need self.image and self.image0 and self.groups to be set
           need self.rect and self.pos to be set
           self.hitpoints must be set to a float, also self.hitpointsfull"""
        image=[]  # list of all images
        gameobjects = {} # a dictionary of all GameObjects, each GameObject has its own number
        number = 0  
        #def __init__(self, pos, layer= 4, area=screenrect, areastop = False, areabounce = False, angle=0, speedmax = 500, friction = 0.95, lifetime = -1):
        def __init__(self, layer= 4, area=screenrect, areastop = False, areabounce = False, angle=0, speedmax = 500, friction = 0.95, lifetime = -1):
            #self.pos = pos
            self._layer = layer                   # assign level
            self.area = area
            self.areastop = areastop
            self.areabounce = areabounce
            self.angle = angle 
            self.oldangle = angle
            self.speedmax = speedmax
            self.friction = friction # between 0 and 1, 1 means no friction, 0 means no more movement is possible
            self.lifetime = lifetime # -1 means infinite lifetime
            pygame.sprite.Sprite.__init__(self,  self.groups  ) #---------------call parent class. NEVER FORGET !
            self.alivetime = 0.0 # how long does this GameObject exist ?
            self.bouncefriction = -0.5 # how much speed is lost by bouncing off a wall. 1 means no loss, 0 means full stop
            self.dx = 0   # wait at the beginning
            self.dy = 0            
            self.number = GameObject.number # get my personal GameObject number
            GameObject.number+= 1           # increase the number for next GameObject
            GameObject.gameobjects[self.number] = self # store myself into the GameObject dictionary
          
        def speedcheck(self):
            speed = (self.dx**2 + self.dy**2)**0.5 ## calculate total speed
            if speed > self.speedmax:
                factor = self.speedmax / speed * 1.0
                self.dx *= factor
                self.dy *= factor
            else:
                self.color = (0,0,128)
            self.percent = self.boss.rockets / self.boss.rocketsmax * 1.0
        
    class GameObject(pygame.sprite.Sprite):
        """generic Game Object Sprite class, to be called from every Sprite
           with a physic collision (Player, Rocket, Monster, Bullet)
           need self.image and self.image0 and self.groups to be set
           need self.rect and self.pos to be set
           self.hitpoints must be set to a float, also self.hitpointsfull"""
        image=[]  # list of all images
        gameobjects = {} # a dictionary of all GameObjects, each GameObject has its own number
        number = 0  
        #def __init__(self, pos, layer= 4, area=screenrect, areastop = False, areabounce = False, angle=0, speedmax = 500, friction = 0.95, lifetime = -1):
        def __init__(self, layer= 4, area=screenrect, areastop = False, areabounce = False, angle=0, speedmax = 500, friction = 0.95, lifetime = -1):
            #self.pos = pos
            self._layer = layer                   # assign level
            self.area = area
            self.areastop = areastop
            self.areabounce = areabounce
            self.angle = angle 
            self.oldangle = angle
            self.speedmax = speedmax
            self.friction = friction # between 0 and 1, 1 means no friction, 0 means no more movement is possible
            self.lifetime = lifetime # -1 means infinite lifetime
            pygame.sprite.Sprite.__init__(self,  self.groups  ) #---------------call parent class. NEVER FORGET !
            self.alivetime = 0.0 # how long does this GameObject exist ?
            self.bouncefriction = -0.5 # how much speed is lost by bouncing off a wall. 1 means no loss, 0 means full stop
            self.dx = 0   # wait at the beginning
            self.dy = 0            
            self.number = GameObject.number # get my personal GameObject number
            GameObject.number+= 1           # increase the number for next GameObject
            GameObject.gameobjects[self.number] = self # store myself into the GameObject dictionary
          
        def speedcheck(self):
            speed = (self.dx**2 + self.dy**2)**0.5 ## calculate total speed
            if speed > self.speedmax:
                factor = self.speedmax / speed * 1.0
                self.dx *= factor
                self.dy *= factor
            #----------- friction -------------            
            if abs(self.dx) > 0 : 
                self.dx *= self.friction  # make the Sprite slower over time
            if abs(self.dy) > 0 :
                self.dy *= self.friction

        def areacheck(self):
            """if GameObject leave self.arena, it is bounced (self.areabounce) or stopped (self.areastop)"""
            if (self.areastop or self.areabounce) and not self.area.contains(self.rect):
                # --- compare self.rect and area.rect
                if self.pos[0] + self.rect.width/2 > self.area.right:
                    self.pos[0] = self.area.right - self.rect.width/2
                    if self.areabounce:
                        self.dx *= self.bouncefriction # bouncing off but loosing speed
                    else:
                        self.dx = 0
                if self.pos[0] - self.rect.width/2 < self.area.left:
                    self.pos[0] = self.area.left + self.rect.width/2
                    if self.areabounce:
                        self.dx *= self.bouncefriction # bouncing off but loosing speed
                    else:
                        self.dx = 0
                if self.pos[1] + self.rect.height/2 > self.area.bottom:
                    self.pos[1] = self.area.bottom - self.rect.height/2
                    if self.areabounce:
                        self.dy *= self.bouncefriction # bouncing off but loosing speed
                    else:
                        self.dy = 0
                if self.pos[1] - self.rect.height/2 < self.area.top:
                    self.pos[1] = self.area.top + self.rect.height/2
                    if self.areabounce:
                        self.dy *= self.bouncefriction # bouncing off but loosing speed
                    else:
                        self.dy = 0
                        
        def rotate_toward_moving(self, dx= None, dy=None):
            if dx is None and dy is None:
                dx = self.dx
                dy = self.dy
            return  math.atan2(-dx, -dy)/math.pi*180.0 
        
        def kill(self):
            GameObject.gameobjects[self.number] =   None # delete sprite from dictionary
            pygame.sprite.Sprite.kill(self) # kill the sprite              
        
        def update(self, seconds):
            self.alivetime += seconds
            # ------- killing --------------
            if self.hitpoints <= 1:
                self.kill()
            if self.lifetime != -1:
                if self.alivetime > self.lifetime:
                    self.kill() # end of natural lifetime
            # --------- rotated ? -------------------
            if self.angle != self.oldangle:            
                self.oldcenter = self.rect.center
                self.image = pygame.transform.rotate(self.image0, self.angle)
                self.rect = self.image.get_rect()
                self.rect.center = self.oldcenter
                self.oldangle = self.angle

            #----------moving ----------------
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            self.speedcheck()    # ------------- movement
            self.areacheck() # ------- check if Bird out of screen
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
    
    class Player(GameObject):
        """a class to hold all players"""
        number = 0
        image = []
        duel = False # duel or cooperative play
        def __init__(self, playernumber = 0):
            self.playernumber = Player.number
            self.bullets_fired = 0
            self.rockets_fired = 0
            self.bullets_hit = 0
            self.rockets_hit = 0
            Player.number += 1 # prepare number for next player 
            self.hitpoints = 450.0
            self.hitpointsfull = 450.0
            self.image = Player.image[self.playernumber] # start with 0
            self.image0 = Player.image[self.playernumber] # start with 0 
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image) # pixelmask ---- necessary ?
            if self.playernumber == 0:
                self.pos = [screen.get_width()/10*2,screen.get_height()-30]
                self.angle = 270
                self.bulletcolor = (200,0,200)
                self.rocket1color = (200,50,50)
                self.rocket2color = (250,100,0)
            elif self.playernumber ==1:
                self.pos = [screen.get_width()/10*8,screen.get_height()-30]
                self.angle = 90
                self.bulletcolor = (0,200,200)
                self.rocket1color = (50,50,200)
                self.rocket2color = (0,200,250)
            # ---------- both players ---------
            self.bulletlifetime = 1.4 # short lifetime, but steals hitpoints
            self.max_abberation = 5.5 # low value means more precise shooting
            self.groups = allgroup, playergroup, gravitygroup
            #  def __init__(self, pos, layer= 4, area=screenrect, areastop = False, areabounce = False, angle=0, speedmax = 500, friction = 0.8, lifetime = -1)
            GameObject.__init__(self, areastop = True, angle = self.angle, speedmax = 300) # ------------------- important ! ----------------------
            self.speed = 200.0 # base movement speed factor
            self.rotatespeed = 3.0 # rotating speed
            self.frags = 100
            Lifebar(self)
            self.cooldowntime = 0.08 #seconds
            self.cooldown = 0.0
            self.rocketcooldowntime = .005 #seconds
            self.rocketcooldown = 0.0
            self.rocketreloadtime = 1.6 # seconds
            self.peacetime = 0.0 # how long no shot was fired
            self.rockets = 0.0   # must be float or bar sprite will not work correctly
            self.rocketsmax = 32.0 # max amount of rockets in stock
                                 # all rockets above rocketsmax/2 are heavy rockets
            Rocketbar(self) # draw bar to indicate how many rockets are left
            self.mass = 400.0
            self.frags = 100
            self.oldangle = -5
            
        def kill(self):
            bombsound.play()
            for _ in range(self.frags):
                RedFragment(self.pos)
            GameObject.kill(self) # call parent method
        
        def get_target_nr(self):
            # select a random monster as target
            if Player.duel:
                if (GameObject.gameobjects[0] is not None) and (GameObject.gameobjects[1] is not None):
                    # both players alive and duel mode, select other player
                    if self.number == 0:
                        return 1
                    else:
                        return 0
                else:
                    Player.duel = False # switch to cooperative mode because only one player is alive
            if not Player.duel and len(Monster.monsters) > 0:
                    return random.choice(Monster.monsters)
            else:
                pass # ------
                
        
        def update(self, seconds):
              pressedkeys = pygame.key.get_pressed()
              self.ddx = 0.0
              self.ddy = 0.0
              self.targetnumber = self.get_target_nr()
              if self.playernumber == 0:
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
              elif self.playernumber == 1:
                    if pressedkeys[pygame.K_KP8]: # forward
                             self.ddx = -math.sin(self.angle*GRAD) 
                             self.ddy = -math.cos(self.angle*GRAD) 
                             Smoke(self.rect.center, -self.ddx , -self.ddy )
                    if pressedkeys[pygame.K_KP5] or pressedkeys[pygame.K_KP2]: # backward
                             self.ddx = +math.sin(self.angle*GRAD) 
                             self.ddy = +math.cos(self.angle*GRAD) 
                             Smoke(self.rect.center, -self.ddx, -self.ddy )
                    if pressedkeys[pygame.K_KP9]: # right side
                             self.ddx = +math.cos(self.angle*GRAD)
                             self.ddy = -math.sin(self.angle*GRAD)
                             Smoke(self.rect.center, -self.ddx , -self.ddy )
                    if pressedkeys[pygame.K_KP7]: # left side
                             self.ddx = -math.cos(self.angle*GRAD) 
                             self.ddy = +math.sin(self.angle*GRAD) 
                             Smoke(self.rect.center, -self.ddx , -self.ddy )                        
              # ------------shoot-----------------
              self.peacetime += seconds # increase peacetime if no shot was fired
              if self.cooldown > 0: # ------ can not shoot
                    self.cooldown -= seconds # pause between bullets
              else: # --------can shoot
                    if ((self.playernumber == 1 and pressedkeys[pygame.K_KP0]) or 
                        (self.playernumber == 0 and pressedkeys[pygame.K_SPACE])): # shoot forward
                            self.ddx = +math.sin(self.angle*GRAD)#recoil
                            self.ddy = +math.cos(self.angle*GRAD)
                            lasersound.play() # play sound
                            Bullet(self, None, self.max_abberation )
                            self.peacetime = 0 # reset peacetime
                            self.cooldown = self.cooldowntime 
                            self.bullets_fired += 1
                            if self.rocketcooldown > 0:
                                self.rocketcooldown -= seconds
                            else:
                                if self.rockets > self.rocketsmax / 2: # heavy sliding rocket
                                    if self.targetnumber is not None:
                                        crysound.play()
                                        Rocket(self,self.targetnumber,1,-30) #boss, target, type, launchangle
                                        Rocket(self,self.targetnumber,1, 30) #boss, target, type, launchangle
                                        self.rockets_fired +=2
                                        self.rockets -= 2
                                        self.rocketcooldown = self.rocketcooldowntime
                                elif self.rockets > 2: # weak seeking rocket
                                    if self.targetnumber is not None:
                                        crysound.play()
                                        Rocket(self,self.targetnumber, 2, -80 )#boss, target, type
                                        Rocket(self,self.targetnumber, 2, 80 )#boss, target, type
                                        self.rockets_fired += 2
                                        self.rockets -= 2
                                        self.rocketcooldown = self.rocketcooldowntime
              #----- add more rockets --------
              if self.peacetime > self.rocketreloadtime:
                  self.rockets += 2
                  self.peacetime = 0
              #-------------rotate----------------
              if self.playernumber == 0:
                    if pressedkeys[pygame.K_a]: # left turn , counterclockwise
                        self.angle += self.rotatespeed
                    if pressedkeys[pygame.K_d]: # right turn, clockwise
                        self.angle -= self.rotatespeed
              elif self.playernumber == 1:
                    if pressedkeys[pygame.K_KP4]: # left turn , counterclockwise
                        self.angle += self.rotatespeed
                    if pressedkeys[pygame.K_KP6]: # right turn, clockwise
                        self.angle -= self.rotatespeed
              # ------------move------------------
              self.dx += self.ddx * self.speed 
              self.dy += self.ddy * self.speed
              # ----- move, rotate etc. ------------  
              GameObject.update(self, seconds)# ------- calll parent function 
            
    class Monster(GameObject):
        """neutral Monster, hunt both players"""
        image = []
        monsters=[]
        def __init__(self, pos=screenrect.center):
            self.groups = allgroup, gravitygroup, playergroup, monstergroup
            self.image = Monster.image[0]
            self.bullets_fired = 0
            self.rockets_fired = 0
            self.bullets_hit = 0
            self.bulletcolor=(0,128,0)
            self.bulletlifetime = 2.8 # longer lifetime than player's bullet, but no lifestealing effect
            self.max_abberation = 6
            self.rocket1color = (20,random.randint(200,255),80)
            self.rocket2color = (20,random.randint(200,255),80)
            self.rockets_hit = 0
            self.rect = self.image.get_rect()
            self.pos = [0.0,0.0]
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.rect.center = pos
            self.hitpoints = 500.0
            self.hitpointsfull = 1000.0
            self.mass = 1000
            self.radius = self.rect.width / 2
            GameObject.__init__(self, layer= 5, area=screenrect, areastop = True, areabounce = True, angle=0, speedmax = 300, friction = 0.95, lifetime = -1)
            Monster.monsters.append(self.number)
            self.frags = 1406 
            self.hunttime = 0.0
            self.targetnumber = self.choose_target_nr()
            self.target = GameObject.gameobjects[self.targetnumber]
            self.playernumber = Player.number
            Player.number += 1
            Lifebar(self)
            self.firetime = 0.0 # how long the fire image is visible
            self.phase =  "nothing" # do not shoot
            self.phases = ["nothing", "bullets", "heavy rockets", "small rockets"]
        
        def kill(self):
            bombsound.play()
            for  _ in range(self.frags):
                RedFragment(self.pos)
            Monster.monsters.remove(self.number)
            GameObject.kill(self)
            
        def choose_target_nr(self):
            # as long as one player exist, target him
            # else, target another monster
            if GameObject.gameobjects[0] is not None and GameObject.gameobjects[1] is not None: # both players alive
               return random.randint(0,1) # choose one of both
            elif GameObject.gameobjects[0] is not None:
                return 0 # choose the surviving player
            elif GameObject.gameobjects[1] is not None:
                return 1 # choose the surviving player
            elif len(monstergroup) > 0: # 1+ Monsters are alive
                mynumber = self.number
                while mynumber == self.number:
                   mynumber = random.choice(Monster.monsters)
                return mynumber
            else:
                return None
                
            
        def update(self, seconds):
            # each second, decide if to hunt player 0 or player 1
            self.hunttime += seconds
            if self.hunttime > 15:
                self.hunttime = 0
                self.targetnumber = self.choose_target_nr()
                self.target = GameObject.gameobjects[self.targetnumber]
            # hunting
            self.image = Monster.image[0] # "normal" xmonster
            if GameObject.gameobjects[self.targetnumber] is not None:
                self.targetdistancex = self.target.pos[0] - self.pos[0]
                self.targetdistancey = self.target.pos[1] - self.pos[1]
                if self.targetdistancex > 0:
                    self.dx += 1
                    if self.targetdistancex > 100:
                        self.image = Monster.image[3] # look right
                        #self.image0 = Monster.image[3] # look right
                elif self.targetdistancex <0:
                    self.dx -= 1
                    if self.targetdistancex < -100:
                        self.image = Monster.image[2] # look left
                        #self.image0 = Monster.image[2] # look left
                if self.targetdistancey > 0:
                    self.dy += 1
                elif self.targetdistancey < 0:
                    self.dy -= 1
                # ----- shoot rockets --------
                # ---- 4 different phases: bullets, heavy rockets, light rockets, pausing
                # ---- chance to change into another phase each full second
                self.phase = self.phases[int(self.alivetime) % 4 ] # fully cycle throug all phases each 3 seconds
                if self.phase == "nothing":
                    pass # do not shoot
                elif self.phase == "bullets":
                    if random.randint(1,2) == 1:
                        Bullet(self, GameObject.rotate_toward_moving(self, self.targetdistancex, self.targetdistancey), self.max_abberation)
                        self.bullets_fired += 1
                        self.firetime = 0.1
                elif self.phase == "heavy rockets":
                    #self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
                    if random.randint(1,50) == 1:
                        Rocket(self, self.targetnumber, 1) # shoot a slow, heavy rocket
                        self.rockets_fired += 1
                        self.firetime = 0.25 # show fire image for this time
                elif self.phase == "small rockets":
                    if random.randint(1,25) == 1:
                        Rocket(self, self.targetnumber, 2) # shoot a small fast rocket
                        self.rockets_fired += 1
                        self.firetime = 0.25 # show fire image for this time
                    
                if self.firetime > 0:
                    self.image = Monster.image[1] # show fire image for monster
                    self.firetime -= seconds    
                else:
                    self.firetime = 0
            GameObject.update(self, seconds)
            
            
    class Fragment(pygame.sprite.Sprite):
        """generic Fragment class. """
        number = 0
        def __init__(self, pos, layer = 9):
            self._layer = layer
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [0.0,0.0]
            self.fragmentmaxspeed = 200# try out other factors !
            self.number = Fragment.number
            Fragment.number += 1
            
        def init2(self):  # split the init method into 2 parts for better access from subclasses
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            self.fragmentradius = random.randint(2,5)
            pygame.draw.circle(self.image, self.color, (5,5), self.fragmentradius)
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
        """explodes outward from (killed) sprite"""
        def __init__(self,pos, stay = False):
            self.groups = allgroup, fragmentgroup, gravitygroup
            Fragment.__init__(self,pos)
            self.stay = stay # if the Fragment stay still or moves
            self.color = (random.randint(25,255),0,0) # red            
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            if self.stay:
                self.dx = 0
                self.dy = 0
            else:
                self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
                self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.lifetime = 0.5 + random.random() # max 1.5 seconds
            self.init2() # continue with generic Fragment class
            self.mass = 48.0
            
    class Wound(Fragment):
        """yellow impact wound that shows the exact location of the hit"""
        def __init__(self, pos, greenmin = 200, greenmax = 255 ):
            self.greenmin = greenmin
            self.greenmax = greenmax
            self.color = ( random.randint(200,255), random.randint(self.greenmin,self.greenmax), random.randint(0,50))
            self.groups = allgroup
            Fragment.__init__(self, pos, 7) # layer
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.lifetime = 1 + random.random()*2 # max 3 seconds
            Fragment.init2(self)
            self.dx = 0
            self.dy = 0
        
        def update(self,time):
            self.color = ( random.randint(200,255), random.randint(self.greenmin,self.greenmax), random.randint(0,50))
            pygame.draw.circle(self.image, self.color, (5,5), self.fragmentradius)
            self.image = self.image.convert_alpha()
            Fragment.update(self, time)
            
    class Smoke(Fragment):
        """black exhaust indicating that the sprite is moved.
           Exhaust direction is inverse of players movement direction"""
        def __init__(self, pos, dx, dy, colmin=1, colmax=50):
           self.color = ( random.randint(colmin,colmax), random.randint(colmin,colmax), random.randint(colmin,colmax) )
           self.groups = allgroup
           Fragment.__init__(self,pos, 3) # give startpos and layer 
           self.pos[0] = pos[0]
           self.pos[1] = pos[1]
           self.lifetime = 0.25 + random.random()*0.5 # 
           Fragment.init2(self)
           self.smokespeed = 120.0 # how fast the smoke leaves the Bird
           self.smokearc = .3 # 0 = thin smoke stream, 1 = 180 Degrees
           arc = self.smokespeed * self.smokearc
           self.dx = dx * self.smokespeed + random.random()*2*arc - arc
           self.dy = dy * self.smokespeed + random.random()*2*arc - arc
           
    class Bullet(GameObject):
        """a bullet flying in the direction of the boss sprite's facing.
           If shooting direction should be independent of boss sprite's facing,
           angle can be given as argument"""
        def __init__(self, boss, myangle = None, max_abberation = 5.5):
            self.boss = boss
            if myangle is None:
                myangle = self.boss.angle 
            self.abberation = random.uniform(-max_abberation,max_abberation) # no shot is perfect
            myangle += self.abberation # spoil the perfect shot
            dx =  -math.sin(myangle*GRAD) 
            dy =  -math.cos(myangle*GRAD)
            self.color = self.boss.bulletcolor
            self.groups = allgroup, bulletgroup, gravitygroup,projectilegroup
            self.lifetime = self.boss.bulletlifetime 
            self.image = pygame.Surface((4,20))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,4,20) )
            pygame.draw.rect(self.image, (10,0,0), (0,0,4,4)) # point
            self.image = self.image.convert_alpha()
            self.image0 = self.image.copy()
            self.rect = self.image.get_rect()
            self.pos = self.boss.pos[:]
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            #GameObject.__init__(self, self.boss.pos, layer= 4, area=screenrect, areastop = False, areabounce = False, angle=self.boss.angle, speedmax = 500, friction = 1.0, lifetime = 1.2)
            GameObject.__init__(self, layer= 4, area=screenrect, areastop = True, areabounce = True, angle=myangle + self.abberation, speedmax = 400, friction = 1.0, lifetime = self.lifetime)
            self.dx = dx * self.speedmax  
            self.dy = dy * self.speedmax
            self.damage = 10
            self.hitpoints = 3
            self.mass = 50
            self.radius = self.rect.width / 2.0
            
        def update(self, seconds):
            self.angle = GameObject.rotate_toward_moving(self)
            #GameObject.speedcheck(self)
            GameObject.update(self, seconds)
            
            
    class Rocket(GameObject):
        """a rocket flying and steering toward a target
           type 1 is a haevy damage, slow-flying, sliding rocket
           type 2 is a light damage, fast-flying, direct seeking rocket"""
        def __init__(self, boss, targetnr, type=1, launchangle = 0):
            self.boss = boss
            if type == 1:   # --------heavy sliding missile ----------
                self.size = 6
                self.color = self.boss.rocket1color
                self.damage = 15
                self.mass = 40
                self.hitpoints = 5 # more hitpoints because less hard to avoid
                self.lifetime = 38 # longer lifetime because less hard to avoid
                self.speed = 50
                self.starttime = 0.9 # missles are launched but are not homing in this time
                rocketfriction = 0.989            
            elif type==2:            # ---------light direct seeking missile ----------------
                self.size = 4
                self.color = self.boss.rocket2color
                self.damage = 5
                self.hitpoints = 2
                self.mass = 10
                self.lifetime = 14
                self.speed = 155 # pixel per second ?
                self.starttime = 0.9 # missles are launched but are not homing in this time
                rocketfriction = 0.99
            self.boss = boss
            self.targetnr = targetnr
            self.target = GameObject.gameobjects[targetnr] # player ?
            self.type = type
            #---------- image --------------
            self.image = pygame.Surface((self.size,20))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,self.size,20) )
            pygame.draw.rect(self.image, (10,0,0), (0,0,self.size,4)) # point
            self.image = self.image.convert_alpha()
            self.image0 = self.image.copy()
            self.rect = self.image.get_rect()
            self.angle = launchangle + self.boss.angle
            self.groups = allgroup, rocketgroup, projectilegroup
            #GameObject.__init__(self, self.boss.pos[:], layer= 8, area=screenrect, areastop = False, areabounce = False, angle=self.angle, speedmax = 800, friction = rocketfriction, lifetime = self.lifetime)
            self.pos = self.boss.pos[:]
            GameObject.__init__(self, layer= 8, area=screenrect, areastop = True, areabounce = False, angle=self.angle, speedmax = 800, friction = rocketfriction, lifetime = self.lifetime)
            self.ddx = -math.sin(self.angle*GRAD) 
            self.ddy = -math.cos(self.angle*GRAD) 
            self.dx = self.ddx * self.speed
            self.dy = self.ddy * self.speed
            self.rotspeed = 5 # grad per second
            self.radius = self.rect.width / 2.0
            self.frags = 5
            self.smokechance = 3 # probability of 1:5 for each frame to launch Smoke
            
        def kill(self):
            #for _ in range(self.frags):
            #    RedFragment(self.pos)
            Wound(self.pos, 0,50)
            GameObject.kill(self)
            
        def update(self, seconds):
            
            self.alivetime += seconds
            if self.alivetime > self.lifetime:
                self.kill() 
            if self.hitpoints < 1:
                self.kill()
            if GameObject.gameobjects[self.targetnr] is None:
                self.kill()
            if self.alivetime < self.starttime:
                #--------- rotate into direction of movement ------------
                self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
            else:
                #-------- rotate toward target
                if self.target is not None:
                    ix = self.target.pos[0] - self.pos[0]
                    iy = self.target.pos[1] - self.pos[1]
                    self.angle = radians_to_degrees(math.atan2(iy,- ix))+90
                self.ddx = -math.sin(self.angle*GRAD)  
                self.ddy = -math.cos(self.angle*GRAD) 
            if self.type == 1: # sliding
                self.dx += self.ddx  #* self.speed
                self.dy += self.ddy  #* self.speed
                if random.randint(1,self.smokechance) ==1:
                    Smoke(self.pos, -self.ddx * 2, -self.ddy * 2)
            elif self.type == 2: #seeking
                self.dx = self.ddx * self.speed
                self.dy = self.ddy * self.speed
                if random.randint(1, self.smokechance) ==1:
                    Smoke(self.pos, -self.ddx, -self.ddy, 25, 75)
            #----------- both ------------
            GameObject.speedcheck(self)
            oldrect = self.rect.center
            self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0) 
            self.rect = self.image.get_rect()   
            self.rect.center = oldrect
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
    #------------- end of classes -----------------
    # ----------------- background artwork -------------  
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white
    background.blit(write("red player:  w,a,s,d,q,e fire: SPACE", (130,130,130)),(50,110))
    background.blit(write("blue player: Numpad 8,4,5,6,7,9 fire: 0", (130,130,130)),(50,140))
    background.blit(write("icrease # of rockets by not firing", (130,130,130)), (50, 170))
    background.blit(write("ESC=quit, m=new monster o=more overtime", (130,130,130)), (50,200))
    background = background.convert()  # jpg can not have transparency
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)
    #-----------------define sprite groups------------------------
    playergroup = pygame.sprite.Group() 
    monstergroup = pygame.sprite.Group()
    bulletgroup = pygame.sprite.Group()
    fragmentgroup = pygame.sprite.Group()
    rocketgroup = pygame.sprite.Group()
    gravitygroup = pygame.sprite.Group()
    projectilegroup = pygame.sprite.Group()
    # only the allgroup draws the sprite, so i use LayeredUpdates() instead Group()
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated, can draw sprites in layers 

    #-------------loading files from data subdirectory -------------------------------
    try:
        Player.image.append(pygame.image.load(os.path.join(folder,"player_red2.png")).convert_alpha())   #0
        Player.image.append(pygame.image.load(os.path.join(folder,"player_blue2.png")).convert_alpha())  #1
        Monster.image.append(pygame.image.load(os.path.join(folder, "xmonster_s.png")).convert_alpha())        #0
        Monster.image.append(pygame.image.load(os.path.join(folder, "xmonster_fire_s.png")).convert_alpha())   #1
        Monster.image.append(pygame.image.load(os.path.join(folder, "xmonster_left_s.png")).convert_alpha())   #2
        Monster.image.append(pygame.image.load(os.path.join(folder, "xmonster_right_s.png")).convert_alpha())  #3

        # ------- load sound -------
        crysound = pygame.mixer.Sound(os.path.join(folder,'claws.ogg'))  #load sound
        warpsound = pygame.mixer.Sound(os.path.join(folder,'wormhole.ogg'))
        bombsound = pygame.mixer.Sound(os.path.join(folder,'bomb.ogg'))
        lasersound = pygame.mixer.Sound(os.path.join(folder,'shoot.ogg'))
        hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))
        impactsound = pygame.mixer.Sound(os.path.join(folder,'explode.ogg'))
    except:
        raise(UserWarning, "Sadly i could not loading all graphic or sound files from %s" % folder)
    
    # ------------- before the main loop ----------------------
    screentext1 = Text("first line", (255,0,255),(0,0))
    screentext2 = Text("second line",(0,0,0),(0,25))
    screentext3 = Text("third line", (255,0,0),(0,50))
    screentext4 = Text("fourth line", (0,0,255),(0,75))
    
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True                    # if False, game ends
    FPS = 60                           # desired max. framerate in frames per second. 
    player1 = Player() # game object number 0
    player2 = Player() # game object number 1
    warpsound.play()   # play new monster sound
    Monster() # create a single Monster
    overtime = 15 # time in seconds to admire the explosion of player before the game ends
    gameOver = False # if True, game still continues until overtime runs out
    gametime = 360 # how long to play (seconds)
    playtime = 0  # how long the game was played
    gravity = False # gravity can be toggled
    
        
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
                elif event.key == pygame.K_g:
                    gravity = not gravity # toggle gravity
                elif event.key == pygame.K_m:
                    warpsound.play()
                    Monster() # create a new monster
                    Player.duel = False
                elif event.key == pygame.K_o:
                    if gameOver:
                        overtime += 10 # more overtime to watch monsters fight each other
        #---- new Monster ?
        #if random.randint(1,1000) == 1:
        #    Monster()
        pygame.display.set_caption("Monster duel. FPS: %.2f"   % clock.get_fps())
        if len(monstergroup) == 0:
            Player.duel = True
        else:
            Player.duel = False
            
        for player in playergroup:  # test if a player crash into enemy bullet ... vamipr health stealing effect !
            crashgroup = pygame.sprite.spritecollide(player, bulletgroup, False, pygame.sprite.collide_mask)
            for bullet in crashgroup: # this include friendly fire
                if bullet.boss.playernumber != player.playernumber: # only care for unfriendly fire
                    if bullet.boss.number < 2:
                        hitsound.play() # only "crysound" if player shot at monster
                    player.hitpoints -= bullet.damage
                    bullet.boss.bullets_hit += 1
                    bullet.boss.hitpoints += 1 # shooter steals at least one hitpoint from victim. Vampire effect
                    Wound(bullet.pos[:]) # pos, victim, move_with_victim = False
                    elastic_collision(bullet, player) # impact on player
                    bullet.kill()
            # player vs player
            crashgroup = pygame.sprite.spritecollide(player, playergroup, False, pygame.sprite.collide_circle)
            for crashplayer in crashgroup:
                if player.number > crashplayer.number:
                    elastic_collision(crashplayer, player) # impact on player
                    # player.hitpoints -= crashplayer.damage
                # no damage ?
        
            # test if player crash into enemy rocket
            crashgroup = pygame.sprite.spritecollide(player, rocketgroup, False, pygame.sprite.collide_mask)
            for rocket in crashgroup:
                #if projectile.physicnumber > crashbody.physicnumber: #avoid checking twice
                if rocket.boss.playernumber != player.playernumber: # avoid friendly fire
                   impactsound.play()
                   player.hitpoints -= rocket.damage
                   rocket.boss.rockets_hit += 1
                   Wound(rocket.pos[:])
                   elastic_collision(rocket, player)
                   rocket.kill()
        
        for projectile in projectilegroup:
            # rocket vs rocket vs bullet vs bullet
            crashgroup = pygame.sprite.spritecollide(projectile, projectilegroup, False )
            for crashthing in crashgroup:
                if projectile.number > crashthing.number:
                    if crashthing.boss.playernumber != projectile.boss.playernumber:
                        projectile.hitpoints -= crashthing.damage
                        crashthing.hitpoints -= projectile.damage
                        elastic_collision(projectile, crashthing)
            
        if gravity: # ---- gravity check ---
            for thing in gravitygroup:  # gravity suck down bullets, players, monsters
                thing.dy += 2.81 # pixel per second square earth: 9.81 m/s
        # ------game Over ? -------------
        #if  (playtime > gametime) and not gameOver:
        #    gameOver = True # do those things once when the game ends
        if GameObject.gameobjects[0] is None and GameObject.gameobjects[1] is None:
            gameOver = True # both players death
            screentext1.newmsg("Game Over. Time played: %.2f seconds" % playtime)
            screentext2.newmsg("both players killed")
        elif GameObject.gameobjects[0] is None or GameObject.gameobjects[1] is None:
            if player1.hitpoints > 0:
                textname = "Red Player"
                textcolor = (255,0,0)
            else:
                textname = "Blue Player"
                textcolor = (0,0,255)
            if len(monstergroup) == 0: 
                gameOver = True # one player dead, all monsters dead
                screentext2.newmsg("%s, you win!" % textname, textcolor)
            elif len(monstergroup) == 1:
                screentext2.newmsg("%s, fight the monster !" % textname, textcolor)
            else:
                screentext2.newmsg("%s, fight the monsters !" % textname, textcolor)
        elif len(monstergroup) == 0:
            Player.duel = True # both players alive, no monsters alive
            screentext2.newmsg("Duel mode. Both Players, fight each other!", (255,0,255))
        elif len(monstergroup) == 1:
            Player.duel = False
            screentext2.newmsg("Both players, fight the monster", (255,0,255))
        elif len(monstergroup) > 1:
            Player.duel = False
            screentext2.newmsg("Both players, fight the monsters", (255,0,255))
        if gameOver: # overtime to watch score, explosion etc
            overtime -= seconds
            screentext1.newmsg("Game over. Overtime: %.2f" % overtime)
            if overtime < 0:
                mainloop = False
        else: # not yet gameOver
            screentext1.newmsg("Time left: %.2f" % (gametime - playtime),(255,0,255))
            #if player1.bullets_fired > 0:
            screentext3.newmsg("Red player: bullets: %i hit: %i quota: %.2f%% rockets: %i hits: %i quota: %.2f%%"
                               % (player1.bullets_fired, player1.bullets_hit, player1.bullets_hit *100.0 / max(1, player1.bullets_fired),
                               player1.rockets_fired, player1.rockets_hit, player1.rockets_hit * 100.0 / max(1,player1.rockets_fired))
                               ,(255,0,0))
            screentext4.newmsg("Blue player: bullets: %i hit: %i quota: %.2f%% rockets: %i hits: %i quota: %.2f%%"
                               % (player2.bullets_fired, player2.bullets_hit, player2.bullets_hit *100.0 / max(1, player2.bullets_fired),
                               player2.rockets_fired, player2.rockets_hit, player2.rockets_hit * 100.0 / max(1,player2.rockets_fired))
                               ,(0,0,255))
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
