# "stars" demo adapted from https://github.com/lordmauve/pgzero/tree/master/examples/basic to pygame

import pygame
import random
import math

class Star:
    accel = 1.0  # Warp factor per second
    drag = 0.3#0.71  # Fraction of speed per second
    trail_length = 2
    min_warp_factor = 0.1
    warp_factor = 0.1
    stars = []

    def __init__(self, position, velocity):
        self.pos = position
        self.vel = velocity
        self.brightness = 100
        self.speed = velocity.length()

    @property
    def end_pos(self):
        """Get the point where the star trail ends."""
        x, y = self.pos.x, self.pos.y
        vx, vy = self.vel.x, self.vel.y
        return pygame.math.Vector2(
            x - vx * Star.warp_factor * Star.trail_length / 60,
            y - vy * Star.warp_factor * Star.trail_length / 60,
        )

    def update(self, seconds):
        self.pos += self.vel * seconds
        # Grow brighter
        self.brightness = min(self.brightness + Star.warp_factor * 200 * seconds, self.speed, 255)


    def draw(self, screen):
        b = self.brightness
        pygame.draw.line(screen, (b,b,b), (self.pos.x, self.pos.y), (self.end_pos.x, self.end_pos.y))



class Viewer:
    width = 0
    height = 0
    max_stars = 0


    def __init__(self, screenwidth=800, screenheight=600, max_stars=300):
        Viewer.width = screenwidth
        Viewer.height = screenheight
        Viewer.max_stars = max_stars
        self.setup()
        self.run()

    def setup(self):

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.DOUBLEBUF)
        self.screenrect = self.screen.get_rect()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))  # fill background black
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.playtime = 0.0   # how many seconds the game was played


    def run(self):
        running = True
        while running:
            # ------start of event handler ----
            for event in pygame.event.get():
                seconds = self.clock.tick(self.fps) / 1000
                self.playtime += seconds

                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            # --- end of event handler -----

            # create new stars until we have reached max_stars
            while len(Star.stars) < Viewer.max_stars:
                # Pick a direction and speed
                angle = random.uniform(0, 360)
                speed = 255 * random.uniform(0.3, 1.0) ** 2
                v = pygame.math.Vector2(speed,0)
                v.rotate_ip(angle)

                # Turn the direction into position and velocity vectors
                #dx = math.cos(angle)
                #dy = math.sin(angle)
                dx = v.x / v.length()
                dy = v.y / v.length()
                d = random.uniform(25 + Star.trail_length, 100)
                pos = pygame.math.Vector2(self.screenrect.centerx + dx * d, self.screenrect.centery + dy * d)
                #vel = speed * dx, speed * dy
                Star.stars.append(Star(pos, v))

            #print(len(Star.stars))
            self.screen.blit(self.background, (0,0))
            # update warp
            Star.warp_factor = (
                    Star.min_warp_factor +
                    (Star.warp_factor - Star.min_warp_factor) * Star.drag ** seconds
            )
            for s in Star.stars:
                s.update(seconds)
            # check if a star is outside the screenrect -> delete
            #print(Star.stars)
            #print(Star.stars[0].__dict__)
            Star.stars = [s  for s in Star.stars if self.screenrect.collidepoint(s.end_pos)]
            for s in Star.stars:
                s.draw(self.screen)



            text = "fps: {:.2f} stars: {}  Press ESC to quit".format(self.clock.get_fps(), len(Star.stars))
            pygame.display.set_caption(text)
            pygame.display.flip()
        # --- end of pygame main loop --
        pygame.quit()


if __name__ == "__main__":
    Viewer(800,600)
