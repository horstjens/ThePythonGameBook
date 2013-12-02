# part of http://ThePythonGameBook.com
# (c) 2013 by Horst JENS ( horst.jens@spielend-programmieren.at )
# license: gpl3, see http://www.gnu.org/copyleft/gpl.html
# written for python3
# little adventure game with different rooms
# you can walk between the rooms
# changes:
# each item "knows" it's own location. no more inventorys for rooms and player
# item can be carried by monster: location ist then a negative monster number
# player is a child class of monster
# STATUS: does not work
# TODO: 
# * ab sucesschance bei Effect weitermachen
# * game unnötig machen?
# * user-interface von player klasse sauberer trennen

import random
import sys

if sys.version_info[0] < 3:
    print("this script need python3. You are using python 2 or lower.")
    sys.exit()
    
class Game(object):
    """
    holds all information for a game. Later it may be
    possible to load / save different games
    """
    number = 0

    def __init__(self):
        self.number = Game.number
        Game.number += 1
        self.rooms = {} # dictionary of rooms, key is room number
        self.items = {} # dictionary of items, key is item number
        self.monsters = {} # dictionary of monsters, key is monster number
        self.players = [] # dictionary of players, key is player number, value = monsternumber
        self.effects = {} # dictionary of effects (for items), key is effect name



class Monster(object):
    number = 1 # number 1 should be reserved for player

    def __init__(self, game, where= 0, adjective="", description="",
         boss=False, carrier=False):
        self.number = Monster.number
        Monster.number += 1
        game.monsters[self.number] = self # add monster into game dict
        self.adjective = adjective
        self.location = where # room number
        self.description = description
        self.hitpoints = random.randint(5,15)
        self.player = False
        self.carrier = carrier # can carry items ?
        if description == "":
            if boss:
                self.adjective = random.choice(("deadly","fantastic",
                        "creepy","ugly","epic"))
                self.description = random.choice(("dragon","cave drake",
                        "sea serpent","gorgon","giant beetle","arch druid"))
                self.hitpoints *= 5
            else:
                self.adjective = random.choice(("weak","boring",
                        "tired","cheap","old"))
                self.description = random.choice(("goblin","ork","troll",
                    "mice","rat","dwarf","spider"))

    def info(self):
        txt = "Monster number {}: {} {} with {} hitpoints\n".format(
            self.number, self.adjective, self.description, self.hitpoints)
        if self.carrier:
            txt += "This monster can carry items\n"
        return txt


class Player(Monster):
    #playernumber = 1
    def __init__(self, game, where=0, name="hero"):
        """need game instance. 
        """
        Monster.__init__(self, game, where, carrier = True)
        game.players.append(self.number) # add my monsternumber to game.players
        self.playerindex = len(game.players) - 1 
        self.name = name
        self.player = True
        self.description = "player" # overwrite monster
        self.adjective = "human"                     # overwrite monster
        #self.inventory = [] # list of itemnumbers (player carry items)
        self.maxcarry = 100 # kg
        self.carry = 0 # current mass of all carried items in kg
        #self.loaction = where # start room number

    def show_inventory(self, game):
        txt = ""
        txt += "\n==== Your inventory ====\n"        
        for itemnumber in game.items:
            #print("debug item:",itemnumber, "location:", game.items[itemnumber].location)
            if game.items[itemnumber].location == self.number * -1: # my negative monster number
                txt+="{}...{}...{} kg\n".format(itemnumber,
                      game.items[itemnumber].description, game.items[itemnumber].mass)
        
        txt += "You're currently carrying {:.2f} kg, that is {:.2f}% of your capacity".format(
            self.carry, (self.carry / self.maxcarry)*100)
        return txt  

    def list_items(self, game):
        """returns list of itemnumber
        of the items in the inventory of the player"""
        txt = ""
        items = []
        for itemnumber in game.items:
            if game.items[itemnumber].location == self.number * -1: # negative monster number
               items.append(itemnumber)
               #txt += game.items[itemnumber].description
        return items

    def pickup_item(self, game):
        txt, items = game.rooms[self.location].list_items(game)
        if len(items) >0:
            output("please select item number to pick up\n")
            output(txt)
            i = select_number(items)
            m = game.items[i].mass 
            if m > self.maxcarry:
                return "You fail to pick up this item. Reason: You can only carry {} kg. \n and try to pick up {} kg. Become stronger and try again!".format(m, self.maxcarry)
            elif m + self.carry > self.maxcarry:
                return "You fail to pick up this item. Reason: You already carry {} kg. Picking up {} would exceed your max. carry capacity of {} kg. Drop some items first or become stronger!".format(self.carry, m, self.maxcarry)
            else:
                game.items[i].location = -1 * self.number # negative monster number
                self.carry += m
            
        else: 
            return "this room has no items so there is nothing to pick up\n"

    def drop_item(self, game):
        items = self.list_items(game)
        if len(items)>0:
            output(self.show_inventory(game))
            output("select itemnumber to drop\n")
            i = select_number(items)
            game.items[i].location = self.location # drop item in my room
            self.carry -= game.items[i].mass  # update player
            return "you drop the {} to the floor\n".format(game.items[i].description)
        else:
            return "you carry no items so you can drop nothing\n"           
            
   
    def use_item(self, game):
        items = self.list_items(game)
        if len(items)>0:
            output(self.show_inventory(game))
            output("select itemnumber to use\n")
            i = select_number(items)
            if game.items[i].effect == None:
                return "this item has no effect"
            txt = ""
            game.items[i].charges -= 1
            if game.items[i].charges == 0:
                # destroy item (move to room 0)
                game.items[i].location = 0
                txt += "while using the effect, the item has destroyed itself\n"
            txt += game.effects[game.items[i].effect].action(game, victim=self.number)
            return txt
        else:
            return "you carry no items so you can use nothing"

    def nextAction(self, game):
        """ask the user to select only one of many options"""
        output("please select your next action:")
        cd = game.rooms[self.location].connectiondict(game) #cd = connectiondict
        #print("debug cd:",cd)
        txt = ""
        #txt = "goto room(s):\n"
        for roomnumber in cd:
            txt+= "{}....goto {}\n".format(roomnumber, cd[roomnumber])
        #txt += "other actions:\n"
        txt += "i....inspect inventory\nd....drop item\np....pick up item\n"
        txt += "u....use item\n"
        txt += "f....fight monsters\n"
        txt += "please type number/char and press ENTER or q and ENTER to quit\n"
        # generate valid answerlist:
        chars = ("i","d","p","u","f", "q")
        answers = []
        for roomnumber in cd:
            answers.append(str(roomnumber))
        answers.extend(chars)
        output(txt)
        answer = select_answer(answers)
        if not answer in chars:
            # room change
            self.location = int(answer)
        elif answer =="q":
            sys.exit()
        elif answer =="i":
            output(self.show_inventory(game))
        elif answer == "d":
            output(self.drop_item(game))
        elif answer == "p":
            output(self.pickup_item(game))
        elif answer == "u":
            output(self.use_item(game))
        elif answer == "f":
            output("you fight monsters. (not yet functional)")
        
class Item(object):
    number = 0

    def __init__(self, game, where=0, description="", mass=-1, effect=None, charges =1):
        """need game instance. primary key of all items is the unique
        item number, so that you can have several items with the same
        name"""
        self.number = Item.number
        Item.number += 1
        game.items[self.number] = self # add item into game dict
        self.effect = effect
        self.charges = charges # how many times you can use this effect before item is destroyed
        self.location = where # positive values are room number,
                              # negative values refer to monster(!) number
        self.description=description
        if mass == -1:
            self.mass = round(random.randint(1,50))
        else:
            self.mass = mass
        if self.description == "":
            self.description = random.choice(("helmet","chestplate","pants",
                    "shoes","small healing potion","medium healing potion",
                    "gold","sword","bow and arrows","shield", "teleport pill"))
            if self.description == "small healing potion":
                self.effect = "heal5"
            elif self.description == "medium healing potion":
                self.effect = "heal10"
            elif self.description == "teleport pill":
                self.effect = "randomteleport"


    def info(self, game):
        txt =  "Item Number {}: ".format(self.number)
        txt += self.description + "\n"
        #if self.location >= 0:
        #   #txt +="\n current location: room {}, {}".format(self.location, game.rooms[self.location].description) 
        #else:
        #    txt += "\n currently carried by {}".format(game.monsters[self.location*-1].description)
        #return txt



class Effect(object):
    def __init__(self, game, name, function, description="",  
                 arg1=0, arg2=0, success=.5):
        #victim 0 means the effect is targeted at the player (monsternumber 0)
        self.name = name
        self.function = function
        self.description = description
        self.success = success # probability .5 means it has a chance of 50% to work correct
        #self.victim = victim # if the effect is aimed at somebody
        # -1 means the effect is targeted at the first player
        #self.roomnumber=roomnunmber # if the effect is in a certain room only
        self.arg1 = arg1  # reserve
        self.arg2 = arg2  # reserve
        self
        game.effects[self.name] = self
        
    def action(self, game, victim=-1):
        """gives effect to monster with monsternumber == victim"""
        # successchance 
        luck = random.random() # TODO: add players evocation ability here
        if luck > self.success:
            return "Item FAIL ! bad luck, the item/effect refuses to work. try again ?" 
        if self.function == "teleport":
            if self.arg1 != 0:
                # teleport into specific room number
                target = self.arg1
            else:
                # random teleport
                while True:
                    target = random.choice(game.rooms)
                    if target != 0:  # anywhere but the void room
                        break
            game.monsters[victim].location = target
            return "the teleport effect works ! Victim is transported by magic into room number {}".format(target)
        elif self.function == "heal":
            game.monsters[victim].hitpoints += self.arg1
            return "healing effect works! gained {} hitpoints".format(self.arg1)
        return "unknow effect worked correctly"
           

class Room(object):
    number = 0

    def __init__(self, game, name="", description="", connections=[],
                 explored=False, itemchances=[0.5,0.25,0.1],
                 monsterchances=[0.3,0.2,0.1,0.05],
                 bosschances=[0.0] ):
        """need game instance"""
        self.number = Room.number # void room has number 0
        game.rooms[self.number] = self # add room into game dict
        Room.number += 1
        self.explored = explored # True or False
        self.name = name
        self.description = description
        self.connections = connections
        self.itemchances = itemchances
        self.monsterchances = monsterchances
        self.bosschances = bosschances
     
        # create items
        for chance in self.itemchances:  
            if random.random()< chance:
                newItem = Item(game, self.number) # create item in this room

        # create monsters
        for chance in self.monsterchances:
            if random.random() < chance:
                newMonster = Monster(game, self.number) # create monster in this room
        # create boss(es)
        for chance in self.bosschances:
            if random.random() < chance:
                newMonster = Monster(game, self.number, boss=True)


    def list_items(self, game):
        """return string with itemnumbers and item description 
        as well as list of itemnumbers"""
        txt = "items in this room:\n"
        items = []
        for itemnumber in game.items:
            if game.items[itemnumber].location == self.number:
                txt +=  "{}....{}\n".format(itemnumber, 
                     game.items[itemnumber].description)
                items.append(itemnumber)
        return txt, items
        
    def connectiondict(self, game):
        """returns a dict with connections from this room.
        key is room number, value is room description (or "unknown",
        depending if the room is yet bo be explored"""
        namesdict = {} # temp list of room names
        #print("debug: self.connections", self.connections)
        for c in self.connections:
            if game.rooms[c].explored:
                namesdict[c] = game.rooms[c].name
            else:
                namesdict[c] = "unknown room"
        return namesdict

    def info(self, game):
        """return string with all information about this room"""
        txt = "Room number {}: {}\n".format(self.number, self.name)
        txt += self.description + "\n"
        # itmes ?
        txt2 = ""
        itemcounter = 0
        for itemnumber in game.items:
            if game.items[itemnumber].location == self.number:
                itemcounter += 1
                if itemcounter > 1:
                    txt2 += ", "
                txt2 +=  game.items[itemnumber].description 
        if itemcounter > 0:
            txt += "You see {} item(s) here: \n".format(itemcounter) + txt2
        else:
            txt += "This room has no items."
        # doors
        txt += "\nYou see {} door(s) and ".format(len(self.connections))
        # monsters ?
        monstercounter = 0
        txt2 = ""
        for monsternumber in game.monsters:
            if game.monsters[monsternumber].location == self.number:
                if not game.monsters[monsternumber].player:
                    monstercounter +=1
                    txt2 += game.monsters[monsternumber].info() 
        if monstercounter > 0:
            txt +="{} monster(s) here:\n".format(monstercounter)
            txt += txt2
        else:
            txt += "no monsters in this room, fortunately.\n"
       
        #txt += "\n"
        return txt

#------------- generic functions ------
# this function use print, replace later with gui commands
def output(txt):
    """can be later replaced by gui or graphical output"""
    print(txt)

def select_number(list_of_numbers):
        """The player select *one* number of a list of numbers"""
        answer = ""
        while ((not answer.isdecimal()) or int(answer) not in list_of_numbers):
                answer=input("Please type selected number and press ENTER: ")
        return int(answer)

def select_answer(list_of_answers):
    """The player select *one* char out of a list"""
    answer = ""
    while not answer in list_of_answers:
        answer = input(">>>")
    return answer
      



# create a game instance
g = Game()

# add rooms with  description and connections.
# Each room will have a unique number and add himself to game
# room 0 is the "exit from the game" room
# room 1 is the starting room for the player
# room number 0 .... void, game over, lowest possible room number
# syntax: Room(game, roomname, description, connections...)
Room(g,"end of the world (game over)", [], explored=True)
# room number 1 .... starting lobby
tmp = Room(g,"starting lobby","xx", [0, 2], explored = True)
tmp.description = """The room where your adventure starts. If you 
go to the room number 0, the game is over"""
# room number 2 .... first room 
Room(g,"first room", "a boring room with many doors", [1,3,4,5])
# room number 3 ..... storage room
tmp = Room(g,"storage room", "you see shelfs, empty boxes and a lot of dust and debris", [2,4])
tmp.itemchances = [0.6,0.4,0.33]
# room number 4 ..... gear room
Room(g,"gear room", "a room full of stuff", [2,3], itemchances=[1.0,1.0,0.7,0.7])
# room number 5 
Room(g,"npc room", "a ladder leads from here to the roof", [2,7,8], monsterchances=[1.0])
# room number 6 ..... secret room
tmp = Room(g, "secret room", "this is where the monsters dump loot and treasures", [9])
tmp.itemchances = [1,1,1,1,1]
# room number 7 .... roof
Room(g, "roof", "you can jump from here directly into the boss room", [5,9])
# room number 8 .... barrier (blocks path to boss room)
tmp = Room(g, "barrier room", "", [5])
tmp.description = """a mighty magical one-way barrier blocks your path into the
nearby boss room. Maybe there is another way into the boss room?"""
# room number 9 .... boss room
# the boss room has 1 to 6 minions and 1 to 3 bosses
Room(g,"boss chamber", "you smell blood", [8], monsterchances=[1.0,0.9,0.8,0.5,0.5,0.5],
     bosschances = [1.0,0.15,0.05])

# ----------- effects ----------
Effect(g,"randomteleport","teleport")
Effect(g,"hometeleport", "teleport", arg1 = 1)
Effect(g,"heal5", "heal", arg1=5)
Effect(g,"heal10", "heal", arg1=10)
Effect(g,"heal15", "heal", arg1=15)


# ---------- items ------------
# syntax: Item(game, where, description, mass, effect)
Item(g,1, "blue fearsome chicken feather",0.1,"hometeleport")
Item(g,1, "red fearsome chicken feather",0.2, "hometeleport")
Item(g,4, "yellow mockingbird feather", 0.1, "randomteleport")
Item(g,3, "pink mockingbird feather", 0.1, "randomteleport")
Item(g,4, "potion of instant healing",0.25, "heal15")
Item(g,1, "small healing potion", 0.25, "heal5")
Item(g,3, "big wheel of cheese", 0.50, "heal5", 5) # works 5 times



# start player in lobby (room 0)
# where = 0 # the actual room number
p = Player(g, where=1) # create player in room 1

# main loop
turns = 1
while p.location != 0 and p.hitpoints > 0:
    output("----- turn: {} -----".format(turns))
    if not g.rooms[p.location].explored:
        output("You explore a new room!")
        g.rooms[p.location].explored = True # explore this room
    #print("debug rooms:", g.rooms)
    output("You are now here with {} hitpoints left:\n{}".format(p.hitpoints, g.rooms[p.location].info(g)))
    p.nextAction(g)
    turns += 1
output("\n==================\n")
output("Thank you for playing. Have a nice real life")
