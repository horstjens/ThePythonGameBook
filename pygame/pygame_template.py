#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name:    pygmin.py
Purpose: Minimal code skeleton for pygame experiments 
URL:     
Author:  yipyip
Licence: gpl, see http://www.gnu.org/licenses/gpl.html
"""

####

import pygame

####

class PygView(object):

  
    def __init__(self, width=640, height=400):
        
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.fps = 30 # frames per second
        pygame.display.set_caption("Press ESC to quit")
       

    def run(self):
        """The mainloop
        """
        self.clock = pygame.time.Clock() 
        running = True
        while running:
            self.seconds = self.clock.tick(self.fps)/1000.0 # seconds since last frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.set_caption("press Esc to quit. Fps: %.2f (%i x %i)"%(self.clock.get_fps(), self.width, self.height))
            pygame.display.flip()          
        pygame.quit()

####

if __name__ == '__main__':
    #PygView(width=800, height=600).run()
    PygView().run()
