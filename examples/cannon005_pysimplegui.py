# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion
# https://de.wikipedia.org/wiki/Wurfparabel#/media/Datei:Wurfparabel_Zusammenfassung_aktualisierung.png
# this variant uses PySimpleGui (using Tkinter)
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress
# install PySimpleGUI via pip command or download it directly from Github: https://pysimplegui.readthedocs.io/en/latest/

import math
import PySimpleGUI as sg

class Data:
    """store global variables here"""
    speed = 100
    angle = 20
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

def main():
    """main loop for pysimplegui"""
    # Define the window's contents
    layout_buttons    = sg.Column(vertical_alignment="top",layout=[
                                       [sg.Text("speed:", size=(6,1), justification="right"), sg.Input(key="speed", size=(10,1), default_text=Data.speed),],
                                       [sg.Text("angle:", size=(6,1), justification="right"), sg.Input(key="angle", size=(10,1), default_text=Data.angle),],
                                       [sg.Button('Fire cannon', key="fire", size=(15,1))],
                                       [sg.Button('Change Settings', key="settings", size=(15,1))],
                                       [sg.Button('Clear', size=(15,1)),],
                                       [sg.Button('Quit', size=(15,1)),],
                                       ])
    layout_settings  = sg.Column(layout=[[sg.Text(k+":", size=(22,1), justification="right"), sg.Input(key=k, size=(14,1), default_text = v, disabled=True) ]  for k, v in Data.__dict__.items() if "__" not in k and k not in ("history", "speed", "angle")],)
    layout_history   = sg.Multiline(default_text=Data.history, key="history", disabled=True, autoscroll=True, size=(40,12))
    layout = [  [sg.Text("play:", size=(20,1)), sg.Text("settings:", size=(45,1)), sg.Text("history:", size=(30,1))],
                [sg.HorizontalSeparator()],
                [layout_buttons, sg.VerticalSeparator(), layout_settings, sg.VerticalSeparator(), layout_history],
                [sg.HorizontalSeparator()],
                [sg.Graph(canvas_size=(800,600), key="graph", graph_bottom_left=(0,0), graph_top_right=(200,200),border_width=1)],
              ]

    # Create the window
    window = sg.Window('Cannon Game Title', layout)

    # Display and interact with the Window using an Event Loop
    calculate_world(window["graph"]) # for graph size, change hidden size attributes inside Data
    window.finalize()
    make_grid(window["graph"])
    Data.__number = 0
    Data.history = []
    change_settings = True
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        # Output a message to the window
        elif event == "settings":
            # change or accept settings
            #print("window settings ist:", window["settings"], window["settings"].__dict__)
            if change_settings:
                # enable changing of settings
                change_settings = False
                window["settings"].Update("Accept Settings")
                window["fire"].Update(disabled=True)
                window["Clear"].Update(disabled=True)
                for key in [k for k in Data.__dict__.keys() if "__" not in k and k not in ("history", "speed", "angle")]:
                    window[key].Update(disabled=False)
            else:
                # accept changed settings, start a new game
                change_settings = True
                window["settings"].Update("Change Settings")
                window["fire"].Update(disabled=False)
                window["Clear"].Update(disabled=False)
                for key in [k for k in Data.__dict__.keys() if "__" not in k and k not in ("history", "speed", "angle")]:
                    window[key].Update(disabled=True)
                    setattr(Data, key, float(values[key]))
                calculate_world(window["graph"])
                window["graph"].erase()
                make_grid(window["graph"])
                Data.__number = 0
                Data.history = []

        elif event == "Clear":
            # clear old tracer lines from the Graph widget, but the game continues
            window["graph"].erase()
            make_grid(window["graph"])
        elif event == "fire":
            # update Data
            Data.angle = float(values["angle"])
            Data.speed = float(values["speed"])
            #print("bumm!")
            #print("angle:", Data.angle, "speed:", Data.speed)
            Data.__number += 1
            shoot(window["graph"])
            # update history widget AFTER shooting
            window["history"].update("\n".join(Data.history))

    window.close()



def shoot(graph_widget):
        """shooting one cannonball"""
        vx0 = math.cos(math.radians(Data.angle)) * Data.speed
        vy0 = math.sin(math.radians(Data.angle)) * Data.speed
        t = 0
        Data.__ball_x = Data.cannon_x
        Data.__ball_y = Data.cannon_y
        while t < Data.t_max:
            t += Data.dt  # next time step
            x = Data.cannon_x + vx0 * t  # constant horizontal speed
            y = Data.cannon_y + vy0 * t + 0.5 * Data.gravity * t * t
            print(x,y)
            dx = x - Data.__ball_x
            dy = y - Data.__ball_y
            graph_widget.draw_line(point_from = (Data.__ball_x, Data.__ball_y),
                                   point_to = (x,y),
                                   color="red",
                                   width=1)
            Data.__ball_x = x
            Data.__ball_y = y
            # relocating happens too fast to be observed ... or missing graph update command inside the loop
            #graph_widget.relocate_figure(figure = Data.__ball_id,
            #                             x = Data.__ball_x,
            #                             y = Data.__ball_y)
            #graph_widget.update()
            #print(f"time: {t:.3f}, x:{x:.3f} y:{y:.3f} ")
            # vector math
            distance_to_target = ((Data.__ball_x  - Data.target_x ) ** 2 + (Data.__ball_y - Data.target_y) ** 2)**0.5
            if distance_to_target <= Data.critical_distance_to_target:
                break
            elif Data.gravity < 0 and dy < 0 and y < Data.target_y:
                break
            elif Data.gravity > 0 and dy > 0 and y > Data.target_y:
                break
            if dx < 0 and x < Data.__lower_left_x:
                break
            if dx > 0 and x > Data.__upper_right_x:
                break

        text = f"#{Data.__number} (speed:{Data.speed} angle:{Data.angle}) is {abs(distance_to_target):.2f} m too {'short' if Data.__ball_x < Data.target_x else 'wide'}"
        Data.history.append( text)
        if distance_to_target < Data.critical_distance_to_target:
            # print("you hit the target!")
            text = "Congratulations, You hit the target!"
            Data.history.append( text )

def calculate_world(graph_widget):
    """for grid calculation"""
    Data.__lower_left_x = min(-10, Data.cannon_x - 10, Data.target_x * 2)
    Data.__lower_left_y = min(-10, Data.cannon_y - 10, Data.target_y - 10)
    Data.__upper_right_x = max(10, Data.cannon_x * 1, Data.target_x * 2)
    Data.__upper_right_y = max(10, Data.cannon_y * 1, Data.target_x * 2, Data.target_y + 10)
    graph_widget.change_coordinates(graph_bottom_left=(int(Data.__lower_left_x), int(Data.__lower_left_y)),
                                    graph_top_right  =(int(Data.__upper_right_x), int(Data.__upper_right_y)))

def make_grid(graph_widget):
    """paints a grid and the position of target and cannon. cleans every existing figure on the graph widget"""
    graph_widget.erase()
    graph_widget.draw_line(point_from=(Data.__lower_left_x, 0), point_to=(Data.__upper_right_x, 0), color="grey",
                           width=2.5)
    graph_widget.draw_line(point_from=(0, Data.__lower_left_y), point_to=(0, Data.__upper_right_y), color="grey",
                           width=2.5)
    graph_widget.draw_text(text="y",
                           location=(Data.__lower_left_x+3,Data.__upper_right_y-3),
                           font=("CourierNew", 10),
                           angle=0,
                           text_location="center")
    graph_widget.draw_text(text="x",
                           location=(Data.__upper_right_x - 3, Data.__lower_left_y + 3),
                           font=("CourierNew", 10),
                           angle=0,
                           text_location="center")
    for y in range(int(Data.__lower_left_y), int(Data.__upper_right_y), (int(Data.__upper_right_y) - int(Data.__lower_left_y)) // 20 ):
        graph_widget.draw_line(point_from=(Data.__lower_left_x, y),
                               point_to = (Data.__upper_right_x, y),
                               color="grey",
                               width=1)
        graph_widget.draw_text(text=f"{y:>4}",
                           location=(Data.__lower_left_x +3  , y),
                           color="black",
                           font=("CourierNew", 10),
                           angle=0,
                           text_location="center",
                           )

    for x in range(int(Data.__lower_left_x), int(Data.__upper_right_x), (int(Data.__upper_right_x) - int(Data.__lower_left_x)) // 20 ):
        graph_widget.draw_line(point_from=(x, Data.__lower_left_y),
                               point_to=(x, Data.__upper_right_y),
                               color="grey",
                               width=1)
        graph_widget.draw_text(text=f"{x:>4}",
                               location=(x , Data.__lower_left_y + 2),
                               color="black",
                               font=("CourierNew", 10),
                               angle=90,
                               text_location="center",
                               )


    #for y in range(Data.__lower_left_y, Data.__upper_right_y, (Data.__upper_right_y - Data.__lower_left_y) //20):
    Data.__cannon_id = graph_widget.draw_rectangle(top_left=(Data.cannon_x -1, Data.cannon_y+1 ),
                                bottom_right=(Data.cannon_x +1, Data.cannon_y - 1),
                                fill_color="blue",
                                line_color="green",
                                line_width=5)
    Data.__cannon_text_id = graph_widget.draw_text(text= "             cannon",
                           font=("Arial", 8),
                           angle=80,
                           location=(Data.cannon_x , Data.cannon_y)
                           )

    Data.__target_id = graph_widget.draw_circle(center_location =(Data.target_x , Data.target_y ),
                                         radius = 2,
                                         fill_color="black",
                                         line_color="red",
                                         line_width=2)
    Data.__target_text_id = graph_widget.draw_text(text="                  target",
                                         font=("Arial", 8),
                                         angle = 80,
                                         location=(Data.target_x, Data.target_y)
                                         )
    #Data.__ball_id = graph_widget.draw_circle(center_location = (Data.cannon_x, Data.cannon_y),
    #                                          radius=5,
    #                                          fill_color="red",
    #                                          line_width=0)
    Data.__ball_x = Data.cannon_x
    Data.__ball_y = Data.cannon_y

if __name__ == "__main__":
    main()
