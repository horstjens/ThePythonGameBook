# -*- coding: utf-8 -*-
import random
import easygui


        
def openDie(sides = 6, minValue = 1):
    """an open-ended die, inspired from the game Dominions3 by Illwinter.
       If you roll the hightes number, you can roll the die again.
       Basically, if the highest side of the dice is thrown, the score 
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

def multiDie(dice=2, sides=6, normal=True, minValue=1):
    """throw several dices and return the sum of the eyes
       accept several dicetypes:
       if normal = True a (6-sided) die is used. Else, you may roll
       again if you roll a 6).
       """
    eyes = 0
    for _ in range(dice):
        if normal:
            eyes += normalDie(sides, minValue)
        else:
            eyes += openDie(sides, minValue)
    return eyes
        



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

    def calcSum(self):
        """calculate a sum of all attributes. the higher the sum, the 
           better is the monster"""
        statSum = 0
        statSum += self.hitpoints
        statSum += self.attack
        statSum += self.defense
        statSum += self.armor
        statSum += self.damage
        statSum += self.speed
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
    
    def __init__(self):
        Monster.__init__(self) # call parent __init__ function !
        self.hitpoints =  5 + openDie()
        self.damage = 10 + openDie()
        self.attack = 10 + openDie()
        self.defense = 10 + openDie()
        self.armor = 5 + openDie()
        self.speed = 10 + openDie()
        self.resMagic = -0.50  #  1.0 means 100%
        self.resAcid = 0.25
        self.resPoison = 0.50
        self.statSum = self.calcSum()
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
    
    def __init__(self):
        Monster.__init__(self) # call parent __init__ function !
        self.hitpoints =  10 + openDie()
        self.damage = 10 + openDie()
        self.attack = 10 + openDie()
        self.defense = 10 + openDie()
        self.armor = 10 + openDie()
        self.speed = 5 + openDie()
        self.inspect() # introduce yourself

    
    def createName(self):
        answer = ""
        while answer == "":
            answer= raw_input("please enter your name, noble knight:")
        return answer
    

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
              sucessful armor penetration
    """
    msg = ""
    # calculatin luck
    luckAttack = openDie()
    luckDefense = openDie()
    luckDamage = openDie()
    luckArmor = openDie()
    attackValue = attacker.attack + luckAttack # + attackbonus
    defenseValue = defender.defense + luckDefense # defensebonus
    if attackValue > defenseValue:
        msg+="Hit !(%i+%i):(%i+%i) %s manage to hit %s \n" % (attacker.attack, luckAttack,
                     defender.defense, luckDefense, attacker.name, defender.name )
        damageValue = attacker.damage + luckDamage # + damagebonus
        armorValue = defender.armor + luckArmor # + armorbonus
        if damageValue > armorValue:
            msg+="Armor Penetration! (%i+%i):(%i+%i) \n" %( attacker.damage , luckDamage, defender.armor, luckArmor)
            loss = damageValue - armorValue
            defender.hitpoints -=  loss
            msg+="Hitpoint loss: %i (remaining: %i) \n" % ( loss, defender.hitpoints)
            if defender.hitpoints < 1:
                msg += "Victory for %s !\n" % attacker.name
        else:
            msg+="Glancing Blow (%i+%i):(%i+%i) %s could not penetrate the armor of %s \n" % ( attacker.damage, luckDamage,
                      defender.armor, luckArmor, attacker.name, defender.name)
    else:
        msg+="Evaded !(%i+%i):(%i+%i) %s does not manage to hit %s \n " % (attacker.attack, luckAttack,
                    defender.defense, luckDefense, attacker.name, defender.name )
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
        speedLuckA = openDie()
        speedLuckB = openDie()
        speedValueA = a.speed + speedLuckA
        speedValueB = b.speed + speedLuckB
        if speedValueA == speedValueB:
            speedValueA += random.choice((-1,1))
        if speedValueA > speedValueB:
            msg += "First Attack (%i+%i):(%i+%i) for %s \n" % (a.speed, speedLuckA, b.speed, speedLuckB, a.name)
            msg += meleeAction(a, b)
            if b.hitpoints > 0:
                msg += "Counter-attack of %s \n" % b.name
                msg += meleeAction(b,a)
        else:
            msg += "First Attack (%i+%i):(%i+%i) for %s \n" % (b.speed, speedLuckB, a.speed, speedLuckA, b.name)
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
    msg += "damage:    %.3i %s %.3i\n" % (a.damage, table[a.damage.__cmp__(b.damage)], b.damage)
    msg += "attack:    %.3i %s %.3i\n" % (a.attack, table[a.attack.__cmp__(b.attack)], b.attack)
    msg += "defense:   %.3i %s %.3i\n" % (a.defense, table[a.defense.__cmp__(b.defense)], b.defense)
    msg += "speed:     %.3i %s %.3i\n" % (a.speed, table[a.speed.__cmp__(b.speed)], b.speed)
    msg += "-----------------------\n"
    msg += "sum:       %.3i %s %.3i\n\n" % (a.calcSum(), table[a.calcSum().__cmp__(b.calcSum())], b.calcSum())
    if verbose:
        print msg
    return msg

player = Player()
enemy = Goblin()

compare(player, enemy)
#meleeBattle(player, enemy)


    
    
     
