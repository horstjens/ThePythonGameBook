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
        
    def relative_health(self):
        """return percentage of full health"""
        return self.hitpoints / self.fullhealth
        
def re_roll(faces=6, start=0):
    """open ended die throw, can re-roll at highest face)"""
    while True: 
        roll = random.randint(1, faces)
        if roll != faces:
            return roll + start 
        return re_roll(faces, roll-1+start )
            
def strike(attacker, defender):
    """Calculate effect of strike and returns combat log text string"""
    attack = attacker.attack + random.gauss(0.5,0.2)  
    defense = defender.defense + random.gauss(0.5,0.1) 
    output = ""   
    dmg = 0       
    if attack > defense: # did the attacker hit his opponent ?
        output += "\n Smack! {} hits {} with a most skilled ".format(
                    attacker.name, defender.name)
        output += "attack: {:.2f}>{:.2f}".format(attack, defense)
        # use 2 dice with re-rolling (re-roll at 6, return sum)
        dmg = re_roll()  # no parameters, using default values
        output += "\n ...and inflicts {} damage!".format(dmg)
        # changing hitpoints inside the class instance
        defender.hitpoints -= dmg
    else:
        output += "\n Oh no! {} does not even hit {} ".format(
                    attacker.name, defender.name)
        output += "{:.2f} < {:.2f}".format(attack, defense)
    return output  

def combat_sim():
    """simulating combat between 2 monsters with random first strike"""
    grunty = Monster("Grunty",0.4, 0.7, 95) # name, attack, defense, hp
    stinky = Monster("Stinky",0.8, 0.3, 109)
    combatants = [grunty,stinky] # a list of all participating monsters
    logfile = " Grunty vs. Stinky"  
    combatround = 0 

    while stinky.hitpoints > 0 and grunty.hitpoints >0:
        combatround += 1 
        logfile += "\n*** Round: {} ***".format(combatround) 
        logfile += " Grunty has {} hp {:.0f}%,".format(grunty.hitpoints,
                                        grunty.relative_health()*100)
        logfile += " Stinky has {} hp {:.0f}%".format(stinky.hitpoints, 
                                        stinky.relative_health()*100)
        random.shuffle(combatants) #  sort the combatants by random
        first, second = combatants[0], combatants[1] #first strike?
        logfile += "\n{} strikes first:".format(first.name)
        logfile += strike(first, second) # this may change the hitpoints
        if second.hitpoints < 1:         # first striker already victor?
            break                        # exit this while loop
        logfile += strike(second, first)
    logfile += "\n" + "- " * 20 
    if first.hitpoints > second.hitpoints:
        winner = first.name
    else:
        winner = second.name
    logfile += "\nVictory for {} after {} rounds".format(winner,combatround)
    return logfile

if __name__=="__main__":
   print(combat_sim())

