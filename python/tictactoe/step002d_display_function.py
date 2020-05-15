cells = [ ["x", "x", " "],
          [" ", "x", "o"],
          ["o", " ", "o"],
         ]
# define the function
def display():
    """displays the 3x3 array 'cells'
       with heading row and column"""
    print("r\c 0:  1:  2:")
    for index, row in enumerate(cells):
        print("{}: ".format(index), end="")
        for element in row:
            print("[{}] ".format(element), end="")
        print() # force new line
#call the function
display()
