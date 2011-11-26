# -*- coding: utf-8 -*-
import random
import easygui

def goblintaufe():
    vorname = ["Georg", "Dieter", "Grunzdumpf",
                "Heino", "Draufhau", "Minimampf"]
    kleinwort = ["sehr", "wirklich", "etwas", "manchmal",
                 "selten", "kaum", "möglicherweise"]
    eigenschaft = ["stinkende", "grunzende", "üble", 
                   "übelriechende", "dauerkotzende"]
    hauptwort = ["Messerwerfer", "Axtfresser", "Kinderverhauer",
                 "Mistwerfer", "Fassroller", "Grunzer",
                 "Schildbeisser", "Kampfbrotverdauer"]
    name = random.choice(vorname)
    name += " der "
    name += random.choice(kleinwort)
    name += " "
    name += random.choice(eigenschaft)
    name += " "
    name += random.choice(hauptwort)
    return name

#for x in range(10):
#    print goblintaufe()    
                 
class Goblin(object):
    
    def __init__(self):
        self.name = goblintaufe()
        self.hitpoints = 50 + random.randint(-10,20)
        self.damage = 10 + random.randint(-5,5)
        self.attack = 10 + random.randint(-5,5)
        self.defense = 10 + random.randint( -5,5)
        self.armor = random.randint(1,5)
        self.summe = self.hitpoints + self.damage + self.attack + self.defense + self.armor
        
    def gruss(self):
        print " - * - * - * - * - * -"
        print "ich bin ", self.name
        print "ich habe", self.hitpoints, " hitpoints"
        print "ich verursache", self.damage, " Schaden"
        print "meine Attackwert: ", self.attack
        print "mein Defensewert: ", self.defense
        print "meine Rüstung: ", self.armor
        print "meine Summe: ", self.summe
        print "--------------------------"

def wuerfel(anzahl_wuerfel=1, anzahl_flaechen=6):
    summe = 0
    for x in range(anzahl_wuerfel):
        summe += random.randint(1, anzahl_flaechen)
    return summe

def domwuerfel():
    """wenn man eine 6 wuerfelt, darf man 
       noch einmal wuerfeln"""
    summe = 0
    w = random.randint(1, 6)
    if w == 6:
        w = 5 + domwuerfel()
    return w
    
def schlag(angreifer, verteidiger):
    watt = wuerfel() + angreifer.attack
    wdef = wuerfel() + verteidiger.defense
    wdam = wuerfel() + angreifer.damage
    warm = wuerfel() + verteidiger.armor
    
    print angreifer.name, " greift an mit ", watt
    print verteidiger.name, " verteidigt mit ", wdef
    
    if watt > wdef:
        print "Ein Treffer"
        print angreifer.name , "Schaden:" , wdam
        print verteidiger.name, "Rüstung:" , warm
        
        if wdam > warm:
            print "Schaden: ", wdam-warm
            verteidiger.hitpoints -= wdam-warm
            print verteidiger.name, " hat noch "
            print verteidiger.hitpoints, " Hitpoints übrig"
            
            if verteidiger.hitpoints < 1:
                print verteidiger.name , " hat verloren "
        else:        
           print angreifer.name + " ist zu schwach um die Rüstung zu durchschlagen"
    else:
        print angreifer.name + " haut daneben"

easygui.msgbox("Goblin-Kampf", "runde 0", "start",
               image="tuxstick50x50.png" )

a = Goblin()
b = Goblin()

a.attack = input("attackwert goblin a (%i)>" % a.attack)
a.defense = input("defensewert goblin a (%i)>" % a.defense)
a.damage = input("damagewert goblin a (%i)>" % a.damage)
a.armor = input("armorwert goblin a (%i)>" % a.armor)
a.hitpoints = input("hitpoints goblin a (%i)>" % a.hitpoints)

b.attack = input("attackwert goblin b (%i)>" % b.attack)
b.defense = input("defensewert goblin b (%i)>" % b.defense)
b.damage = input("damagewert goblin b (%i)>" % b.damage)
b.armor = input("armorwert goblin b (%i)>" % b.armor)
b.hitpoints = input("hitpoints goblin b (%i)>" % b.hitpoints)


a.gruss()
b.gruss()



                    
# kampf
runde = 0
while (a.hitpoints > 0) and (b.hitpoints > 0):
    runde += 1
    print "----===== Runde: %i =====------" % runde
    schlag(a,b)        
    if b.hitpoints > 0:
        schlag(b,a)
    if runde > 100:
        print "Der Kampf dauert zu lange. Abbruch"
        break

    
    
    
    
    
     
