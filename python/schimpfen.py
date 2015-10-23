# -*- coding: utf-8 -*-
import random as r

e = [
    "ungewaschen", "verseucht", "fett", "ausgekotzt", "zickig", "großmäulig",
    "hirnverbrannt", "breiförmig", "dauerrülpsend", "nervig", "ekelerregend",
    "kopflos", "blöd", "vertrottelt"
]
m = [
    "Bock", "Wurm", "Esel", "Nasenbär", "Rotzlöffel", "Volltrottel", "Pfosten",
    "Koffer"
]
w = [
    "Sau", "Motte", "Schlange", "Blindschleiche", "Wanze", "Laus", "Ratte",
    "Zimtzicke", "Nacktschnecke", "Giftspinne", "Schreckschraube"
]
s = ["Trampeltier", "Stinktier", "Faultier"]
q = [
    "sehr", "titanisch", "unerträglich", "unglaublich", "alptraumhaft",
    "außerirdisch", "äußerst", "absolut", "voll", "gigantisch"
]

# männlich, weiblich oder sächlich ?
for x in range(10):
    geschlecht = r.choice("mmmmmwwwwwwwwws")
    if geschlecht == "m":
        endung = "er"
        hauptwort = r.choice(m)
    elif geschlecht == "w":
        endung = "e"
        hauptwort = r.choice(w)
    else:
        endung = "es"
        hauptwort = r.choice(s)

    eigenschaft = r.choice(e) + endung
    qa = r.choice(q)
    satz = "Du {} {} {}!".format(qa, eigenschaft, hauptwort)

    print satz
