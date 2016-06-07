"""
Simple python program using combat rules from role-playing games.

Name:             goblindice001.py 
Purpose:          teaching basic python: while, if, elif, else, +=
edit this code:   https://github.com/horstjens/ThePythonGameBook/
                  blob/master/python/goblindice/goblindice001.py
edit tutorial:    https://github.com/horstjens/ThePythonGameBook/
                  blob/master/goblindice001.rst                  
main project:     http://ThePythonGameBook.com
Author:           Horst JENS, horst.jens@spielend-programmieren.at
Licence:          gpl, see http://www.gnu.org/licenses/gpl.html
"""
import random

# Grunty, the untrained goblin, has some attack skill
grunty_attack = 3  # integer value

# his opponent is a punchbag or wooden testdummy with poor defense
testdummy_hitpoints = 200  # integer value
testdummy_defense = 1

logfile = " Grunty vs. punchbag"  # string
combatround = 0

while testdummy_hitpoints > 0:
    combatround += 1  # the same as: combatround = combatround +1
    logfile += "\n*** Round: " + str(combatround) + " ***"  # \n new line
    logfile += ", target has {} hitpoints".format(testdummy_hitpoints)
    attack = grunty_attack + random.randint(1, 6) + random.randint(1, 6)
    defense = testdummy_defense + random.randint(1, 6)  # roll one die
    if attack > defense:  # did Grunty hit the testdummy ?
        logfile += "\nSmack! Grunty hits his target with a most "
        logfile += "skilled attack: {} > {}".format(attack, defense)
        damage = random.randint(1, 6) + random.randint(1, 6) - 2  # 0-10 damage
        testdummy_hitpoints -= damage  # subtract damage from hitpoints
        logfile += "\n...and inflicts {} damage!".format(damage)
    elif attack == defense:
        logfile += "\nGrunty manages to nearly hit the target, but "
        logfile += "he makes no damage {0} = {0}".format(attack)
    else:
        logfile += "\n Oh no! Grunty does not even hit his target "
        logfile += "{} < {}".format(attack, defense)
logfile += "\n" + "- " * 20  # make a dashed line by multiplying a string
logfile += "\nVictory for Grunty after {} rounds".format(combatround)

print(logfile)
