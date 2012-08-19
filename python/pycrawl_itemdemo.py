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
# there can be several Items (trap, loot etc. ) on the same x y position
# there can only be one single monster or player at the same x y position ( but several items !)

# a dead monster is no longer an instance of the monster class but instead an instance of the item class ( a dead body )
# monsters are placed in the level and are also running around
# monsters have a primitive state machine (moods): if they run around some time, they get tired and sleep for a while
# if a monster runs over a trap too often it dies and drops an monster corpse item

import random

#mylevel = """\
#XXXXXX
#X.@M.X
#XXXXXX\
#"""

mylevel ="""\
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
X..........#.....X
X..b...:...##M@:?X
X.s....?...######X
X.t........##tt.tX
XXXXXXXXXXXXXXXXXX\
"""


class Tile(object):
    """the level or map is made out of ascii tiles. the properties of the tiles are defined here"""
    tiledict = {} # a dict for all the different tiles
    def __init__(self, char, **kwargs):
        self.char = char
        self.text = ""
        Tile.tiledict[char] = self # put this new Tile into the tiledict
        self.stepin = True # can the player step into this tile ? walls, fire etc: False
        self.action = [] # possible actions on this tile
        self.description = "" # text to be displayed
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
Tile(".", z=0, text="a floor tile", description = "an empty boring space. There is really nothing here.")
Tile("d", z=0, text="a door", description = "an (open) door", action=["open","close"])
Tile("<", z=0, text="a stair up", description = "a stair up to the previous level", action = ["climb up"])
Tile(">", z=0, text="a stair down", description = "a stair down to the next deeper level", action = ["climb down"])
Tile("s", z=0, text="a shop", description = "a shop of a friendly merchant", action=["go shopping"])
# items etc, transportable , z=1
Tile("t", z=1, text="a trap", description = "a dangerous trap !", action = ["disarm", "destroy", "flag"])
Tile("m", z=1, text="a dead monster", description = "a dead monster. Did you kill it?", action=["eat","gather trophy"])
Tile("?", z=1, text="a heap of loot", description = "a heap of loot. Sadly, not yet programmed. But feel yourself enriched" ) # will be seperated into single items
Tile("b", z=1, text="a box", description = "a box. You wonder what is inside. And if it is trapped", action=["force open", "check for traps"])
Tile(":", z=1, text="a single item", description = "a single item. add one more item and you have a heap of loot", action=["pick up / drop"])
# monsters etc, self-moving, z=2
Tile("@", z=2, text="the player", description = "the player. that is you.",  stepin = False, action = ["write grafitti"], blocksight=True)
Tile("M", z=2, text="a living monster",  stepin = False, monster=True, description = "a living monster. You can kill it. It can kill you !", action=["attack","feed","talk"])
Tile("Z", z=2, text="a sleeping monster",  stepin = False, description = "a sleeping monster. You can kill it while it sleeps !", action=["attack","feed","talk"])


class Item(object):
    """generic item class for (transportable) items"""
    number = 0
    book = {}
    def __init__(self, char, x,y, levelnumber):
        """get most attributes from Tile class or generate them now"""
        Item.number += 1
        #self.parent = parent
        self.number = Item.number
        self.book[self.number] = self
        self.x = x
        self.y = y
        self.levelnumber = levelnumber
        self.char = char
        self.text = Tile.tiledict[self.char].text
        if self.char== ":": # a single item    
            self.description = self.generate_text()
            self.text = self.description.split()[-1] # take last word of description
        else:
            self.description = Tile.tiledict[self.char].description   
        self.actions = Tile.tiledict[self.char].action
        
    def generate_text(self):
        """generate a random description for this item for the very lazy coder"""
        word1 = random.choice(("a big", "a small", "a medium", "an epic", "a handsome","a rotting", "an expensive", "a cheap"))
        word2 = random.choice(("yellow", "green", "blue", "red", "white", "black","rusty", "shiny", "blood-smeared"))
        word3 = random.choice(("ring", "drink", "flower", "wand", "fruit"))
        return " ".join((word1, word2, word3)) # put space between words

#class Game(object):
#    """root class containing player, Levels score system etc"""
#    player = None
#    level = {}
#    turns = 0
#    score = 0
#    directions =[(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]  # this is a constant
#    #def __init__(self):
#    #    pass

class Level(object):
    """the Level object is created with a map string and has elegant methods
    to get an specific tile (at position x,y) or set an specific tile or
    to return the whole level
    
    The level is the most important classes. It has as class attribute the player instance
    and each level has a dict of moving Monsters as well as a list of (not-moving) items"""
    number = 0
    book = {} # the book of levels. the level instances are stored here
    player = None # the player class instance will be stored here
    directions =[(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]  # this is a constant
    def __init__(self, rawlevel):
        """raw level comes directly from a creative player and has walls, items and monsters all together.
        The tiles are orderd by z coordinate (see class Tile)
        z= 0 , the groundmap for nonmoving stuff like walls
        z= 1 , the (non-moving) items. Stored in the itemlist of each level
        z= 2,  the (moving) monsters, stored in the movingdict of each level
        """
        Level.number += 1  # create an unique levelnumber (class attribute)
        self.number = Level.number # assign unique levelnumber as instance attribute)
        Level.book[self.number] = self # store instance itself into Level.book
        self.ground_map = list(map(list, rawlevel.split())) # at them moment all stuff, but later only non-moving stuff like walls ( z=0 )
        self.rows = len(self.ground_map)  # width of the level in chars
        self.cols = len(self.ground_map[0]) # height of the level in chars
        self.movingdict = {} # all the moving things ( monster and player) in this level ( key = movingthingsnumber)
        self.itemlist = []  # all the items in this level. Structure inside the list: ( itemnumber)
        #print(self.ground_map, self.rows, self.cols)
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
                    if rawchar == "?":
                        for i in range(random.randint(2,5)): # a heap of random items
                            myitem = Item(":", x,y,self.number) # create random single Item instance
                            self.itemlist.append(myitem.number)     # append item instance to itemlist of this level
                    else:
                            myitem = Item(rawchar, x,y,self.number) # create Item of rawchar instance
                            self.itemlist.append(myitem.number)     # append item instance to itemlist of this level
                elif Tile.tiledict[rawchar].z == 2:
                    # this is a monster. delete from ground_map an put into monster_map
                    self.ground_map[y][x] = "." # empty space floor tile
                    # is it the player himself ?
                    if rawchar == "@":
                        Level.player = Player("@",x,y,self.number) #create player instance
                    else: # create Monster class instance ( will be stored in Movingobject.book )
                        Monster(rawchar, x, y, self.number)
        
    def playerupdate(self):
        """of all things in  movingdict call update method only for the player"""
        #for mokey in self.movingdict: # the same as in firstlevel.movingdict.keys()
        #    if self.movingdict[mokey] == Level.player.number:
        self.movingdict[Level.player.number].update() # should test if player is alive
                #firstlevel.movingdict[mo].update()
        
        
    def monsterupdate(self):
        """iterates over all alive monster -but not the player- in movingdict and call update method"""
        for mokey in self.movingdict:
            if mokey != Level.player.number and self.movingdict[mokey].alive:
                #print ("monsterupdate for ", mokey)
                self.movingdict[mokey].update()
                
        
        
        
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
    
    def getitemlist(self, x,y):
        """get a list of item numbers (including traps) at x,y position"""
        #itemlist = []
        #for myitemnumber in self.itemlist:
        #    if Item.book[myitemnumber].x == x and Item.book[myitemnumber.y == y]:
        #        itemlist.append(itemnumber)
        #return itemlist
        return [nu for nu in self.itemlist if Item.book[nu].x == x and Item.book[nu].y == y]
        
    
    def monstertest(self, x, y): # write filter function ?
        """return the char of a monster if a monster is at x,y or returns empty string"""
        for mokey in self.movingdict:
            if self.movingdict[mokey].x == x and self.movingdict[mokey].y == y:
                return self.movingdict[mokey].char
        return "" #False # no moving object at x,y
    
    def getmonsternumber(self, x,y):  # can this replace monstertest ?
        """return the number of the monster at x,y or False if no monster at x y"""
        for mokey in self.movingdict:
            if self.movingdict[mokey].x == x and self.movingdict[mokey].y == y:
                return mokey
        return False # found no monster
    
    def __str__(self):
        """producing screenstring for output
        """
        screenstring = ""
        for y in range(self.rows):
            for x in range(self.cols):
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
    z=2 for level.monstermap
    also things like a sleeping monsters that currently does not move
    but *could* move any turn"""
    number = 0 # unique number for each  moving object
    #book = {} # the big book of moving objects where each monster/player instance will be stored
    
    def __init__(self, char, x, y, levelnumber):
        """create moveable object"""
        MovingObject.number += 1                # get unique number from class variable
        self.number = MovingObject.number
        # the movingobject lives inside the movinglist of the level
        Level.book[levelnumber].movingdict[self.number] = self
        self.char = char
        self.x = x # position
        self.y = y
        self.dx = 0  # speed
        self.dy = 0
        self.levelnumber = levelnumber
        self.alive = True # also for objects. not alive objects get no update() method in the mainloop
     
    def update(self):
        #print( "this is movingObjectUpdate for ", self.number)
        self.x += self.dx
        self.y += self.dy
        
    def checkmove(self, dx, dy):
        """test if moving into direction dx and dy is possible (not a wall). if yes, return True, else, return False"""
        #if dx == 0 and dy == 0:
        #    #no move, that is always allowed:
        #    return True
        #else:
        targetchar = Level.book[self.levelnumber][self.x + dx, self.y + dy] # the char where i want to go into (hopefully not a wall)
        if not Tile.tiledict[targetchar].stepin: # not allowed on groundmap
            return False
        else:
            # groundmap is ok, now testing for monsters blocking the path
            #monsterchar = Level.book[self.levelnumber].monstertest(self.x + dx, self.y + dy)
            #print("found monster: ", monsterchar)
            #monsterlist = [mo for mo in Level.book[self.levelnumber].movingdict if Level.book[self.levelnumber].movingdict[mo]]
            mokey = Level.book[self.levelnumber].getmonsternumber(self.x + dx, self.y + dy)
            #print("i'm number", self.number, "and want to go to",dx,dy, " and found monster number:", mokey)
            if mokey: # i mokey != False
                if mokey == self.number:
                    #print("i found myself, hahaha")
                    return True # it is allowed to go to a position where you already are (dx and dy == 0)
                else:
                    #print("i found someone blocking")
                    return False
            return True # found nobody
            
            #if monsterchar != "":
                # there is a monster in the path where i want to go ! Attacking ?
                #print("i want to got to %i,%i but there is already something"%(self.x + dx, self.y+dy))
                #return False
            # no blocking monsters ?
            #
            #return True
                
    
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
        #print("Monsterupdate")
        if Level.book[self.levelnumber].traptest(self.x, self.y):
            # i'm on a trap !
            self.hitpoints -= 1
            if self.hitpoints <= 0:
                self.kill()
           
            
        if self.mood == "sleep": # monster is sleeping
            self.char = "Z"
            self.dx = 0
            self.dy = 0
            self.energy += 1 # sleeping regains energy
            if self.energy > 50:
                self.mood = "roam"
        else:                     # monster is awake
            self.char = "M"
            # check possible movements (north, north-west ect.) ( dx, dy)
            # i wanted to delete the illlegal directions while iterating over the direction list
            # but i learned that this is a big NONO. instead, create a new list with valid direcitons
            #validdirections = [d for d in Game.directions if self.checkmove(d[0],d[1])] 
            #mydir = random.choice(validdirections) # i could merge this line with the previous line
            # choose a random valid direction to move (dx,dy)
            mydir = random.choice([d for d in Level.directions if self.checkmove(d[0],d[1])] )
            self.dx = mydir[0]
            self.dy = mydir[1]
            #print("i choose %i %i" % (self.dx, self.dy))
            self.energy -= 1 # to be active makes the monster tired
            if self.energy < 30:
                self.mood = "sleep"
        MovingObject.update(self) # call the update method of MovingObject to update x, y etc.

class Player(MovingObject):
    """The player is much like a monster also a moving object"""
    def __init__(self, char, x, y, levelnumber):
        MovingObject.__init__(self, char, x, y, levelnumber)
        # i'm sexy and i know it - all my core values like x, y are already stored in MovingObjects
        self.hitpoints = 100
        self.itemlist=[]
            
    def update(self):
        # change stats like hungry, healing etc here
        #pass # as none of that is coded i need at least a pass statement or the update method would not work
        #print("playerupdate")
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
        text = Tile.tiledict[Level.book[self.levelnumber][self.x,self.y]].text
        itemlist = Level.book[self.levelnumber].getitemlist(self.x, self.y)
        if itemlist: # if len(itemlist) > 0:
            corrector = 0
            if Level.book[self.levelnumber].traptest(self.x, self.y):
                text += " and a trap"
                corrector = 1
            otheritems = len(itemlist) - corrector
            if otheritems == 1:
                text += " and one item" 
            else:
                text += " and %i items" % otheritems
        return  "You (@) are at position %i, %i with %i hitpoints on %s.\n Press those keys and ENTER:" % ( self.x, self.y, self.hitpoints, text)
    
    def badmove(self, dx, dy):
        """only call this method after a checkmove() returned False"""
        ground = Tile.tiledict[Level.book[self.levelnumber][self.x + dx, self.y + dy]]
        if not ground.stepin:
            reason = ground.text
        else:
            monsterchar = Level.book[self.levelnumber].monstertest(self.x+dx, self.y + dy)
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
        actions = []
        # append actions from groundmap
        for a in Tile.tiledict[firstlevel[Level.player.x, Level.player.y]].action:
            actions.append("%s: %s"%(Tile.tiledict[firstlevel[Level.player.x, Level.player.y]].text, a ))
        #actions.extend( Tile.tiledict[firstlevel[Level.player.x, Level.player.y]].action)
        itemlist = firstlevel.getitemlist(Level.player.x, Level.player.y)
        for i in itemlist:
            for a in Item.book[i].actions:
                actions.append("%s: %s" % (Item.book[i].text, a))
        print(actions)
        if len(actions) == 0:
            actiontext = ""
        else:
            actiontext = "action: a"
        # input
        inputtext = "to move (wait): numpad 84269713 (5) %s examine: d inventory: i quit: q" % actiontext
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
            text = "You see: %s" % Tile.tiledict[firstlevel[Level.player.x,Level.player.y]].description
            # there can be no monster on this tile because the player is on this tile
            # text += firstlevel.monstertest(x,y)
            itemlist = firstlevel.getitemlist(Level.player.x,Level.player.y)
            if itemlist: # the same as if len(itemlsit) > 0:
                text = "You see: %s" % Tile.tiledict[firstlevel[Level.player.x,Level.player.y]].text
                # this is only a list of itemnumbers 
                for itemnumber in itemlist:
                   text+="\n and " + Item.book[itemnumber].description
            print("--------- more detailed description -------")
            print(text)
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
            firstlevel.playerupdate() # i get monster wandering into the player if i delete this line
            #player.update() not needed because the player isupdated with all movingobjects some lines below
            #player.move(dx,dy)
        else:
            print( Level.player.badmove(dx,dy))
            showtext = False
            continue
        showtext = True
        # update (move) all moveableobjects (monsters)
        firstlevel.monsterupdate()
        #for mo in firstlevel.movingdict: # the same as in firstlevel.movingdict.keys()
        #    if firstlevel.movingdict[mo].alive:
        #        firstlevel.movingdict[mo].update()
        # output level
        print(firstlevel)
        if Level.player.hitpoints <= 0:
            print("you are dead. try to avoid traps in the future")
            break
if __name__ == '__main__':
    main()

