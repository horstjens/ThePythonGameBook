

def local_manipulator():
    print("local manipulator at work")
    cells = [1, 2, 3, 4]
    cells.append(66)

    cells.append(999)
    print("local manipulated cells", cells)

def manipulator2():
    game_cells.append(88)
    
def manipulator3(cells):
    cells.append(99)

cells = [1,2,3,4]
print("toplevel cells", cells)
local_manipulator()
print("toplevel cells after local_manipulator", cells)

def game():
    game_cells = [55,66,77]
    print("game_cells:", game_cells)
    #manipulator2()
    #print("game_cells:", game_cells) 
    #would not work because game_cells is not defined in manipulator2
    manipulator3(game_cells)
    print("game_cells:", game_cells)
    
    
game()
    
