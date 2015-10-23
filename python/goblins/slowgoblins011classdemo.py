"""part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins011classdemo.py"""


class Goblin(object):
    counter = 0

    def __init__(self):
        self.attack = 5
        self.defense = 7
        self.hitpoints = 10

    def report(self):
        if self.hitpoints > 0:
            return "i am fine"
        else:
            return "i am in a bad shape"


stinky = Goblin()
grunty = Goblin()
print("Stinky.attack:", stinky.attack)
print("Grunty.defense:", grunty.defense)
print("Grunty.hitpoints:", grunty.hitpoints)
grunty.hitpoints -= 4
print("Grunty take 4 damage:", grunty.hitpoints)
print("Grunty says:", grunty.report())
grunty.hitpoints -= 7
print("Grunty take 7 damage:", grunty.hitpoints)
print("Grunty says:", grunty.report())
