# pycrawl_actiondemo
# my very own rogulike game
# because i play far too much dungeon crawl stone soup
# 2012 by Horst JENS   horstjens@gmail.com
# license: gpl3 see http://www.gnu.org/copyleft/gpl.html
# this game is a part of http://ThePythonGameBook.com

# this is a demo where the player (@) can interact with monsters ( battle ), traps, doors etc.
# the player can pick up and drop items. he also has an inventory
# later on, certain monsters should also be able to pick up at last one item
#


import random



class Game(object):
    """super class, contaier for all other stuff"""
    player = None # the player will instance will be stored here
    level = {} # dict with level instances key = levelnumber
    score = 0
    turns = 0
    history = ""
    #            key, x, y # y from top to down, x from left to right
    dirs ={"7":(-1,-1),
                 "4":(-1, 0),
                 "1":(-1, 1),
                 "8":( 0,-1),
                 "5":( 0, 0),
                 "2":( 0, 1),
                 "9":( 1,-1),
                 "6":( 1, 0),
                 "3":( 1, 1)}  # this is a constant
    #            char : [z, short text, long text , actionlist], ...
    tiledict = { "X": ["an outer wall", "an outer wall of the level. You can not go there" ,["scribble on"]] , 
                 "#": ["an inner wall", "an inner wall. You may destroy this wall with the right tools or spells",
                       ["destroy", "scribble on"]] , 
                 ".": ["a floor tile", "an empty floor tile. Not dangerous, but boring.", ["scribble on"] ], 
                 "d": ["a door", "an open door" , ["close"]],
                 "D": ["a door", "a closed door" ,["open", "destroy"]],   
                 "<": ["a stair up", "a stair up to the previous level" , ["climb up"]],
                 ">": ["a stair down", "a stair down to the next deeper level", ["climb down"]],
                 "s": ["a shop", "a shop of a friendly merchant", ["trade with"]] ,
                 "t": ["a trap", "a dangerous trap !", ["disarm/untrap"]],
                 "m": ["a dead monster", "a dead monster. Did you kill it?", ["eat", "bury"]],
                 "?": ["a heap of loot", "a heap of loot. Feel yourself enriched" , ["kick"]],
                 "b": ["a box", "a box. You wonder what is inside. And if it is trapped", ["open", "destroy", "search/untrap"]], 
                 ":": ["a single item", "a single item. add one more item and you have a heap of loot", ["kick","pull","inspect"]],
                 "@": ["the player", "the player. that is you.", ["attack"]],
                 "M": ["a living monster", "a living monster. You can kill it. It can kill you !", ["attack", "seduce", "offer item to"]],
                 "Z": ["a sleeping monster","a sleeping monster. You can kill it while it sleeps !", ["attack","push"]]
                }
    output = None # output instance

class Level(object):
    """a representation of the current level (lots of GameObjects)
    The level instances live inside Game.level{} """

    def __init__(self, rawlevel, levelnumber):
        self.levelnumber = levelnumber 
        Game.level[self.levelnumber] = self  # store level instance into game class
        #rawmap is a list of lists of chars
        self.rawmap = list(map(list, rawlevel.split())) # at them moment all stuff
        #print(self.rawmap)
        self.rows = len(self.rawmap)  # width of the level in chars
        self.cols = len(self.rawmap[0]) # height of the level in chars
        # make real level from rawmap
        self.pos = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self.pos[c,r] = -1 # not defined game object number # 
        self.monsterkeys = []
        self.itemkeys = []
        self.interpret_rawlevel()
        Game.output = Output(self.rows, self.cols)
        Game.output.drawlevel(self.levelnumber)
        
    
    def interpret_rawlevel(self):
        """generating a 'real'  level info from the rawmap, The rawmap includes traps, walls, monster, player etc. No more random placement needed except for
        generating loot items and single items as indicated in rawmap"""
        for y in range(self.rows):
            for x in range(self.cols):
                rawchar = self.rawmap[y][x]
                if not rawchar in Game.tiledict:
                    raise UserWarning("Bad rawmap char found in rawmap but not in Games.tiledict: %s" % rawchar)
                if rawchar in "dDs#X<>": # not a floor tile but a wall 
                    # create not-floor tile
                    self.pos[(x,y)] = GameObject(x,y,self.levelnumber, rawchar).number
                else:
                    # create floor tile
                    self.pos[(x,y)] = GameObject(x,y,self.levelnumber, ".").number
                if rawchar == "@":
                    if not Game.player:
                        Game.player = Player(x, y, self.levelnumber, "@")
                    else:
                        Game.player.x = x
                        Game.player.y = y
                        Game.player.levelnumber = self.levelnumber
 
                elif rawchar in "MZ": # monster  
                    self.monsterkeys.append(Monster(x,y,self.levelnumber, rawchar).number)  
                elif rawchar in "tbm:": #item        
                    # create Item
                    self.itemkeys.append(Item(x,y,self.levelnumber, rawchar).number)
                elif rawchar == "?": # heap of random items    
                    for a in range(random.randint(2,6)):
                        self.itemkeys.append(Item(x,y,self.levelnumber,":").number)
                
    def pickup(self,x,y):
        ilist = []
        for i in self.itemkeys:
            if GameObject.book[i].x == x and GameObject.book[i].y == y:
                ilist.append(i)
        return ilist
    
    def inspect(self, x,y):
        """gives back a multi-line string describing the actual floor tile, neigboring tiles and all items on this floor tile"""
        t = "At x:%i y:%i you see %s.\n" % (x,y, GameObject.book[self.pos[(x,y)]].longtext )
        items = self.pickup(x,y)
        if len(items) == 0:
            t+= "There are no items laying around"
        else:
            t+= "You see there laying on the floor:\n"
            for i in items:
                t+= GameObject.book[i].longtext + "\n"
        return t
                    
    def __getitem__(self, xy):
        x,y = xy
        return self.pos[(x,y)] # stuff like [ground, itemlist, monster] ?
    
    def __setitem__(self, xy, stuff):
        x,y = xy
        self.pos[(x,y)] = stuff
     

class Output(object):
    """the ascii-map from where the actual output is generated"""
    def __init__(self, rows, cols):
        #print("rows, cols:",rows, cols)
        self.rows = rows
        self.cols = cols
        self.map = [] # self.ground_map = list(map(list, rawlevel.split()))
        # create dummy string of empty tiles
        self.map = [["." for x in range(cols)] for y in range(rows)]

        #print("map:", self.map)
    
    def drawlevel(self, levelnumber):
        level = Game.level[levelnumber]
        for y in range(level.rows):
            for x in range(level.cols):
                # ground
                char = GameObject.book[level.pos[(x,y)]].char
                # items
                itemcount = 0
                for i in level.itemkeys:
                    if GameObject.book[i].x == x and GameObject.book[i].y == y:
                        char = GameObject.book[i].char  #overwrite floor with item
                        itemcount += 1
                if itemcount > 1:
                    char = "?"
                # monsters
                for m in level.monsterkeys:
                    if GameObject.book[m].x == x and GameObject.book[m].y == y:
                        char = GameObject.book[m].char  #overwrite floor with item
                # player
                if Game.player.x == x and Game.player.y == y:
                    char = "@"
                #print("y,x",y,x)
                self.map[y][x] = char # set char    
    
    def make_screenstring(self):
        return "\n".join(self)
    
    def __iter__(self):
        return ("".join(row) for row in self.map)

    def __getitem__(self, xy):
        x, y = xy
        return self.map[y][x] # row, col

    def __setitem__(self, xy, char):
        x, y = xy
        self.map[y][x] = char # row, col


class GameObject(object):
    number = 0
    book = {}
    """each obect in the game Monster, Item, Player, Wall has some shared attributes"""
    def __init__(self, x, y, levelnumber, char, **kwargs):
        self.x = x
        self.y = y
        self.levelnumber = levelnumber
        self.number = GameObject.number
        GameObject.number += 1
        GameObject.book[self.number] = self
        self.char = char
        self.shorttext = Game.tiledict[self.char][0]
        self.longtext = Game.tiledict[self.char][1]
        self.actionlist = Game.tiledict[self.char][2]

class Item(GameObject):
    """individual Item with all attributes"""
    def __init__(self, x, y, levelnumber, char, **kwargs):
        GameObject.__init__(self,x,y,levelnumber, char, **kwargs)
        if self.char == ":": # single item
            self.longtext = self.generate_text()
        else:
            self.longtext = Game.tiledict[self.char][1]

    def generate_text(self):
        """generate a random description for this item for the very lazy coder"""
        word1 = random.choice(("a big", "a small", "a medium", "an epic", "a handsome","a rotting", "an expensive", "a cheap"))
        word2 = random.choice(("yellow", "green", "blue", "red", "white", "black","rusty", "shiny", "blood-smeared"))
        word3 = random.choice(("ring", "drink", "flower", "wand", "fruit"))
        return " ".join((word1, word2, word3)) # put space between words

class Monster(GameObject):
    """individual Monster"""
    def __init__(self,x,y,levelnumber, char, **kwargs):
        GameObject.__init__(self, x,y,levelnumber, char, **kwargs)
        self.itemkeys = [] # list of of itemkeys that the monster carry
        self.hitpoints = 5
        self.mood = "roam"
        self.energy = random.randint(15,25)
        self.lowenergy = 10
        self.highenergy = 30
        
    def update(self):
        if self.mood == "roam":
            # move around
            self.energy -= 1 # roaming cost energy
            if self.energy < self.lowenergy:
                self.mood = "sleep"
        elif self.mood == "sleep":
            self.energy += 1 # sleeping regains energy
            if self.energy > self.highenergy:
                self.mood = "roam"
        
    
class Player(GameObject):
    """the player"""
    def __init__(self,x,y,levelnumber, char, **kwargs):
        GameObject.__init__(self, x,y,levelnumber, char, **kwargs)
        self.itemkeys = [] # list of itemkeys that the player carrys
        self.hitpoints = 50
        self.msg = ""
        
    def checkmove(self,dx, dy):
        newx = self.x + dx
        newy = self.y + dy
        newgroundcharnumber = Game.level[self.levelnumber].pos[(newx, newy)]
        newgroundchar = GameObject.book[newgroundcharnumber].char
        if newgroundchar in "#X":
            self.msg = "Moving not possible. You can not walk into %s" % Game.tiledict[newgroundchar][0]
            return False
        else:
            # check if moving into a monster
            mokeys = Game.level[self.levelnumber].monsterkeys
            for mk in mokeys:
                if GameObject.book[mk].x == newx and GameObject.book[mk].y == newy:
                    self.msg = "Moving not possible, You can not walk into a monster. Try action instead."
                    return False
            return True
        
    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.msg = "Moving (dx: %i dy: %i) sucessfull" % (dx, dy)
    
    def inventory(self):
        """returns a big string listing the players inventory"""
        if len(self.itemkeys) == 0:
            return "Your inventory is empty."
        else:
            t = "You carry those items in your inventory:\n"
            for i in self.itemkeys:
                t+= GameObject.book[i].longtext + "\n"
            return t
    
    def playeractionlist(self, adx=0, ady=0): # actionlist was already used in GameObject.actionlist
        x = self.x + adx
        y = self.y + ady
        li = []
        # ground tile actions
        gl = GameObject.book[Game.level[self.levelnumber].pos[(x,y)]].actionlist
        for groundaction in gl:
            li.append( groundaction + " " + GameObject.book[Game.level[self.levelnumber].pos[(x,y)]].shorttext)
        actionitemkeys = []
        for k in Game.level[self.levelnumber].itemkeys:
            if GameObject.book[k].x == x and GameObject.book[k].y == y:
                actionitemkeys.append(k)
        for ak in actionitemkeys:
            aklist = GameObject.book[ak].actionlist
            for aka in aklist:
                li.append( aka + " " + GameObject.book[ak].longtext )
        monsterkeys = Game.level[self.levelnumber].monsterkeys
        actionmonsterkeys = []
        for mk in monsterkeys:
            if GameObject.book[mk].x == x and GameObject.book[mk].y == y:
                actionmonsterkeys.append(mk)
        for monsterkey in actionmonsterkeys:
            ml = GameObject.book[monsterkey].actionlist
            for action in ml:
                li.append( action + " " + GameObject.book[monsterkey].shorttext)
        return li # the actionlist is returned
        
    
    def pickup(self):
        foundlist = Game.level[self.levelnumber].pickup(self.x, self.y)
        if len(foundlist) == 0:
            self.msg = "i found no items here to pick up"
        else:
            for f in foundlist:
                self.itemkeys.append(f)
                i = Game.level[self.levelnumber].itemkeys.index(f)
                del Game.level[self.levelnumber].itemkeys[i]
            self.msg = "%i item(s) picked up and added to inventory" % len(foundlist)
    
    def show_inventory(self):
        """returns a big sting with each itemnumber and itemdescription of the player's inventory"""
        if len(self.itemkeys) == 0:
           return "The inventory is empty!"
        t = ""
        for k in self.itemkeys:
            t += "\n" + str(k)+ " : " + GameObject.book[k].longtext 
        return t
    
    def drop(self, itemnumber):
        """drop item with itemnumber on the floor, removing it from inventory and adding it to level"""
        if itemnumber in self.itemkeys:
            # update Item x,y with player x,y
            GameObject.book[itemnumber].x = self.x
            GameObject.book[itemnumber].y = self.y
            Game.level[self.levelnumber].itemkeys.append(itemnumber)
            i = self.itemkeys.index(itemnumber)
            del self.itemkeys[i]
            self.msg = "item dropped"
        else:
            self.msg = "illegal itemnumber. dropping canceled"
    


def main():
    """ the main function of the game contains the game loop and is creating / calling all the class methods"""
    
    rawlevel ="""\
XXXXXXXXXXXXXXXXXX
X??....?...##.?..X
X....?..:...d....X
Xtb....t..?##...>X
X.<........##..t.X
X..........##t.<.X
X....tt....dd....X
X..........##....X
X#######..####.##X
X#######..####d##X
X..........#....:X
X..b...:...##M@:?X
X.s....?...######X
X.t........##tt.tX
XXXXXXXXXXXXXXXXXX"""
     
     
     
    # init level 1
    ln = 1 # LevelNumber
    mylevel = Level(rawlevel, ln)
    p = Game.player
    print("output:")
    print(Game.output.make_screenstring())
    gameloop = True
    while gameloop:
        print("press: \n(numpad keys): move (q): quit (p): pickup (d): drop (i): inspect (a): action ")
        i = input(">")
        i = i.lower()
        if i == "q":
           gameloop = False
        elif i in Game.dirs.keys():
            dx, dy = Game.dirs[i]
            if p.checkmove(dx, dy):
                p.move(dx,dy)
                Game.output.drawlevel(ln)
                print(Game.output.make_screenstring())
        elif i == "p": #pickup
            p.pickup()
        elif i == "d": # drop
            print(p.show_inventory())
            i = input("enter number to drop or (c) to cancel")
            p.drop(int(i))
        elif i == "i": # inspect tile where i stand and inventory
            print("press numpad key for inspecting neighboring tile, 5 for inspecting this tile")
            i2 = input("inspect in direction? >")
            if i2 in Game.dirs:
                idx, idy = Game.dirs[i2]
                print("You are on tile x:%i y;%i and inspect x:%i y:%i" % (p.x, p.y, p.x+idx, p.y+idy))
                print(mylevel.inspect(p.x+idx, p.y+idy))
                print("----Your inventory:----")
                print(p.inventory())
                p.msg = "" # clear player status message
            else:
                p.msg = "unknown direction for inspecting. inspecting canceled"
            
        elif i == "a":
            print("press numpad key for action at neighboring tile, 5 for action on this tile")
            i2 = input("action direction? >")
            if i2 in Game.dirs:
                adx, ady = Game.dirs[i2]
                print("You are on tile x:%i y;%i. Choose an action to perform at x:%i y:%i" % (p.x, p.y, p.x+adx, p.y+ady))
                alist = p.playeractionlist(adx, ady)
                for action in alist:
                    print( "%i: %s" % ( alist.index(action) , action))
                print("please enter desired action number or q to cancel")
                i3 = input("action number? >")
                if i3.lower() == "q" or int(i3) not in range(len(alist)):
                    p.msg = "unknown action number. action canceled"
                else:
                    p.msg = "You try to perform this action: %s" % alist[int(i3)]   
                #p.msg = "" # clear player status message
            else:
                p.msg = "unknown direction for action. action canceled"
        if p.msg: # if p.msg != ""
            print(p.msg)
    print("game over. bye !")

if __name__ == '__main__':
    main()



## old code , use , move, and delete:

#    def __init__(self, char, **kwargs):
#        for attr in kwargs.keys(): 
#            if attr in self.__dict__:
#                self.__dict__[attr] = kwargs[attr]
#    def showStats(object):
#        """display all stats of an class instance"""
#        for key in object.__dict__:
#            print( key, ":", object.__dict__[key])



