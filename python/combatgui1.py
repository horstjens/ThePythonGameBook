import Tkinter
import simplerpg


class MyGui():
    def __init__(self, master):
        self.label1 = Tkinter.Label(master, text=player.name).grid(row=0, column=0)
        self.label2 = Tkinter.Label(master, text=" vs. ").grid(row=0, column=1)
        self.label3 = Tkinter.Label(master, text=bozo.name).grid(row=0, column=2)
        self.v1 = Tkinter.StringVar()
        self.v2 = Tkinter.StringVar()
        self.v1.set("1")
        self.v2.set("4")
        self.label4 = Tkinter.Label(master, textvariable=self.v1).grid(row=1, column=0)
        self.label5 = Tkinter.Label(master, text="battles won").grid(row=1, column=1)
        self.label6 = Tkinter.Label(master, textvariable=self.v2).grid(row=1, column=2)
        self.buttonquit = Tkinter.Button(master, text='Quit', command=master.quit).grid(row=3, column=3, sticky=Tkinter.W, pady=4)
        self.buttonfight = Tkinter.Button(master, text='Fight', command=self.fight).grid(row=3, column=0, sticky=Tkinter.W, pady=4)

    def fight(self):
        v = {}
        vi1, vi2, v = simplerpg.testFight(player, bozo, 100)
        print "result: ", vi1, vi2
        self.v1.set(str(vi1))
        self.v2.set(str(vi2))
        #print app.label4.text
        #self.label4=Tkinter.Label(master, text=self.victorys1.get()).grid(row=1, column=0)
        # self.label4.configure(text=self.victorys1.get()) #geht net, none type object has no configure
        print self.v1.get()  # get and set work fine, but how can i force an update of the label field?

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
print "--------battle---------"
#melee(player, bozo)
#simplerpg.testFight(player, bozo, 100)

root = Tkinter.Tk()
app = MyGui(root)
root.mainloop()
