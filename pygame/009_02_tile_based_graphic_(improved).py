#!/usr/bin/env python

"""
009_02_tile_based_graphic_(improved).py

A simple Maze Wanderer.

Improved version of the "ugly" verison
(009_01_tile_based_graphic_(ugly).py)
Works with Python 2.7 and 3.3+.

URL:     http://thepythongamebook.com/en:part2:pygame:step009
Author:  yipyip
License: Do What The Fuck You Want To Public License (WTFPL)
         See http://sam.zoy.org/wtfpl/gpl
"""

#Only needed for Python 2.x.
from __future__ import print_function, division

####

import pygame
import random
import math

#### configuration

mapcolors =\
{'x': (100, 60, 30),
 'd': (30, 120, 10),
 'u': (30, 190, 10),
 'r': (250, 250, 0),
 'e': (250, 0, 0)}

config =\
{'fullscreen': False,
 'visibmouse': False,
 'width': 800,
 'height': 600,
 'back_color': (230, 180, 40),
 'font_ratio': 8,
 'font_color': (255, 255, 255),
 'fps': 100,
 'dt': 0.01,
 'friction': 0.987,
 'player_sizefac': 1.2,
 'player_color': (0, 0, 255),
 'player_accel': 400,
 'width_sensors': 8,
 'height_sensors': 8,
 'title': "Maze Wanderer   (Move with Cursor Keys, press Esc to exit)",
 'waiting_text': "quit=Esc, again=Other Key"}

#### maps
# x = wall
# s = start
# d = level down
# u = level up
# r = random level

# 20 x 16
easy_map =\
["xxxxxxxxxxxxxxxxxxxx",
 "xs.....x...........x",
 "xxxx.......xxxx....x",
 "x.rx.......x..x..xxx",
 "x..x...x......x...dx",
 "x......x......x....x",
 "x...xxxx..xx.......x",
 "x...x.....x........x",
 "x.............x..xxx",
 "xxxxxx.x...xxxx...rx",
 "x......x......x....x",
 "x......x...........x",
 "xxx..x.....xx......x",
 "xrx..xxxx..x...xxxxx",
 "x.................ux",
 "xxxxxxxxxxxxxxxxxxxx"]

# 22 x 16
medium_map =\
["xxxxxxxxxxxxxxxxxxxxxx",
 "xs................x.rx",
 "xxx...x......x....x..x",
 "x.....xx.xxxxxxx.....x",
 "x..x..x..xr...x.....xx",
 "x..xxxx..xx..........x",
 "x.....x..x..xx..xx...x",
 "xxxx.............x.d.x",
 "x......xxx....x..xxx.x",
 "x...x..x....xxxd.....x",
 "xd..x..x..x.......x..x",
 "x...x.xx..xxxxx...x..x",
 "x..xx.........x...x.xx",
 "xx......xx...........x",
 "xr.......x.........xux",
 "xxxxxxxxxxxxxxxxxxxxxx"]

# 26 x 19
hard_map =\
["xxxxxxxxxxxxxxxxxxxxxxxxxx",
 "xs....x........x.....x..rx",
 "xxxx..xx..xxx..x..x..x..xx",
 "x..........x......x......x",
 "x..xxx.....x..xxxxx...xxxx",
 "x..x.....................x",
 "x..x.xxxxxx.x..x.....xx..x",
 "x....xr.....x..xxxx..xd..x",
 "xxx..x......x..xd....xxxxx",
 "x....xxxxx.xx..x..x......x",
 "x........x........x...x.xx",
 "x............x..xxxx..x..x",
 "xx...xxxxx.........x..x..x",
 "x.....x......xxxx........x",
 "x..xxxx...xxxx.rx...x....x",
 "x............x..x...x....x",
 "xxxxxxx..x...x..x..xx..xxx",
 "xd.......x...x..........ex",
 "xxxxxxxxxxxxxxxxxxxxxxxxxx"]

# 5 x 8
test_map=\
["xxxxx",
 "xs..x",
 "x..ux",
 "x..dx",
 "x..rx",
 "x..ex",
 "x...x",
 "xxxxx"]


# game maps
maps =  easy_map, medium_map, hard_map

# testing
# maps = test_map, easy_map, medium_map, hard_map

#### map constants

UP = 1
DOWN = -1
RANDOM = -2
START = -3
PLACES = set(('u', 'd', 'r', 'e'))
NOT_DRAWABLES = set(('.', 's'))

####

class PygView(object):
  """Pygame interface"""

  CURSORKEYS = slice(273, 277)
  QUIT_KEYS = pygame.K_ESCAPE, pygame.K_q
  EVENTS = 'up', 'down', 'right', 'left'

  def __init__(self, controller, config):

    self.controller = controller
    self.width = config.width
    self.height = config.height
    self.back_color = config.back_color
    self.fps = config.fps
    self.font_color = config.font_color

    pygame.init()
    flags = pygame.DOUBLEBUF | [0, pygame.FULLSCREEN][config.fullscreen]
    self.canvas = pygame.display.set_mode((self.width, self.height), flags)
    pygame.display.set_caption(config.title)
    self.clock = pygame.time.Clock()
    pygame.mouse.set_visible(config.visibmouse)
    self.font = pygame.font.Font(None, self.height // config.font_ratio)


  @property
  def frame_duration_secs(self):

    return 0.001 * self.clock.get_time()


  def run(self):
    """Main loop"""

    running = True
    while running:
      self.clock.tick_busy_loop(self.fps)
      running = self.controller.dispatch(self.get_events())
      self.flip()
    else:
      self.quit()


  def get_events(self):

    keys = pygame.key.get_pressed()[PygView.CURSORKEYS]
    move_events = [e for e, k in zip(PygView.EVENTS, keys) if k]

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return 'quit', move_events
      if event.type == pygame.KEYDOWN:
        if event.key in PygView.QUIT_KEYS:
          return 'quit', move_events
        else:
          return 'other_key', move_events
    else:
      return None, move_events


  def rectangle(self, xywh, color, border=0):

    pygame.draw.rect(self.canvas, color, xywh, border)


  def draw_text(self, text):

    fw, fh = self.font.size(text)
    surface = self.font.render(text, True, self.font_color)
    self.canvas.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 2))


  def flip(self):

    pygame.display.flip()
    self.canvas.fill(self.back_color)


  def quit(self):

    pygame.quit()

####

class Grid(object):
  """Calculate points on a rectangular grid."""

  def __init__(self, dx=1, dy=1, xoff=0, yoff=0):

    self.dx = dx
    self.dy = dy
    self.xoff = xoff
    self.yoff = yoff


  def get_point(self, x, y):

    return self.xoff + x * self.dx, self.yoff + y * self.dy


  def get_rect(self, x, y):
    """Return rectangle parameters for pygame."""

    return self.get_point(x, y) + (self.dx, self.dy)


  def get_cell(self, x, y):
    """Snap coordinates to center point grid."""
    x = int(x+0.5)
    y = int(y+0.5)
    return (x-self.xoff+self.dx//2)//self.dx, (y-self.yoff+self.dy//2)//self.dy

####

class Map(object):
  """Maze map representation"""

  def __init__(self, map_data):

    self.width = len(map_data[0])
    self.height = len(map_data)
    self.data = map_data


  def __getitem__(self, xy):
    x = xy[0]
    y = xy[1]
    return self.data[y][x]


  @property
  def start(self):
    """Search the starting point, there should be only one."""

    for i, y in enumerate(self.data):
      for j, x in enumerate(y):
        if x == 's':
          return j, i

####

class Mapper(object):
  """Manage all maps."""

  def __init__(self, maps, width, height):

    self.view_width = width
    self.view_height = height
    self.maps = [Map(m) for m in maps]


  def select(self, mode=START):

    assert mode in (START, UP, DOWN, RANDOM), "wrong selection"

    n = len(self.maps)
    if mode == START:
      self.act_index = 0
    elif mode == RANDOM:
      if len(self.maps) > 1:
        self.act_index = random.choice(list(set(range(n)) - set((self.act_index,))))
    else:
      self.act_index = (self.act_index + n + mode) % len(self.maps)

    self.act_grid, self.act_center_grid = self.adjust_grids()
    return self.act_map, self.act_grid, self.act_center_grid


  def adjust_grids(self):
    """There are 2 sorts of grids:
    a grid for the upper left Corner for drawing rectangles,
    a grid for their center points, which are used for collision detection."""

    smap = self.act_map
    w = self.view_width // smap.width - 1
    h = self.view_height // smap.height - 1
    xoff = self.view_width - smap.width * w
    yoff = self.view_height - smap.height * h
    grid = Grid(w, h, xoff//2, yoff//2)
    # +1 !
    center_grid = Grid(w, h, xoff//2 + w//2 + 1, yoff//2 + h//2 + 1)

    return grid, center_grid


  def draw_map(self, view):

    smap = self.act_map
    grid = self.act_grid
    width = smap.width

    for y in range(smap.height):
      for x in range(width):
        place = smap[x, y]
        if place not in NOT_DRAWABLES:
          view.rectangle(grid.get_rect(x, y), mapcolors[place], place in PLACES)


  @property
  def act_map(self):

    return self.maps[self.act_index]


  @property
  def start(self):

    return self.act_map.start


  def get_point(self, x, y):

    return self.act_grid.get_point(x, y)


  def get_rect(self, x, y):

    return self.act_grid.get_rect(x, y)


  def get_cell(self, x, y):

    return self.act_center_grid.get_cell(x, y)


  @property
  def player_sizehint(self):

    return self.act_grid.dx // 2, self.act_grid.dy // 2

 ####

class Player(object):
  """Representation of the moving player rectangle"""

  dirs = {'up': (0, -1),
          'down': (0, 1),
          'left': (-1, 0),
          'right': (1, 0)}

  sensor_pts = ((0, 0), (1, 0), (1, 1), (0, 1))

  def __init__(self, x, y, width, height, color):

    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.width2 = width // 2
    self.height2 = height // 2
    self.color = color
    self.dx = 0
    self.dy = 0


  @property
  def pos(self):

    return self.x, self.y


  @property
  def oldpos(self):

    return self.xold, self.yold


  def restore_pos(self):

    self.x, self.y = self.oldpos


  @property
  def center(self):

    x, y = self.pos
    return x + self.width2, y + self.height2


  def move(self, dt, friction):

    self.dx *= friction
    self.dy *= friction
    self.xold, self.yold = self.pos
    self.x += self.dx * dt
    self.y += self.dy * dt


  def accelerate(self, direct, acc):

    xdir, ydir = Player.dirs[direct]
    self.accx = xdir * acc
    self.accy = ydir * acc
    self.dx += self.accx
    self.dy += self.accy


  @property
  def vertex_sensors(self):

    x, y = self.pos
    return [(x + sx * self.width, y + sy * self.height) for sx, sy in Player.sensor_pts]


  def north_sensors(self, n):

    x, y = self.pos
    delta = self.width // n
    return [(x + i * delta, y) for i in range(1, n)]


  def south_sensors(self, n):

    x, y = self.pos
    delta = self.width // n
    h = y + self.height
    return [(x + i * delta, h) for i in range(1, n)]


  def west_sensors(self, n):

    x, y = self.pos
    delta = self.height // n
    return [(x, y + i * delta) for i in range(1, n)]


  def east_sensors(self, n):

    x, y = self.pos
    delta = self.height // n
    w = x + self.width
    return [(w, y + i * delta) for i in range(1, n)]


  def bounce(self, west_east, north_south):

    self.dx = (self.dx, -self.dx)[west_east]
    self.dy = (self.dy, -self.dy)[north_south]


  def draw(self, view):

    view.rectangle((self.x, self.y, self.width, self.height), self.color)

####

class Controller(object):
  """Global game control"""

  def __init__(self, view, maps, config):

    self.view = view(self, config)
    self.game = MazeGame(maps, config)
    self.game.reset(START)
    self.state = 'playing'


  def dispatch(self, all_events):
    """Control the game state."""

    event, move_events = all_events
    if event == 'quit':
      self.game.quit()
      return False

    if self.state == 'playing':
      self.state = self.game.process(self.view, move_events)
      return True

    if self.state == 'ending':
      self.game.wait(self.view)
      if event == 'other_key':
        self.state = 'playing'
        self.game.reset(START)

    return True


  def run(self):

    self.view.run()

####

class MazeGame(object):
  """The actual game"""

  def __init__(self, maps, config):

    self.config = config
    self.dtimer = DeltaTimer(config.dt)
    self.mapper = Mapper(maps, config.width, config.height)
    self.player_accel= config.player_accel
    self.friction = config.friction


  def reset(self, mode):

    self.text = ""
    self.mapper.select(mode)
    x, y = self.mapper.get_point(*self.mapper.start)
    w, h =  self.mapper.player_sizehint
    size =  self.config.player_sizefac
    width = int(w * size)
    height = int(h * size)
    self.player = Player(x+1, y+1, width, height, self.config.player_color)


  def accelerate_player(self, events, accel):

    for ev in events:
      self.player.accelerate(ev, accel)


  def check_places(self):

    place = self.mapper.act_map[self.mapper.get_cell(*self.player.center)]
    if place in PLACES:
      if place == 'e':
        return 'ending'
      else:
        self.reset({'u': UP, 'd': DOWN, 'r': RANDOM}.get(place))

    return 'playing'


  def check_collision(self):
    """Check at first 4 sides of the player rectangle,
    if no collision occurs, check corners."""

    smap = self.mapper.act_map
    mapper = self.mapper

    ws = self.config.width_sensors
    hs = self.config.height_sensors
    north = [smap[mapper.get_cell(sx, sy)] == 'x'
             for sx, sy in self.player.north_sensors(ws)]
    south = [smap[mapper.get_cell(sx, sy)] == 'x'
             for sx, sy in self.player.south_sensors(ws)]
    east = [smap[mapper.get_cell(sx, sy)] == 'x'
             for sx, sy in self.player.east_sensors(hs)]
    west = [smap[mapper.get_cell(sx, sy)] == 'x'
            for sx, sy in self.player.west_sensors(hs)]

    west_east = any(west) or any(east)
    north_south = any(north) or any(south)

    if west_east or north_south:
      self.player.bounce(west_east, north_south)
      return True

    csx = False
    for sx, sy in self.player.vertex_sensors:
      if smap[mapper.get_cell(sx, sy)] == 'x':
        csx, csy = sx, sy
        break

    if not csx:
      return False

    old_px, old_py = self.player.oldpos
    px, py = self.player.pos
    old_csx = csx - px + old_px
    old_csy = csy - py + old_py

    old_cellx, old_celly = mapper.get_cell(old_csx, old_csy)
    cellx, celly = mapper.get_cell(csx, csy)
    self.player.bounce(abs(old_cellx - cellx) > 0, abs(old_celly - celly) > 0)

    return True


  def process(self, view, move_events):
    """Main method"""

    dur = view.frame_duration_secs
    #self.text = str(view.frame_duration_secs)
    self.accelerate_player(move_events, dur * self.player_accel)
    self.dtimer += dur
    self.dtimer.integrate(self.transform_player, self.friction)

    self.mapper.draw_map(view)
    self.player.draw(view)
    self.draw_text(view)

    return self.check_places()


  def transform_player(self, dt, friction):
    """Move player in 1 timestep dt."""

    self.player.move(dt, friction)
    collision = self.check_collision()
    if collision:
      self.player.restore_pos()
      self.player.move(dt, friction)


  def wait(self, view):
    """If player finds exit, ask for new game."""

    self.text = self.config.waiting_text
    self.draw_text(view)


  def draw_text(self, view):

    view.draw_text(self.text)


  def quit(self):

    print("Bye")

####

class DeltaTimer(object):
  """Timing control"""

  def __init__(self, dt):

    self.dt = dt
    self.accu = 0.0


  def __iadd__(self, delta):

    self.accu += delta
    return self


  def integrate(self, func, *args):
    """For a fixed timestep dt, adjust movement to fps."""
    while self.accu >= self.dt:
      func(self.dt, *args)
      self.accu -= self.dt

####

class Config(object):
  """Change dictionary to object attributes."""

  def __init__(self, **kwargs):

    self.__dict__.update(kwargs)

####

def main():

  Controller(PygView, maps, Config(**config)).run()

####

if __name__ == '__main__':

  main()
