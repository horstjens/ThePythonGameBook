"""part of http://ThePythonGameBook.com
# source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins010.py"""

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


def output(c_round, hp_stinky, hp_grunty):
    """returns a string with combat_round and both hitpoints"""
    return "\n---combat round {0:2d}--- Stinky: {1:2d} Grunty: {2:2d}".format(c_round, hp_stinky, hp_grunty)


def strike(attA, defB, hpB, counterstrike=False):
    """A strikes B. The function returns the new hpB and a text String with the combat report"""
    if counterstrike:
        t = "counterattack"
    else:
        t = "attack"
    rollAtt = random.randint(1, 6)
    rollDef = random.randint(1, 6)
    scoreA = attA + rollAtt
    scoreD = defB + rollDef
    if scoreA > scoreD:
        striketext = "Sucessfull {} !  ({} > {})".format(t, scoreA, scoreD)
        damage = scoreA - scoreD
        hpB -= damage
        striketext += "\n...doing {} damage.".format(damage)
    else:
        striketext = "The {} failed... ({} <= {})".format(t, scoreA, scoreD)
    return hpB, striketext


def game():
    """the Goblin Dice Duel game main function"""
    hitpoints_stinky = 10
    attack_stinky = 6
    defense_stinky = 9
    hitpoints_grunty = 15
    attack_grunty = 10
    defense_grunty = 3
    combat_round = 0
    text = ""

    text += "\n --- Goblin Dice Duel ---\n\n"
    text += compareValues(
        hitpoints_stinky, attack_stinky, defense_stinky, hitpoints_grunty,
        attack_grunty, defense_grunty
    )
    text += "\n ==== combat start ===="

    while hitpoints_stinky > 0 and hitpoints_grunty > 0:
        text += output(combat_round, hitpoints_stinky, hitpoints_grunty)
        combat_round += 1
        if random.randint(0, 1) == 0:
            text += "\nStinky strikes first: "
            hitpoints_grunty, line = strike(
                attack_stinky, defense_grunty, hitpoints_grunty, False
            )
            text += line
            if hitpoints_grunty > 0:
                text += "\nCounterstrike of Grunty: "
                hitpoints_stinky, line = strike(
                    attack_grunty, defense_stinky, hitpoints_stinky, True
                )
                text += line
        else:
            text += "\nGrunty strikes first: "
            hitpoints_stinky, line = strike(
                attack_grunty, defense_stinky, hitpoints_stinky, False
            )
            text += line
            if hitpoints_stinky > 0:
                text += "\nCounterstrike of Stinky: "
                hitpoints_grunty, line = strike(
                    attack_stinky, defense_grunty, hitpoints_grunty, True
                )
                text += line

    text += output(combat_round, hitpoints_stinky, hitpoints_grunty)  # output of final strike
    text += "\nGame Over"
    if hitpoints_stinky > hitpoints_grunty:
        text += "\nStinky wins"
    elif hitpoints_grunty > hitpoints_stinky:
        text += "\nGrunty wins"
    else:
        text += "Nobody wins ?"
    print(text)


if __name__ == "__main__":
    game()  # call the game function if this code is not imported but directly called
