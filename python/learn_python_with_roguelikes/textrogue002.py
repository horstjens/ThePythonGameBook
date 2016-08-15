# statues that work like traps, no functions
# legend: #=rock  .=floor  f=food  $=gold
DUNGEON = '''
###############################################
#.....fff.#..............#f#.$#.....#.......#$#
#....S....#..............###....###.#.....#.#.#
#....S.S..f.....$...f.........##$......f..#...#
###############################################
'''  # add more lines to the dungeon!
PLAYER = '@'
PROMPT = 'Type your command or ? and press Enter:'
HELPTEXT = 'movement: w,a,s,d\neat: e\nquit: exit or quit or q' 

message = 'welcome {}, move with w,a,s,d'.format(PLAYER)
player_x, player_y = 1, 1
lines = DUNGEON.split()
hunger, treasure, food = 0, 0, 7
player_hitpoints = 25
while hunger < 100 and player_hitpoints > 0:
    # ------ Print dungeon -------
    for y, line in enumerate(lines):
        # y is the line number starting with 0      
        if y == player_y:
            print(line[:player_x] + PLAYER + line[player_x+1:])
        else:
            print(line)
    # ------ Command processing ---------
    status = 'hitpoints: {} hunger:{} food:{} gold:{}\n'.format(
              player_hitpoints, hunger, food, treasure)
    command = input('{}\n{}\n{}'.format(message, status, PROMPT))
    message = ''   
    delta_x, delta_y = 0, 0
    hunger += 1    # getting more hungry, whatever you do
    if command in ['help', '?']:
        message = HELPTEXT
    elif command in ['exit', 'q', 'quit', 'leave']:
        break # exit the game
    elif command in ['e', 'eat']: 
        if food > 0:
            message = 'you eat food'
            food -= 1
            hunger -= 11
            if hunger < 0:
                hunger = 0
                message += ' but your belly is already full'
        else:
            message = 'You have no food!'
    # ------ movement keys -----
    elif command == 'a':
        delta_x = -1  # go left
    elif command == 'd':
        delta_x = 1   # go right
    elif command == 'w':
        delta_y = -1  # go up
    elif command == 's':
        delta_y = 1   # go down
    # ----- check if movement is valid ------
    target = lines[player_y + delta_y][player_x + delta_x]
    if target == '#':
        delta_x, delta_y = 0, 0   # running into wall, cancel movement
        message = 'ouch, you hit the wall'
    elif target in ['f', '$', "S"]:    # run into something interesting
        # replace target with floor tile
        lines[player_y + delta_y] = (
            lines[player_y + delta_y][:player_x + delta_x] + '.' +
            lines[player_y + delta_y][player_x + delta_x + 1:])
        if target == 'f':
            message = 'you found food!'
            food += 1
        elif target == '$':
            message = 'you found gold!'
            treasure += 1
        elif target == "S":
            message = "you destroy a statue and loose hitpoints"
            player_hitpoints -= 5
    # ---- update player position -----
    player_x += delta_x #  movement x
    player_y += delta_y #  movement y
print('Game Over')
