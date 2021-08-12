# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion
# https://de.wikipedia.org/wiki/Wurfparabel#/media/Datei:Wurfparabel_Zusammenfassung_aktualisierung.png
# this variant uses Bokeh to create a local website in your browser
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress
# install instructions for Bokeh:  "sudo pip3 install bokeh" https://docs.bokeh.org/en/latest/docs/first_steps.html#first-steps
# to run, type "bokeh serve cannon006_bokeh.py"  and open your webbrowser at http://localhost:5006/cannon006_bokeh


import math
#import numpy as np
import bokeh
import bokeh.io
import bokeh.layouts
import bokeh.models
import bokeh.plotting
#from bokeh.io import curdoc
#from bokeh.layouts import column, row
#from bokeh.models import ColumnDataSource, Slider, TextInput
#from bokeh.plotting import figure

#DASH_STYLES = ["solid", "dashed", "dotted", "dotdash", "dashdot"]

class Data:
    """store global variables here"""
    speed = 30
    angle = 15
    cannon_x = 0     # x-position of cannon
    cannon_y = 0     # y-position of cannon
    critical_distance_to_target =  1 # how close to the target a cannonball must land to count as a hit
    dt =  0.01   # delta time, a smaller number makes a slower, but more precise calculation of the flight path
    t_max = 100000  #
    gravity =  -9.81
    target_x =  100 # x-postion of the target ,
    target_y = 0
    history = []
    # __ prefix means private variable, should not be manipulated by User via GUI
    __cannon_id = None
    __target_id = None
    __cannon_text_id = None
    __target_text_id = None
    __ball_id = None
    __ball_x = 0
    __ball_y = 0
    __number = 0
    __x_values=[]
    __y_values=[]
    __old_values = []

def calculate_world():
    """for grid calculation"""
    Data.__lower_left_x = min(-10, Data.cannon_x - 10, Data.target_x * 2)
    Data.__lower_left_y = min(-10, Data.cannon_y - 10, Data.target_y - 10)
    Data.__upper_right_x = max(10, Data.cannon_x * 1, Data.target_x * 2)
    Data.__upper_right_y = max(10, Data.cannon_y * 1, Data.target_x * 2, Data.target_y + 10)
    #graph_widget.change_coordinates(graph_bottom_left=(int(Data.__lower_left_x), int(Data.__lower_left_y)),
    #                                graph_top_right  =(int(Data.__upper_right_x), int(Data.__upper_right_y)))


def shoot():
    """shooting one cannonball, updating Data.__x_values and Data.__y_values"""
    vx0 = math.cos(math.radians(Data.angle)) * Data.speed
    vy0 = math.sin(math.radians(Data.angle)) * Data.speed
    t = 0
    Data.__ball_x = Data.cannon_x
    Data.__ball_y = Data.cannon_y
    Data.__x_values = []
    Data.__y_values = []
    while t < Data.t_max:
        t += Data.dt  # next time step
        x = Data.cannon_x + vx0 * t  # constant horizontal speed
        y = Data.cannon_y + vy0 * t + 0.5 * Data.gravity * t * t
        Data.__x_values.append(x)
        Data.__y_values.append(y)
        #print(x, y)
        dx = x - Data.__ball_x
        dy = y - Data.__ball_y
        #graph_widget.draw_line(point_from=(Data.__ball_x, Data.__ball_y),
        #                       point_to=(x, y),
        #                       color="red",
        #                       width=1)
        Data.__ball_x = x
        Data.__ball_y = y
        # relocating happens too fast to be observed ... or missing graph update command inside the loop
        # graph_widget.relocate_figure(figure = Data.__ball_id,
        #                             x = Data.__ball_x,
        #                             y = Data.__ball_y)
        # graph_widget.update()
        # print(f"time: {t:.3f}, x:{x:.3f} y:{y:.3f} ")
        # vector math
        distance_to_target = ((Data.__ball_x - Data.target_x) ** 2 + (Data.__ball_y - Data.target_y) ** 2) ** 0.5
        break_reason = None
        if distance_to_target <= Data.critical_distance_to_target:
            break_reason = "Congratulations, You hit the target!"
            break
        elif Data.gravity < 0 and dy < 0 and y < Data.target_y:
            break_reason = "cannonball reached his heighest y position but is still lower than target y position"
            break
        elif Data.gravity > 0 and dy > 0 and y > Data.target_y:
            break_reason = "cannonball reached his lowest y position but is still higher than target y position"
            break
        if dx < 0 and x < Data.__lower_left_x:
            break_reason = "cannonball reached left border"
            break
        if dx > 0 and x > Data.__upper_right_x:
            break_reason = "cannonball reached right border"
            break

    text = f"#{Data.__number} (speed:{Data.speed} angle:{Data.angle}) is {abs(distance_to_target):.2f} m too {'short' if Data.__ball_x < Data.target_x else 'wide'}"
    Data.history.append(text)
    #Data.__old_values.append([Data.__x_values, Data.__y_values])
    if break_reason is not None:
        Data.history.append(break_reason)
    Data.__number += 1



# Set up callbacks
def update_title(attrname, old, new):
    """callback for title"""
    plot.title.text = text.value

# set up callbacks
def update_angle(attrname, old, new):
    """callback for angle"""
    if new is None:
        return
    Data.angle = angle_widget.value
    print(f"angle changed from {old} to {new}")
    #Data.__cannon_sprite.angle = math.radians(Data.angle)

def update_speed(attrname, old, new):
    """callback for speed"""
    if new is None:
        return
    Data.speed = speed_widget.value

def update_parameters(attrname, old, new):
    """generic callback for other cannonshot paramters that require new drawing"""
    Data.cannon_x = cannon_x_widget.value
    Data.cannon_y = cannon_y_widget.value
    Data.target_x = target_x_widget.value
    Data.target_y = target_y_widget.value

    # TODO: ich kann eine 2. Ellipse erzeugen, aber wie krieg ich die erste ellipse weg bzw wie mach ich ein repaint?
    ##plot.ellipse(Data.cannon_x, Data.cannon_y, fill_color="blue", width=15, height=5, angle=math.radians(33),
    ##             legend_label="cannon")


def fire():
    """callback for fire button"""
    shoot()
    #source.data = dict(x=Data.__x_values, y=Data.__y_values)
    #source.data = dict()
    # plot the last 5 shots

    #for shotnumber, entry in enumerate(Data.__old_values[-5:], start=-5):
    #    plot.line(x=entry[0], y=entry[1], line_width=1, line_color="red", line_alpha= (1 - abs(shotnumber)/10),
    #              line_dash=[shotnumber, shotnumber, shotnumber])
    #print("center:",plot.center)
    plot.line(x=Data.__x_values, y=Data.__y_values, line_width=1, line_color="red",
              line_dash=[Data.__number, Data.__number, Data.__number])


#def main():
# Set up data
calculate_world()
Data.__number = 0
Data.__old_values = []
##shoot()
#print("first shot done")

##source = bokeh.models.ColumnDataSource(data=dict(x=Data.__x_values, y=Data.__y_values))


# Set up plot
plot = bokeh.plotting.figure(height=600, width=800, title="bokeh cannon shot",
              tools="crosshair,pan,reset,save,wheel_zoom",
              #x_range=[0, 4*math.pi], y_range=[-2.5, 2.5])
              x_range=[Data.__lower_left_x, Data.__upper_right_x],
              y_range=[Data.__lower_left_y, Data.__upper_right_y])

#plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
# ellipse for cannon
#Data.__cannon_sprite = plot.ellipse(Data.cannon_x, Data.cannon_y, fill_color="blue", width=15, height=5, angle=math.radians(33), legend_label="cannon")
plot.ellipse(Data.cannon_x, Data.cannon_y, fill_color="blue", width=15, height=5, angle=math.radians(33), legend_label="cannon", alpha=0.5)
##
# circle with cross for target
plot.circle_cross(Data.target_x, Data.target_y, legend_label="target", size=20, line_color="red", fill_color="white")

# Set up widgets
text = bokeh.models.TextInput(title="title", value='my cannon shot')
#offset = bokeh.models.Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
#amplitude = bokeh.models.Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
#phase = bokeh.models.Slider(title="phase", value=0.0, start=0.0, end=2*math.pi)
#freq = bokeh.models.Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)

# set up widgets
#angle_widget = bokeh.models.Slider(title="angle in Degrees", value=30, start=-180.0, end=180.0, step=0.1)
##angle_widget = bokeh.models.NumericInput(title="angle in Degree", value=0)
angle_widget = bokeh.models.Spinner(title="angle in [Grad]", high=180, low=-180, step=0.1, value=Data.angle)
#speed_widget = bokeh.models.Slider(title="speed in m/s", value=40, start= 0.0, end=500.0, step=0.1)
speed_widget = bokeh.models.Spinner(title="speed in [m/s]", value=Data.speed, high=10000, low=0, step=0.1, )
fire_widget = bokeh.models.Button(label="click here to fire a cannonball", background="green")
cannon_x_widget = bokeh.models.NumericInput(title="cannon x", value=0)
cannon_y_widget = bokeh.models.NumericInput(title="cannon y", value=0)
target_x_widget = bokeh.models.NumericInput(title="target x", value=100)
target_y_widget = bokeh.models.NumericInput(title="target y", value=0)

# end of setup
# callbacks
text.on_change('value', update_title)

fire_widget.on_click(fire)

angle_widget.on_change('value', update_angle)
speed_widget.on_change('value', update_speed)
#w.on_change('value', update_speed_and_angle)

for w in [ cannon_x_widget, cannon_y_widget, target_x_widget, target_y_widget]:
    w.on_change('value', update_parameters)


# Set up layouts and add to document
#inputs = bokeh.layouts.column(text, offset, amplitude, phase, freq)
inputs = bokeh.layouts.column(text, angle_widget, speed_widget, fire_widget, cannon_x_widget, cannon_y_widget, target_x_widget, target_y_widget)
bokeh.io.curdoc().add_root(bokeh.layouts.row(inputs, plot, width=800))
bokeh.io.curdoc().title = "cannon"


#if __name__ == "__main__":
#    main()


