# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: template to show how to move pygames Sprites 
around
"""


import pygame 
import math
import random
import os

GRAD = math.pi / 180  # 2 * pi / 360   # math module needs Radiant instead of Grad

class Bar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Boss sprite
        Boss needs a unique number in FlyingObject.numbers,
        self.hitpoints and self.hitpointsfull"""
    
        def __init__(self, bossnumber, height=7, color = (0,255,0), ydistance=10):
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.bossnumber = bossnumber # lookup in Flyingobject.numbers
            self.boss = FlyingObject.numbers[self.bossnumber]
            self.height = height
            self.color = color
            self.ydistance = ydistance
            self.image = pygame.Surface((self.boss.rect.width,self.height))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, (128,128,128), (0,0,self.boss.rect.width,self.height),1)
            self.rect = self.image.get_rect()
            self.oldpercent = 0
            self.percent = 1
            
        def calculate_percent(self):
            pass
            #self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0    
        
        def update(self, time):
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height //2 - self.ydistance
            self.calculate_percent()
            if self.percent != self.oldpercent:
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,self.height-2)) # fill black
                pygame.draw.rect(self.image, self.color, (1,1,
                    int((self.boss.rect.width-2) * self.percent),self.height-2),0) # fill green
                pygame.draw.rect(self.image, (128,128,128), (0,0,self.boss.rect.width,self.height),1)
            self.oldpercent = self.percent
            #check if boss is still alive
            if self.bossnumber not in FlyingObject.numbers:
                self.kill() # kill the hitbar
                
class Hitpointsbar(Bar):
    def calculate_percent(self):
        self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0    
        
class Energybar(Bar):
    def calculate_percent(self):
        self.percent = self.boss.energy / self.boss.energyfull * 1.0    
    

        
    
        

class FlyingObject(pygame.sprite.Sprite):
    """has a unique number"""
    number = 0
    numbers = {}
    
    def __init__(self, layer=5):
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = FlyingObject.number
        FlyingObject.number += 1
        FlyingObject.numbers[self.number] = self
    
    def turn2heading(self):
        """rotate into direction of movement (dx,dy)"""
        self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
        self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
    
    def rotate_toward(self, target):
        """set turndirection to rotate towards target and returns angle"""
        deltax = target.x - self.x
        deltay = target.y - self.y
        self.angle = math.atan2(-deltax, -deltay) / math.pi * 180.0
        self.dx=-math.sin(self.angle * GRAD) * self.speed
        self.dy=-math.cos(self.angle * GRAD) * self.speed
        #  replace 180 with 90, 270, 0 etc if heading is wrong
        #diff = (angle - self.angle - 180) % 360  # reset at 360
        #if diff == 0:
        #    self.turndirection = 0
        #elif diff > 180:
        #    self.turndirection = 1
        #else:
        #    self.turndirection = -1
        #return angle - self.angle

    def rotate(self):
        """rotate because changes in self.angle"""
        self.oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldcenter
    
    
    def kill(self):
        del FlyingObject.numbers[self.number]
        pygame.sprite.Sprite.kill(self)



class Enemy(FlyingObject):
    def __init__(self, x=None, y=None):
        FlyingObject.__init__(self)
        if x is None:
            self.x = PygView.width
        else:
            self.x = x
        if y is None:
            self.y = random.randint(0, PygView.height)
        else:
            self.y = y
        self.hitpoints = 100
        self.hitpointsfull = 100
        self.dx = random.randint(-200, -20)
        self.dy = random.choice((-2,-1,0,0,0,0,0,0,1,2))
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        Hitpointsbar(self.number)
        
    def create_image(self):
        self.image = pygame.Surface((50,50))
        self.image.fill((166,20,33))
        self.image.convert_alpha()
        
    def update(self, seconds):
        
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        if self.hitpoints < 1:
            Enemy()
        if self.x < 100:
            Enemy()
            self.kill()
        
    

class Bullet(FlyingObject):
    """a small Sprite with mass"""

    def __init__(self, boss, target, radius=3, color=(128,0,0), layer=6, damage=1, mass=1, speed=50, lifetime=6):
        FlyingObject.__init__(self)
        #self._layer = layer   #self.layer = layer
        #pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.mass = mass
        self.damage = damage
        self.radius = radius
        self.target = target
        self.color = color
        self.speed = speed
        self.hitpoints = 1
        self.lifetime = lifetime # seconds
        self.bossnumber = boss.number
        self.create_image()
        self.mask = pygame.mask.from_surface(self.image) # pixelmask # 
        self.rect = self.image.get_rect()
        self.x = boss.x
        self.y = boss.y
        self.rect.center = (self.x,self.y)
        self.dx = 0         # movement
        self.dy = 0
        self.ddx = 0 # acceleration and slowing down. set dx and dy to 0 first!
        self.ddy = 0
        self.angle = 0
        self.rotate_toward(target)
       
        
   

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # alive?
        if self.hitpoints < 1:
            self.kill()
        #super(Bullet,self).update(seconds)
        # aging ?
        self.lifetime -= seconds 
        if self.lifetime < 0:
            self.kill() 
            
    def create_image(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2))    
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        


class Crosshair(FlyingObject):
    
    def __init__(self, radius = 50, color=(128,0,0), layer=6):
        FlyingObject.__init__(self)
        self.radius = radius
        self.color = color
        self.image=pygame.Surface((2*self.radius,2*self.radius))
        pygame.draw.circle(self.image, self.color, (radius, radius), radius, 1)
        pygame.draw.circle(self.image, self.color, (radius, radius), int(radius * 0.6), 1)
        pygame.draw.circle(self.image, self.color, (radius, radius), int(radius * 0.3), 1)
        pygame.draw.line(self.image, self.color, (0,0), (radius-5, radius-5))
        pygame.draw.line(self.image, self.color, (0,2*radius), (radius-5, radius+5))
        pygame.draw.line(self.image, self.color, (2*radius,0), (radius+5, radius-5))
        pygame.draw.line(self.image, self.color, (2*radius,2*radius), (radius+5, radius+5))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.x = self.rect.centerx
        self.y = self.rect.centery
        
    def update(self, seconds):
        self.rect.center = pygame.mouse.get_pos()
        self.x = self.rect.centerx
        self.y = self.rect.centery
        

class Player(FlyingObject):
    """hüpft"""
    
    def __init__(self, x, y, layer=4):
        #self._layer = layer   #self.layer = layer
        #pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        FlyingObject.__init__(self)
        self.x = x
        self.y = y
        self.dy = 0
        self.dx = 0
        self.radius = 25 # ???
        self.gravity = 1.2
        self.friction = 0.999
        self.image = PygView.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.stabil = False
        self.hitpoints = 100
        self.hitpointsfull = 100
        self.energy = 200
        self.energyfull = 200
        Hitpointsbar(bossnumber=self.number, ydistance = 5, color=(0,0,255))
        Energybar(bossnumber=self.number, ydistance=15, color=(255,255,0))
        
        
    def update(self, seconds):
        if not self.stabil:
            self.dy += self.gravity
            
        
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.dx *= self.friction
        self.dy *= self.friction
        # bouncing on edge
        # x,y is now the center of self.rect!
        if self.x - self.rect.width //2 < 0:
            self.x = self.rect.width // 2
            self.dx *= -1 
        if self.y - self.rect.height // 2 < 0:
            self.y = self.rect.height // 2
            self.dy *= -1
        if self.x + self.rect.width //2 > PygView.width:
            self.x = PygView.width - self.rect.width //2
            self.dx *= -1
        if self.y + self.rect.height //2 > PygView.height:
            self.y = PygView.height - self.rect.height //2
            self.dy *= -1
        # move rect
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        
        


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y=40, width=100, height = 10, layer=5, dx=-20, randomy = False):
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.x = x
        self.y = y
        if randomy:
            self.y = random.randint(int(PygView.height*0.5), int(PygView.height * 0.85))
        self.width = width
        self.height = height
        self.dy = 0
        self.dx = dx
        self.image = pygame.Surface((width,height))
        self.image.fill((0,200,0))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, seconds):
            self.x += self.dx * seconds
            self.y += self.dy * seconds
            # move rect
            self.rect.centerx = round(self.x, 0)
            self.rect.centery = round(self.y, 0)
            
class Obstacle(FlyingObject):
    def __init__(self, layer=5, radius = 25):
        #self._layer = layer   #self.layer = layer
        #pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        FlyingObject.__init__(self)
        self.x = PygView.height
        self.radius = radius
        self.y = int(random.randint(0, PygView.height))
        self.dx = -1 - random.random() * 100
        self.dy = 0
        self.create_image()
        self.mask = pygame.mask.from_surface(self.image) # pixelmask
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.hitpoints = 50
        self.hitpointsfull = 50
        Hitpointsbar(self.number)
        
    def create_image(self):
        self.image = pygame.Surface((self.radius*2,self.radius*2))
        pygame.draw.circle(self.image, (40,40,40), (self.radius, self.radius), self.radius)
        self.image.convert()    
    
    def update(self, seconds):
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        # move rect
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # hitpoints?
        if self.hitpoints < 1:
            # make a new Obstacle!
            Obstacle()
            self.kill()


def draw_examples(background):
    """painting on the background surface"""
    #------- try out some pygame draw functions --------
    # pygame.draw.line(Surface, color, start, end, width) 
    pygame.draw.line(background, (0,255,0), (10,10), (50,100))
    # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
    pygame.draw.rect(background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
    # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    pygame.draw.circle(background, (0,200,0), (200,50), 35)
    # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
    pygame.draw.polygon(background, (0,180,0), ((250,100),(300,0),(350,50)))
    # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
    pygame.draw.arc(background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
    #return background # not necessary to return the surface, it's already in the memory

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))


class PygView(object):
    width = 0
    height = 0
    images = []
  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.load_resources() 
        
    def load_resources(self):
        """painting on the surface and create sprites"""
        # make an interesting background 
        
        # ----- load images ----
        PygView.images.append(pygame.image.load(os.path.join("data", "babytux.png")))  # hat index 0
        PygView.images[0].convert_alpha() 
        
        draw_examples(self.background)
        # create (pygame) Sprites.
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.repeatgroup = pygame.sprite.Group()
        self.obstaclegroup = pygame.sprite.Group()
        self.platformgroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group() 
        self.bargroup = pygame.sprite.Group()
        self.bulletgroup = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        # for collision detection etc.
        Player.groups = self.allgroup, self.playergroup # each Ball object belong to those groups
        Platform.groups = self.allgroup, self.repeatgroup, self.platformgroup
        Obstacle.groups = self.allgroup, self.repeatgroup, self.obstaclegroup
        Bullet.groups = self.allgroup, self.bulletgroup
        Enemy.groups = self.allgroup, self.enemygroup
        Bar.groups = self.bargroup
        Crosshair.groups = self.allgroup
        self.crosshair1 = Crosshair()   # number 0
        self.player1 = Player(x=100, y=100) # number 1
        
        #self.ball2 = Ball(x=200, y=100) # create another Ball Sprite
        self.boden1a = Platform(x=0, y= self.height-10, width=self.width, dx = -100)
        self.boden1b = Platform(x=self.width, y= self.height-10, width=self.width, dx = -100)
        self.boden2 = Platform(x=600, width=400, dx = -10, randomy = True)
        self.obstacle1 = Obstacle()
        self.enemy1 = Enemy()
        self.enemy2 = Enemy()
       
        #print("player 1 number:", self.player1.number, FlyingObject.numbers)
        
    def run(self):
        """The mainloop"""
        running = True
        #y= 0
        #x = 100
        #dy = 25
        #char = "x"
        while running:
            pygame.display.set_caption("hp1: {} Press ESC to quit".format(self.player1.hitpoints))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    #if event.key == pygame.K_b:
                    #    Ball() # add balls!
                    #if event.key == pygame.K_SPACE:
                    #    self.player1.y -= 5
                    #    self.player1.stabil = False
                    #    self.player1.dy = -50
                        
            # ------------- event handler -------------------------
            # ------------- pressed keys --------------------------
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys[pygame.K_w]: # forward
                 if self.player1.energy >0:
                     self.player1.dy = -50
                     self.player1.stabil = False
                     self.player1.energy -= 1
            else:
                self.player1.energy += 0.1
            if pressedkeys[pygame.K_a]:
                self.player1.x -= 1
            if pressedkeys[pygame.K_d]:
                self.player1.x += 1
            # ----------- mouse buttons ---------------
            if pygame.mouse.get_pressed()[0]:
                Bullet(self.player1, self.crosshair1) 
           
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.bargroup.update(seconds)
            self.allgroup.draw(self.screen)           
            self.bargroup.draw(self.screen)
            for dings in self.repeatgroup:
                if dings.x + dings.rect.width // 2 < 0:
                    dings.x = PygView.width + dings.rect.width//2
            # write text over everything 
            write(self.screen, "Press b to add another ballöÖäÄüÜß",x=self.width//2, y=250, center=True)
            # write moving text (not a Sprite)
            #write(self.screen, char, x, y, color=(0,0,255))
            #y += dy * seconds
            #if y > PygView.height:
            #    x = random.randint(0, PygView.width)
            #    y = 0
            #    char = random.choice( "0123456789abcdefghijklmnopqrstuvwxyz")
            
            
            # enemy fire at player
            
            for e in self.enemygroup:
                # random chance to fire
                if random.random() < 0.1:
                    Bullet(e, self.player1)
            
            
            
            # --------- collision detection --------------
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed
            # ---------- collision detection between player and platform sprites ---------
            for player in self.playergroup:
             
               crashgroup = pygame.sprite.spritecollide(player, self.platformgroup, False, pygame.sprite.collide_rect)
               for platform in crashgroup:
                   print("crash on platform")
                   if player.y < platform.y and player.x + player.rect.width //2 > platform.x - platform.rect.width //2:
                       print("stabil on platform")
                       player.stabil = True
                       player.dy = 0
                       player.y = platform.y - player.rect.height //2  - platform.rect.height // 2
            
            # ----------- collision detection between player and obstacle ----------
            for player in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(player, self.obstaclegroup, False, pygame.sprite.collide_rect)
                for platform in crashgroup:
                    player.hitpoints -= 1
                    if player.hitpoints < 1:
                        print("game over")
                        running = False
            # ----------- collision detection between obstacle and bullet ----------
            for obstacle in self.obstaclegroup:
                crashgroup = pygame.sprite.spritecollide(obstacle, self.bulletgroup, True, pygame.sprite.collide_rect)
                for bullet in crashgroup: 
                       obstacle.hitpoints -= 1
            
                       
                   
                   
                   
                   
                   
                   
            
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    PygView().run() # try PygView(800,600).run()
