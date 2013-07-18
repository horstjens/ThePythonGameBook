"""part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins010.py"""

import random

def sign(a,b):
    """compares a with b and returns a "<","=" or ">" sign"""
    if a < b:
        return "<"
    elif a > b:
        return ">"
    else:
        return "="

def compareValues(hpA, attA, defA, hpB, attB, defB):
    """returns a string with a table comparing the values of A and B"""
    text = "\n          Stiny | vs. | Grunty "
    text+= "\n ---------------+-----+-----------"
    text+= "\n hitpoints: {0:3d} |  {1}  | {2:3d}".format(hpA, sign(hpA, hpB), hpB )
    text+= "\n attack:    {0:3d} |  {1}  | {2:3d}".format(attA, sign(attA, attB), attB)
    text+= "\n defense:   {0:3d} |  {1}  | {2:3d}".format(defA, sign(defA,defB), defB)
    text+= "\n"
    return text

def output(combatround,hitpointsStinky,hitpointsGrunty):
    """returns a string with combatround and both hitpoints"""
    return "\n---combat round {0:2d}--- Stinky: {1:2d} Grunty: {2:2d}".format(combatround, hitpointsStinky, hitpointsGrunty)

def strike(attA, defB, hpB, counterstrike=False):
    """A strikes B. The function returns the new hpB and a text String with the combat report"""
    if counterstrike:
        t = "counterattack"
    else:
        t = "attack"
    rollAtt = random.randint(1,6)
    rollDef = random.randint(1,6)
    scoreA = attA + rollAtt
    scoreD = defB + rollDef
    if scoreA > scoreD:
        striketext = "Sucessfull {} !  ({} > {})".format(t, scoreA,scoreD)
        damage = scoreA - scoreD
        hpB -= damage
        striketext += "\n...doing {} damage.".format(damage)
    else:
        striketext = "The {} failed... ({} <= {})".format(t, scoreA, scoreD)
    return hpB, striketext

def game():
    """the Goblin Dice Duel game main function"""
    hitpointsStinky = 10
    attackStinky = 6
    defenseStinky = 9
    hitpointsGrunty = 15
    attackGrunty = 10
    defenseGrunty = 3
    combatround = 0
    text = ""

    text+="\n --- Goblin Dice Duel ---\n\n"
    text+=compareValues(hitpointsStinky, attackStinky, defenseStinky,
                        hitpointsGrunty, attackGrunty, defenseGrunty)
    text+="\n ==== combat start ===="

    while hitpointsStinky >0 and hitpointsGrunty > 0:
        text+=output(combatround, hitpointsStinky, hitpointsGrunty)
        combatround += 1
        if random.randint(0,1) == 0:
            text+="\nStinky strikes first: "
            hitpointsGrunty, t = strike(attackStinky, defenseGrunty, hitpointsGrunty, False)
            text+=t
            if hitpointsGrunty > 0:
                text+="\nCounterstrike of Grunty: "
                hitpointsStinky, t = strike(attackGrunty, defenseStinky, hitpointsStinky, True)
                text+=t
        else:
            text+="\nGrunty strikes first: "
            hitpointsStinky, t = strike(attackGrunty, defenseStinky, hitpointsStinky, False)
            text+=t
            if hitpointsStinky>0:
                text+="\nCounterstrike of Stinky: "
                hitpointsGrunty, t = strike(attackStinky, defenseGrunty, hitpointsGrunty, True)
                text+=t

    text+=output(combatround, hitpointsStinky, hitpointsGrunty) # output of final strike
    text+= "\nGame Over"
    if hitpointsStinky > hitpointsGrunty:
        text+= "\nStinky wins"
    elif hitpointsGrunty > hitpointsStinky:
        text+= "\nGrunty wins"
    else:
        text+= "Nobody wins ?"
    print(text)

if __name__ == "__main__":
    game() # call the game function if this code is not imported but directly called
else:
    pass # do nothing, this code was imported by another python program.
