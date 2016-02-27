# -*- coding: utf-8 -*-
"""003_static_blit_pretty_template.py"""
import pygame 
import random

class PygView(object):
    width = 0
    height = 0
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        PygView.width = width
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)

    def paint(self):
        """painting on the surface"""
        # pygame.draw.line(Surface, color, start, end, width) 
        pygame.draw.line(self.background, (0,255,0), (10,10), (50,100))
        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        pygame.draw.rect(self.background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
        # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        pygame.draw.circle(self.background, (0,200,0), (200,50), 35)
        # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
        pygame.draw.polygon(self.background, (0,180,0), ((250,100),(300,0),(350,50)))
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
        pygame.draw.arc(self.background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
    
    def run(self):
        self.paint() 
        myball = Ball() # creating the Ball object
        running = True
        while running:
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    # keys that you press once and release
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_q: # stopper 
                        myball.dx = 0
                        myball.dy = 0
                        myball.x = PygView.width //3 # one third without remainder
                        myball.y = PygView.height // 2 # one half without remainder
            pressedkeys = pygame.key.get_pressed() # keys that you can press all the time
            if pressedkeys[pygame.K_a]:
                myball.dx -=1
            if pressedkeys[pygame.K_d]:
                myball.dx +=1
            if pressedkeys[pygame.K_w]:
                myball.dy -= 1
            if pressedkeys[pygame.K_s]:
                myball.dy += 1
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            myball.update(seconds)
            myball.blit(self.screen) # blitting it
        pygame.quit()

    def draw_text(self, text):
        """Center text in window"""
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
        self.dx = 0
        self.dy = 0
        # create a rectangular surface for the ball 50x50
        self.surface = pygame.Surface((2*self.radius,2*self.radius))    
        pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        self.surface = self.surface.convert() # for faster blitting. 
        # to avoid the black background, make black the transparent color:
        # self.surface.set_colorkey((0,0,0))
        # self.surface = self.surface.convert_alpha() # faster blitting with transparent color
   
    def update(self, seconds):
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        # wrap around screen
        if self.x < 0:
            self.x = PygView.width
        if self.x > PygView.width:
            self.x = 0
        if self.y < 0:
            self.y = PygView.height
        if self.y > PygView.height:
            self.y = 0

    def blit(self, ground):
        """blit the Ball on the background"""
        ground.blit(self.surface, ( self.x, self.y))
        
if __name__ == '__main__':
    PygView().run() # call with width of window and fps
