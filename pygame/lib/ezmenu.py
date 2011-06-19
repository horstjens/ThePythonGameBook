#! /usr/bin/env python

############################################################
#EzMeNu - A simple module to quickly make menus with PyGame#
############################################################
#Licensed under the GNU Lesser General Public License      #
#Created by PyMike <pymike93@gmail.com>                    #
############################################################

import pygame

class EzMenu:

    def __init__(self, *options):
        """Initialise the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i*self.font.get_height()))
            i+=1
            
    def update(self, events):
        """Update the menu and get input for the menu."""
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN:
                    self.options[self.option][1]()
        if self.option > len(self.options)-1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options)-1

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
        
    def set_font(self, font):
        """Set the font used for the menu."""
        self.font = font
        
    def set_highlight_color(self, color):
        """Set the highlight color"""
        self.hcolor = color
        
    def set_normal_color(self, color):
        """Set the normal color"""
        self.color = color
        
    def center_at(self, x, y):
        """Center the center of the menu at x,y"""
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
