# -*- coding: utf-8 -*-
"""
scrolls an multi-line text vertical in a pygame window. 
like the linux command "less" or like the intro scene in starwars movies
"""


import pygame 
#import simpledefense
import random
import sys
import os.path


      
        
            

class PygView(object):

  
    def __init__(self, text, width=640, height=400, fps=30, color=(0,0,255)):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        
        pygame.mixer.pre_init(44100, -16, 2, 2048) 

        pygame.init()
        
        #jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
        #self.sound1 = pygame.mixer.Sound(os.path.join('data','Pickup_Coin.wav'))
        #self.sound2 = pygame.mixer.Sound(os.path.join('data','Jump.wav'))
        #self.sound3 = pygame.mixer.Sound(os.path.join('data','mix.wav'))
        pygame.display.set_caption("Press ESC to quit, UP / DOWN to scroll")
        self.text = text
        self.color = color
<<<<<<< HEAD
        self.lines = text.split("\n")
=======
        self.lines = text.split()
>>>>>>> 86188f7a4c63056700b116cdf590b50ef2bcc013
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.offset_y = self.height - 10
        self.x = 100
        self.dy = 50
        self.font = pygame.font.SysFont('mono', 24, bold=True)

    def paint(self):
        """painting on the surface"""
        y = self.offset_y
        for line in self.lines:
            self.draw_text(line, self.x, y, self.color)
            y+= self.dy
                

    def run(self):
        """The mainloop
        """
        #self.paint() 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key==pygame.K_DOWN:
                        #print(m.active_itemnumber)
                        self.offset_y += 50
                        #self.sound2.play()
                    if event.key==pygame.K_UP:
                        self.offset_y -= 50
                        self.offset_y = max(0, self.offset_y)
                        #self.sound1.play()
            
                                            
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000
            self.offset_y -= seconds * 10
            self.playtime += milliseconds / 1000.0
            #self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
            #               self.clock.get_fps(), " "*5, self.playtime), color=(30, 120 ,18))
            #pygame.draw.line(self.screen,(random.randint(0,255),random.randint(0,255), random.randint(0,255)),(50,self.height - 80),(self.width -50,self.height - 80) ,3)             
            self.paint()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        #pygame.quit()
        return


    def draw_text(self, text ,x=50 , y=0,color=(27,135,177)):
        if y==0:
            y= self.height - 50
        
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))

    
####

if __name__ == '__main__':

    # call with width of window and fps
    lines = "blabla \n blabal \nbla bla bla\nabc\ndef\nghi\njkl\n\n\n\nende"
    PygView(text=lines).run()
