# pyrogue, a roguelike game written in python3
# intended for new python programmers having fun with games like dungeon crawl
# todo: autopickup loot, monster aggro and movement, traps, interlevel travel

__author__ = "Horst JENS"
__license__ = "GPL 3.0"

import random

LEGEND = {
    "#": "wall",
    ".": "floor",
    "<": "stair up",
    ">": "stair down",
    "T": "trap",
    "M": "monster",
    "$": "loot"}


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class LevelError(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def loadlevel(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line[:-1]) # exclude newline char
    return lines


def checklevel(filename):
    lines = loadlevel(filename)
    if len(lines) == 0:
        raise LevelError("{}: level has no lines".format(filename))
    width = len(lines[0])
    linenumber = 1
    exitup = False
    for line in lines:
        if len(line) != width:
            raise LevelError("{}: bad line length".format(filename)+
                             " in line number {}".format(linenumber))
        x = 1
        for char in line:
            if char == "<":
                exitup = True
            if char not in LEGEND:
                raise LevelError("{}: line {} pos {}:".format(filename, linenumber, x) +
                                 "char {} is not in LEGEND".format(char))
            x += 1
        linenumber += 1
    if not exitup:
        raise LevelError("{}: level has no stair up sign (<)".format(
                         filename))
    return lines


class Monster(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hitpoints = random.randint(10, 20)
        self.gold = random.randint(0, 20)
        
    def update(self):
        pass
        

class Player(Monster):
    def __init__(self, x, y):
        Monster.__init__(self, x, y)
        self.z = 0
        self.hitpoints *= 3
        self.status = ""
        
    
class Item(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.carrier = None
        self.visible = True
        self.hitpoints = 1


class Trap(Item):
    def __init__(self, x, y, difficulty=1):
        Item.__init__(self, x, y)
        if difficulty == 1:
            self.difficulty = random.randint(1,10)
        else:
            self.difficulty = difficulty
        self.hitpoints = 2 * self.difficulty
        self.damage_min = random.randint(1, 10) + self.difficulty
        self.damage_max = self.damage_min + random.randint(1,10)
        self.chance_to_detect = 1.01 - self.difficulty/10
        self.chance_to_disarm = self.chance_to_detect / random.randint(1,5)
        self.detected = False
        #self.delay = 0 # delay in turns for placing a trap
        
    def damage(self):
        return random.randint(self.damage_min, self.damage_max)
    
        
class Loot(Item):
    def __init__(self, x, y, cat="?", value=0):
        Item.__init__(self, x, y)
        if cat == "?":
            self.category = random.choice(("armor", "shield", "spell",
                                           "gold", "scroll", "weapon", "gem", "ring", "amulet"))
        else:
            self.category = cat
        if value == 0:
            self.value = random.randint(1,100)
        else:
            self.value = value
        if random.random() < 0.1:
            self.magic = True
            self.value *= 3
        else:
            self.magic = False
        self.weight = round(random.uniform(0.1, 10), 2)
        
    def __str__(self):
        return "{} {} value: {} weight: {}".format("magic" if self.magic else "normal",
                                                   self.category, self.value, self.weight)
        

class Level(object):
    """ each level need one stair up sign < (also the first level)"""

    help_text = """type one of those commands and [Enter]:
    h or help......display this help text
    ?..............toggle inspect tiles mode
    a..............move player left (west)
    w..............move player up (north)
    s..............move player down (south)
    d..............move player right (east)
    q..............move player up, left (northwest)
    e..............move player up, right (northeast)
    c..............move player down, right (southeast)
    y..............move player down, left (southwest)
    <..............move player to previous level (stair up)
    >..............move player to next level (stair down)
    quit or exit...exit the game"""

    def __init__(self, source):
        self.source = source
        self.layout = []
        self.monsters = []
        self.traps = []
        self.loot = []
        self.connectionsup = {}
        self.connectionsdown = {}
        self.parse()
        self.playerx = 1
        self.playery = 1
        self.height = len(self.source)
        self.width = len(self.source[0])
        
    def getchar(self, x, y):
        """get the char from the level layout: wall, floor, stair"""
        return self.layout[y][x]

    def near_trap(self, x, y):
        """return number of nearby traps"""
        counter = 0
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if x+dx < 0 or x+dx > self.width:
                    continue
                if y+dy < 0 or y+dy > self.height:
                    continue
                if self.is_trap(x+dx, y+dy):
                    # make trap detection check
                    counter += 1
        return counter

    def is_trap(self, x, y):
        for t in self.traps:
            if t.carrier is None and t.x == x and t.y == y:
                return t
        return False
        
    def is_loot(self, x, y):
        for l in self.loot:
            if not l.carrier and l.x == x and l.y == y:
                return l
        return False
        
    def is_stair_up(self, x, y):
        if (x,y) in self.connectionsup:
            return True
            
    def is_stair_down(self, x, y):
        if (x,y) in self.connectionsdown:
            return True
    
    def check_monster(self, x, y):
        for m in self.monsters:
            if y == m.y and x == m.x and m.hitpoints > 0:
                return m
        return False
            
    def check_wall(self, x, y):
        if self.layout[y][x] == "#":
            return True
        else:
            return False
            
    def update(self):
        # clean up dead monsters, drop gold
        for m in self.monsters:
            if m.hitpoints < 1:
                self.loot.append(Loot(m.x,m.y, "gold", m.gold))
        self.monsters = [m for m in self.monsters if m.hitpoints > 0]
        # monsters move around

    def draw(self, player):
        """draw the complete level, including items and monsters"""
        output = ""
        y = 0
        for line in self.layout:
            x = 0
            for char in line:
                char = self.getchar(x, y)
                if char == "#":
                    output += "#"
                elif y == player.y and x == player.x:
                    output += "@"
                elif self.check_monster(x, y):
                    output += "M"
                elif self.is_trap(x, y):
                    output += "T"
                elif self.is_loot(x, y):
                    output += "$"
                else:  
                    output += char
                x += 1
            output += "\n"
            y += 1
        return output

    def parse(self):
        """interpreting the source file, seperating walls from things"""
        y = 0
        for line in self.source:
            x = 0
            goodline = ""
            for char in line:
                if char == "<":
                    self.connectionsup[(x,y)] = None
                    self.playerx = x
                    self.playery = y
                    goodline += char
                elif char == ">":
                    self.connectionsdown[(x,y)] = None
                    goodline += char
                elif char == "#" or char ==".":
                    goodline += char
                elif char == "T":
                    goodline += "."
                    self.traps.append(Trap(x,y))
                elif char == "$":
                    goodline += "."
                    self.loot.append(Loot(x,y))
                elif char == "M":
                    goodline += "."
                    self.monsters.append(Monster(x,y)) 
                x += 1
            self.layout.append(goodline)
            if y == 0:
                self.width = len(goodline)
            y += 1
        self.height = y
        
        
def fight(attacker, defender):
    if random.random() < 0.5:
        defender.hitpoints -= random.randint(1,5)
        return "successfully attacked"
    else:
        attacker.hitpoints -= random.randint(1,5)
        return "attack failed"


def game():
    levels = []
    names = ["level001.txt", "level002.txt"]
    for name in names:
        lines = False
        try:
            lines = checklevel(name)
        except IOError:
            print('Error: cannot open', name)
        except LevelError as e:
            print("sadly, there were errors while loading level(s):")
            print(e)
        if lines:
            levels.append(Level(lines))
    print(len(levels), "level(s) were successfully added to the game")
    print(len(names)-len(levels), 
          "level(s) were not loaded because of errors")
    level = levels[0]
    player = Player(level.playerx, level.playery)
    # main loop
    play = True
    while player.hitpoints > 0 and play:
        if level.is_stair_down(player.x, player.y):
            player.status = "press > or x to descend one level deeper"
        elif level.is_stair_up(player.x, player.y):
            player.status = "press < or x to ascend one level higher"
        print(level.draw(player), end="")  # level ends with a natural \n
        print(player.status)
        c = input("Hp:{} $:{} Level:{} - type command or 'help' >>>".format(player.hitpoints, player.gold,
                  player.z))
        c = c.lower()
        player.status = ""
        if c == "quit" or c == "exit":
            play = False  # exit the game
        elif "help" in c:
            print(level.help_text)
            input("press enter to continue")
            continue
        # move player between levels
        if level.is_stair_up(player.x, player.y):
            if c == "<" or c == "x":
                player.z -= 1
                if player.z < 0:
                    play = False
                    player.status = "You exit the dungeon. Game over"
                else:
                    level = levels[player.z] # TODO: player x,y
        elif level.is_stair_down(player.x, player.y):
            if c == ">" or c == "x":
                player.z += 1
                if player.z > len(levels) -1:
                    play = False
                    player.status = "The next level of the dungeon is not yet constructed. You enter the void."
                else:
                    level = levels[player.z] # TODO: player x,y
        # move player x,y
        dx, dy = 0, 0
        if c == "w":
            dx, dy = 0, -1
        elif c == "s":
            dx, dy = 0, 1
        elif c == "a":
            dx, dy = -1, 0
        elif c == "d":
            dx, dy = 1, 0
        elif c == "q":
            dx, dy = -1, -1
        elif c == "e":
            dx, dy = 1, -1
        elif c == "y":    # TODO: assign key for non-german keyboards
            dx, dy = -1, 1
        elif c == "c":
            dx, dy = 1, 1
        m = level.check_monster(player.x + dx, player.y + dy)
        if m:
            player.status = fight(player, m)
        elif not level.check_wall(player.x + dx, player.y + dy):
            player.x += dx
            player.y += dy
        else: 
            player.status = "You can not move into walls."
        # movement is done. Checking traps
        trap = level.is_trap(player.x, player.y)
        if trap:
            # explode trap, calculate damage
            damage = trap.damage()
            player.hitpoints -= damage
            player.status = "A trap! You take {} damage. ".format(damage)
            trap.hitpoints-=1
            if trap.hitpoints < 1:
                player.status += "The trap is destroyed. "
            else:
                player.status += "The trap is still active! "
        traps_nearby = level.near_trap(player.x, player.y)
        if traps_nearby > 0:
            # calculate how many traps the player can really see
            player.status += "You stand near {} traps".format(traps_nearby)

    print("Game Over")
    print("You left the game with {} hitpoints".format(player.hitpoints))
    
if __name__ == "__main__":
    game()    




