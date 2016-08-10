"""
code originally from Peter Collingridge 
http://www.petercollingridge.co.uk/pygame-physics-simulation
https://github.com/petercollingridge/ 
no license information found

adapted by Horst JENS http://github.com/horstjens
"""

import random
import pygame
import particles 
import os
import math

#todo: universe zoom funktion: height und width anpassen auf universe-screen. aber nur bei rauszoomen
#todo: lambdas wegtun bei controller
#todo: trail farben

class UniverseScreen:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
    def scroll(self, dx=0, dy=0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
        
    def zoom(self, zoom):
        if zoom ==  2:
            zoomin.play()
        elif zoom == 0.5:
            zoomout.play()
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
def calculateRadius(mass):
    return 0.5 * mass ** (0.5)


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init() 
#pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
fail = pygame.mixer.Sound(os.path.join('data','fail.wav'))  #load sound
create = pygame.mixer.Sound(os.path.join('data','jump.wav'))  #load sound
zoomin = pygame.mixer.Sound(os.path.join('data','zoom1.wav'))  #load sound
zoomout = pygame.mixer.Sound(os.path.join('data','zoom2.wav'))  #load sound

(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))

universe = particles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine', 'bounce'])
#universe.addFunctions(['move', 'attract', 'collide', 'combine', 'bounce'])
universe_screen = UniverseScreen(width, height)


for p in range(5):
    particle_mass = random.randint(10,25)
    particle_size = calculateRadius(particle_mass)
    universe.addParticles(mass=particle_mass, size=particle_size, speed=0, 
                          colour=(random.randint(128,255),
                                  random.randint(128,255),
                                  random.randint(128,255)))

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.scroll(dx = 1)),
    pygame.K_RIGHT:  (lambda x: x.scroll(dx = -1)),
    pygame.K_DOWN:   (lambda x: x.scroll(dy = -1)),
    pygame.K_UP:     (lambda x: x.scroll(dy = 1)),
    pygame.K_EQUALS: (lambda x: x.zoom(2)),
    pygame.K_KP_MINUS: (lambda x: x.zoom(0.5)),
    pygame.K_MINUS:  (lambda x: x.zoom(0.5)),
    pygame.K_KP_PLUS: (lambda x: x.zoom(2)),
    pygame.K_PLUS:   (lambda x: x.zoom(2)),
    pygame.K_r:      (lambda x: x.reset())}

clock = pygame.time.Clock()
paused = False
running = True
while running:
    pygame.display.set_caption('mouse, +/-, cursor, space. zoom={:.4f} pause={} particles={}'.format(universe_screen.magnification, paused, len(universe.particles)))
    
    hats = joystick.get_numhats()
    #textPrint.print(screen, "Number of hats: {}".format(hats) )
    #textPrint.indent()
    for i in range( hats ):
        hat = joystick.get_hat( i )
        print(hat)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in key_to_function:
                key_to_function[event.key](universe_screen)
            if event.key == pygame.K_MINUS:
                print("expand!")
                universe.width *= 2
                universe.height *= 2
            if event.key == pygame.K_5:
                particle_mass = random.randint(20,20)
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                 
                universe.addParticles(mass=particle_mass, size=particle_size, speed=0,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py)
                
            elif event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.JOYBUTTONDOWN:
            if event.button == 4: # scrollwheel up
                key_to_function[pygame.K_PLUS](universe_screen)
            elif event.button == 5: # scrollweeel down
                key_to_function[pygame.K_MINUS](universe_screen)
            elif event.button == 1:
            
                # create a new star without speed
                particle_mass = random.randint(1,1)
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                
                 
                universe.addParticles(mass=particle_mass, size=particle_size, speed=0,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py)
            elif event.button == 3:
                # create a new star with intitial random speed
                particle_mass = random.randint(1,1)
                particle_size = calculateRadius(particle_mass)
                x = pygame.mouse.get_pos()[0]  #universe_screen.width 
                y = pygame.mouse.get_pos()[1]  #* universe_screen.magnification
                
                px = x / universe_screen.magnification  - universe_screen.mx / universe_screen.magnification - universe_screen.dx  
                py = y / universe_screen.magnification  - universe_screen.my / universe_screen.magnification - universe_screen.dy  
                angle = random.uniform(0, math.pi*2)
                if hat[0] == 0 and hat[1] == 1:
                    angle = math.pi * 0.0 # oben
                elif hat[0] == 0 and hat[1] == -1:
                    angle = math.pi * 1.0 # unten
                elif hat[0] == -1 and hat[1] == 0:
                    angle = math.pi * 1.5 # links
                elif hat[0] == 1 and hat[1] == 0:
                    angle = math.pi * 0.5 # rechts
               
                elif hat[0] == -1 and hat[1] == 1:
                    angle = math.pi * 1.75 # linksoben
                elif hat[0] == 1  and hat[1] == 1:
                    angle = math.pi * 0.25 # rechtsoben
                elif hat[0] == -1 and hat[1] == -1:
                    angle = math.pi * 1.25 # linksunten
                elif hat[0] == 1 and hat[1] == 1:
                    angle = math.pi * 0.75 # rechtsunten
                    
                    
                
                
                universe.addParticles(mass=particle_mass, size=particle_size, speed=random.random()*1.0,
                                      colour=(random.randint(0,255),random.randint(0,255),255),
                                      x=px,y=py, angle=angle)


    if not paused:
        universe.update()
        
    screen.fill(universe.colour)
    # ---- paint trail of destroyed stars ----
    for minilist in universe.history:
            color = len(minilist)
            for pos in minilist:
                hx = pos[0]
                hy = pos[1]
                hx = int(universe_screen.mx + (universe_screen.dx + hx) * universe_screen.magnification)
                hy = int(universe_screen.my + (universe_screen.dy + hy) * universe_screen.magnification)
                pygame.draw.rect(screen, (255-min(color, p.colour[0]), 255-min(color, p.colour[1]), 255-min(color, p.colour[2])), (hx, hy, 2,2))
            del minilist[0]
    universe.history = [li for li in universe.history if len(li)>0] # cleanup lost trail history
    
    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']
        # --- paint star trail ----
        color = 255
        for pos in p.history:
            hx = pos[0]
            hy = pos[1]
            hx = int(universe_screen.mx + (universe_screen.dx + hx) * universe_screen.magnification)
            hy = int(universe_screen.my + (universe_screen.dy + hy) * universe_screen.magnification)
            #print(color, p.colour, hx, hy)
            pygame.draw.rect(screen, (255-min(color, p.colour[0]), 255-min(color, p.colour[1]), 255-min(color, p.colour[2])), (hx, hy, 2,2))
            color-= 1
        
        # paint star itself
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * universe_screen.magnification)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * universe_screen.magnification)
        size = int(p.size * universe_screen.magnification)

        
                
        if size < 2:
            pygame.draw.rect(screen, p.colour, (x, y, 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (x, y), size, 0)
        
      
    
    for p in particles_to_remove:
        if p.mass > 3:  # impact shards at collision of big planets
            for impact in range(5, 10):
                mass = 1
                size = calculateRadius(mass)
                universe.addParticles(mass=mass, size=size, speed=1+random.random()* 2.0,
                                          colour=(255,0,0),x=p.x,y=p.y)

        if p in universe.particles:
            universe.history.append(p.history)
            universe.particles.remove(p)
            #fail.play()

    pygame.display.flip()
    clock.tick(80)
