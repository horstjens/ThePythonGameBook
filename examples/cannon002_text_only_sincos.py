# cannon shooting example

# see https://en.wikipedia.org/wiki/Projectile_motion
# https://de.wikipedia.org/wiki/Wurfparabel#/media/Datei:Wurfparabel_Zusammenfassung_aktualisierung.png
# this variant is text-only, but includes angle
# inspired by "Physics for Game Prgrammers, by Grant Palmer, Apress


import math

def ask_speed_and_angle(data):
    speed_default = data["speed"]
    try:
        new_speed = float(input(f"inital speed in [m/s] (enter={speed_default})"))
    except ValueError:
        new_speed = speed_default
    print("speed is set to", new_speed)
    data["speed"] = new_speed

    angle_default = data["angle"]
    try:
        new_angle = float(input(f"angle in degree (enter={angle_default})"))
    except ValueError:
        new_angle = angle_default
    print("angle is set to", new_angle)
    data["angle"] = new_angle
    return data

def ask_game_parameters(data):
    """ask for every parameter except angle and speed"""
    for key, value in data.items():
        if key in ["angle", "speed"]:
            continue # skip those
        print(f"the current value for {key} is {value}")
        try:
            new_value = float(input(f"enter new value for {key}: (enter=accept {value})"))
        except ValueError:
            new_value = value
        if new_value != value:
            data[key] = new_value
            print(f"{key} changed to: {new_value}")
    return data
            

def play(data, show_xy=False):
    print(f'the target is at x position {data["target_x"]} and at y position 0')
    print(f'the cannon is at x position {data["x0"]} and at y position {data["y0"]}')
    print("change angle and speed to hit the target as close as possible. (or enter 0 for both values to quit)")
    number = 1
    while True:
        print(f"shot number {number}")
        data = ask_speed_and_angle(data) # ask for speed and angle
        if data["speed"] == 0 and data["angle"] == 0:
            print("aborting game")
            return
        vx0 = math.cos(math.radians(data["angle"])) * data["speed"]
        vy0 = math.sin(math.radians(data["angle"])) * data["speed"]
        t = 0
        y = 0
        if show_xy:
            while y >= 0:
                t += data["dt"]  # next time step
                x = data["x0"] + vx0 * t  # constant horizontal speed
                y = data["y0"] + vy0 * t + 0.5 * data["gravity"] * t * t

                print(f"time: {t:.3f}, x:{x:.3f} y:{y:.3f} ")

        max_range = abs(
            (data["speed"] ** 2 / data["gravity"]) *
             math.cos(math.radians(data["angle"])) *
            (math.sin(math.radians(data["angle"])) + (math.sin(math.radians(data["angle"])) ** 2 +
            (2 * data["y0"] * data["gravity"] / data["speed"] ** 2)) ** 0.5)
        )
        print(f"your shot #{number} lands at x-position {max_range}")
        distance_to_target = data["target_x"] - max_range
        if abs(distance_to_target) < data["critical_distance_to_target"]:
            print("you hit the target!")
            return
        elif max_range < data["target_x"]:
            print(f"Too short! Your shot lands {abs(distance_to_target)} m before the target ")
        else:
            print(f"Too wide! Your shots lands {abs(distance_to_target)} m behind the target")
        print("try again....")
        number += 1

def game():
    print("*** Cannon game ***")
    data = {"speed": 100,
            "angle": 20,
            "x0": 0,
            "y0": 0,
            "critical_distance_to_target": 1,
            "dt": 0.01,
            "gravity": -9.81,
            "target_x": 100,
            }

    while True:

        print("please enter your command:")
        command = input("[c]hange game parameters, [p]lay, play with [d]etails,  [q]uit  (enter=play)")
        if command.lower() not in ["c", "p", "q", "d",  "", "change", "quit", "play", "details"]:
            continue
        elif command.lower() in ["q", "quit"]:
            break
        elif command.lower() in ["c", "change"]:
            data = ask_game_parameters(data)
            continue
        elif command.lower() in ["p", "", "play"]:
            play(data)
        elif command.lower() in ["d", "details"]:
            play(data, show_xy=True)
        else:
            print("i can not understand your command, please try again")

    print ("bye bye! Thanks for playing")


if __name__ == "__main__":
    game()





