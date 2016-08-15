# jumping and fighting statues , no functions
import random 
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
HELPTEXT = 'movement: w,a,s,d\njump: W,A,S,D\neat: e\nquit: quit or q' 

message = 'welcome {}, move with w,a,s,d'.format(PLAYER)
player_x, player_y = 1, 1
lines = DUNGEON.split()
length = len(lines[0])
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
            hunger -= random.randint(5,15)
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
    elif command == "A":
        delta_x = -2  # jump left
        hunger += 1
    elif command == "D": 
        delta_x = 2   # jump right 
        hunger += 1
    elif command == "W": 
        delta_y = -2  # jump up
        hunger += 1
    elif command == "S":
        delta_y = 2   # jump down
        hunger += 1
    # ----- check if movement is valid ------
    if (player_y + delta_y < 0 or player_y + delta_y >= len(lines) or 
       player_x + delta_x < 0 or player_x + delta_x >= length):
       message = "illegal move" 
       continue # back to the start of the while loop
    target = lines[player_y + delta_y][player_x + delta_x]
    if target == '#':
        delta_x, delta_y = 0, 0   # running into wall, cancel movement
        message = 'ouch, you hit the wall'
    elif target in ['f', '$', 'S']:    # run into something interesting
        if target == "S":
            if random.random() < 0.7 : 
                damage = random.randint(1,6)
                message = "the statue fights back, you loose {} hitpoints".format(damage)
                player_hitpoints -= damage
                continue    # back to the start of the while loop
            message =  "you destroy the statue!"   
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
    # ---- update player position -----
    player_x += delta_x #  movement x
    player_y += delta_y #  movement y
else:
	print("hitpoints: {}, hunger: {}".format(player_hitpoints, hunger))
print('Game Over')
