# mana, blink spell and functions
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
HELPTEXT = 'movement: w,a,s,d\njump: W,A,S,D\neat: e\nblink: blink\nquit: quit or q' 
message = 'welcome {}, move with w,a,s,d'.format(PLAYER)
player_x, player_y = 1, 1
lines = DUNGEON.split()
length = len(lines[0])
hunger, treasure, food, mana = 0, 0, 7, 50
player_hitpoints = 25

def enough_mana(amount=10):
    """returns True if mana is greater or equal the amount"""
    if mana < amount:
        return False  # no else necessary because a return exit the function
    return True

def is_inside_dungeon(x, y):
    """returns True if point (x,y) is inside the dungeon"""
    if y < 0 or y >= len(lines) or x < 0 or x >= length:
        return False
    return True

def distance(x1, y1, x2, y2):
    """calculate distance between (x1,y1) and (x2,y2)"""
    return ( (x1-x2)**2 + (y1-y2)**2 ) ** 0.5
    
def blink(x, y, radius=5):
    """choose dx,dy to an random floor location inside radius"""
    if radius < 1:
        raise UserWarning("radius in function blink must be greater than 0")
    attempts = 0
    while attempts < 10000:
       attempts += 1
       dx = random.randint(1, radius) * random.choice((-1,1))
       dy = random.randint(1, radius) * random.choice((-1,1))
       if distance(x, y, x+dx, y+dy) > radius:
           continue 
       if not is_inside_dungeon(x+dx, y+dy):
           continue
       if lines[y+dy][x+dx] != ".":
           continue
       return dx,dy
    print("no target found for blink spell")
    input("please press ENTER")
    return 0,0  

while hunger < 100 and player_hitpoints > 0:
    # ------ Print dungeon -------
    for y, line in enumerate(lines):
        # y is the line number starting with 0      
        if y == player_y:
            print(line[:player_x] + PLAYER + line[player_x+1:])
        else:
            print(line)
    # ------ Command processing ---------
    status = 'hitpoints: {} hunger:{} food:{} gold:{} mana:{:.1f}\n'.format(
              player_hitpoints, hunger, food, treasure, mana)
    command = input('{}\n{}\n{}'.format(message, status, PROMPT))
    message = ''   
    delta_x, delta_y = 0, 0
    hunger += 1    # getting more hungry, whatever you do
    mana += 0.1    # very slow mana regeneration
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
    # ---- jumping costs mana and makes hungry
    elif command in ["A", "D", "W", "S"]:
        if not enough_mana(5):
            message += "not enough mana to jump"
        else:
            hunger += 1
            mana -= 5
            message += "you jump"
            if command == "A":
                delta_x = -2  # jump left   
            elif command == "D": 
                delta_x = 2   # jump right 
            elif command == "W": 
                delta_y = -2  # jump up
            elif command == "S":
                delta_y = 2   # jump down
    # ------ blink spell teleports to a random floor nearby -----
    elif command == "blink":
        if not enough_mana(10):
            message += "not enough mana for blink spell"
        else:
            delta_x, delta_y = blink(player_x, player_y)
            mana -= 10
            message += "you blink magically"
    # ----- check if movement is valid ------
    if not is_inside_dungeon(player_x + delta_x, player_y + delta_y): 
       message = "illegal move" 
       continue # back to the start of the while loop
    target = lines[player_y + delta_y][player_x + delta_x]
    if target == '#':
        delta_x, delta_y = 0, 0   # running into wall, cancel movement
        message = 'ouch, you hit the wall'
    elif target in ['f', '$', 'S']:    # run into something interesting
        if target == "S":
            if random.random() < 0.7 :  # Statue has a 70% chance to strike back!
                damage = random.randint(1,6)
                message = "the statue fights back, you loose {} hitpoints".format(damage)
                player_hitpoints -= damage
                continue    # back to the start of the while loop, no movement
            message =  "you destroy the statue!"   
        if target == 'f':
            message = 'you found food!'
            food += 1
        elif target == '$':
            message = 'you found gold!'
            treasure += 1
        # ---- replace target with floor tile ----
        lines[player_y + delta_y] = (
            lines[player_y + delta_y][:player_x + delta_x] + '.' +
            lines[player_y + delta_y][player_x + delta_x + 1:])
    # ---- update player position -----
    player_x += delta_x #  movement x
    player_y += delta_y #  movement y
else:
    print("hitpoints: {}, hunger: {}".format(player_hitpoints, hunger))
print('Game Over')
