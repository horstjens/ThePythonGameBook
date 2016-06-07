#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       items.py
#
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


class Item(object):
    book = {}  # a dictionary to store all items and with its numbers
    number = 0

    def __init__(self, name=""):
        if name == "":
            name = "the not yet named thing"
        self.name = name
        self.number = Item.number  # unique number
        Item.number += 1  # prepare next unique number
        Item.book[self.number] = self  # store yourself in the book
        self.percent = 100.0  # float 100.0 means perfect, 0.0 means useless
        self.weight = 0.0  # weight in kg
        self.goldvalue = 0  # how much would this item cost in a shop
        self.category = "misc"  #
        print "item number %i with the name %s is created" % (
            self.number, self.name
        )

    def inspect(self):
        print "--------------"
        print "inspecting item %i , named %s" % (self.number, self.name)
        print "this is a: %s " % self.__class__.__name__
        for key in self.__dict__:
            print key, " : ", self.__dict__[key]
        print "--------------"


class Sword(Item):
    def __init__(self, name=""):
        Item.__init__(self, name)  # call the parent __init__ function
        self.category = "weapon"
        self.attackBonus = 2
        self.defenseBonus = 2
        self.damageBonus = 4
        #self.armorBonus = 0
        self.length = 1.0  # weapon length in meter
        self.weight = 3  # kg


class Shield(Item):
    def __init__(self, name=""):
        Item.__init__(self, name)  # call the parent __init__ function
        self.category = "shield"
        self.attackBonus = -1
        self.defenseBonus = 3
        self.damageBonus = 0
        self.armorBonus = 7
        self.weight = 5  # kg
        self.coverpercent = 40.0


def main():
    # hier gehts los
    Item("lucky charm")
    temp = Sword("Ice")
    temp.attackBonus = 15
    temp = Shield("old oak shield")
    temp.coverpercent = 70.7
    for x in Item.book.keys():
        Item.book[x].inspect()
    return 0


if __name__ == '__main__':
    main()
