#!/usr/bin/env python

"""
Name   : 003_blitting.py
URL    : http://thepythongamebook.com/en:part2:pygame:step003
Author : yipyip
Licence: gpl, see http://www.gnu.org/licenses/gpl.html
"""

####

import pygame 
import random

####

class PygView(object):

  
    def __init__(self, width=800, height=600, fps=200):
        """Initializing background surface for static drawing
           and screen surface for dynamic drawing 
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        #self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        # white background
        self.background.fill((255, 255, 255))

        self.fps = fps
        self.clock = pygame.time.Clock()

        self.act_surface = self.screen
        self.act_rgb = 255, 0, 0
        
        self.pulseRadius = 50
        self.pdx = 1 # change of radius


    def draw_static(self):

        self.act_surface = self.background


    def draw_dynamic(self):

        self.act_surface = self.screen


    def set_color(self, rgb):

        self.act_rgb = rgb

        
    def circle(self, x, y, radius):
        """Allocate surface for blitting and draw circle
        """
        surface = pygame.Surface((2 * radius, 2 * radius))
        pygame.draw.circle(surface, self.act_rgb, (radius, radius), radius)
        surface.set_colorkey((0, 0, 0))
        self.act_surface.blit(surface.convert_alpha(), (x, y))
        
    def pulsatingCircle(self, x, y):
        """glittering circle with radius pulsating between 0 and 100"""
        self.pulseRadius += self.pdx
        if self.pulseRadius == 100 or self.pulseRadius ==10:
            self.pdx *=-1
        print self.pulseRadius
        surface = pygame.Surface((2 * self.pulseRadius, 2 * self.pulseRadius))
        color = (random.randint(0,255), 
                 random.randint(0,255), 
                 random.randint(0,255))
        pygame.draw.circle(surface, color, (self.pulseRadius, self.pulseRadius),
                           self.pulseRadius,5)
        surface.set_colorkey((0, 0, 0))
        self.act_surface.blit(surface.convert_alpha(), (x, y))
       

    def run(self, draw_dynamic):
        """The mainloop
        """
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            draw_dynamic()
            self.pulsatingCircle(100,100)
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            pygame.display.set_caption("fps: %.2f" % self.clock.get_fps())
        pygame.quit()

####

class Ball(object):
    """A circle object with no hardcoded dependency on pygame
       (and no other libs too, obviously...)
    """
    def __init__(self, x, y, radius, speed_x, color=(0,0,255)):

        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.color = color


    @property
    def max_x(self):

        return self.x + self.radius * 2
    
        
    def rel_move(self, dx, dy):

        self.x += dx
        self.y += dy


    def draw(self, view):
        """ Draw on a device with an appropriate interface
        """
        view.set_color(self.color)
        view.circle(self.x, self.y, self.radius)
     
####

def action(balls, width, view):
    """ Return a function for the pygame mainloop
    """
    # balls move to the right first 
    right_moving = [True] * len(balls)
    
    def animate_balls():
        """ Draw moving balls
        """
        for i, ball in enumerate(balls):
            if right_moving[i]:
                if ball.max_x < width:
                    ball.rel_move(ball.speed_x, 0)
                else:
                    right_moving[i] = False
            else:
                if ball.x > 0:
                    ball.rel_move(-ball.speed_x, 0)
                else:
                    right_moving[i] = True
            
            ball.draw(view)

    return animate_balls    
        
####

def main(width):
    """Simple example with 2 stationary and 3 moving balls
    """   
    view = PygView(width)
    
    view.draw_static()
    ball01 = Ball(50, 60, 50, 0, (255, 255, 0))
    ball01.draw(view)
    ball02 = Ball(250, 150, 190, 0, (66, 1, 166))
    ball02.draw(view)

    view.draw_dynamic()
    ball1 = Ball(15, 130, 100, 1, (255, 0, 0))
    ball2 = Ball(25, 200, 80, 2, (0, 255, 155))
    ball3 = Ball(800, 400, 70, 3, (250, 100, 255))

    loopfunc = action((ball1, ball2, ball3), width, view)
    view.run(loopfunc)

####
    
if __name__ == '__main__':

    main(900)
    
