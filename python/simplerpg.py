#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       simplerpg.py
#       
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#
#       a simple role-playing game, inspired by rogue-like games
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import random 

# some classes

class BaseObject(object):
    """the common grandfather of all classes in this game"""
    def parameter2attribute(self, **kwargs):
        """setting the attributes of the class instance to existing
           keywords (**kwargs) / parameters"""
        for attr in kwargs.keys():
            if attr in self.__dict__:
                self.__dict__[attr] = kwargs[attr]


class Monster(BaseObject):
    number = 0 # a counter for all monsters
    _book = {}  # a dictionary to hold all monsters
    def __init__(self, **kwargs):
        """to create a new monster:
           mymonster = Monster(str = 7, race="orc")"""
        #print "---- a new monster is born ---"
        Monster.number += 1
        self.number = Monster.number
        Monster._book[self.number] = self
        self.strength = 0 # default values
        self.dexterity = 0
        self.intelligence = 0
        self.gold = 0
        #self.score = 0 # only relevant for player
        self.hitpoints = 10
        self.race = "unknow"
        self.name = "x"
        self.activeWeapon = 0
        self.attack = 10
        self.defense = 10
        self.protection = 0
        self.parameter2attribute(**kwargs)
        

class Item(BaseObject):
    number = 0
    book = {}
    def __init__(self, **kwargs):
        """to create an item in the game, code:
           mybox = Item(shortdescr="box",
                       longdescr="a wooden, locked box", weight=50)"""
        Item.number += 1
        self.number = Item.number
        Item.book[self.number] = self
        self.value = 0
        self.weight = 0
        self.category = ""
        self.shortdescr = ""
        self.longdescr = ""
        self.weapon = False
        #self.addkwargs(**kwargs)
        self.parameter2attribute(**kwargs)
    
    
class Weapon(Item):
    def __init__(self, **kwargs):
        """to create a weapon, code (like an item):
            mysword = Weapon(shortdescr="sword", attack = 7)"""
        Item.__init__(self, **kwargs)
        self.weapon = True
        self.attack = 0
        self.defense = 0
        self.damage = 0
        self.length = 0
        self.parameter2attribute(**kwargs)
        
    
# some functions
def showStats(object):
    """display all stats of an class instance"""
    for key in object.__dict__:
        print key, ":", object.__dict__[key]
        
def domDice(sides = 6, minValue = 1):
    """an open-ended dice, inspired from the game Dominions3 by Illwinter.
       Basically, if the highest side of the dice is thrown, the score 
       of (sides-1) is kept and the dice is throwed again, adding the new score.
       This means there is a very low probaility of a very high throw"""
    if not minValue < sides:
        raise UserWarning, "minValue (%i) must be smaller than sides (%i)" % (minValue, sides)
    #score = 0
    eyes = random.randint(minValue, sides) # number of eyes facing us on the dice after throwing
    if eyes == sides:
        eyes = sides - 1 + domDice(sides, minValue) # recursion
    return eyes 
    
def dice(sides=6, minValue = 1):
    """a conventional dice"""
    if not minValue < sides:
        raise UserWarning, "minValue (%i) must be smaller than sides (%i)" % (minValue, sides)
    return  random.randint(minValue, sides)

def multiDice(dices, dicetype="dice", sides=6, minValue=1):
    """throw several dices and return the sum of the eyes
       accept several dicetypes:
       dice
       domDice"""
    eyes = 0
    for _ in range(dices):
        if dicetype == "dice":
            eyes += dice(sides, minValue)
        elif dicetype == "domDice":
            eyes += domDice(sides, minValue)
    return eyes
        
def meleeAction(attacker, defender, repeldamage=False):
    """the attacker slashes at the defender
       if this is a repel action (for attacking with a shorter weapon)
       then the damage is limited to 1 hitpoint"""
    attackValue = ( attacker.attack + 
                    attacker.dexterity +
                    Weapon.book[attacker.activeWeapon].attack +
                    domDice() )
    defendValue = ( defender.defense +
                    defender.dexterity +
                    Weapon.book[defender.activeWeapon].defense +
                    domDice() )
    # hit or miss ?
    if attackValue >= defendValue:
        if not repeldamage:
            print "Whamm! the attacking %s (%i)" \
                  " hit the defending %s (%i)!"  % (attacker.name, 
                                                attackValue,
                                                defender.name, 
                                                defendValue)
        # damage calculation
        damagevalue = ( attacker.strength +
                        Weapon.book[attacker.activeWeapon].damage +
                        domDice() )
        protectionvalue = ( defender.protection + 
                            domDice() )
        damage = damagevalue - protectionvalue
        if not repeldamage:
            print "damage (%i) vs protection (%i)" % (damagevalue, protectionvalue)
        if damage > 0:
            if repeldamage:
                print "repel action sucessfull! %s looses one hitpoint for attacking with a shorter weapon" % defender.name
                defender.hitpoints -=1 # repel can cause at max 1 hitpoint damage
            else: # non-repel damage
                print "..%s is hit for %i damage " \
                      "(%i hitpoints remaining)" % (defender.name, damage,
                                                defender.hitpoints-damage)
                defender.hitpoints -= damage  # alter hitpoints
            if defender.hitpoints <= 0:
                print "...%s dies !" % defender.name
        else:
            if repeldamage:
                print "the repel action fails to penetrate the attackers armor"
            else:
                print "..but can not penetrate his armor"
    else:
        if repeldamage:
            print "tha attacker manages to evade the repel action"
        else:
            print "%s attack fail to hit the evading %s" % (attacker.name, defender.name)
        
def meleeRound(opponent1, opponent2):
    """the more agile opponent stabs first, if the defender survive 
       he stabs back"""
    dex1 = opponent1.dexterity + domDice()
    dex2 = opponent2.dexterity + domDice()
    print "who is attacking first ? %s (%i) vs. %s (%i)" % (opponent1.name, dex1, opponent2.name,dex2)
    if dex1 == dex2:
        #print "both opponents are equal skilled"
        # randomly choose first attacker
        dex1 = dex2 + random.choice((-1,1))
    if dex1 > dex2:
        #print opponent1.name , "attack first"
        # --- repel ? only for attacker---
        if (Weapon.book[opponent1.activeWeapon].length >
            Weapon.book[opponent2.activeWeapon].length):
            meleeAction(opponent2, opponent1, True) # repel    
        if opponent1.hitpoints > 0:
            meleeAction(opponent1, opponent2) # normal attack
        if opponent2.hitpoints > 0:
            print "riposte" # no repel at riposte
            meleeAction(opponent2, opponent1)
    else:
        #print opponent2.name, "attack first"
        # --- repel ? only for attacker
        if (Weapon.book[opponent2.activeWeapon].length >
            Weapon.book[opponent1.activeWeapon].length):
            meleeAction(opponent1, opponent2, True) # repel    
        if opponent2.hitpoints > 0:
            meleeAction(opponent2, opponent1)
        if opponent1.hitpoints > 0:
            print "riposte" # no repel at riposte
            meleeAction(opponent1, opponent2)

def melee(opponent1, opponent2):
    print "==== opponents ===="
    compareStats(opponent1, opponent2)
    print "==== weapons ===="
    compareStats(Weapon.book[opponent1.activeWeapon], 
                 Weapon.book[opponent2.activeWeapon])
    rounds = 0
    while (opponent1.hitpoints > 0) and (opponent2.hitpoints > 0):
        rounds += 1
        print "----melee round %i----" % rounds
        meleeRound(opponent1, opponent2)
    if opponent1.hitpoints > 0:
        victor = opponent1
    else:
        victor = opponent2
    print "*** Victory for %s ***" % victor.name
    return (rounds, victor)

def compareStats(opponent1, opponent2):
    """ compare the attributes (stats) of two monsters"""
    o = {-2:"-",-1:"<",0:"=",1:">"} # compare results
    ignorelist = ("number", "activeWeapon", "weapon")
    for key in opponent1.__dict__:
        if key in ignorelist:
            continue
        if not (key in opponent2.__dict__):
            continue 
        if "int" in str(type(opponent1.__dict__[key])):
            r = cmp(opponent1.__dict__[key], opponent2.__dict__[key])
        else:
            r=-2 # text can not be compared directly
        print key, ":", opponent1.__dict__[key], o[r], opponent2.__dict__[key]

def testFight(opponent1, opponent2, trials=10000):
    v1 = 0
    v2 = 0
    vrounds = {}
    for x in range(trials):
        savehp1 = opponent1.hitpoints
        savehp2 = opponent2.hitpoints
        print "trial number %i" %x
        trialresult = melee(opponent1, opponent2)
        rounds = trialresult[0]
        victor = trialresult[1]
        if rounds in vrounds.keys():
            vrounds[rounds] +=1
        else:
            vrounds[rounds] = 1
        if victor == opponent1:
            v1 +=1
        else:
            v2 +=1
        # restore hitpoints
        opponent1.hitpoints = savehp1
        opponent2.hitpoints = savehp2
    print "========================="
    print "trial result statistic"
    print "========================="
    print "victorys for", opponent1.name, v1
    print "victorys for", opponent2.name, v2
    print vrounds
    

def game():
    """simple role-playing-game"""
    player = Monster(strength=9, dexetery=12, intelligence=8, protection=5, race="human", name="Gustavo")
    player.score = 0 # additional attribute only for player
    bozo  = Monster(strength=12, dexetery=8, intelligence=2, protection = 3, race="orc", name="grunty")
    axe = Weapon(attack=4, defense = 1, damage=4,
                 length= 1, shortdescr="blue axe", )
    shortsword = Weapon(attack =5, defense = 2, damage=2,
                        length=2, shortdescr="army sword")
    player.activeWeapon =  shortsword.number
    bozo.activeWeapon = axe.number
    print "--------battle---------"
    #melee(player, bozo)
    testFight(player, bozo, 1000)

    
if __name__ == '__main__':
    game()

