"""Game of life, see https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
rules:
cells living in a 2d- array
Any live cell with two or three live neighbours survives.
Any dead cell with three live neighbours becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead.
"""
import PySimpleGUI as sg

class Config:
    """container for globals"""
    rows = 0
    cols = 0
    array = []
    wrap_around = True
    reborn_min = 3
    reborn_max = 3
    stay_alive_min = 2
    stay_alive_max = 3
    turn = 0

#b = [[False, False, False, False, False] for x in range(5)]
#board = [a,b]

def textviewer(array, truechar="x", falsechar="."):
    """print a 2x2 array in text mode"""
    for line in Config.array:
        for cell in line:
            print(truechar if cell else falsechar, end="")
        print()


def process():
    """calculates a new array based on conway's game of life rules on a given array"""
    new =  []
    for line in Config.array:
        newline = [False for element in line]
        new.append(newline)
    for y, line in enumerate(Config.array):
        for x, value in enumerate(line):
            counter = 0
            for (dx, dy) in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)):
                if Config.wrap_around:
                    if (y + dy) >= len(Config.array):
                        dy = -y
                    if (x + dx) >= len(Config.array[0]):
                        dx = -x
                    # <0 ..--> -1 --> is the last element in a python list
                else:
                    if (y+dy) < 0 or (y+dy) >= len(Config.array) or (x+dx) < 0 or (x+dx) >= len(Config.array[0]):
                        continue
                if Config.array[y+dy][x+dx]:
                    counter += 1
            # cell stay alive when 2 or 3 neighbors
            if  Config.array[y][x] and counter >= Config.stay_alive_min and counter <= Config.stay_alive_max:
                new[y][x] = True
            # dead cell becomes alive when exactly 3 neighbors
            elif not Config.array[y][x] and counter >= Config.reborn_min and counter <= Config.reborn_max:
                new[y][x] = True
    return new


#sg.theme('Dark Blue 3')  # please make your windows colorful

def create_layout():
    layout = []
    for y, line in enumerate(Config.array):
        guiline = [
            sg.Button(
                button_text="X" if cell else ".",
                key=str(y) + "_" + str(x),
                size=(1, 1),
                pad=(0, 0),
            )
            for x, cell in enumerate(line)
        ]

        layout.append(guiline)
    layout.append([sg.Button(button_text="next"), sg.Text("turn:"), sg.Text(str(Config.turn), key="turn", size=(5,0))])
    layout.append([sg.Text("reborn min:", size=(13,0)), sg.Input(str(Config.reborn_min), key="reborn_min", size=(2,0)),
                   sg.Text("reborn max:", size=(13,0)), sg.Input(str(Config.reborn_max), key="reborn_max", size=(2,0))])
    layout.append([sg.Text("stay alive min:",size=(13,0)), sg.Input(str(Config.stay_alive_min), key="stay_alive_min", size=(2,0)),
                   sg.Text("stay alive max:", size=(13,0)), sg.Input(str(Config.stay_alive_max), key="stay_alive_max", size=(2,0))])
    layout.append([sg.Checkbox(text = "wrap-around", default=True, key= "wrap_around"), sg.Button("reconfig")])
    return sg.Window('Window Title', layout)

def game(window):
    while True:  # Event Loop
        event, values = window.read()
        #print(event, values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        for y, line in enumerate(Config.array):
            for x, cell in enumerate(line):
                k = str(y)+"_"+str(x)
                if event == k:
                    Config.array[y][x] = not Config.array[y][x]
                    window[k].update("X" if Config.array[y][x] else ".")
        if event == "reconfig":
            Config.wrap_around = window["wrap_around"]
            
            Config.stay_alive_min = int(window["stay_alive_min"])
            Config.stay_alive_max = int(window["stay_alive_max"])
            Config.reborn_min = int(window["reborn_min"])
            Config.reborn_max = int(window["reborn_max"])
            print(Config.__dict__)
        if event == "next":
            print("processing...")
            Config.array = process() #
            Config.turn += 1
            window["turn"].update(str(Config.turn))
            # update gui
            for y, line in enumerate(Config.array):
                for x, cell in enumerate(line):
                    k = str(y) + "_" + str(x)
                    window[k].update("X" if Config.array[y][x] else ".")
        # text print
        textviewer(Config.array)

    window.close()

if __name__ == "__main__":
    while True:
        rows = sg.PopupGetText("how many rows?", default_text="20")
        cols = sg.PopupGetText("how many columns?", default_text ="20")
        try:
            rows = int(rows)
            cols = int(cols)
        except ValueError:
            sg.Popup("please enter olny ineger values > 0. Try again")
            continue
        if rows < 1 or cols < 1:
            sg.Popup("rows and cols must be integer > 0")
            continue
        break
    Config.cols = cols
    Config.rows = rows
    Config.array = [[False for x in range(cols)] for y in range(rows)]
    print(Config.array)
    window = create_layout()
    game(window)




