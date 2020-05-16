# -*- coding: utf-8 -*-
"""
003_static_blit_pretty.py
static blitting and drawing (pretty version)
url: http://thepythongamebook.com/en:part2:pygame:step003
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with pyhton3.4 and python2.7

Blitting a surface on a static position
Drawing a filled circle into ballsurface.
Blitting this surface once.
introducing pygame draw methods
The ball's rectangular surface is black because the background
color of the ball's surface was never defined nor filled."""


import pygame 
import random


class PygView(object):

  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.newflash()
        
    def newflash(self):
        self.points = []
        richtung = random.choice(("n","ne", "e", "se","s","sw", "w", "nw"))
        for x in range(0, self.width//2, self.width//16):
            if richtung == "n":
                self.points.append([self.width//2, self.height//2-x])
            elif richtung == "s":
                self.points.append([self.width//2, self.height//2+x])
            elif richtung == "w":
                self.points.append([self.width//2-x, self.height//2])
            elif richtung == "e":
                self.points.append([self.width//2+x, self.height//2])
            elif richtung == "ne":
                self.points.append([self.width//2+x, self.height//2-x])
            elif richtung == "se":
                self.points.append([self.width//2+x, self.height//2+x])
            elif richtung == "nw":
                self.points.append([self.width//2-x, self.height//2-x])
            elif richtung == "sw":
                self.points.append([self.width//2-x, self.height//2+x])
        #print(self.points)

    def flash(self):
        f = random.randint(0,255)
        farbe = (f,f,255) # zwischen blau und weiß
        dicke = random.randint(2,5)
        if random.random() < 0.28:
            # 5% chance für y Änderung
            i = random.choice(self.points)
            i[1] += random.randint(-35,35)
        if random.random() < 0.28:
            # 5% chance für x Änderung
            i = random.choice(self.points)
            i[0] += random.randint(-35,35)
        # --- blitz zeichnen ---
        start = (self.width//2,self.height//2)
        for p in self.points:
            pygame.draw.line(self.screen, farbe, start, p, dicke)
            start = p
        if random.random() < 0.035:
            #  1/2 % chance auf komplett neuen blitz
            self.newflash()
    
    def paint(self):
        """painting on the surface"""
        #------- try out some pygame draw functions --------
        # pygame.draw.line(Surface, color, start, end, width) 
        #pygame.draw.line(self.background, (0,255,0), (10,10), (50,100))
        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        #pygame.draw.rect(self.background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
        # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        #pygame.draw.circle(self.background, (0,200,0), (200,50), 55, 0)
        
        # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
        #pygame.draw.polygon(self.background, (0,180,0), ((250,100),(300,0),(350,50)))
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
        #pygame.draw.arc(self.background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
        # ------------------- blitting a Ball --------------
        #myball = Ball() # creating the Ball object
        #myball.blit(self.background) # blitting it
        for radius in range(320, 4, -10):
            pygame.draw.circle(self.screen, 
                               (radius%255, 0, radius%255), 
                               (320, 200), radius)
            
            
    def run(self):
        """The mainloop
        """
        self.paint() 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime))
            
            # ---- kreise malen -----
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_k]:
                self.paint()
            # ----- blitze malen ----
            if pressed[pygame.K_b]:
                self.flash()
                
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()


    def draw_text(self, text):
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, (50,150))

class Ball(object):
    """this is not a native pygame sprite but instead a pygame surface"""
    def __init__(self, radius = 50, color=(0,0,255), x=320, y=240):
        """create a (black) surface and paint a blue ball on it"""
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        # create a rectangular surface for the ball 50x50
        self.surface = pygame.Surface((2*self.radius,2*self.radius))    
        # pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame documentation
        pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        self.surface = self.surface.convert() # for faster blitting. 
        # to avoid the black background, make black the transparent color:
        # self.surface.set_colorkey((0,0,0))
        # self.surface = self.surface.convert_alpha() # faster blitting with transparent color
        
    def blit(self, background):
        """blit the Ball on the background"""
        background.blit(self.surface, ( self.x, self.y))


    
####

if __name__ == '__main__':

    # call with width of window and fps
    PygView(800,600).run()
