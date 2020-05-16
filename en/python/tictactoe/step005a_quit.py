"""tic tac toe for 2 players, extra comfortable for humans """
cells = [[" " for x in range(3)] for y in range(3)]  # create a 3 x 3 array
SYMBOLS = ["x", "o"]  # ----- some constants, see code discussion
GREETING = "This is turn {}. Player {}, where do you put your '{}'?: >>> "
TEXT = "If asked for coordinates, please enter: column, row\n" \
       "  like for example: 'A 1' or 'b,2' or 'C3' and press ENTER"


def check_win(char):
    """checks the array cells and returns True if 3 chars build a line"""
    for row in range(3):  # checking rows
        # if cells[row][0] == char and cells[row][1] == char and cells [row][2] == char:
        if cells[row][0:3] == [char, char, char]:  # horizontal slice, see code discussion
            return True
    for col in range(3):  # checking columns
        # if cells[0][col] == char and cells[1][col] == char and cells[2][col] == char:
        if [element[col] for element in cells] == [char, char, char]:  # vertical slice
            return True
    # checking diagonal
    if cells[0][0] == char and cells[1][1] == char and cells[2][2] == char:
        return True
    if cells[2][0] == char and cells[1][1] == char and cells[0][2] == char:
        return True
    return False  # all win condition checked without success, therefore no win


def display():
    """displays the 3x3 array 'cells' with heading row and column
       human-friendly display: Rows are numbered 1-3, columns are numbered A-C"""
    print("\n" + r"r\c A:  B:  C:")  # empty line and header.
    for index, row in enumerate(cells):  # index starts with 0
        print("{}: ".format(index + 1), end="")  # no new line at end of print
        for element in row:  # index starts with 0
            print("[{}] ".format(element), end="")  # no new line at end of print
        print()  # print only a new line
    print()  # empty line after board


def input_checker(user_input):
    """Testing if user_input is a valid and free coordinate
       in a 3x3 matrix (rows:1-3,columns: ABC)
       returns Error Message as string and None, None (for x and y)
       otherwise returns False and x, y as integer values
       user_input must be alreay converted by user_input.strip().upper()   """
    if len(user_input) < 2:
        return "Enter 2 coordinates. Try again!", None, None
    raw_column = user_input[0]
    raw_row = user_input[-1]
    if raw_row in ("A", "B", "C") and raw_column in ("1", "2", "3"):
        raw_column, raw_row = raw_row, raw_column  # swap row with column
    if raw_column not in ("A", "B", "C"):
        return "Enter A or B or C for column. Try again", None, None
    if raw_row not in ("1", "2", "3"):
        return "Enter 1 or 2 or 3 for row. Try again", None, None
    column = ord(raw_column) - 65  # 'A'=chr(65), 'B'=chr(66) 'C'=chr(67)
    row = int(raw_row) - 1
    # ---- checking if the coordinate is still free ----
    if cells[row][column] != " ":
        return "This cell is already occupied. Try again", None, None
    return False, column, row


# ---- the 'main' function of the game -----
def game():
    print(TEXT)
    display()
    for turns in range(9):  # play 9 legal moves, then the board is full
        player = turns % 2  # modulo: the remainder of a division by 2.
        player_char = SYMBOLS[player]
        while True:  # ask until input is acceptable
            prompt = GREETING.format(turns + 1, player + 1, player_char)
            command = input(prompt).strip().upper()
            if command in ("QUIT", "EXIT", "CANCEL", "Q", "BYE"):
                return  # -> bye bye
            error, column, row = input_checker(command)
            if error:  # errormessage is a string or False
                print(error)
                continue  # ask again
            # ----- input accepted, update the game board ------
            cells[row][column] = player_char
            break  # escape the while loop
        # -- end of while loop. got acceptable input ---
        display()
        if check_win(player_char):  # only the active player is checked
            print("Congratulation, player {} has won!".format(player + 1))
            break
        # ---- proceed with the next turn -----
    else:  # ----- for loop has run 9 times without a break  ---
        print("All nine fields are occupied. It's a draw. No winner")
    print("Game Over")


if __name__ == "__main__":
    game()
    print("bye bye")