# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion
# https://de.wikipedia.org/wiki/Wurfparabel#/media/Datei:Wurfparabel_Zusammenfassung_aktualisierung.png
# this variant is text-only, but includes angle and a class instead a dict for data
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress


import math

class Data:
    """store global variables here"""
    speed = 100
    angle = 20
    x0 = 0     # x-position of cannon
    y0 = 0     # y-position of cannon
    critical_distance_to_target =  1 # how close to the target a cannonball must land to count as a hit
    dt =  0.01   # delta time, a smaller number makes a slower, but more precise calculation of the flight path
    gravity =  -9.81
    target_x =  100 # x-postion of the target , y-position of target is always 0


def ask_speed_and_angle():
    speed_default = Data.speed # data["speed"]
    try:
        new_speed = float(input(f"inital speed in [m/s] (enter={speed_default})"))
    except ValueError:
        new_speed = speed_default
    print("speed is set to", new_speed)
    Data.speed = new_speed #data["speed"] = new_speed

    angle_default = Data.angle # data["angle"]
    try:
        new_angle = float(input(f"angle in degree (enter={angle_default})"))
    except ValueError:
        new_angle = angle_default
    print("angle is set to", new_angle)
    Data.angle = new_angle #data["angle"] = new_angle
    #return data

def display_parameters():
    print("parameters:")
    keys = [k for k in Data.__dict__.keys() if "__" not in k and k not in ("angle", "speed", "history")]
    max_length = max([len(key) for key in Data.__dict__.keys()])
    max_length2 = max([len(str(value)) for k, value in Data.__dict__.items() if k in keys])
    print("-"*max_length + "--" + "-" * max_length2+"-----")
    for key in keys:
        value = Data.__dict__[key]
        print(f"{' ' * (max_length-len(key))}{key}: {value:>10.2f}")
    print("-" * max_length + "--" + "-" * max_length2+"-----")

def ask_game_parameters():
    """ask for every parameter except angle and speed and history
       change this value depending on user input"""
    keys = [k for k in Data.__dict__.keys() if "__" not in k and k not in ("angle", "speed", "history")]
    for key in keys:
        value = Data.__dict__[key]
        #print(f"the current value for {key} is {value}")
        try:
            new_value = float(input(f"enter new value for {key}: (enter=accept {value})"))
        except ValueError:
            new_value = value
        if new_value != value:
            #data[key] = new_value
            ## Data.__setattr__(key, value) # wrong!
            setattr(Data, key, new_value)       # right!
            print(f"{key} changed to: {new_value}")
    #return data
    print("crit dist:", Data.critical_distance_to_target)
    display_parameters()
            

def play( show_xy=False):
    print(f'the target is at x position {Data.target_x} and at y position 0')
    print(f'the cannon is at x position {Data.x0} and at y position {Data.y0}')
    print("change angle and speed to hit the target as close as possible. (or enter 0 for both values to quit)")
    number = 1
    while True:
        print(f"shot number {number}")
        ask_speed_and_angle() # ask for speed and angle
        if Data.speed == 0 and Data.angle == 0:
            print("aborting game")
            return
        vx0 = math.cos(math.radians(Data.angle)) * Data.speed
        vy0 = math.sin(math.radians(Data.angle)) * Data.speed
        t = 0
        y = 0
        if show_xy:
            while y >= 0:
                t += Data.dt  # next time step
                x = Data.x0 + vx0 * t  # constant horizontal speed
                y = Data.y0 + vy0 * t + 0.5 * Data.gravity * t * t

                print(f"time: {t:.3f}, x:{x:.3f} y:{y:.3f} ")

        max_range = abs(
            (Data.speed ** 2 / Data.gravity) *
             math.cos(math.radians(Data.angle)) *
            (math.sin(math.radians(Data.angle)) + (math.sin(math.radians(Data.angle)) ** 2 +
            (2 * Data.y0 * Data.gravity / Data.speed ** 2)) ** 0.5)
        )
        print(f"your shot #{number} lands at x-position {max_range}")
        distance_to_target = Data.target_x - max_range
        if abs(distance_to_target) < Data.critical_distance_to_target:
            print("you hit the target!")
            return
        elif max_range < Data.target_x:
            print(f"Too short! Your shot lands {abs(distance_to_target)} m before the target ")
        else:
            print(f"Too wide! Your shots lands {abs(distance_to_target)} m behind the target")
        print("try again....")
        number += 1

def game():
    print("*** Cannon game ***")
    display_parameters()

    while True:
        print("please enter your command:")
        command = input("[c]hange game parameters, [p]lay, play with [d]etails,  [q]uit  (enter=play)")
        if command.lower() not in ["c", "p", "q", "d",  "", "change", "quit", "play", "details"]:
            continue
        elif command.lower() in ["q", "quit"]:
            break
        elif command.lower() in ["c", "change"]:
            data = ask_game_parameters()
            continue
        elif command.lower() in ["p", "", "play"]:
            play()
        elif command.lower() in ["d", "details"]:
            play(show_xy=True)
        else:
            print("i can not understand your command, please try again")

    print ("bye bye! Thanks for playing")


if __name__ == "__main__":
    game()





