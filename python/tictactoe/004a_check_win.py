"""tic tac toe for 2 players, wit win checking"""
# ---- functions ----
def check_win(char):
    """checks the array cells and returns True if 3 chars build a line"""
    # rows
    for row in range(3): # range(3) returns 0, 1, 2
        if cells[row][0] == char and cells[row][1] == char and cells[row][2] == char:
            return True
    # columns
    for col in range(3):
        if cells[0][col] == char and cells[1][col] == char and cells[2][col] == char:
            return True
    # diagonal
    if cells[0][0] == char and cells[1][1] == char and cells[2][2] == char:
        return True
    if cells[2][0] == char and cells[1][1] == char and cells[0][2] == char:
        return True
    # no win
    return False

def is_free(row, column):
    """checks a single coordinate in the the cells array returns True if the cell is free (contains a Space)
    otherwise returns False"""
    try:
        content = cells[row][column]
    except IndexError:
        print("this cell does not exist")
        return False
    return True if content == " " else False

def display():
    """displays the 3x3 array 'cells' with heading row and column"""
    print("r\c 0:  1:  2:")
    for index, row in enumerate(cells):
        print("{}: ".format(index), end="")
        for element in row:
            print("[{}] ".format(element), end="")
        print() # force new line
# ---- variables at module level ----
cells = [[" " for x in range(3)] for y in range(3)]
symbols = ["x", "o"]
greeting = "This is turn {}. Player {}, where do you put your {}?"
text = "Please enter coordinate (0 or 1 or 2) for column and row like for example: 1 2 and press ENTER >>>"
for turns in range(9): # play 9 legal moves, then the board is full
    display()
    player = turns % 2 # modulo: the remainder of a division by 2.
    player_char = symbols[player]
    print(greeting.format(player, turns, player_char))
    while True:  # ask until legal move
        command=input(text)
        command = command.strip()
        try:
            raw_column, raw_row = command[0], command[-1] # 2 variables, 2 values
        except:
            print("Enter 2 coordinates. Try again")
            continue  # go back to the start of the while loop
        try:
            row = int(raw_row)
            column = int(raw_column)
        except ValueError:
            print("Enter numbers only. Try again")
            continue # go back to the start of the while loop
        if is_free(row, column):
            print("input accepted")
            cells[int(raw_row)][int(raw_column)] = player_char
            break
    if check_win(player_char): # only the active player is checked
        print(" -*- -*- -*- Congratulation, You have won, player {} -*- -*- -*-".format(player))
        display() # final 
        break
    print("*** next turn! *****")
print("Game Over")
