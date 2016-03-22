# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: template to show how to reflect balls from rectangles and how 
to rotate turrets toward (moving) targets
this example is tested using python 3.4 and pygame
needs: file 'babytux.png' in subfolder 'data'
"""
import pygame 
import math
import random
import os
import sys

GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad

class FlyingObject(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    images = []
    
    def __init__(self, radius = 50, color=None, x=320, y=240,
                 dx=0, dy=0, layer=4, mass=0):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObject.number # unique number for each sprite
        FlyingObject.number += 1 
        self.radius = radius
        self.mass = mass
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.turnspeed = 5   # onnly important for rotating
        self.speed = 20      # only important for ddx and ddy
        self.angle = 0
        self.x = x           # position
        self.y = y
        self.dx = dx         # movement
        self.dy = dy
        self.ddx = 0 # acceleration and slowing down. set dx and dy to 0 first!
        self.ddy = 0
        self.friction = 1.0 # 1.0 means no friction at all
        if color is None: # create random color if no color is given
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else:
            self.color = color
        self.create_image()
        self.rect= self.image.get_rect()
        self.rect.center = (-100,-100) # avoid blinking image in topleft (0,0) corner
        self.init2()
        
    def init2(self):
        pass # for specific init stuff of subclasses, overwrite init2
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        self.image.fill((self.color))
        self.image = self.image.convert()
        
    def turnleft(self):
        self.angle += self.turnspeed
        
    def turnright(self):
        self.angle -= self.turnspeed
        
    def forward(self):
        self.ddx = -math.sin(self.angle*GRAD) 
        self.ddy = -math.cos(self.angle*GRAD) 
        
    def backward(self):
        self.ddx = +math.sin(self.angle*GRAD) 
        self.ddy = +math.cos(self.angle*GRAD)  
        
    def straferight(self):
        self.ddx = +math.cos(self.angle*GRAD)
        self.ddy = -math.sin(self.angle*GRAD)
    
    def strafeleft(self):
        self.ddx = -math.cos(self.angle*GRAD) 
        self.ddy = +math.sin(self.angle*GRAD) 
        
    def turn2heading(self):
        """rotate into direction of movement (dx,dy)"""
        self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
        self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
    
    def rotate(self):
          """rotate because changes in self.angle"""
          self.oldcenter = self.rect.center
          self.image = pygame.transform.rotate(self.image0, self.angle)
          self.rect = self.image.get_rect()
          self.rect.center = self.oldcenter
          
    def rotate_toward(self, target):
        """set turndirection to rotate towards target and returns angle"""
        deltax = target.x - self.x
        deltay = target.y - self.y
        angle =   math.atan2(-deltax, -deltay)/math.pi*180.0    
        #  replace 180 with 90, 270, 0 etc if heading is wrong
        diff = (angle - self.angle - 180) %360 #reset at 360
        if diff == 0:
            self.turndirection = 0
        elif diff > 180:
            self.turndirection = 1
        else:
            self.turndirection = -1
        return angle - self.angle

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        if abs(self.dx) > 0 : 
            self.dx *= self.friction  # make the Sprite slower over time
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        if self.x - self.width //2 < 0:
            self.x = self.width // 2
            self.dx *= -1 
        if self.y - self.height // 2 < 0:
            self.y = self.height // 2
            self.dy *= -1
        if self.x + self.width //2 > PygView.width:
            self.x = PygView.width - self.width //2
            self.dx *= -1
        if self.y + self.height //2 > PygView.height:
            self.y = PygView.height - self.height //2
            self.dy *= -1
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)

class MovingWall(FlyingObject):
    """a slow moving wall, like a paddle in pong"""
    
    def create_image(self):
        # left/right or up/down?
        if random.randint(0,1) == 0:
            self.leftright = True
            self.image = pygame.Surface((50,10))
        else:
            self.leftright = False
            self.image = pygame.Surface((10,50))
        self.image.fill((0,200,0))
        self.rect= self.image.get_rect()
        self.image = self.image.convert()
    
    def init2(self):
        if self.leftright:
            self.dx = random.randint(5, 25)
            self.dy = 0
        else:
            self.dx = 0
            self.dy = random.randint(5, 25)
        if random.randint(0,1) == 0:
            self.dx *= -1
            self.dy *= -1
        
        

class Ball(FlyingObject):
    """a big pygame Sprite with high mass"""
        
    def init2(self):
        self.mass = 150
        self.dx = random.random() * 100 - 50
        self.dy = random.random() * 100 - 50
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
        pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
        pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        
class Bullet(FlyingObject):
    """a small Sprite with mass"""

    def init2(self):
        if self.mass == 0:
            self.mass = 5
        self.lifetime = 2.5 # seconds

    def update(self, seconds):
        super(Bullet,self).update(seconds)
        self.lifetime -= seconds # aging
        if self.lifetime < 0:
            self.kill() 
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()
        
        
class Tux(FlyingObject):
    """player-controlled character with relative movement. no mass"""
    
    def create_image(self):
        self.image = Tux.images[0]
        self.image0 = Tux.images[0]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        
    def init2(self):
        self.friction = 0.992 # slow down self-movement over time
        
    def update(self, seconds):
          super(Tux,self).update(seconds)
          #self.turn2heading() # use for non-controlled missles etc.
          self.rotate()        # use for player-controlled objects
          self.ddx = 0 # reset movement
          self.ddy = 0 
          self.dx = 0
          self.dy = 0
          
          
class Cannon(FlyingObject):
    """a cannon, sitting in each corner and rotating toward Tux"""
    
    def __init__(self, radius = 50, color=None, x=320, y=240,
                 dx=0, dy=0, layer=4, mass=0, target=None):
        self.target = target
        super(Cannon, self).__init__(radius, color, x, y,
                 dx, dy, layer, mass)
        self.p_shooting = max(0.1, random.random()*0.5)
        self.turnspeed = random.randint(5, 25)
        self.turndirection = 1
        self.angle = 0
        self.speed = 0
        
    def create_image(self):
        self.image = Cannon.images[0]
        self.image0 = Cannon.images[0]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
       
    def update(self, seconds):
        super(Cannon,self).update(seconds)
        diff = self.rotate_toward(self.target)
        self.angle += self.turndirection * self.turnspeed * seconds
        self.rotate() 
        if random.random() < self.p_shooting: # shoot at tux
            if abs(diff) < 15:
                Bullet(radius=5, x=self.x, y=self.y,
                       color = (40,40, 150), mass= 50,
                       dx=-math.sin(self.angle*GRAD)*200,
                       dy=-math.cos(self.angle*GRAD)*200)           
    

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
    
def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .x .y, .dx, dy
           by Leonard Michlmayr"""
        dirx = sprite1.x - sprite2.x
        diry = sprite1.y - sprite2.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp
            
def reflect(ball, rect):
    """collision between a moving ball sprite and a (for this purpose static)
       rectangle sprite. the ball is reflected by the rect (like pong).
       the ball sprite need property .radius, .x, .y, .dx, .dy
       the rect sprite need to have a .rect (pygame rect)
       .x and .y refer to the rect (disc) center"""
    xdistance = abs(ball.x - rect.x)
    ydistance = abs(ball.y - rect.y)
    #if ball.x < rect.x and ball.dx >0:
    #    ball.dx *= -1
    
            
class PygView(object):
    width = 0
    height = 0
  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,..."""
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        
    def create_world(self):
        # make an interesting background 
        try:  # ----------- load sprite images -----------
            #Tux.images.append(pygame.image.load(os.path.join("data", "babytux.png")))
            #Cannon.images.append(pygame.image.load(os.path.join("data", "babytux_neg.png")))
            Tux.images = [pygame.image.load(os.path.join("data", "babytux.png"))]
            Cannon.images = [pygame.image.load(os.path.join("data", "babytux_neg.png"))]
        except:
            print("pygame error:", pygame.get_error())
            print("please make sure there is a subfolder 'data'")
            print("containing the files 'babytux_neg.png' and 'babytux.png'")
            pygame.quit()
            sys.exit()
        # -------  create (pygame) Sprites Groups and Sprites -------------
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.bulletgroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.tuxgroup = pygame.sprite.Group()
        self.wallgroup = pygame.sprite.Group()
        Tux.groups = self.allgroup, self.tuxgroup
        MovingWall.groups = self.allgroup, self.wallgroup
        Cannon.groups = self.allgroup, self.cannongroup
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        Bullet.groups = self.allgroup, self.bulletgroup
        self.tux1 = Tux(x=400, y=200, dx=0, dy=0, layer=5) # over balls layer
        self.cannon1 = Cannon(x=30, y=30, dx=random.randint(10,30), target=self.tux1)
        self.cannon2 = Cannon(x=PygView.width-30, y=30, dy=random.randint(10,20), target = self.tux1)
        self.cannon3 = Cannon(x=30, y=PygView.height-30, dy=random.randint(-20,-10), target = self.tux1)
        self.cannon4 = Cannon(x=PygView.width-30, y=PygView.height-30, dx=random.randint(-30,-10),target = self.tux1)
        # --- moving walls ----
        for x in range(0, PygView.width, 100):
            for y in range(0, PygView.height, 100):
                #MovingWall(x,y) 
                MovingWall(x=x,y=y)
        

    def run(self):
        """The mainloop"""
        self.create_world() 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN: # press and release
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE: # fire forward from tux1 with 300 speed
                        Bullet(radius=5, x=self.tux1.x, y=self.tux1.y,
                               dx=-math.sin(self.tux1.angle*GRAD)*300,
                               dy=-math.cos(self.tux1.angle*GRAD)*300)           
                    if event.key == pygame.K_w:
                        self.tux1.y -= 50
                        self.tux1.angle = 0
                    if event.key == pygame.K_s:
                        self.tux1.y += 50
                        self.tux1.angle = 180
                    if event.key == pygame.K_a:
                        self.tux1.x -= 50
                        self.tux1.angle = 90
                    if event.key == pygame.K_d:
                        self.tux1.x += 50
                        self.tux1.angle = 270
            # control pressed keys (per frame)
            pressedkeys = pygame.key.get_pressed()
            
            
            # ------ paint ----------
            milliseconds = self.clock.tick(self.fps) 
            seconds = milliseconds / 1000
            self.playtime += seconds
            self.screen.blit(self.background, (0, 0))  # clear screen
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            # ---------- collision detection between ball and bullet sprites ---------
            # you can use: pygame.sprite.collide_rect, pygame.sprite.collide_circle, pygame.sprite.collide_mask
            # the False means the colliding sprite is not killed
            #for ball in self.ballgroup:
            #   crashgroup = pygame.sprite.spritecollide(ball, self.bulletgroup, False, pygame.sprite.collide_circle)
            #   for bullet in crashgroup:
            #       elastic_collision(ball, bullet) # change dx and dy of both sprites
            # --------- collision detection between ball and other balls
            #for ball in self.ballgroup:
            #    crashgroup = pygame.sprite.spritecollide(ball, self.ballgroup, False, pygame.sprite.collide_circle)
            #    for otherball in crashgroup:
            #        if ball.number > otherball.number:     # make sure no self-collision or calculating collision twice
            #            elastic_collision(ball, otherball) # change dx and dy of both sprites
            # ---------- collision detection between bullet and other bullets
            for wall in self.wallgroup:
                crashgroup = pygame.sprite.spritecollide(wall, self.bulletgroup, True, pygame.sprite.collide_rect)
            for bullet in self.bulletgroup:
                crashgroup = pygame.sprite.spritecollide(bullet, self.bulletgroup, False, pygame.sprite.collide_circle)
                for otherbullet in crashgroup:
                    if bullet.number > otherbullet.number:
                         elastic_collision(bullet, otherbullet) # change dx and dy of both sprites
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.allgroup.draw(self.screen)           
            # write text over everything 
            write(self.screen, "Press w,a,s,d and q,e to steer tux", x=self.width//2, y=300, center=True)
            write(self.screen, "Press space to fire from tux", x=self.width//2, y=325, center=True)
            # next frame
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    PygView().run() # try PygView(800,600).run()
