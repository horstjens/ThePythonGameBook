# pycrawl_itemdemo
# my very own rogulike game
# because i play far too much dungeon crawl stone soup
# 2012 by Horst JENS   horstjens@gmail.com
# license: gpl3 see http://www.gnu.org/copyleft/gpl.html
# this game is a part of http://ThePythonGameBook.com

# this is a demo where the player (@) runs around in some small rooms.
# the player can pick up and drop items. he also has an inventory
# later on, certain monsters should also be able to pick up at last one item
#
# some ideas were the items are placed vertically:
# each "thing" in a level should have a z coordinate
# z 0 is the floor, some items on it are on z 1
# monsters and players are on z 2
# ( i have to stop myself now and not invent pycraft, made out of blocks in 3 dimensions )
#
#
# also there can be several items sharing the same x y z position.
# this items should form a list


# a dead monster is no longer an instance of the monster class but instead an instance of the item class ( a dead body )
# monsters are placed in the level and are also running around
# monsters have a primitive state machine (moods): if they run around some time, they get tired and sleep for a while

import random


mylevel ="""\
XXXXXXXXXXXXXXXXXX
XM?....M...##.M..X
X....M......d....X
Xtb....t..?##...>X
X.<........##..t.X
X..........##t.<.X
X....tt....dd....X
X..........##....X
X#######..####.##X
X#######..####d##X
X..........##.M.?X
X..b...M...##..@.X
X.s....M...######X
X.t........##ttMtX
XXXXXXXXXXXXXXXXXX\
"""


class Item(object):
    """any transportable thing. can be a weapon, a gem, a sroll, a skull etc."""
    def __init__(self, name):
        self.name = name
        # fixme ---- continue working from here

class Tile(object):
    """the level or map is made out of ascii tiles. the properties of the tiles are defined here"""
    tiledict = {} # a dict for all the different tiles
    def __init__(self, char, **kwargs):
        self.char = char
        self.text = ""
        #Tile.tileset.add(char) # put this new Tile into the tileset
        Tile.tiledict[char] = self # put this new Tile into the tiledict
        self.stepin = True # can the player step into this tile ? walls, fire etc: False
        #self.interact = False
        self.action = [] # possible actions on this tile
        self.description = "" # text to be displayed
        #self.moveable = False
        #self.monster = False
        self.blocksight = False # if the line of sight is blocked by this tile (like a wall) or not (like a trap or floor)
        #self.attackable = False
        self.z = 0 # walls (immobile have z=0, items (transportable) have z=1, monsters (moving) have z=2)
        
        for attr in kwargs.keys(): 
            if attr in self.__dict__:
                self.__dict__[attr] = kwargs[attr]
                
    def showStats(object):
        """display all stats of an class instance"""
        for key in object.__dict__:
            print( key, ":", object.__dict__[key])

# walls etc, z=0, immobile
Tile("X", z=0, text="an outer wall",  description = "an outer wall of the level. You can not go there", stepin = False, action = ["write grafitti"], blocksight=True)
Tile("#", z=0, text="an inner wall", description = "an inner wall. You may destroy this wall with the right tools or spells", stepin = False, blocksight = True)
Tile(".", z=0, text="an empty space", description = "an empty boring space. There is really nothing here.")
Tile("d", z=0, text="a door", description = "an (open) door", action=["open","close"])
Tile("<", z=0, text="a stair up", description = "a stair up to the previous level", action = ["climb up"])
Tile(">", z=0, text="a stair down", description = "a stair down to the next deeper level", action = ["climb down"])
Tile("s", z=0, text="a shop", descriptoin = "a shop of a friendly merchant", action=["go shopping"])
# items etc, transportable , z=1
Tile("t", z=1, text="a trap", description = "a dangerous trap !", action = ["disarm", "destroy", "flag"])
Tile("m", z=1, text="a dead monster", description = "a dead monster. Did you kill it?", action=["eat","gather trophy"])
Tile("?", z=1, text="a heap of loot", description = "a heap of loot. Sadly, not yet programmed. But feel yourself enriched", action=["pick up"])
Tile("b", z=1, text="a box", description = "a box. You wonder what is inside. And if it is trapped", action=["force open", "check for traps"])
Tile(":", z=1, text="a single item", description = "a single item. add one more item and you have a heap of loot", action=["pick up"])
# monsters etc, self-moving, z=2
Tile("@", z=2, text="the player", description = "the player. that is you.",  stepin = False, action = ["write grafitti"], blocksight=True)
Tile("M", z=2, text="a living monster",  stepin = False, monster=True, description = "a living monster. You can kill it. It can kill you !", action=["attack","feed","talk"])
Tile("Z", z=2, text="a sleeping monster",  stepin = False, description = "a sleeping monster. You can kill it while it sleeps !", action=["attack","feed","talk"])



class Item(object):
    """generic item class for (transportable) items"""
    number = 0
    book = {}
    def __init__(self, char, x,y, levelnumber, descr="" ):
        Item.number += 1
        #self.parent = parent
        self.number = Item.number
        self.book[self.number] = self
        #self.parent.items[self.number] = self
        self.x = x
        self.y = y
        self.levelnumber = levelnumber
        self.char = char
        #self.description = description
        if self.char== ":": # a single item
            if descr == "":
                self.description = self.generate_text()
            else:
                self.description = descr
        else:
            self.description = Tile.tiledict[self.char].description
        # x,y : items itself has no self.x nor self.y
        # instead, it "lives" either inside a "parent" container (another item, the player or monster)
        # or lies around in the floor of an level
        
    def generate_text(self):
        """generate a random description for this item for the very lazy coder"""
        word1 = random.choice(("big", "small", "medium", "epic", "handsome","rotting", "expensive", "cheap"))
        word2 = random.choice(("yellow", "green", "blue", "red", "white", "black","rusty", "shiny", "blood-smeared"))
        word3 = random.choice(("ring", "drink", "flower", "wand", "fruit"))
        return word1 + word2 + word3



class Level(object):
    """the Level object is created with a map string and has elegant methods
    to get an specific tile (at position x,y) or set an specific tile or
    to return the whole level"""
    number = 0
    book = {}
    player = None # the player class instance will be stored here
    def __init__(self, rawlevel):
        """raw level comes directly from a creative player and has walls, items and monsters all together.
        Three different maps will be created:
        z= 0 , the groundmap for nonmoving stuff like walls
        z= 1 , the itemmap, for transportable stuff like items, traps, corpses etc.
        z= 2,  the monstermap, for self-moving stuff like monsters and the player
        """
        Level.number += 1
        self.number = Level.number
        Level.book[self.number] = self # store itself into Level.book
        self.ground_map = list(map(list, rawlevel.split())) # at them moment all stuff, but later only non-moving stuff like walls ( z=0 )
        self.rows = len(self.ground_map)  # width of the level in chars
        self.cols = len(self.ground_map[0]) # height of the level in chars
        # at the moment, only one item per xy position is allowed FIXME: make list to handle heap of items at xy position
        #self.item_map = [list("" for c in range(self.cols)) for r in range(self.rows)] # empty textstring for item in each xy position ( z=1)
        #self.monster_map = [list("" for c in range(self.cols)) for r in range(self.rows)] # empty textstring for monster in each xy positoin ( z=2)
        self.movingdict = {} # all the moving things ( monster and player) in this level ( key = movingthingsnumber)
        self.itemlist = []  # all the items in this level. Structure inside the list: ( itemnumber)
        
        print(self.ground_map, self.rows, self.cols)
        # sort out messy raw level map and seperate chars into ground, items and monsters ( z:0,1,2 )
        for y in range(self.rows):
            for x in range(self.cols):
                rawchar = self.ground_map[y][x]
                if Tile.tiledict[rawchar].z == 0:
                    # this is really a wall or a thing that belongs to ground_map 
                    pass
                elif Tile.tiledict[rawchar].z == 1:
                    # this is an item. delete from groundmap
                    self.ground_map[y][x] = "." # empty space floor tile
                    myitem = Item(rawchar, x,y,self.number) # create Item instance
                    self.itemlist.append(myitem.number)
                    
                elif Tile.tiledict[rawchar].z == 2:
                    # this is a monster. delete from ground_map an put into monster_map
                    self.ground_map[y][x] = "." # empty space floor tile
                    # is it the player himself ?
                    if rawchar == "@":
                        Level.player = Player("@",x,y,self.number) #create player instance
                    else: # create Monster class instance ( will be stored in Movingobject.book )
                        Monster(rawchar, x, y, self.number)
        
        
    def __getitem__(self, xy):
        """get the char of groundmap at position x,y (x,y start with 0)
        """
        x, y = xy
        return self.ground_map[y][x] # row, col

    def __setitem__(self, xy, item):
        """ x (col) and y (row) position of char at groundmap to set. (x and y start with 0)"""
        x, y = xy
        self.ground_map[y][x] = item # row, col
        
    #def __iter__(self, z=0):
    #        return ("".join(row) for row in self.ground_map)
    def traptest(self, x, y):
        """return True if on position xy is a trap ( in level.itemlist)
        else return False"""
        for myitemnumber in self.itemlist: # create a filter function istrap() and filter instead ?
            if Item.book[myitemnumber].char == "t":
                if Item.book[myitemnumber].x == x and Item.book[myitemnumber].y == y:
                    return True
        return False
    
    def monstertest(self, x, y): # write filter function ?
        """return the char of a monster if a monster is at x,y or returns empty string"""
        for mokey in self.movingdict:
            if self.movingdict[mokey].x == x and self.movingdict[mokey].y == y:
                return self.movingdict[mokey].char
        return "" #False # no moving object at x,y
        
    def __str__(self):
        """producing screenstring for output
        """
        screenstring = ""
        for y in range(self.rows):
            for x in range(self.cols):
                #monsterchar = "" # draw a monster at x,y ?
                #for mything in self.movingdict: # in self.movingdict.keys() works also
                #    if self.movingdict[mything].x == x and self.movingdict[mything].y == y:
                #        monsterchar = self.movingdict[mything].char
                #        break # there can only be one monster at one x,y position. not necessary to calculate stuff below this monster
                monsterchar = self.monstertest(x,y)
                if monsterchar != "":
                    screenstring += monsterchar   
                else:
                    # it is not a monster. maybe it is an item ?
                    itemchar = "" # draw one or more items ?
                    for mything in self.itemlist:
                        if Item.book[mything].x == x and Item.book[mything].y == y:
                            itemchar += Item.book[mything].char
                    if len(itemchar) > 1:
                        screenstring +="?" # heap of items
                    elif len(itemchar) == 1:
                        screenstring += itemchar # exactly one item
                    else:
                        # no monster, no item.... get the groundmap
                        screenstring += self.ground_map[y][x]
            screenstring += "\n" # end of line
        return screenstring
    


class MovingObject(object):
    """anything that moves, like a player, a monster or an arrow
    z=2 for level.monstermap"""
    number = 0 # unique number for each  moving object
    #book = {} # the big book of moving objects where each monster/player instance will be stored
    
    def __init__(self, char, x, y, levelnumber):
        """create moveable object"""
        MovingObject.number += 1                # get unique number from class variable
        self.number = MovingObject.number
        #MovingObject.book[self.number] = self   # store yourself into class dict ( book )
        # the movingobject lives inside the movinglist of the level
        Level.book[levelnumber].movingdict[self.number] = self
        self.char = char
        self.x = x # position
        self.y = y
        self.dx = 0  # speed
        self.dy = 0
        self.levelnumber = levelnumber
        self.alive = True # also for objects. not alive objects get no update() method in the mainloop
        #self.original = "" # what was there before i was there.... nothing !
        #self.paint()
     
    def update(self):
        #pass # this method is only here to be overwritten by child objects.
        #self.clear()   # correct movement with restoring original floor tiles
        self.x += self.dx
        self.y += self.dy
        #self.original = Level.book[self.levelnumber][self.x, self.y, 2]
        #self.paint()
        
    #def clear(self):
        #"""clear myself and restore the original (empty) char of the level monster_map (z=2) on my position"""
        #Level.book[self.levelnumber][self.x,self.y] = self.original
        
    #def paint(self):
        #Level.book[self.levelnumber][self.x,self.y] = self.char
        
    def checkmove(self, dx, dy):
        """test if moving into direction dx and dy is possible (not a wall). if yes, return True, else, return False"""
        if dx == 0 and dy == 0:
            #no move, that is always allowed:
            return True
        else:
            targetchar = Level.book[self.levelnumber][self.x + dx, self.y + dy] # the char where i want to go into (hopefully not a wall)
            if not Tile.tiledict[targetchar].stepin: # not allowed on groundmap
                return False
            else:
                # now testing for monsters
                monsterchar = Level.book[self.levelnumber].monstertest(self.x + dx, self.y + dy)
                if monsterchar != "":
                    # there is a monster in the path where i want to go ! Attacking ?
                    #print("i want to got to %i,%i but there is already something"%(self.x + dx, self.y+dy))
                    return False
                # no blocking monsters ?
                return True
                

  
    
    
class Monster(MovingObject):
    """Monster class. monster have hitpoints and a state ( attack, roam, sleep, flee)"""
    #number = 0 # unique number for each monster
    #book = {} # the big book of monsters where each monster instance will be stored
    def __init__(self, char, x, y, levelnumber, **kwwargs):
        MovingObject.__init__(self, char, x, y, levelnumber) # calling parent object method)
        #self.char = char # char is already stored in MovingObject !
        self.shortname = "a monster"
        self.hitpoints = 10
        self.moods = ["sleep", "roam", "attack", "flee"]
        self.mood = random.choice(self.moods[0:2])
        self.sensorradius = 4 # aggro. how close the player must come to get the monster's attention
        self.energy = random.randint(1,100) # below 30, monster want to sleep, above 50, monster is awake
        #self.alive = True #  this is already set True in movingobjects
    
    def kill(self):
        """Monster is no longer alive. remove yourself from MovingObjects and create an corpse item at current position"""
        # create an item an this position:
        #Level.book[self.levelnumber][self.x, self.y, 2] = "" # delete myself from Level.monstermap
        mycorpse = Item("m", self.x, self.y, self.levelnumber ) # create dead corpse Item instance
        Level.book[self.levelnumber].itemlist.append(mycorpse.number) # place corpse Item number into actual Level's Itemlist
        #Level.book[self.levelnumber][self.x, self.y, 1] = "m" # create a dead corpse char on Level.itemmap
        # remove myself from movingobjects
        # it is not such an hot idea to del() the Monster from the movingdict because movingdict get iterated at runtime
        self.alive = False
        self.x = -1 # parking position for dead moving objects
        self.y = -1
        self.dx = 0 # no more moving
        self.dy = 0
        #del(Level.book[self.levelnumber].movingdict[self.number]) # this should (in theory) remove the last exiting reference to this monster
        
    def update(self):
        """this method is called from the mainloop (haha, like in pygame!) each turn for each monster"""    
        # do i stand on a trap ?
        if Level.book[self.levelnumber].traptest(self.x, self.y):
            # i'm on a trap !
            self.hitpoints -= 1
            if self.hitpoints <= 0:
                self.kill()
           
            #self.mood = "roam" # force roaming so that monster does not sleep on traps
            
        if self.mood == "sleep": # monster is sleeping
            self.char = "Z"
            self.dx = 0
            self.dy = 0
            self.energy += 1 # sleeping regains energy
            if self.energy > 50:
                self.mood = "roam"
        else:                     # monster is awake
            self.char = "M"
            while True:
                self.dx = random.choice((-1,0,1)) 
                self.dy = random.choice((-1,0,1))
                if self.checkmove(self.dx, self.dy):
                    break
            #self.move(self.dy, self.dy) # ???
            self.energy -= 1 # to be active makes the monster tired
            if self.energy < 30:
                self.mood = "sleep"
        MovingObject.update(self)

class Player(MovingObject):
    """The player is much like a monster also a moving object"""
    def __init__(self, char, x, y, levelnumber):
        MovingObject.__init__(self, char, x, y, levelnumber)
        # i'm sexy and i know it - all my core values like x, y are already stored in MovingObjects
        self.hitpoints = 100
            
    def update(self):
        # change stats like hungry, healing etc here
        #pass # as none of that is coded i need at least a pass statement or the update method would not work
        if Level.book[self.levelnumber].traptest(self.x, self.y):
            # i'm on a trap !
            self.hitpoints -= 1
            if self.hitpoints <= 0:
                self.kill()
        MovingObject.update(self)
        
    def kill(self):
        """have to code this mind-boggling event yet"""
        print("You are dead")
        #pass
    
    def postext(self):
        return  "You (@) are at position %i, %i on %s with %i hitpoints. press:" % ( self.x, self.y, Tile.tiledict[Level.book[self.levelnumber][self.x,self.y]].text, self.hitpoints)
    
    def badmove(self, dx, dy):
        """only call this method after a checkmove() returned False"""
        ground = Tile.tiledict[Level.book[self.levelnumber][self.x + dx, self.y + dy]]
        if not ground.stepin:
            reason = ground.text
        else:
            monsterchar = Level.book[self.levelnumber].monstertest(self.x+dx, self.y + dy)
            #if monsterchar == "":
            #    print("error! badmove called for a valid tile where you can move") # i feel that a more elegant design is necessary
            reason = Tile.tiledict[monsterchar].text    
        return "Bad idea! you can not walk into %s" % reason
    
    
def main():
    """ a demo to move the player in an ascii level map"""
    
    firstlevel = Level(mylevel) # creating the level from raw file
  
    
    print(firstlevel) # first time printing
    showtext = True # for inside the while loop
    
    while True: # game loop
        # output situation text
        postext = Level.player.postext()
        #actions = Tile.tiledict[player.original].action # get the actionlist for this tile
        actions = [] # UGLY !!
        if len(actions) == 0:
            actiontext = "(no action possible)\n"
        else:
            actiontext = "for action: a and ENTER\n"
        # input
        inputtext = "to move (wait): numpad 84269713 (5) and ENTER\n" \
                  "%sto get more a more detailed description: d and ENTER\nto quit: q and ENTER] :" % actiontext
        if showtext: # avoid printing the whole text again for certain answers (action, description etc.)
            print(Level.player.postext())
            print(inputtext)
        i = input(">")
        i = i.lower()
        if "q" in i:
            break
        elif i == "4" : # west
            dx = -1
            dy = 0
        elif i  =="6": # east
            dx = 1
            dy = 0
        elif i == "8": # north
            dx = 0
            dy = -1
        elif i == "2": #south
            dx = 0
            dy = 1
        elif i == "1": # south-west
            dx = -1
            dy = 1
        elif i == "7": # north-west
            dx = -1
            dy = -1
        elif i == "9": # north-east
            dx = 1
            dy = -1
        elif i =="3": # south-east
            dx = 1
            dy = 1
        elif i == "5": # wait
            dx = 0
            dy = 0

        # ------- non-moving actions ---------
        elif i == "d":
            showtext = False
            print("--------- more detailed description -------")
            print("This is",Tile.tiledict[original].description)
            print("------ ----- -------- --------- -----------")
            continue # go to the top of the while loop
        elif len(actions) > 0 and i =="a":
            showtext = False
            print("Those are the possible actions (not yet coded, you can only look at it:)")
            print("------ list of possible actions -------")
            for action in actions:
                print(actions.index(action), action)
            print("------ ----- -------- --------- -------")
            continue # go to the top of the while loop
        else:
            print("unknown input. please enter q for quit or numpad 84261379 for moving")
            continue
        # --------- move the player --------------
        if Level.player.checkmove(dx,dy):
            Level.player.dx = dx
            Level.player.dy = dy
            #player.update() not needed because the player isupdated with all movingobjects some lines below
            #player.move(dx,dy)
        else:
            print( Level.player.badmove(dx,dy))
            showtext = False
            continue
        showtext = True
        # update (move) all moveableobjects (monsters)
        for mo in firstlevel.movingdict: # the same as in firstlevel.movingdict.keys()
            if firstlevel.movingdict[mo].alive:
                firstlevel.movingdict[mo].update()
        # output level
        print(firstlevel)
        if Level.player.hitpoints <= 0:
            print("you are dead. try to avoid traps in the future")
            break
if __name__ == '__main__':
    main()

