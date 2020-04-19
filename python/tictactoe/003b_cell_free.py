cells = [ ["x", "x", " "],
          [" ", "x", "o"],
          ["o", " ", "o"],
         ]

def is_free(row, column):
    """checks a single coordinate in the the cells array
    returns True if the cell is free (contains a Space)
    otherwise returns False"""
    try:
        content = cells[row][column]
    except IndexError:
        return "this cell does not exist"
    except:
        return "not even a legal index"
    # slow but readable
    if content == " ":
        return True
    return False
    # faster but harder to read:
    #return True if content == " " else False

# testing:
print("0,0:",is_free(0,0))
print("2,1:",is_free(2,1))
print("5,6:",is_free(5,6))
print("x,0:",is_free("x",0))
