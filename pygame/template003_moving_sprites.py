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


class Ball(pygame.sprite.Sprite):
    """this class inherits from pygames sprite class"""
    def __init__(self, radius = 50, color=None, x=320, y=240,
                 dx=None, dy=None, layer=4):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.radius = radius
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.x = x
        self.y = y
        if color is None: # create random color if no color is given
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else:
            self.color = color
        if dx is None:
            self.dx = random.random() * 100 - 50 # from -50 to 50
        else:
            self.dx = dx
        if dy is None:
            self.dy = random.random() * 100 - 50
        else:
            self.dy = dy
        # create a rectangular surface for the ball 50x50
        self.image = pygame.Surface((self.width,self.height))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        pygame.draw.circle(self.image, color, (radius, radius), radius) # draw blue filled circle on ball surface
        # left blue eye
        pygame.draw.circle (self.image, (0,0,200) , (radius //2 , radius //2), radius// 3)
        # right yellow yey
        pygame.draw.circle (self.image, (255,255,0) , (3 * radius //2  , radius //2), radius// 3)
        # grey mouth
        pygame.draw.arc(self.image, (32,32,32), (radius //2, radius, radius, radius//2), math.pi, 2*math.pi, 1)
        # self.surface = self.surface.convert() # for faster blitting if no transparency is used. 
        # to avoid the black background, make black the transparent color:
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        #self.image=pygame.image.load("xx.png")
        self.rect= self.image.get_rect()
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # time based movement
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        # bouncing on edge
        # x,y is now the center of self.rect!
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
        # move rect
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        #print("updating:", self.rect.centerx, self.rect.centery)
        
    #def blit(self, background):
    #    """blit the Ball on the given background surface"""
    #    background.blit(self.surface, ( self.x, self.y))

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
  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
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
        self.paint() 
        
    def paint(self):
        """painting on the surface and create sprites"""
        # make an interesting background 
        draw_examples(self.background)
        # create (pygame) Sprites.
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.ballgroup = pygame.sprite.Group()          # for collision detection etc.
        Ball.groups = self.allgroup, self.ballgroup # each Ball object belong to those groups
        
        self.ball1 = Ball(x=100, y=100) # creating a Ball Sprite
        self.ball2 = Ball(x=200, y=100) # create another Ball Sprite

    def run(self):
        """The mainloop"""
        running = True
        y= 0
        x = 100
        dy = 25
        char = "x"
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_b:
                        Ball() # add balls!
            # end of event handler
           
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
            self.allgroup.draw(self.screen)           
        
            # write text over everything 
            write(self.screen, "Press b to add another ballöÖäÄüÜß",x=self.width//2, y=250, center=True)
            # write moving text (not a Sprite)
            write(self.screen, char, x, y, color=(0,0,255))
            y += dy * seconds
            if y > PygView.height:
                x = random.randint(0, PygView.width)
                y = 0
                char = random.choice( "0123456789abcdefghijklmnopqrstuvwxyz")
                
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    PygView().run() # try PygView(800,600).run()
