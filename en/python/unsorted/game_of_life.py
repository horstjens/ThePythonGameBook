"""Game of life, see https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
rules:
cells living in a 2d- array
Any live cell with two or three live neighbours survives.
Any dead cell with three live neighbours becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead.
"""
a = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ]
#b = [[False, False, False, False, False] for x in range(5)]
#board = [a,b]

def viewer(array, truechar="x", falsechar="."):
    """print a 2x2 array in text mode"""
    for line in array:
        for cell in line:
            print(truechar if cell else falsechar, end="")
        print()


def process(array, wrap_around = True, reborn_min = 3, reborn_max = 3,
            stay_alive_min = 2, stay_alive_max=3):
    """calculates a new array based on conway's game of life rules on a given array"""
    new =  []
    for line in array:
        newline = [False for element in line]
        new.append(newline)
    for y, line in enumerate(array):
        for x, value in enumerate(line):
            counter = 0
            for (dx, dy) in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)):
                if wrap_around:
                    if (y + dy) >= len(array):
                        dy = -y
                    if (x + dx) >= len(array[0]):
                        dx = -x
                    # <0 ..--> -1 --> is the last element in a python list
                else:
                    if (y+dy) < 0 or (y+dy) >= len(array) or (x+dx) < 0 or (x+dx) >= len(array[0]):
                        continue
                if array[y+dy][x+dx]:
                    counter += 1
            # cell stay alive when 2 or 3 neighbors
            if  array[y][x] and counter >= stay_alive_min and counter <= stay_alive_max:
                new[y][x] = True
            # dead cell becomes alive when exactly 3 neighbors
            elif not array[y][x] and counter >= reborn_min and counter <= reborn_max:
                new[y][x] = True
    return new

def game(board):
    """plays conways game of life on array a"""
    while True:
        viewer(board)
        command = input("enter drücken")
        if command == "quit":
            break
        board = process(board)


if __name__ == "__main__":
    game(a)




