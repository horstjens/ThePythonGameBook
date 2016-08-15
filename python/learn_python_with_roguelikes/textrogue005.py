# better functions, random fate, stationary trader, loot, dig and jump spell
import random 
# legend: #=rock  .=floor  f=food  $=gold l=loot ?=mushroom T=Trader
DUNGEON = '''
###############################################
#.$$.Tfff.#....lllll.....#f#.$#.....#.......#$#
#ll..S....#......lll.....###....###.#.....#.#.#
#????S.S..f.....$...f.........##$......f..#...#
###############################################
'''  # add more lines to the dungeon!
PLAYER = '@'
PROMPT = 'Type your command or ? and press Enter:'
HELPTEXT = """movement: w,a,s,d\njump: jump w, jump a, jump s, jump d
digging: dig w, dig a, dig s, dig d\nblink: blink\neat: e\nquit: quit or q""" 
lines = DUNGEON.split()
DUNGEONWIDTH = len(lines[0])
DUNGEONHEIGHT = len(lines)

def not_enough(necessary, disposable, resource="mana"):
    """returns a detailed message"""
    return "Not enough {}! You need {} but only have {:.1f}".format(
           resource, necessary, disposable)

def is_inside_dungeon(x, y):
    """returns True if point (x,y) is inside the dungeon"""
    if y < 0 or y >= DUNGEONHEIGHT or x < 0 or x >= DUNGEONWIDTH:
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

def replace_tile(lines,x,y,newTile="."):
    newlines = []
    for nr, line in enumerate(lines):
        if nr == y:
           newlines.append(line[:x] + newTile + line[x + 1:])
        else:
           newlines.append(line)
    return newlines 
   
   

def game(lines):
    message = 'welcome {}, move with w,a,s,d'.format(PLAYER)
    player_x, player_y = 1, 1
    hunger, gold, food, mana, loot = 0, 0, 7, 250, 0
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
        status = 'hitpoints: {} hunger:{} food:{} gold:{} mana:{:.1f} loot:{}\n'.format(
                  player_hitpoints, hunger, food, gold, mana,loot)
        command = input('{}\n{}\n{}'.format(message, status, PROMPT))
        message = ''   
        delta_x, delta_y = 0, 0
        hunger += 1    # getting more hungry, whatever you do
        mana += 0.1    # very slow mana regeneration
        if random.random() < 0.01:
            player_hitpoints += 1 # 1% chance to regain a hitpoint
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
        elif "jump" in command:
            if mana < 5:
                message += not_enough(5, mana, "mana")
            else:
                hunger += 1
                mana -= 5
                if command == "jump a":
                    delta_x = -2  # jump left   
                    message += "you jump west\n"
                elif command == "jump d": 
                    delta_x = 2   # jump right 
                    message += "you jump east\n"
                elif command == "jump w": 
                    delta_y = -2  # jump up
                    message += "you jump north\n"
                elif command == "jump s":
                    message += "you jump south\n"
                    delta_y = 2   # jump down
        # --- jump spell ------
        elif "dig" in command:
            if mana < 50:
                message += not_enough(50, mana, "mana")
            else:
                mana -= 50
                if command == "dig w":
                    delta_y = -1
                    message += "you dig north"
                elif command == "dig s":
                    delta_y = 1
                    message += "you dig south"
                elif command == "dig a":
                    delta_x = -1
                    message += "you dig west"
                elif command == "dig d":
                    delta_x = 1
                    message += "you dig east"
                # ---- replace target with floor tile ----
                lines = replace_tile(lines, player_x + delta_x, player_y + delta_y, ".")
        elif lines[player_y][player_x] == "T":
            # -----special command if player is on a Trader position ---
            if command == "mana":
                if loot > 0:
                    loot -= 1
                    mana += 10
                    message += "you trade loot for mana"
                else:
                    message += not_enough(1, loot, "loot")
            elif command == "food":
                if loot > 1:
                    loot -= 2
                    food += 10
                    message += "you trade loot for food"
                else:
                    message += not_enough(2, loot, "loot")
            elif command == "health":
                if loot > 2:
                    loot -= 3
                    player_hitpoints += 10
                    message += "you trade loot for health"
                else:
                    message += not_enough(3, loot, "loot")
            elif command == "loot":
                if gold > 4:
                    gold -= 5
                    loot += 1
                    message += "you buy one loot for 5 gold"
                else:
                    message += not_enough(5, gold, "gold")
        # ------ blink spell teleports to a random floor nearby -----
        elif command == "blink":
            if mana < 10:
                message += not_enough(10, mana, "mana")
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
        elif target == 'T':
            # Trader, allows buy/sell
            message += '\nA merchant wants to trade with you. Choose:\n'
            message += "command      effect\n"
            message += "mana ....... trade loot for mana\n"
            message += "health ..... trade loot for hitpoints\n"
            message += "food ....... trade loot for food\n"
            message += "loot ....... trade gold for loot\n"
        
        elif target in ['f', '$', 'S', 'l', '?']:    # run into something interesting
            #---- things that are destroyable, like statues ----
            if target == "S":
                if random.random() < 0.7 :  # Statue has a 70% chance to strike back!
                    damage = random.randint(1,6)
                    message = "the statue fights back, you loose {} hitpoints".format(damage)
                    player_hitpoints -= damage
                    continue    # back to the start of the while loop, no movement
                message =  "you destroy the statue!"   
            #----- things that can be collected or instantly used up ------
            if target == 'f':
                message += 'you found food!'
                food += 1
            elif target == 'l':
                message += 'you found loot!'
                loot += 1
            elif target == '$':
                message += 'you found gold!'
                gold += 1
            elif target == '?':
                message += 'You trample on a magic mushroom! The fairies living inside are very upset'
                fate = random.randint(1,10)
                if fate == 1:
                    message +="\nYou eat the mushroom. It tastes boring"
                    hunger -= 2
                elif fate == 2:
                    message +="\nThe fairies attack you"
                    player_hitpoints -= 5
                elif fate == 3:
                    message +="\nThe fairies nearly kill you"
                    player_hitpoints = 1
                elif fate == 4:
                    message +="\nThe fairies steal all your food"
                    food = 0
                elif fate == 5:
                    message += "\nThe fairies steall all your gold"
                    gold = 0
                elif fate == 6:
                    message += "\nYou find some fairy gold and take it"
                    gold += 10
                elif fate == 7:
                    message += "\nYou find some useful fairy stuff"
                    loot += 1
                elif fate == 8:
                    message += "\nYou eat some fairys. The taste is very strange"
                    mana += 5
                elif fate == 9:
                    message += "\nThe fairy shaman steals all your mana"
                    mana = 0
                elif fate == 10:
                    message += "\nThe fairies curse you but nothing happens"
            # ---- replace target with floor tile ----
            lines = replace_tile(lines, player_x + delta_x, player_y + delta_y, ".")
        # ---- update player position -----
        player_x += delta_x #  movement x
        player_y += delta_y #  movement y
    else:
        print("hitpoints: {}, hunger: {}".format(player_hitpoints, hunger))
    print('Game Over')

if __name__ == "__main__":
    game(lines) 
