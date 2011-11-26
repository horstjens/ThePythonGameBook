# -*- coding: utf-8 -*-
import random
#import easygui

winnersign = { -1:"<<", 0:"<=", 1:">>"} # for combat message 
firstattack = { -1: "get attacket first by", 1:"attack first" }

class Item(object):
    """generic item in game, can be a weapon, a health potion or anything"""
    number = 0 # unique item number
    book = {} # the book of all items
    
    def __init__(self, name=""):
        self.number = Item.number # get my unique number
        Item.number += 1 # prepare number for next item
        Item.book[self.number] = self # store item into book
        if name == "":
            self.name = "noname item"
        self.quality = 1.0 # quality in percent 1 = 100 %
        self.weight = 0.0 # weight in kg
        self.goldValue = 0.0
        # boni 
        self.attackBonus = 0
        self.defenseBonus= 0
        self.armorBonus = 0
        self.damageBonus = 0
        self.speedBonus = 0
        self.resMagicBonus = 0.0  #  1.0 means 100%
        self.resFireBonus = 0.0
        self.resColdBonus = 0.0
        self.resAcidBonus = 0.0
        self.resPoisonBonus = 0.0
        self.resElectricityBonus = 0.0
        
        
    def inspect(self, verbose = True):
        """print out all attributes"""
        msg = ""
        msg+= "\n - * - * - * - * - * -"
        msg+= "\ni'm a " + self.__class__.__name__
        msg+= "\nmy attributes are:"
        for x in self.__dict__.keys():
            msg+= "\n%s : %s" % (x, self.__dict__[x])
        msg+ "\n-----------------------"
        if verbose:
            print msg
        return msg

class Sword(Item):
    """handheld melee weapon"""
    def __init__(self, name=""):
        Item.__init__(self, name) # call parent __init__ function
        self.category = "weapon"
        self.hands = 1
        self.attackBonus = 3 + openDie() / 10 # small chance for better values
        self.defenseBonus = 1 + openDie() / 10
        self.damageBonus = 2 + openDie() / 10
        # is this sword better than normal ?
        self.special = self.attackBonus + self.defenseBonus + self.damageBonus - (3+1+7)
        self.length = 1.0 # weapon length in meter
        self.inspect()
        
class Fist(Item):
    """standard weapon for naked humanoids"""
    def __init__(self, name=""):
        Item.__init__(self, name)
        self.category = "weapon"
        self.hands = 1
        self.length = 0.0

class Claw(Item):
    """standard weapon for naked goblins and other animals"""
    def __init__(self, name=""):
        Item.__init__(self, name)
        self.category = "weapon"
        self.hands = 1
        self.length = 0.1
        self.damageBonus = 1

class Monster(object):
    """generic monster class. Each monster has a unique number
       and is stored in the Monster.book"""
       
    number = 0 # unique number for each Monster
    book = {}  # the book of all monsters {number:monster}
    
    def __init__(self, name=""):
        self.number = Monster.number # get my unique monsternumber
        Monster.number += 1  # prepare number for the next monster
        Monster.book[self.number] = self # store myself into the book
        if name == "":
            self.name = self.createName() # choose a random name
        # check if monstername is unique. if not, calculate suffix
        self.nameNumber =  1 # harry the first, harry the second etc.
        for othermonster in Monster.book.keys():
            if self.name == Monster.book[othermonster].name:
                self.nameNumber += 1
        # create default attributes for naked humanoid monster 
        self.hitpoints = 10
        self.attack  = 0
        self.defense = 0
        self.armor  =  0
        self.damage =  0
        self.speed = 0   
        #self.luck = 0
        self.resMagic = 0.0  #  1.0 means 100%
        self.resFire = 0.0
        self.resCold = 0.0
        self.resAcid = 0.0
        self.resPoison = 0.0
        self.resElectricity = 0.0
        # inventory
        self.weapon = Item() ## empty item, no boni
        self.armor = Item()  ## 
        self.gold = 0
        self.inventory = [] 

    def calcSum(self):
        """calculate a sum of all attributes. the higher the sum, the 
           better is the monster"""
        statSum = 0
        statSum += self.hitpoints 
        statSum += self.attack + self.weapon.attackBonus
        statSum += self.defense + self.weapon.defenseBonus
        statSum += self.armor 
        statSum += self.damage + self.weapon.damageBonus
        statSum += self.speed  + self.weapon.speedBonus
        return statSum 
        
    def inspect(self, verbose = True):
        """print out all attributes"""
        msg = ""
        msg+= "\n - * - * - * - * - * -"
        msg+= "\ni'm a " + self.__class__.__name__
        msg+= "\nmy attributes are:"
        for x in self.__dict__.keys():
            msg+= "\n%s : %s" % (x, self.__dict__[x])
        msg+ "\n-----------------------"
        if verbose:
            print msg
        return msg
        
    def createName(self):
        return "not yet named monster"
        
        
                 
class Goblin(Monster):
    """green, small sub-standard foe to populate beginner levels,
       cave systems etc."""
    
    def __init__(self, name=""):
        Monster.__init__(self, name) # call parent __init__ function !
        self.hitpoints =  15 + openDie()
        self.damage = 10 + openDie()
        self.attack = 10 + openDie()
        self.defense = 10 + openDie()
        self.armor = 5 + openDie()
        self.speed = 10 + openDie()
        self.resMagic = -0.50  #  1.0 means 100%
        self.resAcid = 0.25
        self.resPoison = 0.50
        self.statSum = self.calcSum()
        self.weapon = Claw()
        self.inspect() # introduce yourself
        
        
    def createName(self):
        """overwriting the Monster method specially for Goblins"""
        firstName  = ["Ugg", "Ogg", "Slimebread", "Raxx", "Redeye",
                      "Graggog", "Krax", "Rumpy", "Fatass", "Venomclaw",
                       "Thorax", "Detlev", "Stonespit", "Galomir"]
        lastName = ["Eggbiter", "Greenhide", "Dogrunner", "Spitmaster",
                    "Loudfarter", "Stonethrower", "Helmbiter", 
                    "Macemaster", "Sticklord", "Swampbath", "Foulsemller",
                    "Neverbath","Watershy","Soaphater", "Cateater",
                    "Piglover", "Foecrusher", "Doghurler"]
        name = random.choice(firstName) 
        name += " " + random.choice(lastName)
        return name

class Player(Monster):
    """the player is also a Monster :-)"""
    
    def __init__(self, name=""):
        Monster.__init__(self, name) # call parent __init__ function !
        self.hitpoints =  20 + openDie()
        self.damage = 10 + openDie()
        self.attack = 10 + openDie()
        self.defense = 10 + openDie()
        self.armor = 10 + openDie()
        self.speed = 5 + openDie()
        self.weapon = Fist() # unarmed
        self.inspect() # introduce yourself

    
    def createName(self):
        answer = ""
        while answer == "":
            answer= raw_input("please enter your name, noble knight:")
        return answer
    
        
def openDie(sides = 6, minValue = 1):
    """an open-ended die, inspired from the game Dominions3 by Illwinter.
       If you roll the hightes number, you can roll the die again.
       Basically, if the highest side of the die is thrown, the score 
       (sides-1) is kept and the die is rolled again, adding the new score.
       This means there is a very low probaility of a very high throw"""
    if sides <1:
        raise UserWarning, "sides must be > 0 (ideally, larger than 1)"
    if sides <= minValue:
        raise UserWarning, "sides must be > minvalues"
    eyes = random.randint(1, sides) # number of eyes facing us on the dice after throwing
    if eyes == sides:
        eyes = sides - 1 + openDie(sides, minValue) # recursion
    return eyes 
    
def normalDie(sides=6, minValue = 1):
    """a conventional, 6-sided die"""
    if not minValue < sides:
        raise UserWarning, "minValue (%i) must be smaller than sides (%i)" % (minValue, sides)
    return  random.randint(minValue, sides)

def multiDie(amount=2, sides=6, normal=False, minValue=1):
    """throw several (amount) dices and return the sum of the eyes
       accept several dicetypes:
       if normal = True a (6-sided) die is used. Else, you may roll
       again if you roll a 6).
       Default values means 2 independt throwings of  six-sided dice with re-roll at 6,
       resulting in an eye-sum between 2 and more than 12
       """
    eyes = 0
    for _ in range(amount):
        if normal:
            eyes += normalDie(sides, minValue)
        else:
            eyes += openDie(sides, minValue)
    return eyes
        


def meleeAction(attacker, defender, verbose = False):
    """calculate a single melee attack
       using stats and random values
       ** Formula **:
        attack value  = attack stat + attack bonus + luck 
        defense value = defense stat + defense bonus + luck
        if attack > defense: 
           sucessful hit
           damage value = damage stat + damage bounus + luck
           armor value  = armor stat + armor bonus + luck
           if damage > armor:
              sucessful armor penetration, hitpoint loss for victim
           else:
              glancing blow, not hitpoint loss
        else:
           defender dodged the attacker
        
           
    """
    msg = ""
    # calculating luck
    luckAttack = multiDie()
    luckDefense = multiDie()
    luckDamage = multiDie()
    luckArmor = multiDie()
    attackValue = attacker.attack + luckAttack + attacker.weapon.attackBonus 
    defenseValue = defender.defense + luckDefense + defender.weapon.defenseBonus 
    if attackValue > defenseValue:
        msg+="Hit !(%i+%i)>(%i+%i) %s manage to hit %s \n" % (attacker.attack + attacker.weapon.attackBonus, luckAttack,
                     defender.defense + defender.weapon.defenseBonus, luckDefense, attacker.name, defender.name )
        damageValue = attacker.damage + luckDamage + attacker.weapon.damageBonus
        armorValue = defender.armor + luckArmor # + armorbonus
        if damageValue > armorValue:
            msg+="Armor Penetration! (%i+%i)>(%i+%i) \n" %( attacker.damage + attacker.weapon.damageBonus , luckDamage, defender.armor, luckArmor)
            loss = damageValue - armorValue
            defender.hitpoints -=  loss
            msg+="Hitpoint loss: %i (remaining: %i) \n" % ( loss, defender.hitpoints)
            if defender.hitpoints < 1:
                msg += "Victory for %s !\n" % attacker.name
        else:
            msg+="Glancing Blow (%i+%i)<(%i+%i) %s could not penetrate the armor of %s \n" % ( attacker.damage+ attacker.weapon.damageBonus, luckDamage,
                      defender.armor, luckArmor, attacker.name, defender.name) # + armorbonus
    else:
        msg+="Evaded !(%i+%i)<(%i+%i) %s does not manage to hit %s \n " % (attacker.attack + attacker.weapon.attackBonus, luckAttack,
                    defender.defense + defender.weapon.defenseBonus, luckDefense, attacker.name, defender.name )
    if verbose:
        print msg
    return msg
    
def meleeBattle(a, b, verbose = True):
    """several meleeActions between a and b 
       until one opponent has <1 hitpoints"""
    msg = "values: (base value + luck)\n\n"
    rounds = 0
    while a.hitpoints > 0 and b.hitpoints > 0 and rounds <=100:
        rounds +=1
        msg += " ---------- round %i -------------- \n" % rounds
        # speed + luck decide who is attacking first
        speedLuckA = multiDie()
        speedLuckB = multiDie()
        speedValueA = a.speed + speedLuckA + a.weapon.speedBonus
        speedValueB = b.speed + speedLuckB + b.weapon.speedBonus
        if speedValueA == speedValueB:
            speedValueA += random.choice((-1,1))
        msg += "%s %s %s (%i+%i)%s(%i+%i) \n" % (a.name, firstattack[cmp(speedValueA, speedValueB)], b.name,  a.speed + a.weapon.speedBonus, speedLuckA, winnersign[cmp(speedValueA, speedValueB)], b.speed + b.weapon.speedBonus, speedLuckB)
        if speedValueA > speedValueB:
            msg += meleeAction(a, b)
            if b.hitpoints > 0:
                msg += "Counter-attack of %s \n" % b.name
                msg += meleeAction(b,a)
        else:
            #msg += "First Attack (%i+%i)(%i+%i) for %s \n" % (b.speed + b.weapon.speedBonus, speedLuckB, a.speed + a.weapon.speedBonus, speedLuckA, b.name)
            msg += meleeAction(b, a)
            if a.hitpoints > 0:
                msg += "Counter-attack of %s \n" % a.name
                msg += meleeAction(a, b)
    msg+= " -- the battle is over -- \n"
    if rounds > 100:
        msg += "Result: draw (timeout). The battle lastet more than 100 rounds \n"
    if verbose:
        print msg

def compare(a,b, verbose = True):
    """compare the most important values of 2 monsters side by side"""
    table = {-1:"<", 0:"=", 1:">"}
    msg = "\n\n"
    msg += "======================\n"
    msg += "left side: %s \n" % a.name
    msg += "right side: %s \n" % b.name
    msg += "hitpoints: %.3i %s %.3i\n" % (a.hitpoints, table[a.hitpoints.__cmp__(b.hitpoints)], b.hitpoints)
    msg += "armor:     %.3i %s %.3i\n" % (a.armor, table[a.armor.__cmp__(b.armor)], b.armor)
    damA = a.damage + a.weapon.damageBonus
    damB = b.damage + b.weapon.damageBonus
    msg += "damage:    %.3i %s %.3i\n" % (damA, table[damA.__cmp__(damB)], damB)
    attA = a.attack + a.weapon.attackBonus
    attB = b.attack + b.weapon.attackBonus
    msg += "attack:    %.3i %s %.3i\n" % (attA, table[attA.__cmp__(attB)], attB)
    defA = a.defense + a.weapon.defenseBonus
    defB = b.defense + b.weapon.defenseBonus
    msg += "defense:   %.3i %s %.3i\n" % (defA, table[defA.__cmp__(defB)], defB)
    msg += "speed:     %.3i %s %.3i\n" % (a.speed, table[a.speed.__cmp__(b.speed)], b.speed)
    msg += "-----------------------\n"
    msg += "sum:       %.3i %s %.3i\n\n" % (a.calcSum(), table[a.calcSum().__cmp__(b.calcSum())], b.calcSum())
    if verbose:
        print msg
    return msg

player = Player()
enemy = Goblin()

print "naked"
compare(player, enemy)

# uncomment those 2 lines to let the fight be unarmed
player.weapon = Sword()
enemy.weapon = Sword()
    
print "armed"
compare(player, enemy)
    
meleeBattle(player, enemy)     
