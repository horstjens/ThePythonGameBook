# DungeonLevel class, LEGEND,  multi-level dungeons, Door and keys
# not used yet: panic attribute, __repr__ to print monsters


import random

# legend: #=rock  .=floor  f=food  $=gold l=loot ?=mushroom T=Trader

PROMPT = 'Type your command or ? and press Enter:'
HELPTEXT = """movement: w,a,s,d\njump: jump w, jump a, jump s, jump d
digging: dig w, dig a, dig s, dig d\nblink: blink\neat: e\nquit: quit or q"""
LEGEND = '''
#          wall
.          floor
<          stair down
>          stair up
D          Door
T          Trader
l          loot
k          key
$          gold
f          food
?          magic mushroom
@          Player
S          Statue
W          Wolf
'''
DUNGEON1 = '''
###############################################
#.$$.Tfff##<##.lllll.....#f#.$#..k..#.......#>#
#ll..S...#####...lll.....###....###.#.....#.#$#
#????S.S.#####.W$...f...W.....##$......f..#.#D#
#.........f...f...l...l...$...$...............#
###############################################
'''  # add more lines to the dungeon!
DUNGEON2 = '''
##################################################
#.$$.TfffSS<SS..W.....S.WW.fffffff......????#<kWk#
#..WWW...SSSSS..W....TS.WW.llllllll......???####D#
#llllll..SSSSS..W.....S.WW.$$$$$$$$........??.W#l#
#...........................................?.SDS#
##################################################
'''  # add more lines to the dungeon!

lines = DUNGEON.split()
DUNGEONWIDTH = len(lines[0])
DUNGEONHEIGHT = len(lines)

class Game(object):
    """this class holds (global) class variables for the game"""
    levels = []
    players = []
    monsters = {}
    graveyard = []

class DungeonLevel(object):
    """holds one complete floor of th edungeon, including all monsters"""
    number = 0
    def __init__(self, rawstring):
        self.rawstring = levelstring
        DungeonLevel.number += 1
        #Game.levels.append(self)
        self.number = DungeonLevel.number



class Monster(object):
    """generic monster"""
    number = 0  # this is a class variable
    #monsterdict = {}  # this is a class variable

    def __init__(self, x, y, z=1, char="M", name=None):
        self.x = x
        self.y = y
        self.z = z
        self.char = char
        self.hitpoints = int(random.gauss(15, 3))  # around 15 hitpoints
        self.attack = random.randint(1, 6)
        self.defense = random.randint(1, 6)
        self.panic = random.random() * 0.1  # between 0% and 10% chance to panic
        Monster.number += 1
        self.number = Monster.number  # get myself a new number
        Game.monsters[self.number] = self  # append myself to monsterdict
        if name is None:
            name = type(self).__name__ + str(self.number)
        self.name = name

    def ai(self, player_x, player_y):
        """returns dx and dy for monster movement"""
        return 0, 0  # just staying around

    def __repr__(self):
        """returns a string if to the print() function"""
        txt = "i am an instance of the class {}\n".format(type(self).__name__)
        stats = [a for a in dir(self) if a[:2] != "__" and a != "monsterdict"]
        for stat in stats:
            txt += "my {} is {}\n".format(stat, self.__getattribute__(stat))
        return txt

class Player(Monster):
    def __init__(self, x, y, z, char="@", name=None):
        Monster.__init__(self, x, y, z, char, name)
        self.name = name
        self.hunger = 0
        self.gold = 0
        self.mana = 0
        self.food = 7
        self.hitpoints = 250
        self.loot = 0
        self.keys = 0
        self.kills = {}

    def status(self):
        """return a status line with attributes"""
        return '{}: hitpoints: {} hunger:{} food:{} gold:{} mana:{:.1f} loot:{} keys: {}\n'.format(
            self.name, self.hitpoints, self.hunger, self.food, self.gold, self.mana, self.loot, self.keys)


class Statue(Monster):
    """a stationary monster with tons of hitpoints but no defense"""

    def __init__(self, x, y, z, char="S"):
        Monster.__init__(self, x, y, z, char)  # ------- important ---------
        # --- overwriting default monster attributes ------
        self.hitpoints = int(random.gauss(20, 5))
        self.panic = 0
        self.defense = 0


class Wolf(Monster):
    """a clever Monster tracking the player"""

    def __init__(self, x, y, char="W"):
        Monster.__init__(self, x, y, z, char)  # ------- important ---------
        # --- overwriting default monster attributes ------
        self.panic = random.random() * 0.2  # 20% panic at max
        self.sniffrange = random.randint(5, 10)

    def ai(self, player_x, player_y):
        """returns dx, dy toward player if inside sniffrange"""
        if distance(self.x, self.y, player_x, player_y) < self.sniffrange:
            dx, dy = 0, 0
            if player_x > self.x:
                dx = 1
            elif player_x < self.x:
                dx = -1
            if player_y > self.y:
                dy = 1
            elif player_y < self.y:
                dy = -1
        else:
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
        if dx != 0 and dy != 0:
            # do not allow diagonal movement
            if random.random() < 0.5:
                dx = 0
            else:
                dy = 0
        return dx, dy


def battle(m1, m2):
    """a battle round between two monsters/players. m1 attacks m2"""
    attackroll = random.randint(1, 6) + random.randint(1, 6)
    defenseroll = random.randint(1, 6) + random.randint(1, 6)
    damage = random.randint(1, 6) + random.randint(1, 6)
    print("attackvalue {} + attackroll {} vs. defensevalue {} + defenseroll {}".format(
        m1.attack, attackroll, m2.defense, defenseroll))
    if attackroll + m1.attack > defenseroll + m2.defense:
        print("attack successfull! damage is {} ({} hp left)".format(damage, m2.hitpoints))
    else:
        print("attack unsuccessfull")
    m2.hitpoints -= damage


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
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def blink(x, y, radius=5):
    """choose dx,dy to an random floor location inside radius"""
    if radius < 1:
        raise UserWarning("radius in function blink must be greater than 0")
    attempts = 0
    while attempts < 10000:
        attempts += 1
        dx = random.randint(1, radius) * random.choice((-1, 1))
        dy = random.randint(1, radius) * random.choice((-1, 1))
        if distance(x, y, x + dx, y + dy) > radius:
            continue
        if not is_inside_dungeon(x + dx, y + dy):
            continue
        if lines[y + dy][x + dx] != ".":
            continue
        return dx, dy
    print("no target found for blink spell")
    input("please press ENTER")
    return 0, 0


def replace_tile(lines, x, y, newTile="."):
    newlines = []
    for nr, line in enumerate(lines):
        if nr == y:
            newlines.append(line[:x] + newTile + line[x + 1:])
        else:
            newlines.append(line)
    return newlines


def game(lines):
    message = 'welcome @, move with w,a,s,d'
    player1 = Player(1, 1, "@")

    # ------- create monsters (once) ---------
    for y, line in enumerate(lines):
        for x in range(len(line)):
            char = lines[y][x]
            if char == "S":
                Statue(x, y)
                lines = replace_tile(lines, x, y, ".")
            elif char == "W":
                Wolf(x, y)
                lines = replace_tile(lines, x, y, ".")
    # ------------the game begins ----------------------
    while hunger < 100 and player1.hitpoints > 0:
        # ------ Print dungeon -------
        for y, line in enumerate(lines):
            # y is the line number starting with 0      
            newline = ""
            for x in range(len(line)):
                char = "_"
                char = lines[y][x]
                for monsternumber in Monster.monsterdict:
                    monster = Monster.monsterdict[monsternumber]
                    if monster.x == x and monster.y == y:
                        char = monster.char
                newline += char
            print(newline)
        # ------ Command processing ---------

        command = input('{}\n{}\n{}'.format(message, player1.status(), PROMPT))
        message = ''
        delta_x, delta_y = 0, 0
        hunger += 1  # getting more hungry, whatever you do
        mana += 0.1  # very slow mana regeneration
        if random.random() < 0.01:
            player.hitpoints += 1  # 1% chance to regain a hitpoint
        if command in ['help', '?']:
            message = HELPTEXT
        elif command in ['exit', 'q', 'quit', 'leave']:
            break  # exit the game
        elif command in ['e', 'eat']:
            if food > 0:
                message = 'you eat food'
                food -= 1
                hunger -= random.randint(5, 15)
                if hunger < 0:
                    hunger = 0
                    message += ' but your belly is already full'
            else:
                message = 'You have no food!'
        # ------ movement keys -----
        elif command == 'a':
            delta_x = -1  # go left
        elif command == 'd':
            delta_x = 1  # go right
        elif command == 'w':
            delta_y = -1  # go up
        elif command == 's':
            delta_y = 1  # go down
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
                    delta_x = 2  # jump right
                    message += "you jump east\n"
                elif command == "jump w":
                    delta_y = -2  # jump up
                    message += "you jump north\n"
                elif command == "jump s":
                    message += "you jump south\n"
                    delta_y = 2  # jump down
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
                lines = replace_tile(lines, player.x + delta_x, player.y + delta_y, ".")
        elif lines[player.y][player.x] == "T":
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
                delta_x, delta_y = blink(player.x, player.y)
                mana -= 10
                message += "you blink magically"
        # ----- check if movement is valid ------
        if not is_inside_dungeon(player.x + delta_x, player.y + delta_y):
            message = "illegal move"
            continue  # back to the start of the while loop
        target = lines[player.y + delta_y][player.x + delta_x]
        # ----- check if running into another monster ------
        cleanlist = []
        for monsternumber in Monster.monsterdict:
            if monsternumber == 1:
                continue  # player is monster number 1
            monster = Monster.monsterdict[monsternumber]
            if monster.x == player.x + delta_x and monster.y == player.y + delta_y:
                # ---- fight !!! ----
                print("player fights monster!")
                battle(player, monster)
                if monster.hitpoints > 0:
                    print("monster fights back!")
                    battle(monster, player)
                if player.hitpoints <= 0:
                    delta_x, delta_y = 0, 0
                    break
                if monster.hitpoints > 0:
                    # cancel movement
                    delta_x, delta_y = 0, 0
                else:
                    # remove monster
                    cleanlist.append(monsternumber)
        for number in cleanlist:
            del Monster.monsterdict[number]


            # ----
        if target == '#':
            delta_x, delta_y = 0, 0  # running into wall, cancel movement
            message = 'ouch, you hit the wall'
        elif target == 'T':
            # Trader, allows buy/sell
            message += '\nA merchant wants to trade with you. Choose:\n'
            message += "command      effect\n"
            message += "mana ....... trade loot for mana\n"
            message += "health ..... trade loot for hitpoints\n"
            message += "food ....... trade loot for food\n"
            message += "loot ....... trade gold for loot\n"

        elif target in ['f', '$', 'l', '?', 'k']:  # run into something interesting
            # ----- things that can be collected or instantly used up ------
            if target == 'f':
                message += 'you found food!'
                food += 1
            elif target == 'k':
                message += 'you found a key!'
                keys += 1
            elif target == 'l':
                message += 'you found loot!'
                loot += 1
            elif target == '$':
                message += 'you found gold!'
                gold += 1
            elif target == '?':
                message += 'You trample on a magic mushroom! The fairies living inside are very upset'
                fate = random.randint(1, 10)
                if fate == 1:
                    message += "\nYou eat the mushroom. It tastes boring"
                    hunger -= 2
                elif fate == 2:
                    message += "\nThe fairies attack you"
                    player.hitpoints -= 5
                elif fate == 3:
                    message += "\nThe fairies nearly kill you"
                    player.hitpoints = 1
                elif fate == 4:
                    message += "\nThe fairies steal all your food"
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
            lines = replace_tile(lines, player.x + delta_x, player.y + delta_y, ".")
        # ---- update player position -----
        player.x += delta_x  # movement x
        player.y += delta_y  # movement y
        # ---- update moving monsters -----
        cleanlist = []
        monsterplaces = set()
        for monsternumber in Monster.monsterdict:
            if monsternumber == 1:
                continue  # player is monster number 1
            monster = Monster.monsterdict[monsternumber]
            dx, dy = monster.ai(player.x, player.y)
            if monster.x + dx == player.x and monster.y + dy == player.y:
                print("Monster moves into player!")
                battle(monster, player)
                dx, dy = 0, 0
                if player.hitpoints > 0:
                    print("player strikes back!")
                    battle(player, monster)
                    if monster.hitpoints < 1:
                        cleanlist.append(monsternumber)

            target = lines[monster.y + dy][monster.x + dx]
            if target in ["#", "T", "?"]:
                dx, dy = 0, 0  # cancel movement
            if monster.hitpoints > 0:
                monster.x += dx
                monster.y += dy
                # TODO several monsters can be in the same location
        # ------ clean dead monsters -----
        for number in cleanlist:
            del Monster.monsterdict[number]

    else:
        print("hitpoints: {}, hunger: {}".format(player.hitpoints, hunger))
    print('Game Over')


if __name__ == "__main__":
    game(lines)
