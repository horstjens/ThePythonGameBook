"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins012.py

use gauss random function instead of randint
"""
__license__ = 'gpl3'  # see http://www.gnu.org/licenses/gpl.html'

import random


class Goblin(object):
    """generic goblin with randomized stat values"""

    def __init__(self):
        """creates a new goblin instance"""
        self.attack = random.gauss(10, 2)  # float value
        self.defense = random.gauss(10, 2)  # float value
        self.hitpoints = random.gauss(20, 3)  # float value
        self.fullhealth = self.hitpoints  # copy

    def report(self):
        """returns a string with the actual stats"""
        text = "\natt: {} def: {}hp: {}".format(
            self.attack, self.defense, self.hitpoints
        )
        text += "\ni have {0:3f}% of my hitpoints".format(
            self.hitpoints / self.fullhealth
        )
        return text


def sign(a, b):
    """compares a with b and returns a "<","=" or ">" sign """
    if a < b:
        return "<"
    elif a > b:
        return ">"
    else:
        return "="


def compareValues(a, b):
    """returns a string with a table comparing the values of goblins a and b"""
    text = "\n          Stinky | vs. | Grunty "
    text += "\n ----------------+-----+-----------"
    text += "\n hitpoints: {:>4.1f} |  {}  | {:>4.1f}".format(a.hitpoints, sign(a.hitpoints, b.hitpoints), b.hitpoints)
    text += "\n attack:    {:>4.1f} |  {}  | {:>4.1f}".format(a.attack, sign(a.attack, b.attack), b.attack)
    text += "\n defense:   {:>4.1f} |  {}  | {:>4.1f}".format(a.defense, sign(a.defense, b.defense), b.defense)
    text += "\n"
    return text


def output(combatround, a, b):
    """returns a string with combatround and both hitpoints form a and b"""
    return "\n---combat round {0:3d}--- Stinky: {1:.0f} Grunty: {2:.0f}".format(
        combatround, a.hitpoints, b.hitpoints
    )


def strike(attacker, defender, counterstrike=False):
    """attacker strikes at defender. The function changes the new
    hitpoints of the defender and returns a text String with the combat report.
    counterstrike (boolean) indicates that this is a counterattack or not."""
    if counterstrike:
        t = "counterattack"
    else:
        t = "attack"
    rollAtt = random.randint(1, 6)
    rollDef = random.randint(1, 6)
    scoreA = attacker.attack + rollAtt
    scoreD = defender.defense + rollDef
    if scoreA > scoreD:
        striketext = "Sucessfull {0} !  ({1:.2f} > {2:.2f})".format(t, scoreA, scoreD)
        damage = scoreA - scoreD
        defender.hitpoints -= damage
        striketext += "\n...doing {0:.2f} damage.".format(damage)
    else:
        striketext = "The {0} failed... ({1:.2f} <= {2:.2f})".format(t, scoreA, scoreD)
    return striketext


def game():
    """the Goblin Dice Duel game main function"""
    stinky = Goblin()
    grunty = Goblin()

    combatround = 0
    text = ""

    text += "\n --- Goblin Dice Duel ---\n\n"
    text += compareValues(stinky, grunty)
    text += "\n ==== combat start ===="

    while stinky.hitpoints > 0 and grunty.hitpoints > 0:
        text += output(combatround, stinky, grunty)
        combatround += 1
        if random.randint(0, 1) == 0:
            text += "\nStinky strikes first: "
            text += strike(stinky, grunty, False)
            if grunty.hitpoints > 0:
                text += "\nCounterstrike of Grunty: "
                text += strike(grunty, stinky, True)
        else:
            text += "\nGrunty strikes first: "
            text += strike(grunty, stinky, False)
            if stinky.hitpoints > 0:
                text += "\nCounterstrike of Stinky: "
                text += strike(stinky, grunty, True)
    text += output(combatround, stinky, grunty)  # output of final strike
    text += "\nGame Over"
    if stinky.hitpoints > grunty.hitpoints:
        text += "\nStinky wins"
    elif grunty.hitpoints > stinky.hitpoints:
        text += "\nGrunty wins"
    else:
        text += "Nobody wins ?"
    print(text)


if __name__ == "__main__":
    game()
