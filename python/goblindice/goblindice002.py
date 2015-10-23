"""
Simple two player combat sim example using a function.

Name:             goblindice002.py 
Purpose:          introducing a function, parameters and return values
idea:             simple combat simulating 2 players
edit this code:   https://github.com/horstjens/ThePythonGameBook/
                  blob/master/python/goblindice/goblindice002.py
edit tutorial:    https://github.com/horstjens/ThePythonGameBook/
                  blob/master/goblindice002.rst                  
main project:     http://ThePythonGameBook.com
Author:           Horst JENS, horst.jens@spielend-programmieren.at
Licence:          gpl, see http://www.gnu.org/licenses/gpl.html
"""
import random

# Grunty, is better at defending than at attacking
grunty_attack = 4  # integer value
grunty_defense = 7
grunty_hitpoints = 100

# Stinky is better and faster at attacking and can take more damage
stinky_attack = 8
stinky_defense = 2
stinky_hitpoints = 130

logfile = " Grunty vs. Stinky"  # string
combatround = 0

# strike function to avoid writing nearly identical code twice


def strike(attacker_attack, defender_defense, attacker, defender):
    """Return damage value and text output for logfile"""
    attack = attacker_attack + random.randint(1, 6) + random.randint(1, 6)
    defense = defender_defense + random.randint(1, 6) + random.randint(1, 6)
    output = ""  # local variable, only valid inside this function
    dmg = 0  # default damage, also a local variable
    if attack > defense:  # did the attacker hit his opponent ?
        output += "\n Smack! {} hits {} with a most ".format(attacker, defender)
        output += "skilled attack: {} > {}".format(attack, defense)
        dmg = random.randint(1, 6) + random.randint(1, 6) - 2  # 0-10 damage
        output += "\n ...and inflicts {} damage!".format(dmg)
    elif attack == defense:
        output += "\n{} manages to nearly to hit {}".format(attacker, defender)
        output += ", but he makes no damage {0} = {0}".format(attack)
    else:
        output += "\n Oh no! {} does not even hit {} ".format(
            attacker, defender
        )
        output += "{} < {}".format(attack, defense)
    return dmg, output


while stinky_hitpoints > 0 and grunty_hitpoints > 0:
    combatround += 1  # the same as: combatround = combatround +1
    logfile += "\n*** Round: " + str(combatround) + " ***"  # \n new line
    logfile += " Grunty has {} hitpoints,".format(grunty_hitpoints)
    logfile += " Stinky has {} hitpoints".format(stinky_hitpoints)
    # Stinky always strikes first
    damage, text = strike(stinky_attack, grunty_defense, "Stinky", "Grunty")
    grunty_hitpoints -= damage
    logfile += text
    if grunty_hitpoints < 1:  # can Grunty still strike back ?
        break  # exit this while loop
    # Grunty strikes back at Stinky
    damage, text = strike(grunty_attack, stinky_defense, "Grunty", "Stinky")
    stinky_hitpoints -= damage
    logfile += text
logfile += "\n" + "- " * 20  # make a dashed line by multiplying a string
if grunty_hitpoints > stinky_hitpoints:
    winner = "Grunty"
else:
    winner = "Stinky"
logfile += "\nVictory for {} after {} rounds".format(winner, combatround)

print(logfile)
