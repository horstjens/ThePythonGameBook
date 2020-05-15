"""tic tac toe for 2 players, supporting command line parameters
   Each player can be ether human or  easy/medium/hard AI
   call this program with 2 parameters: player1 player2"""
from typing import List, Tuple, Union, Optional
import random
import sys


def check_win(char: str, cells: List[List[str]]) -> bool:
    """checks the array cells and returns True if 3 chars build a line"""
    for row in range(3):  # checking rows
        if cells[row][0:3] == [char, char, char]:  # horizontal slice, see code discussion
            return True
    for col in range(3):  # checking columns
        if [element[col] for element in cells] == [char, char, char]:
            return True  # vertical slice
    # checking diagonal
    if cells[0][0] == char and cells[1][1] == char and cells[2][2] == char:
        return True
    if cells[2][0] == char and cells[1][1] == char and cells[0][2] == char:
        return True
    return False  # all win condition checked without success, therefore no win


def display(cells: List[List[str]]) -> None:
    """displays the 3x3 array 'cells' with heading row and column
       human-friendly display: Rows are numbered 1-3, columns are numbered A-C"""
    print("\n" + r"r\c A:  B:  C:")  # empty line and header.
    for index, row in enumerate(cells):  # index starts with 0
        print("{}: ".format(index + 1), end="")  # no new line at end of print
        for element in row:  # index starts with 0
            print("[{}] ".format(element), end="")  # no new line at end of print
        print()  # print only a new line
    print()  # empty line after board


def input_checker(user_input: str, cells: List[List[str]]) -> \
        Tuple[Union[str, bool], Optional[int], Optional[int]]:
    """Testing if user_input is a valid and free coordinate
       in a 3x3 matrix (rows:1-3,columns: ABC)
       returns Error Message (of False) and x and y
       user_input must be already converted by user_input.strip().upper()   """
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
        # input("enter...")
        return "This cell is already occupied. Try again", None, None
    return False, column, row


def choose_a_free_cell(cells: List[List[str]], my_char: str ,
                       ai: str , silent: bool = False) -> str:
    """chooses a random free cell"""
    other_char = "o" if my_char == "x" else "x"
    free_cells: List[Tuple[int, int]] = []  # calculate free cells from cell
    for y, row in enumerate(cells):
        for x, _ in enumerate(row):
            if cells[y][x] == " ":
                free_cells.append((y, x))
    # free cells are now as list of tuples (row, column) in result
    if ai == "easy":  # choose any free cell
        mycell = random.choice(free_cells)
    else:  # check for winning and blocking move
        hint = find_winning_move(my_char, cells)  # winning move?
        if not silent:
            print("winning:", hint)
        if hint is not None:
            mycell = (hint[0], hint[1])
        else:  # blocking move?
            hint = find_winning_move(other_char, cells)
            if not silent:
                print("blocking:", hint)
            if hint is not None:
                mycell = (hint[0], hint[1])
            elif ai == "medium":
                mycell = random.choice(free_cells)
            elif ai == "hard":
                mycell = (1, 1) if (1, 1) in free_cells else random.choice(free_cells)
            # write code for perfect AI here
    return make_human_coordinates(mycell[0], mycell[1])


def make_human_coordinates(row: int, column: int) -> str:
    """returns a human-readable string, cloumns ABC, rows 123"""
    return "ABC"[column] + "," + str(row + 1)


def find_winning_move(mychar: str, cells: List[List[str]]) -> Optional[Tuple[int, int]]:
    """analyses cells, returns winning move for mychar if found, otherwise None"""
    for y, row in enumerate(cells):
        for x, char in enumerate(row):
            if char != " ":  # skip if cell is not free
                continue
            # ------------ test for near win situations ------------
            if y == 0 and x == 0:  # topleft
                if any([(cells[1][1] == mychar and cells[2][2] == mychar),
                        (cells[0][1] == mychar and cells[0][2] == mychar),
                        (cells[1][0] == mychar and cells[2][0] == mychar)]):
                    return (y, x)
            elif y == 0 and x == 2:  # topright
                if any([(cells[1][1] == mychar and cells[2][0] == mychar),
                        (cells[0][0] == mychar and cells[0][1] == mychar),
                        (cells[1][2] == mychar and cells[2][2] == mychar)]):
                    return (y, x)
            elif y == 2 and x == 0:  # bottomleft
                if any([(cells[1][1] == mychar and cells[0][2] == mychar),
                        (cells[0][0] == mychar and cells[1][0] == mychar),
                        (cells[2][1] == mychar and cells[2][2] == mychar)]):
                    return (y, x)
            elif y == 2 and x == 2:  # bottomright
                if any([(cells[1][1] == mychar and cells[0][0] == mychar),
                        (cells[0][2] == mychar and cells[1][2] == mychar),
                        (cells[2][0] == mychar and cells[2][1] == mychar)]):
                    return (y, x)
            elif y == 0 and x == 1:  # midtop
                if any([(cells[0][0] == mychar and cells[0][2] == mychar),
                        (cells[1][1] == mychar and cells[2][1] == mychar)]):
                    return (y, x)
            elif y == 1 and x == 2:  # midright
                if any([(cells[1][0] == mychar and cells[1][1] == mychar),
                        (cells[0][2] == mychar and cells[2][2] == mychar)]):
                    return (y, x)
            elif y == 2 and x == 1:  # midbottom
                if any([(cells[1][1] == mychar and cells[0][1] == mychar),
                        (cells[2][0] == mychar and cells[2][2] == mychar)]):
                    return (y, x)
            elif y == 1 and x == 0:  # midleft
                if any([(cells[1][1] == mychar and cells[1][2] == mychar),
                        (cells[0][0] == mychar and cells[2][0] == mychar)]):
                    return (y, x)
            else:  # if y == 1 and x == 1:  # middle
                if any([(cells[0][0] == mychar and cells[2][2] == mychar),
                        (cells[2][0] == mychar and cells[0][2] == mychar),
                        (cells[1][0] == mychar and cells[1][2] == mychar),
                        (cells[0][1] == mychar and cells[2][1] == mychar)]):
                    return (y, x)
        # ---- end of for x loop -----
    # ---- end of for y  loop -----
    return None  # ---- no winning move found


# ---- the 'main' function of the game -----
def game(player1: str, player2: str, silent: bool = False) -> int:
    """plays tictactoe, returns 3 for draw or number of winning player (1 or 2)"""
    # ---guardian code ----
    if not isinstance(silent, bool):
        raise SystemError("parameter silent must be True or False")
    players = [player1, player2]
    for p in players:
        if p not in ("human", "easy", "medium", "hard"):
            raise SystemError("player1, player2 must be: " +
                              "'human', 'easy', 'medium','hard'")
    # ---- end of guardian code ---
    cells: List[List[str]] = [[" " for x in range(3)] for y in range(3)]
    SYMBOLS: Tuple[str, str] = ("x", "o")  # ----- some constants, see code discussion
    GREETING: str = "This is turn {}. Player{}, where do you put your '{}'?: >>> "
    TEXT: str = "If asked for coordinates, please enter: column, row\n" \
                "  like for example: 'A 1' or 'b,2' or 'C3' and press ENTER"
    if not silent and player1 == "human":
        print(TEXT)
        display(cells)
    for turns in range(9):  # play 9 legal moves, then the board is full
        playerindex = turns % 2  # modulo: the remainder of a division by 2.
        player_char = SYMBOLS[playerindex]
        suffix = "AI" if players[playerindex] != "human" else ""
        while True:  # ask until input is acceptable
            if players[playerindex] == "human":  # human player
                prompt = GREETING.format(turns + 1, playerindex + 1, player_char)
                command = input(prompt).strip().upper()
                if command in ("QUIT", "EXIT", "CANCEL", "Q", "BYE"):
                    print("bye-bye")
                    return 0  #
                if command in ("?", "HELP"):
                    print(TEXT)
                    continue
            else:
                command = choose_a_free_cell(cells, player_char, players[playerindex], silent)
            if not silent:
                print("player{} ({}{}) plays: {}".format(playerindex + 1,
                                                         players[playerindex],
                                                         suffix, command))
            error, column, row = input_checker(command, cells)
            if error:  # errormessage is a string or False
                if not silent:
                    print(error)
                continue  # ask again
            # ----- input accepted, update the game board ------
            cells[row][column] = player_char
            break  # escape the while loop
        # -- end of while loop. got acceptable input ---
        if not silent:
            display(cells)
        if check_win(player_char, cells):  # only the active player is checked
            if not silent:
                print("Congratulation, player {} ({}{}) has won!".format(
                    playerindex + 1, players[playerindex], suffix))
            return playerindex + 1
        # ---- proceed with the next turn -----
    #else:  # ----- for loop has run 9 times without a break  ---
    if not silent:
        print("All nine fields are occupied. It's a draw. No winner")
    return 3  # draw


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 1:
        first_player = "human"
        second_player = "easy"
    elif len(sys.argv) == 2:
        first_player = sys.argv[1]
        second_player = "human"
    else:
        first_player = sys.argv[1]
        second_player = sys.argv[2]

    game(first_player, second_player)
