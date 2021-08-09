# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion
# https://de.wikipedia.org/wiki/Wurfparabel#/media/Datei:Wurfparabel_Zusammenfassung_aktualisierung.png
# this variant is text-only, but includes angle and a class instead a dict for data
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress


import math
import turtle

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


def ask_speed_and_angle():
    #speed_default = Data.speed # data["speed"]
    #try:
        #new_speed = float(input(f"inital speed in [m/s] (enter={speed_default})"))
    lines = "\n".join(Data.history)
    new_speed = turtle.numinput(title= "please enter speed: (0 to quit)",

                                    prompt= f"{lines}\n\nspeed in [m/s] >>>",
                                    default= Data.speed,
                                    minval = 0,
                                    maxval = 1000000)
    #except ValueError:
    #    new_speed = speed_default
    #print("speed is set to", new_speed)
    Data.speed = new_speed #data["speed"] = new_speed

    #angle_default = Data.angle # data["angle"]
    #try:
        #new_angle = float(input(f"angle in degree (enter={angle_default})"))
    new_angle = turtle.numinput(title="please enter angle: (0 to quit)",
                                prompt = f"{lines}\n\nangle in [Grad] >>>",
                                default = Data.angle,
                                minval = 0,
                                maxval = 90)
    #except ValueError:
    #    new_angle = angle_default
    #print("angle is set to", new_angle)
    Data.angle = new_angle #data["angle"] = new_angle
    #return data


def ask_game_parameters():
    """ask for every parameter except angle and speed and history
       change this value depending on user input"""
    keys = [k for k in Data.__dict__.keys() if "__" not in k and k not in ("angle", "speed", "history")]
    for key in keys:
        value = Data.__dict__[key]
        #print(f"the current value for {key} is {value}")
        #try:
        #    new_value = float(input(f"enter new value for {key}: (enter=accept {value})"))
        #except ValueError:
        #    new_value = value
        new_value = turtle.numinput(title="change or accept parameter",
                                    prompt=f"enter new value for {key}",
                                    default=value)
        if new_value != value:
            #if key in ["x0", "y0"] and new_value < 0:
            #    continue
            #data[key] = new_value
            ## Data.__setattr__(key, value) # wrong!
            setattr(Data, key, new_value)       # right! updating a class attribute
            #print(f"{key} changed to: {new_value}")
    #return data
    #display_parameters()
            

def play():
    #print(f'the target is at x position {Data.target_x} and at y position 0')
    #print(f'the cannon is at x position {Data.x0} and at y position {Data.y0}')
    #print("change angle and speed to hit the target as close as possible. (or enter 0 for both values to quit)")
    number = 1

    #turtle.clearscreen()
    cannon=turtle.Turtle()
    cannon.shape("arrow")
    cannon.pencolor("blue")
    cannon.speed(0)
    cannon.penup()
    cannon.goto(Data.cannon_x, Data.cannon_y)
    ball = turtle.Turtle()
    ball.shape("circle")
    red_value = (1 - number * 0.05) % 1  # can not be negative

    ball.pencolor((red_value,0,0))
    goal = turtle.Turtle()
    goal.shape("square")
    goal.penup()
    goal.speed(0)
    goal.goto(Data.target_x, Data.target_y)
    goal.pencolor("green")
    pen = turtle.Turtle()
    pen.penup()
    pen.speed(0)



    while True:
        pen.goto(Data.target_x, Data.target_x*2 - 10)
        pen.write(f"shot number {number}", align="center", font=("Arial", 20, "normal"))

        #print(f"shot number {number}")
        ask_speed_and_angle()  # ask for speed and angle
        pen.clear()
        if Data.speed == 0 and Data.angle == 0:
            print("aborting game")
            return
        cannon.setheading(Data.angle)
        #cannon.pendown()

        #goal.pendown()
        #ball.clear()
        ball.penup()
        ball.speed(0)
        ball.goto(cannon.pos())
        ball.pendown()

        # max_range does not seem to work correctly when x0 and y0 is changed
        #max_range = abs(
        #    (Data.speed ** 2 / Data.gravity) *
        #    math.cos(math.radians(Data.angle)) *
        #    (math.sin(math.radians(Data.angle)) + (math.sin(math.radians(Data.angle)) ** 2 +
        #                                           (2 * Data.y0 * Data.gravity / Data.speed ** 2)) ** 0.5)
        #)
        vx0 = math.cos(math.radians(Data.angle)) * Data.speed
        vy0 = math.sin(math.radians(Data.angle)) * Data.speed
        t = 0
        y = 0
        #if show_xy:
        #ball.penup()
        #ball.goto()
        #cannonball = turtle.Turtle
        while t < Data.t_max:
            t += Data.dt  # next time step
            x = Data.cannon_x + vx0 * t  # constant horizontal speed
            y = Data.cannon_y + vy0 * t + 0.5 * Data.gravity * t * t
            dx = x - ball.xcor()
            dy = y - ball.ycor()
            ball.goto(x,y)
            #print(f"time: {t:.3f}, x:{x:.3f} y:{y:.3f} ")
            distance_to_target = ball.pos() - goal.pos()
            if abs(distance_to_target) <= Data.critical_distance_to_target:
                break
            if dy < 0 and y < goal.ycor():
                break
            if dx < 0 and x < Data.__lower_left_x:
                break
            if dx > 0 and x > Data.__upper_right_x:
                break

            #print("dist:", distance_to_target)


        #pen.penup()
        #pen.goto(Data.target_x, Data.target_x * 2 - 20)
        #pen.write()
        #distance_to_target = Data.target_x - max_range
        text = f"your shot #{number} (speed: {Data.speed} angle: {Data.angle}) lands {abs(distance_to_target):.2f} m  too {'short' if ball.xcor() < goal.xcor() else 'wide'}"
        Data.history.append( text)
        if abs(distance_to_target) < Data.critical_distance_to_target:
            # print("you hit the target!")
            turtle.textinput(title="You won!",

                             prompt = "\n".join(Data.history) + f"\ncritical distance to target = {Data.critical_distance_to_target}\nCongratulations!!!\nYou won\npress enter to continue")
            #pen.write("you hit the target! (click to exit", align="center", font=('Arial', 12, 'normal'))
            #turtle.exitonclick()
            return

        #text_y = Data.target_x * 2
        #text_x = Data.target_x
        #for line_number, line in enumerate(Data.history, 1):
        #    pen.goto(text_x, text_y - line_number * 10)
        #    pen.write(line, align="center", font=('Arial', 12, 'normal'))
        #pen.penup()
        #pen.goto(Data.target_x, Data.target_x * 2 - 40)
        #pen.write("try again...", align="center", font=('Arial', 8, 'normal'))
        #print("try again....")
        number += 1

def quit():
    turtle.bye()


def display_parameters():
    """returns an array of text lines (without \n) containing the formatted parameters"""
    lines = []
    lines.append("parameters:")
    keys = [k for k in Data.__dict__.keys() if "__" not in k and k not in ("angle", "speed", "history")]
    max_length = max([len(key) for key in Data.__dict__.keys()])
    max_length2 = max([len(str(value)) for k, value in Data.__dict__.items() if k in keys])
    lines.append("-"*max_length + "--" + "-" * max_length2 +"-----")
    for key in keys:
        value = Data.__dict__[key]
        lines.append(f"{' ' * (max_length-len(key))}{key}: {value:>10.2f}")
    lines.append("-" * max_length + "--" + "-" * max_length2 +"-----")
    return lines

def make_grid():
    myscreen = turtle.getscreen()
    Data.__lower_left_x = min(-100, Data.cannon_x * 2, Data.target_x * 2)
    Data.__lower_left_y = min(-100, Data.cannon_y * 2, Data.target_y * 2)
    Data.__upper_right_x = max(100, Data.target_x * 2, Data.cannon_x * 2)
    Data.__upper_right_y = max(100, Data.cannon_y * 2, Data.target_y * 2)
    myscreen.setworldcoordinates(Data.__lower_left_x, Data.__lower_left_y, Data.__upper_right_x, Data.__upper_right_y)
    gridpen = turtle.Turtle()
    gridpen.speed(0)
    gridpen.penup()
    for y in range(Data.__lower_left_y, Data.__upper_right_y, (Data.__upper_right_y - Data.__lower_left_y) // 20 ):
        gridpen.goto(Data.__lower_left_x, y)
        gridpen.goto(gridpen.pos()[0] + 5, gridpen.pos()[1] + 1)
        gridpen.write(f"{y:>4}", align="right", font=("CourierNew", 8, "normal") )
        gridpen.goto(Data.__lower_left_x, y)
        gridpen.pendown()
        gridpen.goto(Data.__upper_right_x, y)
        gridpen.penup()
    for x in range(Data.__lower_left_x, Data.__upper_right_x, (Data.__upper_right_x - Data.__lower_left_x) // 20 ):
        gridpen.goto(x, Data.__lower_left_y)
        gridpen.goto(gridpen.pos()[0] + 5, gridpen.pos()[1] + 1)
        gridpen.write(f"{x:>4}", align="right", font=("CourierNew", 8, "normal") )
        gridpen.goto(x, Data.__lower_left_y)
        gridpen.pendown()
        gridpen.goto(x, Data.__upper_right_y)
        gridpen.penup()
    # thick zero axis
    gridpen.pensize(2)
    gridpen.goto(Data.__lower_left_x,0 )
    gridpen.pendown()
    gridpen.goto(Data.__upper_right_x, 0)
    gridpen.penup()
    gridpen.goto(0, Data.__lower_left_y)
    gridpen.pendown()
    gridpen.goto(0, Data.__upper_right_y)
    gridpen.hideturtle()




def game():
    print("*** Cannon game ***")
    myscreen = turtle.getscreen()
    myscreen.setup(width=.85, height=0.85, startx=None, starty=None)  # turtle window is 85% of screen width/height

    #myscreen.setworldcoordinates(min(0, Data.cannon_x), min(0, Data.cannon_y), max(Data.target_x * 2, 0), max(Data.target_x * 2, Data.target_y * 2, 0))

    #turtle.clearscreen()
    #write_menu()
    while True:
        turtle.clearscreen()
        make_grid()
        menupen = turtle.Turtle()
        menupen.pencolor("green")
        menupen.speed(0)
        menupen.penup()
        menupen.goto(Data.__lower_left_x + (Data.__upper_right_x - Data.__lower_left_x) //2,  Data.__upper_right_y - 10 )
        menupen.right(90)
        menupen.write("Cannon Game", align="center", font=('Arial', 20, 'bold'))
        #menupen.goto(Data.target_x, Data.target_x * 2 - 40)
        menupen.forward(20)
        menupen.write("change angle and speed of your cannon to hit the target", align="center",
                      font=('Arial', 15, 'bold'))
        menupen.forward(10)

        for line in display_parameters():
            menupen.forward(5)
            menupen.write(line, align="left", font=('CourierNew', 12, 'normal'))




        #print("please enter your command:")
        #command = input("[c]hange game parameters, [p]lay,  [q]uit  (enter=play)")
        command = turtle.textinput(title="Cannon Game Menu",
                                   prompt = "press:\nc ...  to change game parameters\np ...  to play\nq ... to quit\n\ntype your command please (and ENTER) >>>")
        if command.lower() == "p" or command == "":
            play()
        elif command.lower() == "c":
            ask_game_parameters()
            myscreen.setworldcoordinates(0, 0, Data.target_x * 2, Data.target_x * 2)

        elif command.lower() == "q":
            quit()
        #myscreen.onkey(play, "p")                     # function name  without parantheses!
        #myscreen.onkey(ask_game_parameters, "c")
        #myscreen.onkey(quit, "q")
        #myscreen.listen()  # set focus to turtlescreen and listen to keyboard events
        #if command.lower() not in ["c", "p", "q", "", "change", "quit", "play",]:
        #    continue
        #elif command.lower() in ["q", "quit"]:
        #    break
        #elif command.lower() in ["c", "change"]:
        #    data = ask_game_parameters()
        #    continue
        #elif command.lower() in ["p", "", "play"]:
        #    play(show_xy=True)
        #elif command.lower() in ["d", "details"]:
        #    play(show_xy=True)
        #else:
        #    print("i can not understand your command, please try again")

    print ("bye bye! Thanks for playing")


if __name__ == "__main__":
    game()





