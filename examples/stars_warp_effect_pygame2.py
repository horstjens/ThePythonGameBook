# "stars" demo adapted from https://github.com/lordmauve/pgzero/tree/master/examples/basic to pygame

import pygame
import random

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
            x - vx * Star.warp_factor * Star.trail_length / 15,
            y - vy * Star.warp_factor * Star.trail_length / 15,
        )

    def update(self, seconds):
        self.pos += self.vel * seconds
        # Grow brighter
        self.brightness = min(self.brightness + Star.warp_factor * 200 * seconds, self.speed, 150)


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

    def create_star(self):
        # Pick a direction and speed
        angle = random.uniform(0, 360)
        speed = 255 * random.uniform(0.3, 1.0) ** 2
        v = pygame.math.Vector2(speed, 0)
        v.rotate_ip(angle)

        # Turn the direction into position and velocity vectors
        dx = v.x / v.length()
        dy = v.y / v.length()
        d = random.uniform(25 + Star.trail_length, 100)
        pos = pygame.math.Vector2(self.screenrect.centerx + dx * d, self.screenrect.centery + dy * d)
        Star.stars.append(Star(pos, v))

    def run(self):
        running = True
        pygame.mouse.set_visible(False)
        while running:
            seconds = self.clock.tick(self.fps) / 1000
            self.playtime += seconds
            # ---- event handler ---
            # --- press and release key ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            # --- pressed keys ----
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]:
                Star.warp_factor += Star.accel * seconds
            # ------ end of event handler -----

            # create new stars until we have reached max_stars
            while len(Star.stars) < Viewer.max_stars:
                self.create_star()

            # --- clear screen ----
            self.screen.blit(self.background, (0,0))
            # update warp factor
            Star.warp_factor = (Star.min_warp_factor +
                    (Star.warp_factor - Star.min_warp_factor) * Star.drag ** seconds)
            for s in Star.stars:
                s.update(seconds)
            # check if a star is outside the screenrect -> delete
            Star.stars = [s  for s in Star.stars if self.screenrect.collidepoint(s.end_pos)]
            # ---- draw ----
            for s in Star.stars:
                s.draw(self.screen)
            # ---- gui ----
            text = "fps: {:.2f} stars: {} warp: {:.2f} Press ESC to quit".format(self.clock.get_fps(), len(Star.stars), Star.warp_factor)
            pygame.display.set_caption(text)
            pygame.display.flip()
        # --- end of pygame main loop --
        pygame.mouse.set_visible(True)
        pygame.quit()


if __name__ == "__main__":
    Viewer(800,600)
