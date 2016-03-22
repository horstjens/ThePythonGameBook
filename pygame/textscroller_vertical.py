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

  
    def __init__(self, text, width=640, height=400, fps=30, textcolor=(0,0,255), 
                 bgcolor=(255,255,255), font=('mono', 24, True), new_init=True, bg_filename=None):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        
        #pygame.mixer.pre_init(44100, -16, 2, 2048) 

        if new_init:
            pygame.init()
        
        #jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
        #self.sound1 = pygame.mixer.Sound(os.path.join('data','Pickup_Coin.wav'))
        #self.sound2 = pygame.mixer.Sound(os.path.join('data','Jump.wav'))
        #self.sound3 = pygame.mixer.Sound(os.path.join('data','mix.wav'))
        pygame.display.set_caption("Press ESC to quit, curosr keys / PgUp, PgDown to scroll")
        self.text = text
        self.bgcolor = bgcolor
        self.textcolor = textcolor
        self.lines = text.split("\n")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        if bg_filename is None:
           self.background.fill(self.bgcolor) # fill background white
        else:
           try:
               print("i try to load:", bg_filename)
               self.background = pygame.image.load(bg_filename)
               self.background = pygame.transform.scale(self.background, (self.width, self.height))
           except:
                print("exception while processing:", bg_filename)
                self.background.fill(self.bgcolor) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.offset_y = self.height - 10
        self.x = 100
        self.dy = 50
        self.text_height = len(self.lines) * self.dy
        self.bold = font[2]
        self.font = pygame.font.SysFont(font[0], font[1], self.bold)

    def paint(self):
        """painting on the surface"""
        y = self.offset_y
        for line in self.lines:
            self.draw_text(line, self.x, y, self.textcolor, self.bold )
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
                    if event.key==pygame.K_UP:
                        #print(m.active_itemnumber)
                        self.offset_y += 50
                        #self.sound2.play()
                    if event.key==pygame.K_DOWN:
                        self.offset_y -= 50
                    if event.key==pygame.K_LEFT:
                        self.x -= self.dy
                    if event.key == pygame.K_RIGHT:
                        self.x += self.dy
                    if event.key == pygame.K_PAGEUP:
                        self.offset_y += self.height
                    if event.key == pygame.K_PAGEDOWN:
                        self.offset_y -= self.height
                        
            
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0 # important for python2
            self.offset_y -= seconds * 10 # scroll 10 pixels / second
            if self.offset_y * -1 > self.text_height:
                running = False
            self.playtime += milliseconds / 1000.0
            self.paint()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        #pygame.quit()
        return


    def draw_text(self, text ,x=50 , y=0,color=(27,135,177), bold=True):
        #if y==0:
        #    y= self.height - 50
        
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, bold, color)
        self.screen.blit(surface, (x,y))

    
####

if __name__ == '__main__':

    # call with width of window and fps
    lines = "first line \nsecond line \nanother line \nnothing \n\n\nThe end is near\n\nThis is the end"
    PygView(text=lines).run()
