# -*- coding: utf-8 -*-
"""003_static_blit_pretty_template.py"""
import pygame 
import random


def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))




        
            
        

class Flytext(pygame.sprite.Sprite):
    def __init__(self, x, y, text="hallo", color=(255, 0, 0),
                 dx=0, dy=-50, duration=2, acceleration_factor = 1.0, delay = 0, fontsize=22):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
        self.text = text
        self.r, self.g, self.b = color[0], color[1], color[2]
        self.dx = dx
        self.dy = dy
        self.x, self.y = x, y
        self.duration = duration  # duration of flight in seconds
        self.acc = acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.
        self.image = make_text(self.text, (self.r, self.g, self.b), fontsize)  # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.time = 0 - delay

    def update(self, seconds):
        self.time += seconds
        if self.time < 0:
            self.rect.center = (-100,-100)
        else:
            self.y += self.dy * seconds
            self.x += self.dx * seconds
            self.dy *= self.acc  # slower and slower
            self.dx *= self.acc
            self.rect.center = (self.x, self.y)
            if self.time > self.duration:
                self.kill()      # remove Sprite from screen and from groups




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
        self.rotate_image(self.angle)
        if self.has_hitpointbar:
            Hitpointbar(mothership=self)
            
        
        
    
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
        if "control_method" not in kwargs:
            self.control_method = None
        if "move" in kwargs:
            self.speed = self.move.length()
            self.angle = pygame.math.Vector2(1,0).angle_to(self.move)
        else:
            if "speed" not in kwargs:
                self.speed = 50
            if "angle" not in kwargs:
                self.angle = 0 # facing right?
            # create move from speed and angle 
            self.move = pygame.math.Vector2(self.speed,0)
            self.move.rotate(self.angle)
        
        if "pos" not in kwargs:
            if "x" in kwargs and "y" in kwargs:
                self.pos = pygame.math.Vector2(self.x,-self.y)
            else:
                self.pos = pygame.math.Vector2(100,-200)
            
        #if "radius" not in kwargs:
         #   self.radius = None
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
        if "radius" not in kwargs:
            self.radius = 10
        #print(self.pos, self.move, self.speed)
        
        if "has_hitpointbar" not in kwargs:
            self.has_hitpointbar = False
   
        
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
        keyboard = False
        if self.control_method == "cursor":
            keyboard = True
            upkey = pygame.K_UP
            downkey = pygame.K_DOWN
            leftkey = pygame.K_LEFT
            rightkey = pygame.K_RIGHT
        if self.control_method == "wasd":
            keyboard = True
            
            upkey = pygame.K_w
            downkey = pygame.K_s
            leftkey = pygame.K_a
            rightkey = pygame.K_d
        if self.control_method == "ijkl":
            keyboard = True     
            upkey = pygame.K_i
            downkey = pygame.K_k
            leftkey = pygame.K_j
            rightkey = pygame.K_l 
            
        if self.control_method == "tgfh":
            keyboard = True
            upkey = pygame.K_t
            downkey = pygame.K_g
            leftkey = pygame.K_f
            rightkey = pygame.K_h
                   
            
            
        if keyboard:    
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
        #print("speed", self.speed)
        self.move = pygame.math.Vector2(self.speed, 0)
        self.move = self.move.rotate(self.angle)
         
         
    def reflect(self, wallvector):
           """changing angle of Sprite by reflecting it's move vector with a given wallvector"""
           self.move.reflect_ip(wallvector)
           self.angle = pygame.math.Vector2(1,0).angle_to(self.move)
           for x in range(10):
               Fragment(x=self.pos.x,y = -self.pos.y)
           
    def wallcheck(self):
        """check if Sprite is touching screen edge""" 
        if self.kill_on_edge:
            if (self.pos[0] - self.width // 2 < 0 or
                self.pos[1] + self.height // 2  > 0 or 
                self.pos[0] + self.width //2  > PygView.width or
                self.pos[1] - self.height // 2 < -PygView.height):
                #print(self.width, self.height, "i kill on edge")
                self.kill()
                for x in range(5):
                    Fragment(x=self.pos.x,y = -self.pos.y)     
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
        
        
class Hitpointbar(FlyingObject):
    
    def create_image(self):
        good = (0,170,0) #green
        medium = (255,255,0) #yellow
        bad = (255,128,0) #orange
        critical = (200,0,0) #red
        wfull = self.mothership.rect.width
        #hp = self.mothership.hitpoints
        #hpfull = self.mothership.hitpointsfull
        p = self.mothership.hitpoints / self.mothership.hitpointsfull
        w = int(wfull * abs(p))
        
        
        #define hitpointbarcolor
        hp = self.mothership.hitpoints
        if hp > 80:
            color = good
        elif hp > 50:
            color = medium
        elif hp > 25:
            color = bad
        else:
            color = critical 
                    
        
        
        self.image = pygame.Surface((wfull,5))
        pygame.draw.rect(self.image, color, (0,0,w,5))
        pygame.draw.rect(self.image, (100,100,100), (0,0,wfull,5),1)
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
    
   
        
    
    def update(self, seconds):
        self.rect.x = self.mothership.rect.x
        self.rect.y = self.mothership.rect.y - 10  
        self.create_image()      


        
         
class Fragment(FlyingObject):
    
    def _overwrite_parameters(self):
        self.radius = random.randint(1, 4)
        self.speed = random.randint(50, 300)
        self.max_age = random.random() * 1.5
        self.angle = random.random() * 360
        self.color = ( random.randint(128,255),
                       random.randint(0,90),
                       0 )
    def create_image(self):
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) 
        self.image.set_colorkey((0,0,0))               
        

        

class Rocket(FlyingObject):
    
    def _overwrite_parameters(self):
        self.radius = 10
        self.damage = 3
        self.kill_on_edge = True
        self.color = self.mothership.color
        self.pos = pygame.math.Vector2(self.mothership.pos[0], 
                                       self.mothership.pos[1])
        self.angle += self.mothership.angle
        self.speed = self.mothership.speed + self.speed
      
      
        
        
    def create_image(self):
        self.image = pygame.Surface((20,10))
        pygame.draw.polygon(self.image, self.color, [ (0,0), (15,0),
               (20,5), ( 15,10), ( 0,10)])
        pygame.draw.polygon(self.image, (150,150,150), [ (5,2), (10,2), (15,5), (10, 8), (5,8)])
        self.image.set_colorkey((0,0,0))
        
 
class Rocket2(FlyingObject):
    
    def _overwrite_parameters(self):
        self.radius = 15
        self.damage = 5
        self.kill_on_edge = True
        self.color = (30,30,30)
        self.pos = pygame.math.Vector2(self.mothership.pos[0], 
                                       self.mothership.pos[1])
        self.angle += self.mothership.angle
        self.speed = self.mothership.speed + self.speed
        
        
        
    def create_image(self):
       self.image = pygame.Surface((25,20))
       pygame.draw.polygon(self.image, self.color, [ (0,0), (0,15), (20,15), (25,10), (20,0) ])
       pygame.draw.line(self.image, (200,0,0), (20,0), (20,15)) 
       self.image.set_colorkey((0,0,0))
        
 
class Turret(FlyingObject):
    
    def create_image(self):
        
       self.image = pygame.Surface((120,120))
       self.radius  = 40 
       pygame.draw.circle(self.image,(100,100,100), (50,50), (self.radius))
       pygame.draw.rect(self.image,(150,150,150), (50,50 - 10, 120, 20))
        
        
        
       self.image.set_colorkey((0,0,0))
       self.image = self.image.convert_alpha()
        
 
        

class Spaceship2(FlyingObject):
    
    def create_image(self):
        pass
       #self.image = pygame.Surface((100,100))
       #self.radius = 50
       #pygame.draw.polygon(self.image, self.color, [ (0,0),(75,25),(50,50),(75,75),(0,100)])
       #pygame.draw.line(self.image,(220,0,0), (0,50), (50,50),5)
       #pygame.draw.line(self.image,(220,0,0), (0,0), (50,50),5)
       #pygame.draw.line(self.image, (220,0,0), (0,100), (50,50),5)
       #pygame.draw.line(self.image, (220,0,0), (50,75), (50,25),5)
       
       #self.image.set_colorkey((0,0,0))
       #self.image = self.image.convert_alpha()
    
    
class Spaceship3(FlyingObject):
    # def _overwrite_parameters(self):
    #   self.color = (0,200,200)
       
    def create_image(self):
        pass
     #  self.image = pygame.Surface((100,100))
      # self.radius = 50
      # pygame.draw.polygon(self.image, self.color, [ (20,40),(30,40),(30,35),(45,35),(45,40), (65,40), (90,50), (65,60), (45,60), (45,65), (30,65),(30,60), (20,60)])
       #pygame.draw.line(self.image, (7,7,7), (65,40), (65,60),4)
       #pygame.draw.line(self.image, (7,7,7), (45,40), (45,60),4)
       
       
       #self.image.set_colorkey((0,0,0))
       #self.image = self.image.convert_alpha()
        
   
    
    
class Spaceship(FlyingObject):
        
    def create_image(self):  
       pass # self.image = Spaceship.image # image loaded from file
        
        
       
   

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
        self.paint()
        self.preparesprites()
        
    def preparesprites(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.shipgroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.bargroup = pygame.sprite.Group()
        #...allocate sprites to groups
        FlyingObject.groups = self.allgroup
        Spaceship.groups = self.allgroup, self.shipgroup
        Rocket.groups = self.allgroup, self.rocketgroup
        Rocket2.groups = self.allgroup, self.rocketgroup
        Spaceship2.groups = self.allgroup, self.shipgroup
        Spaceship3.groups = self.allgroup, self.shipgroup
        Flytext.groups = self.allgroup
        Hitpointbar.groups = self.allgroup, self.bargroup
        # ... create the sprites ...
        self.player1 = Spaceship(x=100, y=200, color = ( 0,200,0),bounce_on_edge=True, control_method = "wasd", has_hitpointbar=True, hitpoints = 105) # creating the Ball object
        self.player2 = Spaceship3( x = 400, y = 200, bounce_on_edge=True, control_method = "ijkl", has_hitpointbar=True, hipoints = 105)
        #self.test1 = FlyingObject(bounce_on_edge=True, control_method = "cursor")
        self.player3 = Spaceship2(color = (30,30,30), control_method = "tgfh", bounce_on_edge=True, has_hitpointbar=True, hitpoints = 120)
        self.turret1 = Turret(x= 200, y=200, speed = 0)

    def paint(self):
        """painting on the surface"""
        
        #resource loading wallpaper
        PygView.background1 = pygame.image.load("bg_space1.jpg").convert()
        #https://pixabay.com/en/wallpaper-background-eclipse-1492818/ 
        # CC0
        PygView.background2 = pygame.image.load("bg_space2.jpg").convert()
        #https://pixabay.com/en/space-science-fiction-cosmos-911785/
        # CC0
        PygView.background3 = pygame.image.load("bg_space3.jpg").convert()
        #https://pixabay.com/en/space-galaxy-planet-universe-1569133/
        # CC0
        PygView.background4 = pygame.image.load("bg_space4.jpg").convert()
        #https://pixabay.com/en/fractal-abstract-background-cosmos-1280107/
        # CC0
        #scale to screen size
        PygView.background1 = pygame.transform.scale(PygView.background1, (PygView.width, PygView.height))
        PygView.background2 = pygame.transform.scale(PygView.background2, (PygView.width, PygView.height))      
        PygView.background3 = pygame.transform.scale(PygView.background3, (PygView.width, PygView.height))
        PygView.background4 = pygame.transform.scale(PygView.background4, (PygView.width, PygView.height))
        self.background = PygView.background1
        
        #resource loading sprite images
        Spaceship.image = pygame.image.load("fighter3.png").convert_alpha()
        #https://opengameart.org/content/speed-runners-2
        # author https://opengameart.org/users/scay
        # CC - BY 40
        Spaceship2.image = pygame.image.load("fighter2.png").convert_alpha()
        #https://opengameart.org/content/transforming-fighter-ship-1
        # author https://opengameart.org/users/clayster2012
        # CC - BY 40
        Spaceship3.image = pygame.image.load("fighter1.png").convert_alpha()
        #https://opengameart.org/content/transforming-fighter-ship-1
        # author https://opengameart.org/users/clayster2012
        # CC - BY 40
        
        
        
        
        
        
        
        # pygame.draw.line(Surface, color, start, end, width) 
        #pygame.draw.line(self.background, (0,255,0), (10,10), (50,100))
        #pygame.draw.line(self.background, (0,0,0), (0,0), (1000,500))
        #pygame.draw.line(self.background, (255,255,0), (1000,0), (0,500))
        # ...
       # pygame.draw.ellipse(self.background, (200,110,100), (0,PygView.height - 60,100,60))
        #pygame.draw.ellipse(self.background, (0,200,200), (PygView.width - 45, 0,20,90))
        #for x in range(100,19,-20):         
         #   pygame.draw.circle(self.background, (0,0,random.randint(0,255)), (PygView.width // 2, PygView.height // 2), x)
        #pygame.draw.circle(self.background, (0,0,0), (200,80), (36))
        #pygame.draw.rect(self.background, (0,255,100), (PygView.width / 2 - 50 , PygView.height / 2 - 25, 100, 50))
        #pygame.draw.line(self.background, (255,40,255), (PygView.width, 0), (0, PygView.height))
        #pygame.draw.line(self.background, (255,90,205), (0,0), (PygView.width,PygView.height))
        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        #pygame.draw.rect(self.background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
        #pygame.draw.rect(self.background, (0,0,255), (70,70,80,30))
        # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        #pygame.draw.circle(self.background, (0,200,0), (200,50), 35)
        # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
        #pygame.draw.polygon(self.background, (0,180,0), ((250,100),(300,0),(350,50)))
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
        #pygame.draw.arc(self.background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
        #...
        #pygame.draw.polygon(self.background, (0,255,188), ((370,300), (320,200), (185,200), (190,200), (170,300)))
        #pygame.draw.polygon(self.background, (255,165,0), ((PygView.width / 2, 0), (PygView.width / 2 - 90, PygView.height - 80), (PygView.width / 2, PygView.height), (PygView.width / 2 + 90, PygView.height - 80), (PygView.width / 2, 0)))
        
        
    def kill_ship_and_hitpointbar(self, ship):
        """ kills the hitpointbar of a ship and the ship itself.
            neccesary: hitpointbar has attribute self.mothership (the Ship),
                   and Hitpointbar is member of PygView.bargroup"""
                   
        for b in self.bargroup:
            if b.mothership == ship:
                b.kill()
                break
        ship.kill()     
        
    
    def run(self):
        #self.paint() 
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
                    if event.key == pygame.K_p:
                        Rocket2(mothership=self.player2, speed=300)
                    if event.key == pygame.K_SPACE:
                        Rocket(mothership=self.player3, speed = 320)
                    if event.key == pygame.K_TAB:
                        Rocket(mothership=self.player1, speed = 300)
                        
                    if event.key == pygame.K_RETURN:
                        
                       self.background = random.choice((self.background1, self.background2, self.background3, self.background4))  
    
                    
                    #if event.key == pygame.K_RETURN:
                    #    Rocket(self.player3)
            # --- mouse events ---
            left,middle,right = pygame.mouse.get_pressed()
            if left:
                for f in range(random.randint(10,20)):
                    Fragment(x=pygame.mouse.get_pos()[0],
                    y=pygame.mouse.get_pos()[1])
            if right:
                Flytext(pygame.mouse.get_pos()[0],
                        pygame.mouse.get_pos()[1],
                        "hallo")
                        
                    
            # ---- collision detection----       
                    
            for ship in self.shipgroup:
                crashgroup = pygame.sprite.spritecollide(ship, self.rocketgroup,
                             False, pygame.sprite.collide_circle)
                for rocket in crashgroup:
                    if rocket.mothership == ship:
                        continue
                    ship.hitpoints -= rocket.damage
                    if ship.hitpoints < 1:
                        self.kill_ship_and_hitpointbar(ship)
                    for f in range(10):
                        Fragment(x=rocket.pos.x, y=-rocket.pos.y)
                    rocket.kill()                        
                        
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            pygame.display.set_caption("player1: HP: {} player 2: HP {} player 3: HP {} ".format(
                   self.player1.hitpoints, self.player2.hitpoints, self.player3.hitpoints))
            # --- paint tails ----
            #for ship in self.shipgroup:
             #   oldpos = (ship.pos.x, ship.pos.y)
              #  for n, pos in enumerate(ship.tail):
               #     pygame.draw.line(self.screen, (255-n,255-n,255-n), (oldpos[0], -oldpos[1]), (pos[0], -pos[1]))
                #    oldpos = pos
        pygame.quit()

    def draw_text(self, text):
        """Center text in window"""
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, (50,150))

        
if __name__ == '__main__':
    PygView(1400, 800).run() # call with width of window and fps
