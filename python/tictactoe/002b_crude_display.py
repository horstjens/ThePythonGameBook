cells = [ ["x", "x", " "],
          [" ", "x", "o"],
          ["o", " ", "o"],
         ]
board="""
r\c 0:  1:  2:
0: [{}] [{}] [{}]
1: [{}] [{}] [{}]
2: [{}] [{}] [{}]"""
print(board.format(cells[0][0], cells[0][1], cells[0][2],
                   cells[1][0], cells[1][1], cells[1][2],
                   cells[2][0], cells[2][1], cells[2][2] ))
