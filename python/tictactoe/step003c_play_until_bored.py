"""tic tac toe for 2 players, without win checking"""

# ----- defnine some top-level variables ------
cells = [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "],
         ]
# ore more elegant:
# cells = [[" " for x in range(3)] for y in range(3)]
symbols = ("x", "o")    # tuples are read-only
greeting = "This is turn {}. Player {}, where do you put your '{}'?"
text = "Please enter numbers (0 or 1 or 2) for column and row\n"
text += "   like for example: '1 2' or '02' or '2x1'\n"
text += "   and press ENTER >>> "


# ---- functions ----
def is_free(row, column):
    """checks a single coordinate in the the cells array
    returns True if the cell is free (contains a Space)
    otherwise returns False"""
    try:
        content = cells[row][column]
    except IndexError:
        print("this cell does not exist")
        return False
    return True if content == " " else False


def display():
    """displays the 3x3 array 'cells' with heading row and column"""
    print(r"r\c 0:  1:  2:")  # header line. r\c is not an escape sequence, leading r -> raw string
    for index, row in enumerate(cells):
        print("{}: ".format(index), end="")  # no new line at end of print
        for element in row:
            print("[{}] ".format(element), end="")  # no new line at end of print
        print()  # print only a new line
    print()  # empty line after board


for turns in range(9):  # play 9 legal moves, then the board is full
    display()
    player = turns % 2  # modulo: the remainder of a division by 2.
    print(greeting.format(turns, player, symbols[player]))
    while True:  # ask until legal move
        command = input(text)
        command = command.strip()
        if len(command) < 2:
            print("Enter 2 coordinates. Try again!")
            continue
        raw_column, raw_row = command[0], command[-1]  # 2 variables, 2 values
        try:
            row, column = int(raw_row), int(raw_column)  # 2 variables, 2 values and only one line inside try: block
        except ValueError:
            print("Enter numbers only. Try again")
            continue  # go back to the start of the while loop
        if is_free(row, column):
            print("input accepted\n")  # extra new line
            cells[row][column] = symbols[player]
            break  # breaks out of this while loop
    # print("*** next turn! *****")
print("all fields are full. Game Over")