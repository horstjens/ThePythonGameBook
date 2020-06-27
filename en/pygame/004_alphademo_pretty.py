#!/usr/bin/env python

"""
004_alphademo_pretty.py
Experiments with colorkey and alpha-value
URL: http://thepythongamebook.com/en:part2:pygame:step004
Author: horst.jens@spielend-programmieren.at, prettifying by yipyip
per-pixel-alpha code by Claudio Canepa <ccanepacc@gmail.com>
updated to python 3.8 by by Áron Boros
Licence: gpl, see http://www.gnu.org/licenses/gpl.html
"""

####

import pygame
import os
import itertools



####

BLENDMODES = ((pygame.BLEND_ADD, "ADD"),
              (pygame.BLEND_SUB, "SUB"),
              (pygame.BLEND_MULT, "MULT"),
              (pygame.BLEND_MIN, "MIN"),
              (pygame.BLEND_MAX, "MAX"),
              (pygame.BLEND_RGBA_ADD, "RGBA ADD"),
              (pygame.BLEND_RGBA_SUB, "RGBA SUB"),
              (pygame.BLEND_RGBA_MULT, "RGBA MULT"),
              (pygame.BLEND_RGBA_MIN, "RGBA MIN"),
              (pygame.BLEND_RGBA_MAX, "RGBA MAX"))

####

def load_pic(name, path="data"):

    return pygame.image.load(os.path.join(path, name))

####

def check(x, minval=0, maxval=255):

    return min(maxval, max(minval, x))
    
####
 
def get_alpha_surface(surface, rgba=(128, 128, 128, 128), mode=pygame.BLEND_RGBA_ADD):
    """
    Return a copy of a surface object with user-defined 
    values for red, green, blue and alpha. Values from 0-255. 
    (Thanks to Claudio Canepa <ccanepacc@gmail.com>)
    """  
    #new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA|pygame.HWSURFACE)
    new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
    new_surface.fill(rgba)
    new_surface.blit(surface, (0, 0), surface.get_rect(), mode)
    
    return new_surface

####

class AlphaDemo(object):


    def __init__(self, width=900, height=600, fontsize=24):

        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.SysFont('None', fontsize)
        self.clock = pygame.time.Clock()
        
        #self.background.fill((255, 255, 255))
        venus = load_pic("800px-La_naissance_de_Venus.jpg").convert()
        # transform venus and blit 
        pygame.transform.scale(venus, (width, height), self.background)
        
        # .png and .gif graphics can have transparency, use convert_alpha()
        self.png_monster = load_pic("colormonster.png").convert_alpha()
        
        # jpg image, no transparency!
        self.jpg_monster = load_pic("colormonster.jpg").convert()

        # per pixel rgba
        self.pp_rgba = [255, 255, 255, 128]
        alpha_up = range(0, 256, 4)
        alpha_down = alpha_up[-1::-1]
#        self.glob_alphas = itertools.cycle(alpha_up + alpha_down)
        self.glob_alphas = itertools.cycle(itertools.chain(itertools.chain(alpha_up,alpha_down)))
        self.step = 4
        self.mode_nr = 7


    def run(self):
        """
        Mainloop
        """
        mainloop = True
        while mainloop:
            self.clock.tick(20)
            # draw background every frame
            self.screen.blit(self.background, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False

            self.action(pygame.key.get_pressed())
            pygame.display.flip()
        pygame.quit()
           

    def action(self, pressed_keys):
        red, green, blue, alpha = self.pp_rgba
        if pressed_keys[pygame.K_UP]: 
            blue = blue + self.step
        if pressed_keys[pygame.K_DOWN]: 
            blue = blue - self.step    
        if pressed_keys[pygame.K_PERIOD]:
            green = green + self.step    
        if pressed_keys[pygame.K_COMMA]:
            green = green - self.step
        if pressed_keys[pygame.K_RIGHT]:
            red = red + self.step    
        if pressed_keys[pygame.K_LEFT]:
            red = red - self.step   
        if pressed_keys[pygame.K_MINUS]:
            alpha = alpha - self.step  
        if pressed_keys[pygame.K_PLUS]:
            alpha = alpha + self.step
        if pressed_keys[pygame.K_RETURN]:
            self.mode_nr = (self.mode_nr + 1) % len(BLENDMODES)    
        
        mode, mode_text = BLENDMODES[self.mode_nr]
        self.pp_rgba = list(map(check, (red, green, blue, alpha)))
        glob_alpha = next(self.glob_alphas)
        self.show_surfaces(self.png_monster.copy(), 'png', 0, 0, 200, 180,
                           glob_alpha, self.pp_rgba, mode)
        self.show_surfaces(self.jpg_monster, 'jpg', 0, 300, 200, 180,
                           glob_alpha, self.pp_rgba, mode)

        text = "left/right=red>%d  comma/period=green>%d  up/dwn=blue>%d  "\
               "+/-=ppalpha>%d  " % tuple(self.pp_rgba)
        pygame.display.set_caption("%s  Enter: Mode>%s" % (text, mode_text))
      
  
    def show_surfaces(self, surf, pictype, x, y, x_delta, height,
                      glob_alpha, pp_rgba, mode):
        
        yh = y + height
        
        #pure surface
        self.screen.blit(surf, (x, y))
        self.write(x, y + height, "%s pure" % pictype)
        # with with colorkey
        ck_surf = surf.copy()
        ck_surf.set_colorkey((255,255,255))
        x = x + x_delta
        self.screen.blit(ck_surf, (x, y))
        self.write(x, yh, "%s colorkey" % pictype)
        # with alpha for whole surface 
        alpha_surf = surf.copy()
        alpha_surf.set_alpha(glob_alpha)
        x = x + x_delta
        self.screen.blit(alpha_surf, (x, y))
        self.write(x, yh, "%s alpha> %d" % (pictype, glob_alpha))
        
        # with per-pixel alpha
        ppa_surf = surf.copy()
        ppa_surf = get_alpha_surface(ppa_surf, pp_rgba, mode)
        x = x + x_delta
        self.screen.blit(ppa_surf, (x, y))
        self.write(x, yh, "%s, per-pixel-alpha" % pictype)


    def write(self, x, y, msg, color=(255,255,0)):

        self.screen.blit(self.font.render(msg, True, color).convert_alpha(), (x, y))
            
####
        
if __name__ == "__main__":
    
    AlphaDemo().run()
