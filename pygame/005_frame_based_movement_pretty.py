#!/usr/bin/env python

"""
Name   : blit_pulse2.py
URL    : http://thepythongamebook.com/en:part2:pygame:step003
Author : yipyip
Licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with pyhton3.4 and python2.7
"""

####

import pygame as pyg
import random as rand

####

def random_rgb():
    
   return rand.randint(0, 255), rand.randint(0,255), rand.randint(0, 255)

####

class PygView(object):

  
    def __init__(self, width=800, height=600, fps=50):
        """Initializing background surface for static drawing
           and screen surface for dynamic drawing 
        """
        pyg.init()
        pyg.display.set_caption("Press ESC to quit")
        
        self.width = width
        self.height = height
        
        self.screen = pyg.display.set_mode((self.width, self.height), pyg.DOUBLEBUF)
        self.background = pyg.Surface(self.screen.get_size()).convert()  
        # white blackground
        self.background.fill((255, 255, 255))

        self.act_surface = self.screen
        self.act_rgb = 255, 0, 0

        
    def draw_static(self):

        self.act_surface = self.background


    def draw_dynamic(self):

        self.act_surface = self.screen


    def set_color(self, rgb):

        self.act_rgb = rgb

        
    def circle(self, x, y, radius, width):
        """Allocate surface for blitting and draw circle
        """
        rad2 = 2 * radius
        surface = pyg.Surface((rad2, rad2))
        pyg.draw.circle(surface, self.act_rgb, (radius, radius), radius, width)
        surface.set_colorkey((0, 0, 0))
        self.act_surface.blit(surface.convert_alpha(), (x, y))


    def run(self, draw_dynamic):
        """The mainloop
        """
        running = True
        while running:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    running = False 
                elif event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        running = False

            draw_dynamic()
            pyg.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pyg.quit()

####

class Ball(object):
    """A circle object with no hardcoded dependency on pygame
       (and other libs too, obviously...)
    """
    def __init__(self, x, y, radius, speed_x=1, speed_pulse=0, color=(0,0,255), width=0):

        self.x = x
        self.y = y
        self.radius = radius
        self.act_radius = radius
        self.speed_x = speed_x
        self.speed_pulse = speed_pulse
        self.color = color
        self.width = width
        self.shrinking = True


    @property
    def max_x(self):

        return self.x + self.radius * 2
    
        
    def rel_move(self, dx, dy):

        self.x += dx
        self.y += dy


    def pulse(self):
        """Shrink or expand ball
        """
        if not self.speed_pulse:
            return

        # balls are shrinking first 
        if self.shrinking:
            if self.act_radius > self.width:
                self.act_radius -= self.speed_pulse
                self.act_radius = max(self.act_radius, self.width)
            else:
                self.shrinking = False
        else:
            if self.act_radius < self.radius:
                self.act_radius += self.speed_pulse
            else:
                self.shrinking = True
        
        
    def draw(self, view):
        """ Draw on a device with an appropriate interface
        """
        if self.speed_pulse:
            color = random_rgb()
        else:
            color = self.color 
        view.set_color(color)
        view.circle(self.x, self.y, self.act_radius, self.width)
     
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
            
            ball.pulse() 
            ball.draw(view)

    return animate_balls    
        
####

def main(width):
    """Simple example with stationary and moving balls
    """   
    view = PygView(width)
    
    view.draw_static()
    # args:  x, y, radius, speed_x, speed_pulse, color, border_width
    # border_width <= radius !
    ball01 = Ball(50, 60, 50, 0, 0, (255, 255, 0))
    ball01.draw(view)
    ball02 = Ball(250, 150, 190, 0, 0, (66, 1, 166))
    ball02.draw(view)

    view.draw_dynamic()
    ball1 = Ball(15, 130, 100, 1, 0, (255, 0, 0))
    ball2 = Ball(25, 200, 80, 2, 0, (0, 255, 155))
    ball3 = Ball(20, 220, 110, 1, 1, (100, 55, 155))
    ball4 = Ball(20, 400, 70, 3, 0, (250, 100, 255))
    ball5 = Ball(90, 390, 70, 0, 1, (250, 100, 255), 1)

    loopfunc = action((ball1, ball2, ball4, ball5), width, view)
    view.run(loopfunc)

####
    
if __name__ == '__main__':

    main(900)
    
