#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       combatgame.py
#       
#       Copyright 2012 Horst JENS <horst.jens@spielend-programmieren.at>
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
    number = 0  # a counter for all monsters
    _book = {}  # a dictionary to hold all monsters

    def __init__(self, **kwargs):
        """to create a new monster:
           mymonster = Monster(str = 7, race="orc")"""
        #print "---- a new monster is born ---"
        Monster.number += 1
        self.number = Monster.number
        Monster._book[self.number] = self
        self.strength = 10  # default value, influence damage afflicted to others
        self.dexterity = 10  # default value, influence chance to attack first
        self.intelligence = 10
        self.gold = 0
        #self.score = 0 # only relevant for player
        self.hitpoints = 10  # default value, how much damage can be taken
        self.race = "unknow"
        self.name = "x"
        self.activeWeapon = 0
        self.activeShield = 0
        self.activeArmor = 0  # body armor
        self.activeHelm = 0
        self.activeShoe = 0
        self.activeGlove = 0
        self.activeMisc1 = 0
        self.activeMisc2 = 0
        self.activeMisc3 = 0
        self.activeMisc4 = 0
        self.attack = 10  # default value, chance to sucessful hit opponent
        self.defense = 10  # default value, chance to evade attack
        self.protection = 0  # default value, how much damage can be negated
        self.parameter2attribute(**kwargs)  # a method of parent class BaseObject


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
        self.MeleeWeapon = False
        self.shield = False
        self.armor = False
        self.parameter2attribute(**kwargs)  # a method of parent class BaseObject


class MeleeWeapon(Item):
    def __init__(self, **kwargs):
        """to create a MeleeWeapon, code (like an item):
            mysword = MeleeWeapon(shortdescr="sword", attack = 7)"""
        Item.__init__(self, **kwargs)
        self.MeleeWeapon = True
        self.attack = 0
        self.defense = 0
        self.damage = 0
        self.length = 0  # melee attacking with a shorter weapon faces a repel action (max. 1 damage)
        self.parameter2attribute(**kwargs)


        # some functions
def showStats(object):
    """display all stats of an class instance"""
    for key in object.__dict__:
        print key, ":", object.__dict__[key]


def domDice(sides=6, minValue=1):
    """an open-ended dice, inspired from the game Dominions3 by Illwinter.
       Basically, if the highest side of the dice is thrown, the score 
       of (sides-1) is kept and the dice is throwed again, adding the new score.
       This means there is a very low probaility of a very high throw"""
    if not minValue < sides:
        raise UserWarning, "minValue (%i) must be smaller than sides (%i)" % (
            minValue, sides
        )
    #score = 0
    eyes = random.randint(minValue, sides)  # number of eyes facing us on the dice after throwing
    if eyes == sides:
        eyes = sides - 1 + domDice(sides, minValue)  # recursion
    return eyes


def dice(sides=6, minValue=1):
    """a conventional dice"""
    if not minValue < sides:
        raise UserWarning, "minValue (%i) must be smaller than sides (%i)" % (
            minValue, sides
        )
    return random.randint(minValue, sides)


def multiDice(dices=2, dicetype="domDice", sides=6, minValue=1):
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
       if this is a repel action (for attacking with a shorter MeleeWeapon)
       then the damage is limited to 1 hitpoint"""
    attDice = multiDice()
    defDice = multiDice()
    attWeapon = MeleeWeapon.book[attacker.activeMeleeWeapon].attack
    defWeapon = MeleeWeapon.book[defender.activeMeleeWeapon].defense
    attackValue = attacker.attack + attWeapon + attDice
    defendValue = defender.defense + defWeapon + defDice
    #---
    damDice = multiDice(1)  # fewer influence of random than at attack vs. defense (1 dice vs. 2 dice)
    protDice = multiDice(1)
    #protDice = 0  # no random bonus for armor !!
    damWeapon = MeleeWeapon.book[attacker.activeMeleeWeapon].damage
    damageValue = attacker.strength + damWeapon + damDice
    protectionValue = defender.protection + protDice  # Shield ????????
    damage = damageValue - protectionValue
    # hit or miss ?
    if attackValue > defendValue:
        if repeldamage:
            w1 = "..Ouch!!"
            w2 = "'s repel action"
        else:
            w1 = "Whamm!"
            w2 = ""
        print "%s %s%s (%i+%i+%i)  hits %s (%i+%i+%i) with %i:%i!" % (
            w1, attacker.name, w2, attacker.attack, attWeapon, attDice,
            defender.name, defender.defense, defWeapon, defDice, attackValue,
            defendValue
        )

        # damage calculation
        if repeldamage:
            w1 = "..repel damage"
            w2 = ""
            if damage > 0:
                w3 = "1 max. repel"
            else:
                w3 = "no repel"
        else:
            w1 = ".damage"
            w2 = ""
            if damage > 0:
                w3 = str(damage)
            else:
                w3 = "no"
        print "%s (%i+%i+%i)%s minus protection (%i+%i) is %i-%i=%s damage" % (
            w1, attacker.strength, damWeapon, damDice, w2, defender.protection,
            protDice, damageValue, protectionValue, w3
        )

        if damage > 0:
            if repeldamage:
                defender.hitpoints -= 1  # repel can cause at max 1 hitpoint damage
                print "..Repel action sucess ! %s looses one hitpoint  (%i left)" % (
                    defender.name, defender.hitpoints
                )

            else:  # non-repel damage
                print "..%s is hit for %i damage " \
                      "(%i hitpoints remaining)" % (defender.name, damage,
                                                defender.hitpoints-damage)
                defender.hitpoints -= damage  # alter hitpoints
            if defender.hitpoints <= 0:
                print "...%s dies !" % defender.name
        else:
            if repeldamage:
                print "..the repel action fails to penetrate the attackers armor"
            else:
                print "..but can not penetrate his armor"
    else:
        # def > att
        if repeldamage:
            w1 = "dodge"
            w2 = "repel action"
        else:
            w1 = "evade"
            w2 = "attack"
        print "... but %s can %s (%i+%i+%i) the %s (%i+%i+%i) with %i:%i" % (
            defender.name, w1, defender.defense, defWeapon, defDice, w2,
            attacker.attack, attWeapon, attDice, defendValue, attackValue
        )


def meleeRound(opponent1, opponent2):
    """the more agile (dex) opponent stabs first, if the defender survive 
       he stabs back"""
    dex1 = opponent1.dexterity + multiDice()
    dex2 = opponent2.dexterity + multiDice()
    #print "who is attacking first ? %s (%i) vs. %s (%i)" % (opponent1.name, dex1, opponent2.name,dex2)
    if dex1 == dex2:
        #print "both opponents are equal skilled"
        # randomly choose first attacker
        dex1 = dex2 + random.choice((-1, 1))
    if opponent1.hitpoints > 0 and opponent2.hitpoints > 0:
        print "+++Attack! " + dexmsg(opponent1, opponent2, dex1, dex2)
        if dex1 > dex2:
            meleeAttack(opponent1, opponent2)  # attack
            if opponent2.hitpoints > 0 and opponent1.hitpoints > 0:
                print "+++Counter-Attack!"
                meleeAttack(opponent2, opponent1)  # riposte
        else:
            meleeAttack(opponent2, opponent1)  # attack
            if opponent1.hitpoints > 0 and opponent2.hitpoints > 0:
                print "+++Counter-Attack!"
                meleeAttack(opponent1, opponent2)  # riposte


def dexmsg(opponent1, opponent2, dex1, dex2):
    """ returns a message of who is attacking who first. uses cmp to compare stats.
        cmp(a,b) returns -1 if a<b, 0 if a == b and 1 if a>b"""
    mydic1 = {-1: "slower", 0: "equal fast", 1: "faster"}
    mydic2 = {-1: "is attacked first by", 0: "???", 1: "attacks first"}
    msg = "The %s %s (%i) %s %s (%i) with %i:%i" % (
        mydic1[cmp(opponent1.dexterity, opponent2.dexterity)], opponent1.name,
        opponent1.dexterity, mydic2[cmp(dex1, dex2)], opponent2.name,
        opponent2.dexterity, dex1, dex2
    )
    return msg


def meleeAttack(opponent1, opponent2):
    """
    The melee attack checks if the defender has a longer weapon. if yes,
    the attacker can loose max. 1 hitpoint due to repel action before 
    continuing his attac.
    Note: a meleeround consist of two meleAttacks (attack and counter-attack). Both check for repel damage.
    """
    if (
        MeleeWeapon.book[opponent1.activeMeleeWeapon].length <
        MeleeWeapon.book[opponent2.activeMeleeWeapon].length
    ):
        print "Repel action: %s attacks with %s (%i) against  %s (%i)" % (
            opponent1.name,
            MeleeWeapon.book[opponent1.activeMeleeWeapon].shortdescr,
            MeleeWeapon.book[opponent1.activeMeleeWeapon].length,
            MeleeWeapon.book[opponent2.activeMeleeWeapon].shortdescr,
            MeleeWeapon.book[opponent2.activeMeleeWeapon].length
        )

        meleeAction(opponent2, opponent1, True)  # repel action, max. 1 damage
    if opponent1.hitpoints > 0 and opponent2.hitpoints > 0:
        meleeAction(opponent1, opponent2)  # normal attack


def melee(opponent1, opponent2):
    """melee combat inspired by the dominions3 rules.
       basic formular:
       if attacking with a shorter melee weapon (weapon length),
       the attacker must defend against a repel action, whose damage is
       limited to 1 hitponts. after that, he continues his attack.
       the attacker throws 2 x a 6-sided dice (and re-rolls at a 6), see
       MultiDice) and adds his attack value vs. the defenders defense
       value and his Multidice.
       if the attacker is sucessfull, damage is calculated at damage value
       + strength + multidice vs. protection + multidice.
       **not yet coded: the attack vs. defense value must be higher
       than the defenders shield parry value
       **not yet coded: sum all items for attack + defense + protection boni/mali
       **not yet coded: each part of body has its own protection value,
       depending on armor (shoe, helm, shield...) of defender
       **not yet coded: critical hit, affliction damage 
       """

    #print "==== opponents ===="
    #compareStats(opponent1, opponent2)
    #print "==== MeleeWeapons ===="
    #compareStats(MeleeWeapon.book[opponent1.activeMeleeWeapon], 
    #             MeleeWeapon.book[opponent2.activeMeleeWeapon])
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
    o = {-2: "-", -1: "<", 0: "=", 1: ">"}  # compare results
    ignorelist = ("activeMeleeWeapon", "MeleeWeapon")
    for key in opponent1.__dict__:
        if key in ignorelist:
            continue
        if not (key in opponent2.__dict__):
            continue
        if "int" in str(type(opponent1.__dict__[key])):
            r = cmp(opponent1.__dict__[key], opponent2.__dict__[key])
        else:
            r = -2  # text can not be compared directly
        print key, ":", opponent1.__dict__[key], o[r], opponent2.__dict__[key]


def testFight(opponent1, opponent2, trials=10000):
    v1 = 0
    v2 = 0
    vrounds = {}
    for x in range(trials):
        savehp1 = opponent1.hitpoints
        savehp2 = opponent2.hitpoints
        print "========================= new battle ====================="
        print "trial number %i" % x
        trialresult = melee(opponent1, opponent2)
        rounds = trialresult[0]
        victor = trialresult[1]
        if rounds in vrounds.keys():
            vrounds[rounds] += 1
        else:
            vrounds[rounds] = 1
        if victor == opponent1:
            v1 += 1
        else:
            v2 += 1
        # restore hitpoints
        opponent1.hitpoints = savehp1
        opponent2.hitpoints = savehp2
    print "========================="
    print "trial result statistic"
    print "========================="
    print "victorys for", opponent1.name, v1
    print "victorys for", opponent2.name, v2
    print "number of combat rounds and battles fought with this number of rounds:", vrounds


def domDiceTest():
    """print a table of stat differences 
       and the chance that:
       2domDice + stat differecne > 2domDice
       see page 5 of the domionons3 manual"""
    r = {}
    for zahl in range(-14, 15, 1):
        r[zahl] = 0
        for x in range(1000):
            a = multiDice()
            b = multiDice()
            print zahl, a, b
            if a + zahl > b:
                r[zahl] += 1
    print "---------"
    for key in sorted(r.keys()):
        print key, ":", r[key]


def game():
    """simple role-playing-game"""
    # edit those values !
    player = Monster(
        strength=10,
        dexterity=11,
        hitpoints=10,
        intelligence=8,
        protection=10,
        race="human",
        name="lordling"
    )
    player.score = 0  # additional attribute only for player
    bozo = Monster(
        strength=11,
        dexterity=10,
        hitpoints=11,
        intelligence=8,
        protection=10,
        race="orc",
        name="bozo"
    )
    axe = MeleeWeapon(
        attack=5,
        defense=1,
        damage=3,
        length=1,
        shortdescr="axe",
    )
    shortsword = MeleeWeapon(
        attack=5,
        defense=2,
        damage=2,
        length=2,
        shortdescr="army sword"
    )
    player.activeMeleeWeapon = shortsword.number
    bozo.activeMeleeWeapon = axe.number
    print "--------battle---------"
    #melee(player, bozo)
    testFight(player, bozo, 100)


if __name__ == '__main__':
    game()
