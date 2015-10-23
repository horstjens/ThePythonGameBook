"""
RPG game combat sim using a recursion and functions from module random.

Name:             goblindice003.py 
Purpose:          introducing a recursion and default parameters.
                  introducing  __name__ and __main__ 
idea:             simulate open-ended dice using a recursion, make
                  use of random.random() and random.gauss() functions
                  for a more detailed combat model.
edit this code:   https://github.com/horstjens/ThePythonGameBook/
                  blob/master/python/goblindice/goblindice003.py
edit tutorial:    https://github.com/horstjens/ThePythonGameBook/
                  blob/master/goblindice003.rst                  
main project:     http://ThePythonGameBook.com
Author:           Horst JENS, horst.jens@spielend-programmieren.at
Licence:          gpl, see http://www.gnu.org/licenses/gpl.html
"""
import random


def re_roll(faces=6, start=0):
    """open ended die throw, can re-roll at highest face)"""
    while True:
        roll = random.randint(1, faces)
        if roll != faces:
            return roll + start
        return re_roll(faces, roll - 1 + start)


def strike(attacker_attack, defender_defense, attacker, defender):
    """Return damage value and text output for logfile"""
    # add a random float from 0.0 to 1.0 to the attack value
    attack = attacker_attack + random.random()
    # add a random float ( 0.5 +- something) to the defense value
    defense = defender_defense + random.gauss(0.5, 0.2)
    output = ""
    dmg = 0
    if attack > defense:  # did the attacker hit his opponent ?
        output += "\n Smack! {} hits {} with a most skilled ".format(
            attacker, defender
        )
        output += "attack: {:.2f}>{:.2f}".format(attack, defense)
        # use 2 dice with re-rolling (re-roll at 6, return sum)
        dmg = re_roll()  # no parameters, using default values
        output += "\n ...and inflicts {} damage!".format(dmg)
    else:
        output += "\n Oh no! {} does not even hit {} ".format(
            attacker, defender
        )
        output += "{:.2f} < {:.2f}".format(attack, defense)
    return dmg, output


def combat_sim():
    """2 player combat sim.
    
    Returns a text string with the combat log to either a print function
    (if __name__== "__main__") or to another calling program with a more
    complex display method."""

    # Grunty, is better at defending than at attacking
    grunty_attack = 0.4  # float (decimal)  instead of integer
    grunty_defense = 0.7  # defense is also a float now
    grunty_hitpoints = 100  # hitpoints are still integer, as is damage

    # Stinky is better and faster at attacking and can take more damage
    stinky_attack = 0.8  # can be interpreted as 80% success chance
    stinky_defense = 0.3
    stinky_hitpoints = 130

    logfile = " Grunty vs. Stinky"  # string
    combatround = 0

    while stinky_hitpoints > 0 and grunty_hitpoints > 0:
        combatround += 1
        logfile += "\n*** Round: {} ***".format(combatround)
        logfile += " Grunty has {} hitpoints,".format(grunty_hitpoints)
        logfile += " Stinky has {} hitpoints".format(stinky_hitpoints)
        # Stinky always strikes first
        damage, text = strike(stinky_attack, grunty_defense, "Stinky", "Grunty")
        grunty_hitpoints -= damage
        logfile += text
        if grunty_hitpoints < 1:  # can Grunty still strike back ?
            break  # exit this while loop
        damage, text = strike(grunty_attack, stinky_defense, "Grunty", "Stinky")
        stinky_hitpoints -= damage
        logfile += text
    logfile += "\n" + "- " * 20
    if grunty_hitpoints > stinky_hitpoints:
        winner = "Grunty"
    else:
        winner = "Stinky"
    logfile += "\nVictory for {} after {} rounds".format(winner, combatround)
    return logfile


if __name__ == "__main__":
    print(combat_sim())
