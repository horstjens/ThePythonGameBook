cells = [ ["x", "x", " "],
          [" ", "x", "o"],
          ["o", " ", "o"],
         ]
board="""
r\c 0:  1:  2:
0: [{}] [{}] [{}]
1: [{}] [{}] [{}]
2: [{}] [{}] [{}]"""
# convert the list of list (cells) into a one-dimensional array
flat_cells = []
for row in cells:
    for element in row:
        flat_cells.append(element)
print(flat_cells)
# or, in a neat one-liner:
flat_cells2 = [item for row in cells for item in row]
print(flat_cells2)
# pass the flat_cells array as argument list
print(board.format(*flat_cells))
