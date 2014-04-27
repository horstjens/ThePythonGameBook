"""
Name:          goblindice001.py 
Purpose:       combat sim of one goblin against a test dummy
edit code:     https://gist.github.com/horstjens/11267180#file-goblindice001-py
edit website:  https://github.com/horstjens/ThePythonGameBook/tree/gh-pages
main project:  http://ThePythonGameBook.com
Author:        Horst JENS, horst.jens@spielend-programmieren.at
Licence:       gpl, see http://www.gnu.org/licenses/gpl.html
"""
 
import random 
 
# Grunty, the untrained goblin, has some attack skill
grunty_attack = 0.3   # float value 
 
# the wooden, unmovable testdummy has poor defense, but many hitpoints
testdummy_hitpoints = 200 # integer value
testdummy_defense = 0.1 
 
logfile = " Grunty vs. the wooden testdummy"   # string
combatround = 0 
 
while testdummy_hitpoints > 0:
    combatround += 1 # the same as: combatround = combatround +1
    logfile += "\n*** Round: {} *** The Testdummy ".format(combatround) 
    logfile += "has {} hitpoints left.".format(testdummy_hitpoints)
    attack= grunty_attack + random.random() 
    defense = testdummy_defense + random.random()
    # did Grunty hit the testdummy ?
    if attack > defense:
        logfile += "\n Smack! Grunty hits the testdummy with a most "
        logfile += "skilled attack: "
        logfile +=  "({:.2f} > {:.2f})".format(attack, defense)
        # calculate damage
        damage = random.randint(1,10) # integer value
        # make damage
        testdummy_hitpoints -= damage 
        logfile += "\n...and does {} damage!".format(damage)
    else:
        logfile += "\n Oh no! Grunty does not even hit the testdummy "
        logfile +=  "({:.2f} <= {:.2f})".format(attack, defense)
# vicotry for Grunty !
logfile += "\n------------------"
logfile += "Victory for Grunty after {} rounds".format(combatround)
 
print(logfile)

