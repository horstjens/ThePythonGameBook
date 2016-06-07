# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt or http://thepythongamebook.com
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: grid game with moving walls and 4 cannons aiming at the player
this example is tested using python 3.4 and python2.7 and pygame"""

from __future__ import division, print_function  # only necessary for python2
import pygame
import math
import random
import os
import sys

GRAD = math.pi / 180  # 2 * pi / 360   # math module needs Radiant instead of Grad

def write(background, text, x=50, y=150, color=(0, 0, 0),
          fontsize=None, center=False):
    """write text on pygame surface. """
    if fontsize is None:
        fontsize = 24
    font = pygame.font.SysFont('mono', fontsize, bold=True)
    fw, fh = font.size(text)
    surface = font.render(text, True, color)
    if center:  # center text around x,y
        background.blit(surface, (x - fw // 2, y - fh // 2))
    else:  # topleft corner is x,y
        background.blit(surface, (x, y))


class Bar(pygame.sprite.Sprite):
    def __init__(self, boss, color = (0,200,200)):
        """create healt-bar to show the hitpoints of boss sprite.
           bar is full if boss has 100 or more hitpoints"""
        self.boss = boss #
        self.color = color
        self._layer = self.boss._layer + 1  # self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups)  # call parent class. NEVER FORGET !
        self.image = pygame.Surface((self.boss.rect.width, 7))
        self.distance = self.boss.rect.height - 15 # adapt this
        self.rect = self.image.get_rect()
        self.rect.center = (self.boss.x, self.boss.y - self.distance)
        
    def update(self, seconds):
        """paint a green filled bar if boss has 100 or more hitpoints"""
        if self.boss.hitpoints < 1:
            self.kill()
        if self.boss.hitpoints >= 100:
            width = self.boss.width - 2
        else:
            width = int(self.boss.hitpoints / 100 * self.boss.width) - 2
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image, (128,0,0), (0,0,self.boss.width, 7), 1)
        pygame.draw.rect(self.image, self.color, (1,1,width, 5))
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()  # faster blitting with transparent color
        self.rect.center = (self.boss.x, self.boss.y - self.distance)
            

class FlyingObject(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    images = []

    def __init__(self, radius=50, color=None, x=320, y=240,
                 dx=0, dy=0, layer=4, mass=0):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer  # self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups)  # call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObject.number  # unique number for each sprite
        FlyingObject.number += 1
        self.radius = radius
        self.mass = mass
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.turnspeed = 5  # onnly important for rotating
        self.speed = 20  # only important for ddx and ddy
        self.angle = 0
        self.x = x  # position
        self.y = y
        self.dx = dx  # movement
        self.dy = dy
        self.ddx = 0  # acceleration and slowing down. set dx and dy to 0 first!
        self.ddy = 0
        self.friction = 1.0  # 1.0 means no friction at all
        if color is None:  # create random color if no color is given
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.init2()

    def init2(self):
        pass  # for specific init stuff of subclasses, overwrite init2

    def create_image(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.image = self.image.convert()

    def turnleft(self):
        self.angle += self.turnspeed

    def turnright(self):
        self.angle -= self.turnspeed

    def forward(self):
        self.ddx = -math.sin(self.angle * GRAD)
        self.ddy = -math.cos(self.angle * GRAD)

    def backward(self):
        self.ddx = +math.sin(self.angle * GRAD)
        self.ddy = +math.cos(self.angle * GRAD)

    def straferight(self):
        self.ddx = +math.cos(self.angle * GRAD)
        self.ddy = -math.sin(self.angle * GRAD)

    def strafeleft(self):
        self.ddx = -math.cos(self.angle * GRAD)
        self.ddy = +math.sin(self.angle * GRAD)

    def turn2heading(self):
        """rotate into direction of movement (dx,dy)"""
        self.angle = math.atan2(-self.dx, -self.dy) / math.pi * 180.0
        self.image = pygame.transform.rotozoom(self.image0, self.angle, 1.0)

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
        angle = math.atan2(-deltax, -deltay) / math.pi * 180.0
        #  replace 180 with 90, 270, 0 etc if heading is wrong
        diff = (angle - self.angle - 180) % 360  # reset at 360
        if diff == 0:
            self.turndirection = 0
        elif diff > 180:
            self.turndirection = 1
        else:
            self.turndirection = -1
        return angle - self.angle

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        if self.ddx != 0 or self.ddy != 0:
            self.dx += self.ddx * self.speed
            self.dy += self.ddy * self.speed
        if self.friction < 1:
            if abs(self.dx) > 0:
                self.dx *= self.friction  # make the Sprite slower over time
            if abs(self.dy) > 0:
                self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        if self.x - self.width // 2 < 0:
            self.x = self.width // 2
            self.dx *= -1
        if self.y - self.height // 2 < 0:
            self.y = self.height // 2
            self.dy *= -1
        if self.x + self.width // 2 > PygView.width:
            self.x = PygView.width - self.width // 2
            self.dx *= -1
        if self.y + self.height // 2 > PygView.height:
            self.y = PygView.height - self.height // 2
            self.dy *= -1
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)


class MovingWall(FlyingObject):
    """a slow moving wall, like a paddle in pong"""

    def create_image(self):
        if random.randint(0, 1) == 0:  # left/right or up/down?
            self.leftright = True
            self.image = pygame.Surface((PygView.grid - 5, 7))
        else:
            self.leftright = False
            self.image = pygame.Surface((7, PygView.grid - 5))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.image = self.image.convert()

    def init2(self):
        if self.leftright:
            self.dx = random.randint(5, 25)
            self.dy = 0
        else:
            self.dx = 0
            self.dy = random.randint(5, 25)
        if random.randint(0, 1) == 0:
            self.dx *= -1
            self.dy *= -1


class Bullet(FlyingObject):
    """a small Sprite with mass"""

    def init2(self):
        self.lifetime = PygView.bulletlifetime

    def update(self, seconds):
        super(Bullet, self).update(seconds)
        self.lifetime -= seconds  # aging
        if self.lifetime < 0:
            self.kill()

    def create_image(self):
        self.image = pygame.Surface((self.width, self.height))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius),
                           self.radius)  # draw blue filled circle on ball surface
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()  # faster blitting with transparent color
        self.rect = self.image.get_rect()


class Player(FlyingObject):
    """player-controlled character with relative movement. no mass"""

    def create_image(self):
        self.image = Player.images[0]
        self.image0 = Player.images[0]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

    def init2(self):
        self.friction = 0.992  # slow down self-movement over time
        self.maxx = (PygView.width // PygView.grid - 0.5) * PygView.grid
        self.maxy = (PygView.height // PygView.grid - 0.5) * PygView.grid
        self.minx = self.miny = PygView.grid // 2
        self.hitpoints = 100
        self.tilesrevealed = 0

    def update(self, seconds):
        super(Player, self).update(seconds)
        # self.turn2heading() # use for non-controlled missles etc.
        self.rotate()  # use for player-controlled objects
        self.ddx = 0  # reset movement
        self.ddy = 0
        self.dx = 0
        self.dy = 0
        # center position on grid
        if self.x < self.minx:
            self.x = self.minx
        elif self.x > self.maxx:
            self.x = self.maxx
        if self.y < self.miny:
            self.y = self.miny
        elif self.y > self.maxy:
            self.y = self.maxy


class Door(FlyingObject):
    """invisible door sprite to test if a passage is blocked"""

    def create_image(self):
        self.image = pygame.Surface((PygView.grid // 2, PygView.grid // 2))
        # self.image.fill((66,66,66))
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()


class Heart(FlyingObject):
    def create_image(self):
        self.image = Heart.images[0]
        self.image0 = Heart.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.lifetime = random.randint(1, 5)  # seconds
        self.image1 = pygame.transform.rotozoom(self.image, 0, 1.5)
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

    def update(self, seconds):
        super(Heart, self).update(seconds)
        self.lifetime -= seconds  # aging
        if self.lifetime < 0:
            self.kill()
        if round(self.lifetime * 3, 0) % 2 == 0:
            self.image = self.image0
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        else:
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)


class Cannon(FlyingObject):
    """a cannon, sitting in each corner and rotating toward Player"""

    def __init__(self, radius=50, color=None, x=320, y=240,
                 dx=0, dy=0, layer=4, mass=0, target=None):
        self.target = target
        super(Cannon, self).__init__(radius, color, x, y,
                                     dx, dy, layer, mass)
        # self.p_shooting = max(0.1, random.random()*0.5)
        self.p_shooting = 0.35
        self.turnspeed = random.randint(5, 25)
        self.turndirection = 1
        self.angle = 0
        self.speed = 0
        self.cone = 15

    def create_image(self):
        self.image = Cannon.images[0]
        self.image0 = Cannon.images[0]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

    def update(self, seconds):
        super(Cannon, self).update(seconds)
        diff = self.rotate_toward(self.target)
        self.angle += self.turndirection * self.turnspeed * seconds
        self.rotate()
        if random.random() < self.p_shooting:  # shoot at tux
            if abs(diff) < self.cone:
                Bullet(radius=5, x=self.x, y=self.y,
                       color=self.color, mass=50,
                       dx=-math.sin(self.angle * GRAD) * 200,
                       dy=-math.cos(self.angle * GRAD) * 200)


class PygView(object):
    width = 0
    height = 0
    grid = 0
    bulletlifetime = 0

    def __init__(self, width=800, height=600, fps=30, grid=50, bulletlifetime=3.5, p_wall=0.5, picturepath='data'):
        """Initialize pygame, window, background, font,..."""
        pygame.init()
        PygView.width = width  # make global readable
        PygView.height = height
        PygView.bulletlifetime = bulletlifetime # how many seconds a bullet is visible
        self.p_wall = p_wall # probability for each grid of creating a wall ( 0.0 - 1.0 )
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0
        self.picturepath = picturepath # path to folder with jpg images
        self.grid = grid  # pixel for grid
        self.gridmaxx = self.width // self.grid
        self.gridmaxy = self.height // self.grid
        PygView.grid = grid
        # self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.backgroundfilenames = []  # every .jpg file in folder 'data'
        for root, dirs, files in os.walk(self.picturepath):
            for file in files:
                if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                    self.backgroundfilenames.append(file)
        random.shuffle(self.backgroundfilenames) # remix sort order
        if len(self.backgroundfilenames) == 0:
            print("Error: no .jpg files found in folder 'data'")
            pygame.quit
            sys.exit()
        self.level = 1
        self.loadbackground()

    def loadbackground(self):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255, 255, 255))  # fill background white
        self.prettybackground = pygame.image.load(
            os.path.join(self.picturepath, self.backgroundfilenames[self.level % len(self.backgroundfilenames)]))
        self.prettybackground = pygame.transform.scale(self.prettybackground, (PygView.width, PygView.height))
        self.prettybackground.convert()

    def levelup(self):
        self.level += 1
        self.loadbackground()
        self.paintgrid()
        # make the game harder
        for c in self.cannongroup:
            c.turnspeed *= 1.1  # 10% increase
            c.speed *= 1.1
            c.cone *= 1.1
    
    def paintgrid(self):
        for x in range(self.grid // 2, PygView.width, self.grid):
            for y in range(self.grid // 2, PygView.height, self.grid):
                pygame.draw.rect(self.background, (0, 128, 0),
                                 (x - self.grid // 2, y - self.grid // 2, self.grid, self.grid), 1)
                self.tiles[(x, y)] = True
    
    def create_world(self):
        """create the game world with background picture, sprites, walls and grid"""
        self.tiles = {}
        for x in range(self.grid // 2, PygView.width, self.grid):
            for y in range(self.grid // 2, PygView.height, self.grid):
                pygame.draw.rect(self.background, (0, 128, 0),
                                 (x - self.grid // 2, y - self.grid // 2, self.grid, self.grid), 1)
                self.tiles[(x, y)] = True
        try:  # ----------- load sprite images -----------
            Player.images = [pygame.image.load(os.path.join("data", "babytux.png"))]
            Cannon.images = [pygame.image.load(os.path.join("data", "babytux_neg.png"))]
            Heart.images = [pygame.image.load(os.path.join("data", "heart.png"))]
        except:
            print("pygame error:", pygame.get_error())
            print("please make sure there is a subfolder 'data'")
            print("containing the files 'babytux_neg.png' and 'babytux.png' and 'heart.png'")
            print("and several .jpg files for the background art")
            pygame.quit()
            sys.exit()
        # -------  create (pygame) Sprites Groups and Sprites -------------
        self.allgroup = pygame.sprite.LayeredUpdates()  # for drawing
        # self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        self.bulletgroup = pygame.sprite.Group()
        self.cannongroup = pygame.sprite.Group()
        self.goodiegroup = pygame.sprite.Group()
        self.heartgroup = pygame.sprite.Group()
        self.tuxgroup = pygame.sprite.Group()
        self.wallgroup = pygame.sprite.Group()
        self.doorgroup = pygame.sprite.Group()
        Player.groups = self.allgroup, self.tuxgroup
        MovingWall.groups = self.allgroup, self.wallgroup
        Cannon.groups = self.allgroup, self.cannongroup
        Heart.groups = self.allgroup, self.goodiegroup, self.heartgroup
        Bullet.groups = self.allgroup, self.bulletgroup
        Bar.groups = self.allgroup    # does not need another group
        Door.groups = self.doorgroup  # do not paint the invisible door
        self.player1 = Player(x=self.grid * 2.5, y=self.grid * 2.5, dx=0, dy=0, layer=5)  # over balls layer
        Bar(self.player1) # create healt-bar for player1 
        self.cannon1 = Cannon(x=30, y=30, dx=random.randint(10, 30), target=self.player1, color=(255,0,0))
        self.cannon2 = Cannon(x=PygView.width - 30, y=30, dy=random.randint(10, 20), target=self.player1, color=(0,255,0))
        self.cannon3 = Cannon(x=30, y=PygView.height - 30, dy=random.randint(-20, -10), target=self.player1, color=(0,0,255))
        self.cannon4 = Cannon(x=PygView.width - 30, y=PygView.height - 30, dx=random.randint(-30, -10),color = (255,0,255),
                              target=self.player1)
        self.door1 = Door()  # invisible sprite to test if movement throug moving walls is possible
        # --- tiles and moving walls ----
        for x in range(self.grid, PygView.width - self.grid, self.grid):
            for y in range(self.grid, PygView.height - self.grid, self.grid):
                if random.random() < self.p_wall:
                    MovingWall(x=x, y=y)

    def check_passage(self, x, y):
        """checks if a point on the grid is blocked by wall(s)
           returns True if passage is possibe, else returns False"""
        self.door1.rect.center = (x, y)
        crashgroup = pygame.sprite.spritecollide(self.door1, self.wallgroup, False, pygame.sprite.collide_rect)
        if len(crashgroup) > 0:  # are sprites in the crashgroup?
            return False
        return True

    def run(self):
        """The mainloop"""
        self.create_world()
        running = True
        while running:
            hiddentiles = len([v for v in self.tiles.values() if v])
            pygame.display.set_caption(
                "Level: {} Hitpoints: {} Tiles left: {}".format(self.level, self.player1.hitpoints, hiddentiles))
            for event in pygame.event.get():  # event handler
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  # press and release
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        if event.key == pygame.K_SPACE:  # fire forward from tux1 with 300 speed
                            Bullet(radius=5, x=self.player1.x, y=self.player1.y,
                                   dx=-math.sin(self.player1.angle * GRAD) * 300,
                                   dy=-math.cos(self.player1.angle * GRAD) * 300)
                        if event.key == pygame.K_w or event.key == pygame.K_UP: # up
                            self.player1.angle = 0
                            if self.check_passage(self.player1.x, self.player1.y - self.grid // 2):
                                self.player1.y -= self.grid
                        if event.key == pygame.K_s or event.key == pygame.K_DOWN:  # down
                            self.player1.angle = 180
                            if self.check_passage(self.player1.x, self.player1.y + self.grid // 2):
                                self.player1.y += self.grid
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.player1.angle = 90  # left
                            if self.check_passage(self.player1.x - self.grid // 2, self.player1.y):
                                self.player1.x -= self.grid
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # right
                            self.player1.angle = 270
                            if self.check_passage(self.player1.x + self.grid // 2, self.player1.y):
                                self.player1.x += self.grid
            if self.player1.hitpoints < 1:
                #    write(self.screen, "GAME OVER", x=10, color=(200,0,200), fontsize=50)
                #    write(self.screen, "PLAYER ONE", x=10, y= self.height // 2 + 60, color=(200,0,200), fontsize=50)
                running = False
            # pressedkeys = pygame.key.get_pressed()
            # ------- new heart -------------
            if random.random() < 0.015:  # 1/30 ~ once per second at 30 fps
                Heart(x=self.grid * random.randint(1, self.gridmaxx) - self.grid // 2,
                      y=self.grid * random.randint(1, self.gridmaxy) - self.grid // 2)
            # ------ paint ----------
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000
            self.playtime += seconds
            self.screen.blit(self.background, (0, 0))  # clear screen
            # ---- paint under player1 ----
            # if tile is True, blit prettybackground and set tile to False
            if (self.player1.x, self.player1.y) in self.tiles and self.tiles[(self.player1.x, self.player1.y)]:
                self.background.blit(self.prettybackground,
                                     (self.player1.x - self.grid // 2, self.player1.y - self.grid // 2),
                                     area=(self.player1.x - self.grid // 2, self.player1.y - self.grid // 2, self.grid,
                                           self.grid))
                self.tiles[(self.player1.x, self.player1.y)] = False
                self.player1.tilesrevealed += 1
            if hiddentiles == 0:     # -- new level ?
                self.player1.hitpoints = max(self.player1.hitpoints, 2) # refill to 100 hitpoints
                self.levelup()
            # write text below sprites
            write(self.screen, "Press ESC to quit. FPS: {:6.3}  PLAYTIME: {:.1f} SECONDS".format(
                self.clock.get_fps(), self.playtime), color=(200, 0, 0), x=10, y=self.grid // 2, fontsize=10)
            write(self.screen, "Press w,a,s,d to steer", x=self.width // 2, y=self.height - self.grid // 2, center=True)
            # --------- collision detection bullet vs. moving wall
            for wall in self.wallgroup:
                crashgroup = pygame.sprite.spritecollide(wall, self.bulletgroup, False, pygame.sprite.collide_rect)
                for bullet in crashgroup: # reflect bullet
                    if wall.leftright:
                        bullet.dy *= -1
                    else:
                        bullet.dx *= -1
                    if random.random() < 0.1:
                        bullet.kill()
            # --------- collision detection bullet vs. other-color bullet
            for bullet in self.bulletgroup:
                crashgroup = pygame.sprite.spritecollide(bullet, self.bulletgroup, False, pygame.sprite.collide_circle)
                for otherbullet in crashgroup:
                    if bullet.number > otherbullet.number:
                        if bullet.color != otherbullet.color:
                            #Star(bullet.x, bullet.y)
                            for line in range(5):
                                pygame.draw.line(self.screen, (random.randint(0,255),random.randint(0,255), random.randint(0,255)),
                                                (bullet.x, bullet.y), (bullet.x +random.randint(-20,20), bullet.y + random.randint(-20,20)),1)
                            otherbullet.kill()
                            bullet.kill()                                
                            break
                
            # ---- got heart ? -----
            crashgroup = pygame.sprite.spritecollide(self.player1, self.heartgroup, False, pygame.sprite.collide_rect)
            for heart in crashgroup:
                heart.kill()
                self.player1.hitpoints += 1
            # --- got Bullet ? ----
            crashgroup = pygame.sprite.spritecollide(self.player1, self.bulletgroup, False, pygame.sprite.collide_rect)
            for bullet in crashgroup:
                bullet.kill()
                self.player1.hitpoints -= 1
            # ----------- clear, draw , update, flip -----------------  
            self.allgroup.update(seconds)  # would also work with ballgroup
            self.allgroup.draw(self.screen)
            pygame.display.flip()
        # seconds = self.playtime / 1000
        print("Game over Player One")
        print("You played {:.2f} seconds, reached level {} and revealed {} tiles.\nThat is {:.2f} tiles per second!".format(
              self.playtime, self.level, self.player1.tilesrevealed, self.player1.tilesrevealed / self.playtime))
        pygame.quit()
        #sys.exit() # no sys.exit() because we want to go back to the calling game menu

if __name__ == '__main__':
    PygView(1000, 600, grid=50, bulletlifetime=10, p_wall= 0.7, fps=60).run()  # try out other values and your own picturefolder, like picturepath="/home/horst/.config/variety/Favorites/"
