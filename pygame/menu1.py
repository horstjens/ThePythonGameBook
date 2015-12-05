# -*- coding: utf-8 -*-
"""
TODO: soll auch ohne bbb funktionieren
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
#import simpledefense
import random
import sys
import os.path



class Menu(object):
    def __init__(self):
        self.menudict={"root":["Play","Difficulty", "Help", "Credits", "Options","Quit"],
        
                       "Options":["Turn music off","Turn sound off","Change screen resolution"],
                       "Difficulty":["easy","medium","hard","ultimate","hardcore"],
                       "Change screen resolution":["640x400","800x640","1024x800"],
                       "Credits":["Graphics:Alex Wilfinger","Producer:Alex Wilfinger","Coder:Alex Wilfinger","Idea:Alex Wilfinger","Sound:Alex Wilfinger"],
                       "Help":["To shoot with the Archer,klick Leftmousebutton","To shoot with the cannons,klick Rightmousebutton", "To see the range of the archer and cannons press R"]
                       } 
        self.menuname="root"
        self.menuname_old = []
        self.items=self.menudict[self.menuname]
        self.aktivitemnumber=0
    
    def nextitem(self):
        if self.aktivitemnumber==len(self.items)-1:
            self.aktivitemnumber=0
        else:
            self.aktivitemnumber+=1
        return self.aktivitemnumber
            
    def previousitem(self):
        if self.aktivitemnumber==0:
            self.aktivitemnumber=len(self.items)-1
        else:
            self.aktivitemnumber-=1
        return self.aktivitemnumber 
        
    def get_text(self):
        """ change into submenu?"""
        try:
           text = self.items[self.aktivitemnumber]
        except:
           text = "root"
        if text in self.menudict:
            self.menuname_old.append(self.menuname)
            self.menuname = text
            self.items = self.menudict[text]
            # necessary to add "back to previous menu"?
            if self.menuname != "root":
                self.items.append("back")
            self.activitemnumber = 0
            return None
        elif text == "back":
            #self.menuname = self.menuname_old[-1]
            # remove last item from old
            self.menuname =  self.menuname_old.pop(-1)
            self.items = self.menudict[self.menuname]
            if self.menuname != "root":
                self.items.append("back")
            self.activitemnumber = 0
            return None
        return self.items[self.aktivitemnumber] 
        
        
        
            

class PygView(object):

  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        
        pygame.mixer.pre_init(44100, -16, 2, 2048) 

        pygame.init()
        
        #jump = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
        #self.sound1 = pygame.mixer.Sound(os.path.join('data','Pickup_Coin.wav'))
        #self.sound2 = pygame.mixer.Sound(os.path.join('data','Jump.wav'))
        #self.sound3 = pygame.mixer.Sound(os.path.join('data','mix.wav'))
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

    def paint(self):
        """painting on the surface"""
        for i in  m.items:
            n=m.items.index(i)
            if n==m.aktivitemnumber:
                self.draw_text("-->",50,  m.items.index(i)*30+10,(0,0,255))
                self.draw_text(i, 100, m.items.index(i)*30+10,(0,0,255))
            else:
                self.draw_text(i, 100, m.items.index(i)*30+10)
                

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
                        print(m.aktivitemnumber)
                        m.nextitem()
                        print(m.aktivitemnumber)
                        #self.sound2.play()
                    if event.key==pygame.K_UP:
                        m.previousitem()
                        #self.sound1.play()
                    if event.key==pygame.K_RETURN:
                        #self.sound3.play()
                        print(m.get_text())
                        if m.get_text()=="Play":
                            # simpledefense.PygView().run()
                            print("activating external program")
                            # save return 
                            PygView().run()
                        if m.get_text()=="Quit":
                            pygame.quit()
                            sys.exit()
                                            

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime), color=(30, 120 ,18))
            pygame.draw.line(self.screen,(random.randint(0,255),random.randint(0,255), random.randint(0,255)),(50,self.height - 80),(self.width -50,self.height - 80) ,3)             
            self.paint()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()


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
    m=Menu()
    credit_lines=["This game was coded ",
             "2015 by Alex Wilfinger "]
    help_lines=["Defend the castle",
                "Press left mousbutton",
                "to shoot with the archers",
                "Press right mousbutton ",
                "to shoot with the cannons",
                "Press P to poison the monster",
                "Press M to made a mass destruktion",
                "and the mass destruktion kill all ",
                "the enemy."
                "Press R to see the radius of the",
                "cannons and of the archers"]
                    
    PygView().run()
