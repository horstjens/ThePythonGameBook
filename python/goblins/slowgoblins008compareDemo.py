"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins008comareDemo.py"""


def sign(a, b):
    """Compares a with b and returns  '<' or '=' or '>' depending on compare result between a and b."""
    if a < b:
        return "<"
    elif a > b:
        return ">"
    else:
        return "="


def compareValues(hpA, attA, defA, hpB, attB, defB):
    """returns a string with a table comparing the values of A and B"""
    text = "\n          Stiny | vs. | Grunty "
    text += "\n ---------------+-----+-----------"
    text += "\n hitpoints: {0:3d} |  {1}  | {2:3d}".format(hpA, sign(hpA, hpB), hpB)
    text += "\n attack:    {0:3d} |  {1}  | {2:3d}".format(attA, sign(attA, attB), attB)
    text += "\n defense:   {0:3d} |  {1}  | {2:3d}".format(defA, sign(defA, defB), defB)
    text += "\n"
    return text


hitpoints_stinky = 22
attack_stinky = 6
defense_stinky = 9
hitpoints_grunty = 43
attack_grunty = 5
defense_grunty = 3

# python lines can be several physical lines long if inside brackets
print(
    compareValues(
        hitpoints_stinky, attack_stinky, defense_stinky, hitpoints_grunty,
        attack_grunty, defense_grunty
    )
)
