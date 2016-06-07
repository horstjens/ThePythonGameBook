# -*- coding: utf-8 -*-
"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: template to show how to move surfaces (not pygames Sprite class!)
around
"""


import pygame 
import math
import random


class Ball(object):
    """this is not a native pygame sprite but instead a pygame surface"""
    def __init__(self, radius = 50, color=None, x=320, y=240, dx=None, dy=None):
        """create a (black) surface and paint a blue ball on it"""
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
        self.surface = pygame.Surface((self.width,self.height))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        # left blue eye
        pygame.draw.circle (self.surface, (0,0,200) , (radius //2 , radius //2), radius// 3)
        # right yellow yey
        pygame.draw.circle (self.surface, (255,255,0) , (3 * radius //2  , radius //2), radius// 3)
        # grey mouth
        pygame.draw.arc(self.surface, (32,32,32), (radius //2, radius, radius, radius//2), math.pi, 2*math.pi, 1)
        # self.surface = self.surface.convert() # for faster blitting if no transparency is used. 
        # to avoid the black background, make black the transparent color:
        self.surface.set_colorkey((0,0,0))
        self.surface = self.surface.convert_alpha() # faster blitting with transparent color
        
    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # time based movement
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        # bouncing on edge
        # x,y is always the upper left corner of the rect
        if self.x < 0:
            self.x = 0
            self.dx *= -1 
        if self.y < 0:
            self.y = 0
            self.dy *= -1
        if self.x + self.width > PygView.width:
            self.x = PygView.width - self.width
            self.dx *= -1
        if self.y + self.height > PygView.height:
            self.y = PygView.height - self.height
            self.dy *= -1
        
    def blit(self, background):
        """blit the Ball on the given background surface"""
        background.blit(self.surface, ( self.x, self.y))

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
           default arguments 
        """
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
        """painting on the surface"""
        # make an interesting background 
        draw_examples(self.background)
        # create (non-pygame) Sprites. 
        self.ball1 = Ball(x=100, y=100) # creating the Ball object (not a pygame Sprite)
        self.ball2 = Ball(x=200, y=100) # create another Ball object (not a pygame Sprite)
        self.ballgroup = [ self.ball1, self.ball2 ] # put all "Sprites" into this list
        


    def run(self):
        """The mainloop"""
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_b:
                        self.ballgroup.append(Ball()) # add balls!
            # end of event handler
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            # not-pygame-sprites
            for myball in self.ballgroup:
                myball.update(seconds)
            for myball in self.ballgroup:
                myball.blit(self.screen)
            # write text over everything 
            write(self.screen, "Press b to add another ball", x=self.width//2, y=250, center=True)
            # next frame
            pygame.display.flip()
            
        pygame.quit()


if __name__ == '__main__':
    PygView().run()
