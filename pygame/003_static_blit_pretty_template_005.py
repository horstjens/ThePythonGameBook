# -*- coding: utf-8 -*-
"""003_static_blit_pretty_template.py"""
import pygame 
import random


class FlyingObject(pygame.sprite.Sprite):
    number = 0
    
    def __init__(self, **kwargs):
        self._default_parameters(**kwargs) # named parameters
        self._overwrite_parameters()       # overwrite some parameters
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.number = FlyingObject.number
        FlyingObject.number += 1
        self.create_image()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        
        
    
    def _overwrite_parameters(self):
        """ use this method to overwrite attributes before create_image() is called"""
        pass 
    
    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""
           
        for key, arg in kwargs.items():
            setattr(self, key, arg)  # make an attribute (self. ) out of an parameter
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            if "x" in kwargs and "y" in kwargs:
                self.pos = pygame.math.Vector2(x,-y)
            else:
                self.pos = pygame.math.Vector2(100,-200)
        if "move" not in kwargs:
            if "dx" in kwargs and "dy" in kwargs:
                self.move = pygame.math.Vector2(dx, dy)
            elif "speed" in kwargs:
                self.move = v.Vec2d(speed,0)
                if "angle" in kwargs:
                    self.move.rotate(angle)
            else:
                self.move = pygame.math.Vector2(0,0)
                self.speed = 0
                self.angle = 0
        if "speed" not in kwargs:
            self.speed = self.move.length()
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "radius" not in kwargs:
            self.radius = None
        #if "width" not in kwargs:
        #    self.width = self.radius * 2
        #if "height" not in kwargs:
        #    self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "max_age" not in kwargs:
            self.max_age = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "control_method" not in kwargs:
            self.control_method = "cursor"
        if "radius" not in kwargs:
            self.radius = 10
        #print(self.pos, self.move, self.speed)
   
        
    def create_image(self):
        self.image = pygame.Surface((2 * self.radius, 2* self.radius))
        pygame.draw.polygon(self.image, self.color, [ (0,0), (2*self.radius,self.radius),(0, 2*self.radius),])
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
     
     
    def rotate_image(self, angle):
        """rotates the original image (image0) for angle degrees"""
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        
    def control(self):
        if self.control_method == "cursor":
            upkey = pygame.K_UP
            downkey = pygame.K_DOWN
            leftkey = pygame.K_LEFT
            rightkey = pygame.K_RIGHT
            # --- keyboard control ----
            pressedkeys = pygame.key.get_pressed() # keys that you can press all the time
            if pressedkeys[leftkey]:
                    #self.dx -=1
                    self.angle += 1
            if pressedkeys[rightkey]:
                    #self.dx +=1
                    self.angle -= 1
            if pressedkeys[upkey]:
                    #self.dy -= 1
                    self.speed += 1
            if pressedkeys[downkey]:
                    #self.dy += 1
                    self.speed -= 1
        self.move = pygame.math.Vector2(self.speed, 0)
        self.move = self.move.rotate(self.angle)
         
         
    def reflect(self, wallvector):
           """changing angle of Sprite by reflecting it's move vector with a given wallvector"""
           self.move.reflect_ip(wallvector)
           self.angle = pygame.math.Vector2(1,0).angle_to(self.move)
           
    def wallcheck(self):
        """check if Sprite is touching screen edge""" 
        if self.kill_on_edge:
            if self.pos[0] - self.width // 2 < 0 or self.pos[1] - self.height // 2  < 0 or self.pos[0] + self.width //2  > PygView.width or self.pos[1] + self.height // 2 > PygView.height:
                self.kill()
        elif self.bounce_on_edge:
            h = pygame.math.Vector2(1,0) # ... horizontal vector
            v = pygame.math.Vector2(0,1) # ... vertical vector
            if self.pos[0] - self.width // 2 < 0:
                self.reflect(h)
            elif self.pos[0] + self.width // 2 > PygView.width:
                self.reflect(h)
            if self.pos[1] + self.height // 2 > 0:
                self.reflect(v)
            elif self.pos[1] - self.height // 2 < -PygView.height:
                self.reflect(v)
            
    def update(self, seconds):
        self.age += seconds
        # agekill?
        if self.max_age is not None:
            if self.age > self.max_age:
                self.kill()
        # calculate movement
        self.oldangle = self.angle
        self.control()
        self.pos += self.move  * seconds
        self.wallcheck()
        if self.angle != self.oldangle:
            self.rotate_image(self.angle) # only necessary if angle is changed
        self.rect.center = (self.pos[0], -self.pos[1])
        
        # ---- print!!! ---
        #print("pos, move, angle, speed:", self.pos, self.move, self.angle, self.speed)
         
        

class Rocket(pygame.sprite.Sprite):
    
    def __init__(self, mothership, speed= 50):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.color = mothership.color
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, self.color, [ (0,0), (15,0),
               (20,5), ( 15,10), ( 0,10)])
        pygame.draw.polygon(self.image, (150,150,150), [ (5,2), (10,2), (15,5), (10, 8), (5,8)])
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.x = mothership.x
        self.y = mothership.y
        self.dx = 0
        self.dy = 0
        self.angle = mothership.angle
        self.speed = mothership.speed + speed
        self.age = 0
        self.maxage = 5
       
    def rotate_image(self, angle):
        """rotates the original image (image0) for angle degrees"""
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        
    def update(self, seconds):
         # ---- calculate movement ----  
         self.move = pygame.math.Vector2(self.speed, 0)
         self.move = self.move.rotate(self.angle)
         self.dx = self.move[0]
         self.dy = -self.move[1]
         self.rotate_image(self.angle)
         self.x += self.dx * seconds
         self.y += self.dy * seconds
         #self.checkbounce()
         self.rect.centerx = self.x
         self.rect.centery = self.y
         # .... kill ? ....
         self.age += seconds
         if self.age > self.maxage:
             self.kill()
             return
         if self.x < 0 or self.x > PygView.width or self.y < 0 or self.y > PygView.height:
             self.kill()
             return
    
    
class Spaceship(pygame.sprite.Sprite):
    """this is not a native pygame sprite but instead a pygame surface"""
    def __init__(self, radius = 50, color=(0,0,255), x=0, y=0, slim = 20, control = "wasd"):
        """create a (black) surface and paint a blue ball on it"""
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.radius = radius
        self.color = color
        self.pos = pygame.math.Vector2(x,-y) # negative y!!!!!
        #self.x = x
        #self.y = y
        #self.dx = 0
        #self.dy = 0
        self.slim = slim
        self.control = control
        # create a rectangular surface for the ball 50x50
        self.image = pygame.Surface((2*self.radius,2*self.radius))
        pygame.draw.polygon(self.image, self.color, 
                ((0,0 + self.slim),(self.radius // 2, self.radius), (0,2 * self.radius - self.slim), (self.radius * 2, self.radius)))    
        #pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        #self.surface = self.surface.convert() # for faster blitting. 
        # to avoid the black background, make black the transparent color:
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.move = pygame.math.Vector2(0,0)
        self.angle = 0
        self.speed = 0
        self.tail = []
        
     
    def rotate_image(self, angle):
        """rotates the original image (image0) for angle degrees"""
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        
             
    def wrap(self):
        # wrap around screen
        if self.x < 0:
            self.x = PygView.width
        if self.x > PygView.width:
            self.x = 0
        if self.y < 0:
            self.y = PygView.height
        if self.y > PygView.height:
            self.y = 0
    
    def checkbounce(self):
        return
        if self.x > PygView.width:
            self.x = PygView.width
            self.speed = 0
            #self.dx *= -1
            #self.move = self.move.reflect(pygame.math.Vector2(0,1))
            #self.angle = self.move.angle_to(pygame.math.Vector2(1,0))
        if self.x < 0:
            self.x = 0
            self.speed = 0
            #self.dx *= -1
            #self.move = self.move.reflect(pygame.math.Vector2(0,1))
            #self.angle = self.move.angle_to(pygame.math.Vector2(1,0))
        if self.y > PygView.height:
            self.y = PygView.height
            self.speed = 0
            #self.dy *= -1
            #self.move = self.move.reflect(pygame.math.Vector2(1,0))
            #self.angle = self.move.angle_to(pygame.math.Vector2(1,0))
        if self.y < 0:
            self.y = 0
            self.speed = 0
            #self.dy *= -1
            #self.move = self.move.reflect(pygame.math.Vector2(1,0))
            #self.angle = self.move.angle_to(pygame.math.Vector2(1,0))
            
                
            
    def update(self, seconds):
         if self.control == "wasd" or self.control == "ijkl" or self.control == "cursor":
             if self.control == "wasd":
                 upkey = pygame.K_w
                 downkey = pygame.K_s
                 leftkey = pygame.K_a
                 rightkey = pygame.K_d
             elif self.control == "ijkl":
                 upkey = pygame.K_i
                 downkey = pygame.K_k
                 leftkey = pygame.K_j
                 rightkey = pygame.K_l
             elif self.control == "cursor":
                 upkey = pygame.K_UP
                 downkey = pygame.K_DOWN
                 leftkey = pygame.K_LEFT
                 rightkey = pygame.K_RIGHT
             # --- keyboard control ----
             pressedkeys = pygame.key.get_pressed() # keys that you can press all the time
             if pressedkeys[leftkey]:
                    #self.dx -=1
                    self.angle += 1
             if pressedkeys[rightkey]:
                    #self.dx +=1
                    self.angle -= 1
             if pressedkeys[upkey]:
                    #self.dy -= 1
                    self.speed += 1
             if pressedkeys[downkey]:
                    #self.dy += 1
                    self.speed -= 1
           
       
         # ---- calculate movement ----  
         self.move = pygame.math.Vector2(self.speed * seconds, 0)
         self.move = self.move.rotate(self.angle)
         
         #self.dx = self.move[0]
         #self.dy = -self.move[1]
         # rotate image
         self.rotate_image(self.angle)
         
         self.pos += self.move 
         
         #self.x += self.dx * seconds
         #self.y += self.dy * seconds
         #self.checkbounce()
         self.rect.center = (self.pos[0], -self.pos[1]) # negative y!!!
         
         # ---- print!!! ---
         #print("pos, move, angle, speed:", self.pos, self.move, self.angle, self.speed)
         
         #self.rect.centery = self.pos
         #self.tail.insert(0, (self.pos[0], self.pos[1]))
         #self.tail = self.tail[:255]
         
        
   

class PygView():
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
        self.background.fill((110,110,140)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.preparesprites()
        
    def preparesprites(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.shipgroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        #...allocate sprites to groups
        FlyingObject.groups = self.allgroup
        Spaceship.groups = self.allgroup, self.shipgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        # ... create the sprites ...
        self.player1 = Spaceship(x=100, y=200) # creating the Ball object
        self.player2 = Spaceship(color = (100,200,100), x = 400, y = 200, control = "ijkl")
        self.test1 = FlyingObject(bounce_on_edge=True)

    def paint(self):
        """painting on the surface"""
        # pygame.draw.line(Surface, color, start, end, width) 
        pygame.draw.line(self.background, (0,255,0), (10,10), (50,100))
        pygame.draw.line(self.background, (0,0,0), (0,0), (1000,500))
        pygame.draw.line(self.background, (255,255,0), (1000,0), (0,500))
        # ...
        pygame.draw.ellipse(self.background, (200,110,100), (0,PygView.height - 60,100,60))
        pygame.draw.ellipse(self.background, (0,200,200), (PygView.width - 45, 0,20,90))
        for x in range(100,19,-20):         
            pygame.draw.circle(self.background, (0,0,random.randint(0,255)), (PygView.width // 2, PygView.height // 2), x)
        #pygame.draw.circle(self.background, (0,0,0), (200,80), (36))
        #pygame.draw.rect(self.background, (0,255,100), (PygView.width / 2 - 50 , PygView.height / 2 - 25, 100, 50))
        pygame.draw.line(self.background, (255,40,255), (PygView.width, 0), (0, PygView.height))
        pygame.draw.line(self.background, (255,90,205), (0,0), (PygView.width,PygView.height))
        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        pygame.draw.rect(self.background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
        pygame.draw.rect(self.background, (0,0,255), (70,70,80,30))
        # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        pygame.draw.circle(self.background, (0,200,0), (200,50), 35)
        # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
        pygame.draw.polygon(self.background, (0,180,0), ((250,100),(300,0),(350,50)))
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
        pygame.draw.arc(self.background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
        #...
        #pygame.draw.polygon(self.background, (0,255,188), ((370,300), (320,200), (185,200), (190,200), (170,300)))
        pygame.draw.polygon(self.background, (255,165,0), ((PygView.width / 2, 0), (PygView.width / 2 - 90, PygView.height - 80), (PygView.width / 2, PygView.height), (PygView.width / 2 + 90, PygView.height - 80), (PygView.width / 2, 0)))
      
    
    def run(self):
        self.paint() 
        running = True
        while running:
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime))
            h = pygame.math.Vector2(1,0) # .... horizontal
            v = pygame.math.Vector2(0,1) # .....vertical
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    # keys that you press once and release
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        Rocket(self.player1)
                    if event.key == pygame.K_SPACE:
                        Rocket(self.player2)
    
                    
                    #if event.key == pygame.K_RETURN:
                    #    Rocket(self.player3)
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            pygame.display.set_caption("player1: x:{:.2f} y:{:.2f} angle:{:.2f} speed:{:.2f}, move: {}, winkel: {:.2f} ".format(
                   self.player1.pos.x, self.player1.pos.y, self.player1.angle, self.player1.speed, self.player1.move, self.player1.move.angle_to(pygame.math.Vector2(1,0))))
            # --- paint tails ----
            for ship in self.shipgroup:
                oldpos = (ship.pos.x, ship.pos.y)
                for n, pos in enumerate(ship.tail):
                    pygame.draw.line(self.screen, (255-n,255-n,255-n), (oldpos[0], -oldpos[1]), (pos[0], -pos[1]))
                    oldpos = pos
        pygame.quit()

    def draw_text(self, text):
        """Center text in window"""
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, (50,150))

        
if __name__ == '__main__':
    PygView(1000, 500).run() # call with width of window and fps
