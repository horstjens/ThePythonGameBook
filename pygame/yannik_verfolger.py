import pygame
import random


class Ball(object):
    def __init__(self, radius = 50, color=(0,0,255), x=320, y=240, friction=0.999):
        self.radius = radius
        self.hitpoints =100
        self.color = color
        self.x = x
        self.friction = friction
        self.dy=0
        self.dx=0
        self.y = y
        self.surface = pygame.Surface((2*self.radius,2*self.radius))
        pygame.draw.circle(self.surface, color, (radius, radius), radius)
        self.surface = self.surface.convert()
        self.liste= []
        for i in range(11):
            self.liste.append((self.x,self.y))
        
    def update(self,seconds):
        
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        if self.x<0:
            self.hitpoints-=1
            #self.x= PygView.width
            self.x = 0
            self.dx *= -0.3
        if self.x > PygView.width:
            self.hitpoints-=1
            self.x = PygView.width
            self.dx *= -0.3
        if self.y < 0:
            self.hitpoints-=1
            #self.y = PygView.height
            self.y = 0
            self.dy *= -0.3
        if self.y>PygView.height:
            self.hitpoints-=1
            self.y = PygView.height
            self.dy *= -0.3
        self.dx *= self.friction
        self.dy *= self.friction
        
    def blit(self, background):
        background.blit(self.surface, (self.x, self.y))

class PygView(object):
    width = 0
    height = 0
    def __init__(self, width=640, height=400, fps=100):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        PygView.width = width
        self.height = height
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height),pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont("mono", 24, bold=True)
    
    def paint(self):
        pygame.draw.line(self.background, (11,11,235), (10,10), (50,100)) 
        pygame.draw.rect(self.background, (255,230,48), (45,45,100,45))
        pygame.draw.rect(self.background, (184,255,48), (40,40,80,35))
        pygame.draw.rect(self.background, (61,255,48), (35,35,60,25))
        pygame.draw.rect(self.background, (48,255,200), (30,30,40,15))
        pygame.draw.rect(self.background, (255,230,48), (45,195,100,45))
        pygame.draw.rect(self.background, (184,255,48), (40,220,80,35))
        pygame.draw.rect(self.background, (61,255,48), (35,245,60,25))
        pygame.draw.rect(self.background, (48,255,200), (30,260,40,15))
        pygame.draw.circle(self.background, (11,11,225), (205, 35),45)
        pygame.draw.circle(self.background, (255,72,48), (205, 35),40)
        pygame.draw.circle(self.background, (255,48,203), (205, 35),35)
        pygame.draw.circle(self.background, (198,255,48), (205, 35),30)
        pygame.draw.circle(self.background, (111,255,48), (205, 35),25)
        pygame.draw.circle(self.background, (48,255,75), (205, 35),20)
        pygame.draw.circle(self.background, (48,255,192), (205, 35),15)
        pygame.draw.polygon(self.background, (11,11,215),((250,100),(300,0),(350,50)))
        pygame.draw.arc(self.background, (11,11,205),(400,10,150,100), 0, 3.14)

    def run(self):
       self.paint()
       running = True
       myball1 = Ball(radius=5,color=(0,255,255))
       myball2=Ball(radius=5,color=(255,45,45))
       verfolger1=Ball(radius=6,color=(255,255,255), friction=0.99)
       clock=pygame.time.Clock()
      
       while running:
           pygame.display.set_caption("hitpoints: myball1: {} myball2: {} verfolger1: {}".format(myball1.hitpoints, myball2.hitpoints, verfolger1.hitpoints))
           milliseconds= clock.tick(self.fps)
           seconds=milliseconds /1000.0
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   running = False
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       running = False
                   if event.key == pygame.K_LCTRL:
                       myball1.x =random.randint(0,self.width)
                       myball1.y =random.randint(0,self.height)
                   if event.key == pygame.K_q:
                       myball1.x =self.width//2     
                       myball1.y =self.height//2
                       myball1.dx=0
                       myball1.dy=0
                      
                   if event.key == pygame.K_RCTRL:
                       myball2.x =random.randint(0,self.width)
                       myball2.y =random.randint(0,self.height)
                   if event.key == pygame.K_p:
                       myball2.x =self.width//3     
                       myball2.y =self.height//3
                       myball2.dx=0
                       myball2.dy=0
                    
           pressedkeys = pygame.key.get_pressed()
           if pressedkeys[pygame.K_UP]:
               myball2.dy-=1
           if pressedkeys[pygame.K_DOWN]:
               myball2.dy+=1
           if pressedkeys[pygame.K_LEFT]:
               myball2.dx-=1
           if pressedkeys[pygame.K_RIGHT]:
               myball2.dx+=1            
                       
           pressedkeys = pygame.key.get_pressed()
           if pressedkeys[pygame.K_w]:
               myball1.dy-=1
           if pressedkeys[pygame.K_s]:
               myball1.dy+=1
           if pressedkeys[pygame.K_a]:
               myball1.dx-=1
           if pressedkeys[pygame.K_d]:
               myball1.dx+=1
           # verfolger,  wo will ich hin?
           dx1 = abs(verfolger1.x - myball1.x)
           dy1= abs(verfolger1.y- myball1.y)
           dx2= abs(verfolger1.x- myball2.x)
           dy2= abs(verfolger1.y- myball2.y)
           d1 = (dx1**2 + dy1**2)**0.5
           d2 = (dx2**2 + dy2**2)**0.5
           if d1>d2:
               # verfolger fährt zum myball2
               if myball2.x > verfolger1.x:
                   verfolger1.dx += 1
               else:
                   verfolger1.dx -= 1
               if myball2.y > verfolger1.y:
                   verfolger1.dy +=1
               else:
                   verfolger1.dy -= 1
           else:
               # verfolger fährt zum myball1
               if myball1.x > verfolger1.x:
                   verfolger1.dx += 1
               else:
                   verfolger1.dx -= 1
               if myball1.y > verfolger1.y:
                   verfolger1.dy +=1
               else:
                   verfolger1.dy -= 1
           milliseconds = self.clock.tick(self.fps)
           self.playtime += milliseconds / 1000.0
           self.draw_text("FPS: {:5.3f}{}PLAYTIME: {:6.3} SECONDS".format(
                          self.clock.get_fps(), " "*5, self.playtime))
           pygame.display.flip()
           self.screen.blit(self.background, (0, 0))
           pygame.draw.line(self.screen, (55,55,55), (myball1.x, myball1.y), (myball2.x, myball2.y), 1)
           myball1.update(seconds)
           myball1.blit(self.screen)
           myball2.update(seconds)
           myball2.blit(self.screen)
           verfolger1.update(seconds)
           verfolger1.blit(self.screen)
       pygame.quit()
       
    def draw_text(self, text):
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, (50,150))

if __name__ == "__main__":
    PygView().run()
