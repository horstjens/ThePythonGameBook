"""
RPG combat sim with monster class and variable first strike order

Name:             goblindice004.py 
idea:             decide at each combat round who strikes first
edit this code:   https://github.com/horstjens/ThePythonGameBook/
                  blob/master/python/goblindice/goblindice004.py
edit tutorial:    https://github.com/horstjens/ThePythonGameBook/
                  blob/master/goblindice004.rst                  
main project:     http://ThePythonGameBook.com
Author:           Horst JENS, horst.jens@spielend-programmieren.at
Licence:          gpl, see http://www.gnu.org/licenses/gpl.html
"""
import random


class Monster(object):
    """general-purpose monster class for combats"""

    def __init__(self, name, attack, defense, hitpoints):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hitpoints = hitpoints
        self.fullhealth = hitpoints

    def __repr__(self):
        """a string describing myself, used in print and others"""
        return "{} att: {:.2f} def: {:.2f} hp: {}/{}".format(
            self.name, self.attack, self.defense, self.hitpoints,
            self.fullhealth
        )

    def relative_health(self):
        """return percentage of full health"""
        return self.hitpoints / self.fullhealth


def re_roll(faces=6, start=0):
    """open ended die throw, can re-roll at highest face)"""
    while True:
        roll = random.randint(1, faces)
        if roll != faces:
            return roll + start
        return re_roll(faces, roll - 1 + start)


def strike(attacker, defender):
    """Calculate effect of strike and returns combat log text string"""
    attack = attacker.attack + random.gauss(0.5, 0.2)
    defense = defender.defense + random.gauss(0.5, 0.1)
    output = ""
    dmg = 0
    if attack > defense:  # did the attacker hit his opponent ?
        output += "\n Smack! {} hits {} with a most skilled ".format(
            attacker.name, defender.name
        )
        output += "attack: {:.2f}>{:.2f}".format(attack, defense)
        # use 2 dice with re-rolling (re-roll at 6, return sum)
        dmg = re_roll()  # no parameters, using default values
        output += "\n ...and inflicts {} damage!".format(dmg)
        # changing hitpoints inside the class instance
        defender.hitpoints -= dmg
    else:
        output += "\n Oh no! {} does not even hit {} ".format(
            attacker.name, defender.name
        )
        output += "{:.2f} < {:.2f}".format(attack, defense)
    return output


def combat_sim(monster1, monster2):
    """simulating combat between 2 monsters with random first strike
    
    requires 2 Monster instances as arguments
    returns victor name, victor hitpoints, number of rounds, logtext"""

    monsterlist = [monster1, monster2]  # a list of all participants
    log = "{} vs. {}".format(monster1.name, monster2.name)
    combatround = 0

    while monster1.hitpoints > 0 and monster2.hitpoints > 0:
        combatround += 1
        log += "\n*** Round: {} ***".format(combatround)
        log += " {} has {} hp ({:.0f}%),".format(
            monster1.name, monster1.hitpoints, monster1.relative_health() * 100
        )
        log += " Stinky has {} hp ({:.0f}%)".format(
            monster2.name, monster2.hitpoints, monster2.relative_health() * 100
        )
        random.shuffle(monsterlist)  # sort the combatants by random
        first, second = monsterlist[0], monsterlist[1]  #first strike?
        log += "\n{} strikes first:".format(first.name)
        log += strike(first, second)  # this may change the hitpoints
        if second.hitpoints < 1:  # first striker already victor?
            break  # exit this while loop
        log += strike(second, first)  # revenge
    log += "\n" + "- " * 20
    if first.hitpoints > second.hitpoints:
        winner = first
    else:
        winner = second
    log += "\nVictory for {} after {} rounds".format(winner.name, combatround)
    return winner.name, winner.hitpoints, combatround, log


if __name__ == "__main__":
    m1 = Monster("Grunty", 0.4, 0.7, 95)  # name, attack, defense, hp
    m2 = Monster("Stinky", 0.8, 0.3, 109)  #
    print(combat_sim(m1, m2)[3])  # only print the 4th returned value
