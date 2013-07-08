__author__ = 'Horst JENS'
# see http://ThePythonGameBook.com
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
    return "\n{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(combatround, hitpointsStinky, hitpointsGrunty)


def game():
    """the Goblin Dice Duel game main function"""
    hitpointsStinky = 22
    attackStinky = 6
    defenseStinky = 9
    hitpointsGrunty = 43
    attackGrunty = 5
    defenseGrunty = 3
    combatround = 0
    text = ""


    text+=("\n --- Goblin Dice Duel ---\n\n")
    text+=compareValues(hitpointsStinky, attackStinky, defenseStinky,
                        hitpointsGrunty, attackGrunty, defenseGrunty)
    text+=("\n\nround    hitpoints\n")
    while hitpointsStinky >0:
        text+=output(combatround, hitpointsStinky, hitpointsGrunty)
        combatround += 1
        hitpointsGrunty -= random.randint(0,6)
        if hitpointsGrunty <= 0:
            break
        hitpointsStinky -= random.randint(0,6)
    text+=output(combatround, hitpointsStinky, hitpointsGrunty) # output of final strike
    text+=("\nGame Over")
    if hitpointsStinky > hitpointsGrunty:
        text+=("\nStinky wins")
    elif hitpointsGrunty > hitpointsStinky:
        text+=("\nGrunty wins")
    else:
        text+=("Nobody wins ?")
    text+=("\nthank you for playing Goblin Dice Duel. bye-bye!")
    # printing everything
    print(text)

if __name__ == "__main__":
    game() # call the game function in this code is not imported but directly called
else:
    pass # do nothing, this code was imported by another python program.