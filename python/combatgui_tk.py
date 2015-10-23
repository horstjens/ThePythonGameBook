#/usr/bin/env/python
#       combatgui_tk.py
#       needs simplerpg.py in the same folder
#       and makes an Tkinter gui for it
#
#       2012 by Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#
#       a simple role-playing game, inspired by rogue-like games
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       see http://www.gnu.org/licenses/gpl.html for GNU General Public License

import Tkinter
import simplerpg


class MyGui():
    def __init__(self, master):
        """creates the Tkinter Gui with all Labels and Buttons etc."""
        self.label1 = Tkinter.Button(master, text=player.name).grid(row=0, column=1)  # was once a label, is no w a button
        self.label2 = Tkinter.Label(master, text=" Fighters: ").grid(row=0, column=0)
        self.label3 = Tkinter.Button(master, text=bozo.name).grid(row=0, column=2)  # was once a label, is no w a button
        self.v1 = Tkinter.StringVar()
        self.v2 = Tkinter.StringVar()
        self.vrounds = Tkinter.StringVar()  # result table
        self.vleftwins = Tkinter.StringVar()  # result table
        self.vrightwins = Tkinter.StringVar()  # result table
        self.vtotal = Tkinter.StringVar()  # result table
        self.v4 = Tkinter.StringVar()  # rounds to fight
        self.v4.set(100)
        self.v1.set(0)
        self.v2.set(0)
        self.label4 = Tkinter.Label(master, textvariable=self.v1).grid(row=1, column=1)
        self.label5 = Tkinter.Label(master, text="battles won;").grid(row=1, column=0)
        self.label6 = Tkinter.Label(master, textvariable=self.v2).grid(row=1, column=2)
        self.label7 = Tkinter.Label(master, text="# of rounds").grid(row=2, column=0)
        self.label8 = Tkinter.Label(master, text="victorys").grid(row=2, column=1)
        self.label9 = Tkinter.Label(master, text="victorys").grid(row=2, column=2)
        self.label10 = Tkinter.Label(master, text="# of battles").grid(row=2, column=3)
        # courier font for non-proportional chars (each char has the same width, good for tables)
        self.message7 = Tkinter.Message(master, font="courier", textvariable=self.vrounds).grid(row=3, column=0)
        self.message8 = Tkinter.Message(master, font="courier", textvariable=self.vleftwins).grid(row=3, column=1)
        self.message9 = Tkinter.Message(master, font="courier", textvariable=self.vrightwins).grid(row=3, column=2)
        self.message10 = Tkinter.Message(master, font="courier", textvariable=self.vtotal).grid(row=3, column=3)
        self.label11 = Tkinter.Label(master, text="# of battles to fight:").grid(row=0, column=3)
        self.entry11 = Tkinter.Entry(master, textvariable=self.v4).grid(row=1, column=3)
        self.buttonquit = Tkinter.Button(master, text='Quit', command=master.quit).grid(row=5, column=3, sticky=Tkinter.W, pady=4)
        self.buttonfight = Tkinter.Button(master, text='Fight', command=self.fight).grid(row=5, column=0, sticky=Tkinter.W, pady=4)

    def fight(self):
        """calculates a number of fights and print the results"""
        vi1, vi2, v = simplerpg.testFight(player, bozo, int(self.v4.get()))  # self.v4 is number of battles
        self.v1.set(str(vi1))
        self.v2.set(str(vi2))
        textrounds = ""
        textleftwins = ""
        textrightwins = ""
        texttotal = ""
        for x in v.keys():  # create result table
            # right align number with 8 whitespaces and a line ending
            textrounds += "{:>8}".format("%i :\n" % x)
            textleftwins += "{:>8}".format("%i \n" % v[x][0])
            textrightwins += "{:>8}".format("%i \n" % v[x][1])
            texttotal += "{:>8}".format("%i \n" % v[x][2])
        self.vrounds.set(textrounds)
        self.vleftwins.set(textleftwins)
        self.vrightwins.set(textrightwins)
        self.vtotal.set(texttotal)

# initialize fighters and weapons
#from simplerpg
# edit those values !
player = simplerpg.Monster(
    strength=10,
    dexterity=11,
    hitpoints=10,
    intelligence=8,
    protection=10,
    race="human",
    name="lordling"
)
player.score = 0  # additional attribute only for player
bozo = simplerpg.Monster(
    strength=11,
    dexterity=10,
    hitpoints=11,
    intelligence=8,
    protection=10,
    race="orc",
    name="bozo"
)
axe = simplerpg.MeleeWeapon(
    attack=5,
    defense=1,
    damage=3,
    length=1,
    shortdescr="axe",
)
shortsword = simplerpg.MeleeWeapon(
    attack=5,
    defense=2,
    damage=2,
    length=2,
    shortdescr="army sword"
)
player.activeMeleeWeapon = shortsword.number
bozo.activeMeleeWeapon = axe.number
#print "--------battle---------"
#melee(player, bozo)
#simplerpg.testFight(player, bozo, 100)

root = Tkinter.Tk()
app = MyGui(root)
root.mainloop()
