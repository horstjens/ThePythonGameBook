from typing import List, Tuple, Union, Optional

def display() -> None:
    """displays the 3x3 array 'cells' with heading row and column
       human-friendly display: Rows are numbered 1-3, columns are numbered A-C"""
    print("\n" + r"r\c A:  B:  C:")  # empty line and header.
    for index, row in enumerate(cells):  # index starts with 0
        print("{}: ".format(index + 1), end="")  # no new line at end of print
        for element in row:  # index starts with 0
            print("[{}] ".format(element), end="")  # no new line at end of print
        print()  # print only a new line
    print()  # empty line after board



def make_human_coordinates(row: int, column: int) -> str:
    """returns a human-readable string, cloumns ABC, rows 123"""
    return "ABC"[column]+","+str(row+1)


def find_winning_move(mychar: str) -> Optional[str]:
    """analyses cells, returns winning move for mychar if found, otherwise None"""
    for y, row in enumerate(cells):
        for x, char in enumerate(row):
            # test for near win situation

            if y == 0 and x == 0: # topleft
                if any([( cells[1][1] == mychar and cells[2][2] == mychar ),
                        ( cells[0][1] == mychar and cells[0][2] == mychar ),
                        ( cells[1][0] == mychar and cells[2][0] == mychar )]):
                    return make_human_coordinates(y, x)
            if y == 0 and x == 2: # topright
                if any([( cells[1][1] == mychar and cells[2][0] == mychar ),
                        ( cells[0][0] == mychar and cells[0][1] == mychar ),
                        ( cells[1][2] == mychar and cells[2][2] == mychar )]):
                    return make_human_coordinates(y, x)
            if y == 2 and x == 0: # bottomleft
                if any([( cells[1][1] == mychar and cells[0][2] == mychar ),
                        ( cells[0][0] == mychar and cells[1][0] == mychar ),
                        ( cells[2][1] == mychar and cells[2][2] == mychar )]):
                    return make_human_coordinates(y, x)
            if y == 2 and x == 2:  # bottomright
                if any([(cells[1][1] == mychar and cells[0][0] == mychar),
                        (cells[0][2] == mychar and cells[1][2] == mychar),
                        (cells[2][0] == mychar and cells[2][1] == mychar)]):
                    return make_human_coordinates(y, x)
            if y == 0 and x == 1: # midtop
                if any([(cells[0][0] == mychar and cells[0][2] == mychar),
                        (cells[1][1] == mychar and cells[2][1] == mychar)]):
                    return make_human_coordinates(y, x)
            if y == 1 and x == 2:  # midright
                if any([(cells[1][0] == mychar and cells[1][1] == mychar),
                        (cells[0][2] == mychar and cells[2][2] == mychar)]):
                    return make_human_coordinates(y, x)
            if y == 2 and x == 1:  # midbottom
                if any([(cells[1][1] == mychar and cells[0][1] == mychar),
                        (cells[2][0] == mychar and cells[2][2] == mychar)]):
                    return make_human_coordinates(y, x)
            if y == 1 and x == 0:  # midleft
                if any([(cells[1][1] == mychar and cells[1][2] == mychar),
                        (cells[0][0] == mychar and cells[2][0] == mychar)]):
                    return make_human_coordinates(y, x)
            if y == 1 and x == 1:  # middle
                if any([(cells[0][0] == mychar and cells[2][2] == mychar),
                        (cells[2][0] == mychar and cells[0][2] == mychar),
                        (cells[1][0] == mychar and cells[1][2] == mychar),
                        (cells[0][1] == mychar and cells[2][1] == mychar)]):
                    return make_human_coordinates(y, x)
        # ---- end of x loop ---
    # ---- end of y loop ----
    return None # ---- no winning move found



#cells: List[List[str]] = [[" " for x in range(3)] for y in range(3)]  # create a 3 x 3 array of strings
cells = [ ["x", "x", " "],
          [" ", " ", " "],
          [" ", " ", " "]]
display()
print(find_winning_move("x"))