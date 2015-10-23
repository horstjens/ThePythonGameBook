"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins009.py"""

import random


def sign(a, b):
    """compares a with b and returns a "<","=" or ">" sign"""
    if a < b:
        return "<"
    elif a > b:
        return ">"
    else:
        return "="


def compareValues(hpA, attA, defA, hpB, attB, defB):
    """returns a string with a table comparing the values of A and B"""
    text = "\n         Stinky | vs. | Grunty "
    text += "\n ---------------+-----+-----------"
    text += "\n hitpoints: {0:3d} |  {1}  | {2:3d}".format(hpA, sign(hpA, hpB), hpB)
    text += "\n attack:    {0:3d} |  {1}  | {2:3d}".format(attA, sign(attA, attB), attB)
    text += "\n defense:   {0:3d} |  {1}  | {2:3d}".format(defA, sign(defA, defB), defB)
    text += "\n"
    return text


def output(combat_round, hitpoints_stinky, hitpoints_grunty):
    """returns a string with combat_round and both hitpoints"""
    return "\n{0:2d} Stinky: {1:2d} Grunty: {2:2d}".format(combat_round, hitpoints_stinky, hitpoints_grunty)


def game():
    """the Goblin Dice Duel game main function"""
    hitpoints_stinky = 22
    attack_stinky = 6
    defense_stinky = 9
    hitpoints_grunty = 43
    attack_grunty = 5
    defense_grunty = 3
    combat_round = 0
    text = ""

    text += ("\n --- Goblin Dice Duel ---\n\n")
    text += compareValues(
        hitpoints_stinky, attack_stinky, defense_stinky, hitpoints_grunty,
        attack_grunty, defense_grunty
    )
    text += ("\n\nround    hitpoints\n")
    while hitpoints_stinky > 0:
        text += output(combat_round, hitpoints_stinky, hitpoints_grunty)
        combat_round += 1
        hitpoints_grunty -= random.randint(0, 6)
        if hitpoints_grunty <= 0:
            break
        hitpoints_stinky -= random.randint(0, 6)
    text += output(combat_round, hitpoints_stinky, hitpoints_grunty)  # output of final strike
    text += ("\nGame Over")
    if hitpoints_stinky > hitpoints_grunty:
        text += ("\nStinky wins")
    elif hitpoints_grunty > hitpoints_stinky:
        text += ("\nGrunty wins")
    else:
        text += ("Nobody wins ?")
    text += ("\nthank you for playing Goblin Dice Duel. bye-bye!")
    # printing everything
    print(text)


if __name__ == "__main__":
    game()  # call the game function in this code is not imported but directly called
