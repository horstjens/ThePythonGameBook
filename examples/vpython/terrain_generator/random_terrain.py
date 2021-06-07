# inspiration: https://github.com/ragnraok/RandomlandscapeTerrain-Vpython
# run pip install -r requirements.txt in this folder or
# install via pip: vpython see http://vpython.org
# install via pip: hkb-diamondsquare see https://github.com/buckinha/DiamondSquare
import vpython as v
from hkb_diamondsquare import DiamondSquare as DS  # this in turns install numpy
#map1 = DS.diamond_square(shape=(4,4),
#                         min_height=1,
#                         max_height=100,
#                         roughness=0.75)
#print(map1)

class Game:
    world_size = 5
    background_color = v.vector(1,1,0)
    dt = 0.005 # =delta-time ... how fast the simulation should run
    grid_size = 1 # must be positive integer. TODO: allow numpy array for floats
    grid = []
    busy = False # lock flag to avoid too much widghets events
    points = None
    water = None
    # for diamond-square
    min_y = 0.0 # lowest valley
    max_y = 5.0 # highest peak
    ## # below sea, all is blue. between snow and sea, all is green. above snow, all is white
    sea_level = 1 #0.4 # must be between 0 and 1 #
    snow_level = 4 #0.8 # must be between 0 and 1 #
    roughness = 0.65 # must be between 0 and 1 # near 0: very smooth. near 1: very rough terrain
    landscape = None # final object
    scene1 = v.canvas(title=f"landscape world {world_size} x {world_size}, roughness {roughness}",
                      width=1800,
                      height=700,
                      center=v.vector(0, 0, 0),
                      background=background_color,
                      resizable=False
                      )
    scene1.autoscale = False
    # globals


def func_sea_level(s):
    """for sea level slider"""
    print(s, s.number)
    if s.number is None:
        return # empty or useless value in field
    if Game.busy:
        return
    Game.busy = True
    Game.sea_level=min(s.number, Game.snow_level) # can not be higher than snow-level
    #Game.sea_level=max(Game.sea_level, min(0, Game.min_y))
    Game.label_sea_level.text = f" ={Game.sea_level:.2f} "
    #Game.input_snow_level.min = Game.sea_level ## not possible after creation of slider
    Game.water.visible = False
    Game.water.delete()
    make_water()
    repaint_landscape()
    Game.busy = False

def func_snow_level(s):
    """for snow level slider"""
    if s.number is None:
        return # useless value in field
    if Game.busy:
        return
    Game.busy = True
    print("number, sea, snow, maxy a:", s.number, Game.sea_level, Game.snow_level, Game.max_y)
    Game.snow_level=max(s.number, Game.sea_level) # can not be lower than snow-level
    #Game.snow_level=min(Game.snow_level, Game.max_y)
    print("number, sea, snow maxy b:", s.number, Game.sea_level, Game.snow_level, Game.max_y)
    Game.label_snow_level.text = f" ={Game.snow_level:.2f} "
    #Game.input_sea_level.max = Game.snow_level ## not possible to change after creation
    repaint_landscape()
    Game.busy = False

def func_roughness(s):
    """for roughness slider"""
    if Game.busy:
        return
    Game.busy = True
    Game.roughness = s.value
    Game.label_roughness.text = f" ={Game.roughness:.2f} (0 = very smooth, 1= very rough)"
    #try:
    Game.landscape.visible = False
    Game.landscape.delete()
    #except:
    #    print("could not delete landscape")
    recalc_y_values()
    Game.busy = False

def func_world_size(s):
    """for world size slider"""
    if s.number is None:
        return
    if Game.busy:
        return
    Game.busy = True
    Game.world_size = max(1, int(s.number))
    Game.label_world_size.text = f" = {Game.world_size} x {Game.world_size} tiles"
    Game.landscape.visible = False
    Game.landscape.delete()
    Game.worldbox.visible = False
    Game.worldbox.delete()
    for curve in Game.grid:
        curve.visible = False
        curve.delete()
    create_grid()
    recalc_y_values()
    Game.water.visible = False
    Game.water.delete()
    make_water()
    Game.busy = False

def func_min_y(s):
    """for slider_min_y"""
    if s.number is None:
        return
    if Game.busy:
        return
    Game.busy = True
    #print("min max number", Game.min_y, Game.max_y, s.number)
    Game.min_y = min(s.number, Game.max_y) # can not be greater than max_y
    Game.label_min_y.text = f" ={Game.min_y:.2f}"
    #Game.label_sea_level.text=f"{Game.sea_level * 100:.0f} % of (max. height- min. height) = {Game.min_y + Game.sea_level * (Game.max_y - Game.min_y):.2f}"
    #Game.label_snow_level.text=f"{Game.snow_level*100:.0f} % of (max. height- min. height) = {Game.min_y + Game.snow_level* (Game.max_y - Game.min_y):.2f}"
    Game.landscape.visible = False
    Game.landscape.delete()
    Game.worldbox.visible = False
    Game.worldbox.delete()
    for curve in Game.grid:
        curve.visible = False
        curve.delete()
    create_grid()
    recalc_y_values()
    Game.water.visible = False
    Game.water.delete()
    make_water()
    Game.busy = False

def func_max_y(s):
    """for slider_max_y"""
    if s.number is None:
        return
    if Game.busy:
        return
    Game.busy = True
    Game.max_y = max(s.number, Game.min_y)  # can not be lesser than min_y
    Game.label_max_y.text= f" ={Game.max_y:.2f}"
    #Game.label_sea_level.text = f"{Game.sea_level * 100:.0f} % of (max. height- min. height) = {Game.min_y + Game.sea_level * (Game.max_y - Game.min_y):.2f}"
    #Game.label_snow_level.text = f"{Game.snow_level * 100:.0f} % of (max. height- min. height) = {Game.min_y + Game.snow_level * (Game.max_y - Game.min_y):.2f}"
    Game.landscape.visible = False
    Game.landscape.delete()
    Game.worldbox.visible = False
    Game.worldbox.delete()
    for curve in Game.grid:
        curve.visible = False
        curve.delete()
    create_grid()
    recalc_y_values()
    Game.water.visible = False
    Game.water.delete()
    make_water()
    Game.busy = False

def func_recalc():
    """for button recalc"""
    Game.busy = True
    Game.landscape.visible = False
    Game.landscape.delete()
    Game.worldbox.visible = False
    Game.worldbox.delete()
    for curve in Game.grid:
        curve.visible = False
        curve.delete()
    create_grid()
    recalc_y_values()
    Game.water.visible = False
    Game.water.delete()
    make_water()
    Game.busy = False


def create_widgets():
    Game.scene1.append_to_caption("\n\n")
    # ------- roughness of terrain ----------------
    Game.scene1.append_to_caption("change terrain roughness to")
    Game.slider_roughness = v.slider(bind=func_roughness, min=0, max=1.0, step=0.01,
                                     value=Game.roughness, length=500)
    Game.label_roughness = v.wtext(text=f" ={Game.roughness:.2f} (0 = very smooth, 1= very rough)")
    Game.scene1.append_to_caption(Game.label_roughness)
    Game.scene1.append_to_caption(v.button(text="generate new landscape", bind=func_recalc))
    Game.scene1.append_to_caption("\n\n")
    # ---- winputs fields: fields that accept an text entry that will be converted into a number ---
    Game.scene1.append_to_caption("type in values and press ENTER:\n\n ")
    # --------sea level---------------
    Game.scene1.append_to_caption("change sea level to")
    #Game.input_sea_level = v.slider(bind=func_sea_level, min=0.0, max=Game.snow_level, step=0.01, value=Game.sea_level)
    Game.input_sea_level = v.winput(bind=func_sea_level, type="numeric", text=Game.sea_level)
    Game.label_sea_level = v.wtext(text=f" ={Game.sea_level:.2f} ")
    Game.scene1.append_to_caption(Game.label_sea_level)
    Game.scene1.append_to_caption(" (must be lesser than snow level)\n\n")
    # ------- snow level --------------
    Game.scene1.append_to_caption("change snow level to")
    #Game.input_snow_level = v.slider(bind=func_snow_level, min=Game.sea_level, max=1.0, step=0.01, value=Game.snow_level)
    #Game.label_snow_level = v.wtext(text=f"{Game.snow_level*100:.0f} % of (max. height- min. height) = {Game.min_y + Game.snow_level*(Game.max_y-Game.min_y):.2f}")
    Game.input_snow_level = v.winput(bind=func_snow_level, type="numeric", text=Game.snow_level)
    Game.label_snow_level = v.wtext(text=f" ={Game.snow_level:.2f} ")
    Game.scene1.append_to_caption(Game.label_snow_level)
    Game.scene1.append_to_caption(" (must be greater than sea level)\n\n")

    # --------world size ---------------
    Game.scene1.append_to_caption("change world size to: ")
    #Game.input_world_size = v.slider(bind=func_world_size, min=1, max=100, step=1,
    #                                  value=Game.world_size)
    Game.input_world_size = v.winput(bind=func_world_size, type="numeric", text=Game.world_size)
    Game.label_world_size = v.wtext(text=f" = {Game.world_size} x {Game.world_size} tiles")
    Game.scene1.append_to_caption(Game.label_world_size)
    Game.scene1.append_to_caption("\n\n")
    # -------- min height, max height --------------
    Game.scene1.append_to_caption("change minimum height to:")
    Game.input_min_y = v.winput(bind=func_min_y, type="numeric", text=Game.min_y)
    Game.label_min_y = v.wtext(text=f" ={Game.min_y:.2f}")
    Game.scene1.append_to_caption(Game.label_min_y)
    Game.scene1.append_to_caption("  change maximum height to:")
    Game.input_max_y = v.winput(bind=func_max_y, type="numeric",text=Game.max_y)
    Game.label_max_y = v.wtext(text=f" ={Game.max_y:.2f}" )
    Game.scene1.append_to_caption(Game.label_max_y)
    Game.scene1.append_to_caption("\n\n")
    # --------
    Game.scene1.append_to_caption("change color of ")
    



def repaint_landscape():
    # because water level has changed...
    # do NOT change height values of landscape, only change color values
    for line in Game.points:
        for point in line:
            point.color = get_color_from_y(point.pos.y)
    try:
        Game.landscape.visible = False
        Game.landscape.delete()
    except:
        print("could not delete non-existing landscape...")
    create_landscape_from_points()


def recalc_y_values():
    ## make diamond-square map (a list of lists of integer values) of y-values
    cells = len(range(0, Game.world_size+1, Game.grid_size)) # +1 is important because quads need neighbors
    map1 = DS.diamond_square(
                    shape=(cells, cells),
                    min_height=Game.min_y,
                    max_height=Game.max_y,
                    roughness = Game.roughness)

    Game.points = []
    for z, line in enumerate(map1):
        pointline = []
        for x , y_value in enumerate(line):
            pointline.append(v.vertex(pos=v.vec(x,y_value,z), color=get_color_from_y(y_value)))
        Game.points.append(pointline)
    #Game.points = points
    create_landscape_from_points()

def create_landscape_from_points():
    # --- create quads
    quadlist = []
    for y, line in enumerate(Game.points):
        for x, point in enumerate(line):
            #a = point
            try:
                a = Game.points[y][x]
                b = Game.points[y][x+1]
                c = Game.points[y+1][x+1]
                d = Game.points[y+1][x]
            except IndexError:
                continue
            quadlist.append(v.quad(vs=[a,b,c,d]))


    Game.landscape = v.compound(quadlist,  origin=v.vector(0,0,0), pos=v.vector(0,0,0))
    #Game.quadlist = quadlist
    #Game.map1 = map1

def get_color_from_y(y_value):
    # returns a color for height map
    # everything below Game.sea_level is blue
    # everything above Game.snow_level is white
    # everything between is green
    max_diff = Game.max_y - Game.min_y
    # calculate y as % of max_diff
    #try:
    y_percent = (y_value - Game.min_y) / max_diff
    #except:
    #    return(v.vector(0.5,0.5,0.5))
    if y_value < Game.sea_level:
        # 0 is dark blue, sea-level is green- blue
        c = (y_value - Game.min_y) / (Game.sea_level - Game.min_y)
        return v.vector(0, 0, c) # blue
    elif y_value < Game.snow_level:
        # 0 is green, snow_level is grey-black
        c = (y_value - Game.sea_level) / (Game.snow_level - Game.sea_level)
        return v.vector(c*0.5, 1-c*0.5, c*0.5) #green
    else:
        # 0 is grey-black, 1 is white
        c = ( y_value - Game.snow_level) / ( Game.max_y - Game.snow_level)
        return v.vector(c,c,c)

def create_grid():
    Game.grid = [] # for curves
    basecolor = v.vector(0.5,0.5,0.5)
    #xbaselines = []
      # return values
    # create xz ground
    floor = v.box(pos=v.vector(Game.world_size /2,0, Game.world_size/2, ),
                   size=v.vector(Game.world_size, 0.1, Game.world_size),
                   color=v.vector(0.1, 0.1, 0.1),
                   opacity=0.25)
    for z in range(0, Game.world_size + 1, Game.grid_size):
        Game.grid.append(v.curve(v.vector(0, 0, z), v.vector(Game.world_size, 0, z), color=basecolor))
    for x in range(0, Game.world_size + 1, Game.grid_size):
        Game.grid.append(v.curve(v.vector(x, 0, 0), v.vector(x, 0, Game.world_size), color=basecolor))
    # xy wall
    starty = 0 if Game.min_y >= 0 else int(Game.min_y) - 1
    endy = int(Game.max_y) + 1 if Game.max_y > 0 else 0
    wall1 =   v.box(pos=v.vector(Game.world_size/2, starty + (endy-starty)/2, 0),
                   size=v.vector( Game.world_size, (endy-starty), 0.1),
                   color=v.vector(0.1, 0.1, 0.1),
                   opacity=0.25)
    for y in range(starty, endy, Game.grid_size):
        Game.grid.append(v.curve(v.vector(0, y, 0), v.vector(Game.world_size, y, 0), color=basecolor))
    for x in range(0, Game.world_size + 1, Game.grid_size):
        Game.grid.append(v.curve(v.vector(x, starty, 0), v.vector(x, endy, 0), color=basecolor))
    # zy wall
    wall2 = v.box(pos=v.vector(0, starty + (endy-starty)/2, Game.world_size/2),
                   size=v.vector(0.1, (endy-starty),  Game.world_size),
                   color=v.vector(0.1, 0.1, 0.1),
                   opacity=0.25)
    for y in range(starty, endy, Game.grid_size):
        Game.grid.append(v.curve(v.vector(0, y, 0), v.vector(0, y, Game.world_size), color=basecolor))
    for z in range(0, Game.world_size + 1, Game.grid_size):
        Game.grid.append(v.curve(v.vector(0, starty, z), v.vector(0, endy, z), color=basecolor))
    #curves CANNOT be part of compound
    max_y_box = v.box(pos=v.vector(0, Game.max_y, 0),
                      color=v.vector(1,1,0),
                      size=v.vector(1,0.1,1))
    min_y_box = v.box(pos=v.vector(0, Game.min_y, 0),
                      color=v.vector(0,1,1),
                      size=v.vector(1,0.1,1))
    Game.worldbox=v.compound([floor, wall1, wall2, max_y_box, min_y_box], origin=v.vector(0,0,0))



def make_water():

    starty = min(0, Game.min_y, Game.sea_level)
    height = max(0.1, Game.sea_level - starty)
    y1 = starty + height /2
    Game.water = v.box(color=v.vector(0, 0, 1),
               opacity=0.45,
               pos=v.vector(Game.world_size / 2, y1,  Game.world_size / 2),
               size=v.vector(Game.world_size ,  height, Game.world_size ),
               )

# ---------------

def create_world():
    """create ground and an axis cross at 0,0,0 """
    mybox = v.box(pos=v.vector(0, 0, 0), size=v.vector(0.5, 0.5 ,0.5),
                  color=v.vector(0.2, 0.2, 0.2), opacity=0.25)
    xarrow = v.arrow(pos=v.vector(0, 0, 0), axis=v.vector(1, 0, 0), color=v.vector(1, 0, 0))
    xletter = v.text(pos=xarrow.axis, text="x", color=xarrow.color,
                     height=0.5, lenght=0.5, depth=0.1, billboard=False,
                     axis=xarrow.axis, up=v.vector(0, 1, 0))
    yarrow = v.arrow(pos=v.vector(0, 0, 0), axis=v.vector(0, 1, 0), color=v.vector(0, 1, 0))
    yletter = v.text(pos=yarrow.axis, text="y", color=yarrow.color,
                     height=0.5, lenght=0.5, depth=0.1, billboard=False,
                     axis=yarrow.axis, up=v.vector(0, 1, 0))
    zarrow = v.arrow(pos=v.vector(0, 0, 0), axis=v.vector(0, 0, 2), color=v.vector(0, 0, 1))
    zletter = v.text(pos=zarrow.axis, text="z", color=zarrow.color,
                     height=0.5, lenght=0.5, depth=0.1, billboard=False,
                     axis=zarrow.axis, up=v.vector(0, 1, 0))


def main():
    """main game function"""
    create_world()
    create_widgets()
    create_grid()
    recalc_y_values()
    make_water()
    #create_rover()

    while True:
        v.rate(1/Game.dt)
        keys = v.keysdown()
        if "f" in keys:
            print("f was pressed")

if __name__ == "__main__":
    main()
