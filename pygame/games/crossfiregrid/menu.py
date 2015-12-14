# -*- coding: utf-8 -*-
"""
game menu to set parameters for crossfiregrid"""


import pygame 
import random
import sys
import os.path
import crossfiregrid
from libs import easygui



class Menu(object):
    """menu system, consisting of self.menudict. Each menu name with submenu(es) must be unique
       returns the selected menu item.
       returns None when "back" or submenu name is selected
       keeps a history of chosen menu items
       current menu name can be accessed via self.menuname
       each submenu has "back" as last menuitem automatically added
       
       This menu changes the values of:
       self.fps, self.width, self.height, self.grid, self.bulletlifetime, self.p_wall
       if "play" is selected, the game crossfiregrid is started and the menu
       continues with the same values as before
       """
    # https://en.wikipedia.org/wiki/List_of_common_resolutions#Computer_graphics
    def __init__(self):
        self.menudict={"root": ["play","graphics", "difficulty", "help", "credits", "highscore","quit"],
                       "graphics": ["screen resolution", "fps", "picture folder"],
                       "difficulty": ["wall probability", "bullet duration", "grid size"], 
                       "screen resolution": ["320x200", "640x400","800x640", "1024x800","1280x960","1280x1024", "1920x1024", "custom"],
                       "grid size": ["10", "25", "50", "100", "200", "custom"],
                       "wall probability": ["0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "custom"],
                       "bullet duration": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "custom"],
                       "fps": ["30","60","custom"], 
                       } 
        self.menuname="root" # main menu with sub menues
        self.history = []
        self.historynumber = []
        self.items=self.menudict[self.menuname]
        self.itemnumber=0
    
    def nextitem(self):
        self.itemnumber+=1
        if self.itemnumber==len(self.items):
            self.itemnumber=0
        return self.itemnumber
            
    def previousitem(self):
        self.itemnumber-=1
        if self.itemnumber < 0:
            self.itemnumber=len(self.items)-1
        return self.itemnumber 
        
    def get_text(self):
        """ change into submenu?"""
        try:
           print("i found:", self.itemnumber, self.items[self.itemnumber])
           text = self.items[self.itemnumber]
        except:
           text = "root"
           print("exception -> root")
        if text in self.menudict:
            self.history.append(self.menuname)
            self.historynumber.append(self.itemnumber)
            self.menuname = text
            self.items = self.menudict[text]
            self.itemnumber = 0
            
        elif text == "back":
            # remove last item from old
            self.menuname =  self.history.pop(-1)
            self.itemnumber = self.historynumber.pop(-1)
            self.items = self.menudict[self.menuname]
        if self.menuname != "root":
            self.items.append("back")
        if text in self.menudict or text == "back":
            return None
        return text
        

class PygView(object):

    def __init__(self, width=640, height=400, fps=30, grid=50, 
                 bulletlifetime = 3.5, p_wall = 0.5, picturepath="data"):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        
        pygame.mixer.pre_init(44100, -16, 2, 2048) 

        pygame.init()
        print("pygame initialized")
        
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
        self.m = Menu()
        #---
        self.grid = grid
        self.p_wall = p_wall
        self.bulletlifetime = bulletlifetime
        self.picturefolder = picturepath

    def paint(self):
        """painting the menu on the surface"""
        deltay = 50
        self.draw_text("menu node: {}".format(self.m.menuname), 100, 10, (0,128,0))
        for i in  self.m.items:
            n=self.m.items.index(i)
            if n==self.m.itemnumber:
                self.draw_text("-->",50,  self.m.items.index(i)*30+deltay,(0,0,255))
                self.draw_text(i, 100, self.m.items.index(i)*30+deltay,(0,0,255))
            else:
                self.draw_text(i, 100, self.m.items.index(i)*30+deltay)
                
    def draw_text(self, text ,x=50 , y=0,color=(27,135,177)):
            if y==0:
                y= self.height - 50
            """Center text in window"""
            fw, fh = self.font.size(text)
            surface = self.font.render(text, True, color)
            self.screen.blit(surface, (x,y))


    def run(self):
        """The mainloop
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key==pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP2:
                        print(self.m.itemnumber)
                        self.m.nextitem()
                        print(self.m.itemnumber)
                        #self.sound2.play()
                    if event.key==pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8:
                        self.m.previousitem()
                        #self.sound1.play()
                    if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER :
                        #self.sound3.play()
                        text = self.m.get_text()
                        if text=="play":
                            #print("activating external program")
                            crossfiregrid.PygView(self.width, self.height, 
                                          grid=self.grid, bulletlifetime = self.bulletlifetime, 
                                          p_wall = self.p_wall, fps = self.fps, picturepath=self.picturefolder ).run()
                            PygView(width=self.width, height=self.height, fps=self.fps, grid=self.grid, 
                 bulletlifetime = self.bulletlifetime, p_wall = self.p_wall).run()
                        elif text=="quit":
                            pygame.quit()
                            sys.exit()
                        elif text=="picture folder":
                            self.picturefolder = easygui.diropenbox("please choose a folder containing pretty .jpg pictures")
                        elif text is not None: # not "back" and not a submenu name
                            if self.m.menuname == "screen resolution":
                                if text == "custom":
                                    self.width = easygui.integerbox("please enter screen width in pixel", lowerbound=100, upperbound=4000, default=600)
                                    self.height = easyghi.integerbox("please enter screen height in pixel", lowerbound=100, upperbound=4000, default = 400)
                                else:
                                    self.width = int(text.split("x")[0])
                                    self.height  = int(text.split("x")[1])
                                self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
                                self.background = pygame.Surface(self.screen.get_size()).convert()  
                                self.background.fill((255,255,255)) # fill background white
                            elif self.m.menuname == "fps":
                                if text == "custom":
                                    self.fps = easygui.integerbox("please enter desired value for frames per second", lowerbound=1, upperbound=500, default=30)
                                else:
                                    self.fps = int(text) # text is "30" or "60"
                            elif self.m.menuname == "wall probability":
                                if text == "custom":
                                    self.p_wall = easygui.integerbox("please enter desired value for wall probability in promille.\n examples: \n10% = 100\n50.5% = 505\n99.9% = 999", default=500, lowerbound=1, upperbound = 999) / 1000
                                else:
                                    self.p_wall = float(text)
                            elif self.m.menuname == "grid size":
                                self.grid = int(text)
                            elif self.m.menuname == "bullet duration":
                                self.bulletlifetime = float(text)
                                

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("FPS: {:6.3} graphic: {}x{}".format(
                           self.clock.get_fps(), self.width, self.height  ), y=self.height - 50, color=(30, 120 ,18))
            self.draw_text("p_wall: {:.2f} grid size: {} bullet: {:.1f}".format(self.p_wall,self.grid, self.bulletlifetime), y=self.height - 25, color=(30, 120 ,18))
            pygame.draw.line(self.screen,(random.randint(0,255),random.randint(0,255), random.randint(0,255)),(50,self.height - 80),(self.width -50,self.height - 80) ,3)             
            self.paint() # redraw menu
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            
        pygame.quit()
        sys.exit()


    

    
####

if __name__ == '__main__':

    # call with width of window and fps
    PygView().run()
