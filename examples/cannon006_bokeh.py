# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion
# https://de.wikipedia.org/wiki/Wurfparabel#/media/Datei:Wurfparabel_Zusammenfassung_aktualisierung.png
# this variant uses Bokeh to create a local website in your browser
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress
# install instructions for Bokeh:  "sudo pip3 install bokeh" https://docs.bokeh.org/en/latest/docs/first_steps.html#first-steps
# to run, type "bokeh serve cannon006_bokeh.py"  and open your webbrowser at http://localhost:5006/cannon006_bokeh


# TODO: how to update RANGE of plot?
# done: tracer soll bis zum bildschirmrand laufen
# done: min distance to target während dem ganzen flug berechnen für ball
# TODO: reset button
# TODO: Animation?
#  # plot wird crazy be negativen werten für target/cannon bzw out-of range werten -> braucht x-range/y-range update
# done: achsenbeschriftung https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html?highlight=axis%20label#titles

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
    critical_distance_to_target =  15 # how close to the target a cannonball must land to count as a hit
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
    Data.__lower_left_x = min(Data.cannon_x - 10, Data.target_x -10)
    Data.__lower_left_y = min(Data.cannon_y - 10, Data.target_y - 10)
    Data.__upper_right_x = max(Data.cannon_x +10, Data.target_x +10)
    Data.__upper_right_y = max(Data.cannon_y +10, Data.target_y +10, Data.target_x+10)

def shoot():
    """shooting one cannonball, updating Data.__x_values and Data.__y_values"""
    vx0 = math.cos(math.radians(Data.angle)) * Data.speed
    vy0 = math.sin(math.radians(Data.angle)) * Data.speed
    t = 0
    Data.__ball_x = Data.cannon_x
    Data.__ball_y = Data.cannon_y
    Data.__x_values = []
    Data.__y_values = []
    best_distance_to_target = ((Data.cannon_x - Data.target_x) ** 2 + (Data.cannon_y - Data.target_y) ** 2) ** 0.5
    #print("plot range borders x:", plot.x_range.start, plot.x_range.end )
    while t < Data.t_max:
        t += Data.dt  # next time step
        x = Data.cannon_x + vx0 * t  # constant horizontal speed
        y = Data.cannon_y + vy0 * t + 0.5 * Data.gravity * t * t
        Data.__x_values.append(x)
        Data.__y_values.append(y)
        dx = x - Data.__ball_x
        dy = y - Data.__ball_y

        Data.__ball_x = x
        Data.__ball_y = y
        distance_to_target = ((Data.__ball_x - Data.target_x) ** 2 + (Data.__ball_y - Data.target_y) ** 2) ** 0.5
        if distance_to_target < best_distance_to_target:
            best_distance_to_target = distance_to_target
        break_reason = "t_max reached"
        if distance_to_target <= Data.critical_distance_to_target:
            break_reason = "<b>Congratulations, You hit the target!</b>"
            break
        #elif Data.gravity < 0 and dy < 0 and y < Data.target_y:
        if Data.gravity < 0 and y < Data.__lower_left_y:
            break_reason = "cannonball reached lower border"
            break
        #elif Data.gravity > 0 and dy > 0 and y > Data.target_y:
        elif Data.gravity > 0 and y > Data.__upper_right_y:
            break_reason = "cannonball reached upper border"
            break
        if dx < 0 and x < Data.__lower_left_x:
            break_reason = "cannonball reached left border"
            break
        if dx > 0 and x > Data.__upper_right_x:
            break_reason = "cannonball reached right border"
            break
    if t >= Data.t_max:
        break_reason = "all timesteps calculated"

    #text = f"#{Data.__number} (speed:{Data.speed} angle:{Data.angle}) is {abs(distance_to_target):.2f} m too {'short' if Data.__ball_x < Data.target_x else 'wide'}"
    text = f"#{Data.__number} (speed:{Data.speed} angle:{Data.angle}): best distance to target = {best_distance_to_target} m"
    if best_distance_to_target < Data.critical_distance_to_target:
        break_reason = "<b>Congratulations, You hit the target!</b>"
    Data.history.insert(0, text + ", " + break_reason) # newest history line should be on top
    Data.__number += 1



# Set up callbacks
#ef update_title(attrname, old, new):
#   """callback for title"""
#   plot.title.text = text.value

# set up callbacks
def update_angle(attrname, old, new):
    """callback for angle"""
#    if new is None:
#        return
    Data.angle = angle_widget.value
    # update cannon sprite
    paint_cannon_and_target()

def update_speed_and_gravity(attrname, old, new):
    """callback for speed"""
    #if new is None:
    #    return
    Data.speed = speed_widget.value
    Data.gravity = gravity_widget.value

def update_parameters(attrname, old, new):
    """generic callback for other cannonshot paramters that require new drawing"""
    Data.cannon_x = cannon_x_widget.value
    Data.cannon_y = cannon_y_widget.value
    Data.target_x = target_x_widget.value
    Data.target_y = target_y_widget.value
    Data.critical_distance_to_target = crit_distance_widget.value
    calculate_world()
    plot.x_range.start = Data.__lower_left_x
    plot.x_range.end = Data.__upper_right_x
    plot.y_range.start = Data.__lower_left_y
    plot.y_range.end = Data.__upper_right_y
    #plot.x_range = bokeh.models.Range([Data.__lower_left_x, Data.__upper_right_x])
    #plot.y_range = bokeh.models.Range([Data.__lower_left_y, Data.__upper_right_y])
    #plot.x_range = (Data.__lower_left_x, Data.__upper_right_x),
    #plot.y_range = (Data.__lower_left_y, Data.__upper_right_y),
    paint_cannon_and_target()


def update_parameters2(attrname, old, new):
    """generic callback for harmless parameter widgets that don't require redrawing"""
    Data.dt = dt_widget.value
    Data.t_max = t_max_widget.value


def paint_cannon_and_target():
    cannon = plot.select(name="cannon")
    cannon.visible = False
    target = plot.select(name="target")
    target.visible = False
    target_radius = plot.select(name="target_radius")
    target_radius.visible = False

    #plot.ellipse(Data.cannon_x, Data.cannon_y, fill_color="blue", width=15, height=5, angle=math.radians(Data.angle-90),
    #             legend_label="cannon", alpha=0.5, name="cannon")
    plot.circle_cross(Data.cannon_x, Data.cannon_y, size=20, angle=math.radians(Data.angle-90), legend_label="cannon", alpha=0.5, name="cannon")
    plot.circle_dot(Data.target_x, Data.target_y, legend_label="target", size=20, line_color="red",
                      fill_color="white", name="target")
    plot.circle(Data.target_x, Data.target_y, legend_label="target radius", radius=Data.critical_distance_to_target,
                line_color="black", line_dash="dotted", fill_color=None, name="target_radius" )


def fire():
    """callback for fire button"""
    shoot()

    plot.line(x=Data.__x_values, y=Data.__y_values, line_width=1, line_color="red",
              line_dash=[Data.__number, Data.__number, Data.__number], name="tracer")
    result_widget.update(text="<br>".join(Data.history))

def clear():
    """callback for clear button"""
    # clear history
    Data.history = []
    Data.__number = 1
    # clear result field
    result_widget.update(text="<br>".join(Data.history))
    lines = plot.select(name="tracer")
    lines.visible = False


#def main(): # ---------------------------------------------------------
calculate_world()
Data.__number = 1 # necessary or first shot wil not work

# Set up plot
plot = bokeh.plotting.figure(height=600, width=800, title="bokeh cannon shot",
              tools="crosshair,pan,reset,save,wheel_zoom",
              #x_range=[0, 4*math.pi], y_range=[-2.5, 2.5])
              sizing_mode="stretch_width",
              #x_range=[Data.__lower_left_x, Data.__upper_right_x],
              #y_range=[Data.__lower_left_y, Data.__upper_right_y],

              )
plot.xaxis.axis_label = "x-position in [m]"
plot.yaxis.axis_label = "y-position in [m]"
plot.yaxis.major_label_orientation = "vertical"
#p.xaxis.axis_line_width = 3
#p.xaxis.axis_line_color = "red"

# change some things about the y-axis

#p.yaxis.major_label_text_color = "orange"

#plot.add_layout(bokeh.models.Title(text="x-position in [m]", align="center"), "below")
#plot.add_layout(bokeh.models.Title(text="y-position in [m]", align="center"), "left")

paint_cannon_and_target()
# Set up widgets
angle_widget = bokeh.models.Spinner(title="angle in [Grad]:", high=180, low=-180, step=0.1, value=Data.angle)
speed_widget = bokeh.models.Spinner(title="speed in [m/s]:", value=Data.speed, high=10000, low=0, step=0.1, )
gravity_widget = bokeh.models.Spinner(title = "gravity in [m/s²]:", high=50, low=-50, step=0.1, value=Data.gravity)
fire_widget = bokeh.models.Button(label="fire a cannonball", background="green")
clear_widget = bokeh.models.Button(label="clear old shots",  background="green")
cannon_x_widget = bokeh.models.NumericInput(title="cannon x in [m]:", value=Data.cannon_x, mode="float")
cannon_y_widget = bokeh.models.NumericInput(title="cannon y in [m]:", value=Data.cannon_y, mode="float")
target_x_widget = bokeh.models.NumericInput(title="target x in [m]:", value=Data.target_x, mode="float")
target_y_widget = bokeh.models.NumericInput(title="target y in [m]:", value=Data.target_y, mode="float")
dt_widget = bokeh.models.Spinner(title="delta time (dt)  in [s]", value=Data.dt, high=0.99, low=0.01, step=0.01)
t_max_widget = bokeh.models.NumericInput(title="max. number of timesteps", value=Data.t_max, mode="float")
crit_distance_widget = bokeh.models.NumericInput(title="target radius in [m]", value=Data.critical_distance_to_target, mode="float")
result_widget = bokeh.models.Div(text="results:", width=800)


# callbacks
#text.on_change('value', update_title)
# ---- notice: passing as second argument the function name without quotes, without parentheses ----
fire_widget.on_click(fire)
clear_widget.on_click(clear)
angle_widget.on_change('value', update_angle)
speed_widget.on_change('value', update_speed_and_gravity)
gravity_widget.on_change('value', update_speed_and_gravity)
#w.on_change('value', update_speed_and_angle)

for w in [ cannon_x_widget, cannon_y_widget, target_x_widget, target_y_widget, crit_distance_widget]:
    w.on_change('value', update_parameters)

for w in [ dt_widget, t_max_widget]:
    w.on_change('value', update_parameters2)


# Set up layouts and add to document
#inputs = bokeh.layouts.column(text, offset, amplitude, phase, freq)
buttons = bokeh.layouts.row( fire_widget, clear_widget , width=300)
my_widgets = bokeh.layouts.column( angle_widget, speed_widget, gravity_widget,
                                   #clear_widget, cannon_x_widget, cannon_y_widget, target_x_widget, target_y_widget,
                                   buttons, cannon_x_widget, cannon_y_widget, target_x_widget, target_y_widget,
                                   dt_widget, t_max_widget, crit_distance_widget, width=400, sizing_mode="fixed")
#bokeh.io.curdoc().add_root(bokeh.layouts.row(plot, my_widgets, width=800))
bokeh.io.curdoc().add_root(bokeh.layouts.row(plot, my_widgets, sizing_mode="stretch_width",))
bokeh.io.curdoc().add_root(bokeh.layouts.row(result_widget))
bokeh.io.curdoc().title = "cannon shot simulator"


#if __name__ == "__main__":
#    main()


