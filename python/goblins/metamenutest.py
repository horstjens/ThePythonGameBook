#!/usr/bin/env python

#
#  Copyright (C) 2012  Christian Hausknecht
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
    ~~~~~~~~~~~
    metamenu.py
    ~~~~~~~~~~~

    Even more sophisticated approach compared to `submenu.py` as this module
    adds some meta data to each menu, so there is more information about each
    menu printed and therefore a better usability is provided.

    Still it is realized only with basic Python data types.

    There are only decent changes compared to `submenu.py`, to be more precise
    we enhance the menu structure at the 'value' part of the menu keys.

    Each menu consists of this dictionary structure:

        {
            "root": {
                "title": <string>
                "items": (
                    (<string>, <function object>),

                        or

                    (<string>, <string of key to submenu>)
                )
            },
            "submenu1": {
                "title": <string>
                "items": (
                    ...
                )
            }
        }

    We added a dictionary as value of the outer keys. In this dictionary there
    have to be the two keys 'title', followed by the name of the menu as
    string, and 'items'

    Every menu must habe a 'root' key. That is the entrypoint for the
    `handle_menu` function. To make an entry that leads to a submenu, just
    put the key of that submenu as second parameter of one menu item. This
    way you can also 'go back' from a submenu to the 'root'-menu.

    To be more generic, each 'callable' can be used as second argument.

    The user can choose via an computed index, which action should be
    triggered by the core function `handle_menu`.

    Hint: `print_menu` has changed as the new parameter `title` is now needed,
    which is basically the main issue of this menu version ;-)

    This is esspecially written for beginners, so there is no magic like
    `functools.partial` or some closures to create demo functions.

    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import sys

#
# Some little demo functions that does not have any sensfull functionality
#


def hello():
    print("Hallo Welt!")


def python():
    print("Python rocks!")


def special():
    print("Wow! So special we must put it into a submenu...")

#
# Functions for our simple menu system
#


def print_menu(entries, title):
    """
    Function that prints our menu items. It adds an numeric index to each
    item in order to make that the choosebale index for the user.

    :param entries: tuple with entries of a (sub)menu
    :param title: string
    """
    print("", "-" * len(title), "{}".format(title), "-" * len(title), sep="\n")
    for index, entry in enumerate(entries, 1):
        print("{}  {}".format(index, entry[0]))


def get_user_input(entries):
    """
    This function implements a simple user input with validation. As the
    input data should match with existing menu items, we check, if the value
    is valid.

    :param entries: tuple with entries of a (sub)menu

    :returns: int
    """
    while True:
        try:
            choice = int(input("Ihre Wahl?: ")) - 1
            if 0 <= choice < len(entries):
                return choice
            else:
                raise IndexError
        except (ValueError, IndexError):
            print("Bitte nur Zahlen aus dem Bereich 1 - {} eingeben".format(len(entries)))


def handle_menu(menudef):
    """
    Core function of our menu system. It handles the complete process of
    printing the menu, getting the user input and calling the corresponding
    function.

    We recognize if a 'submenu' is called by comparing the type of the second
    parameter of our entry item. If that is a string, we interpret that as the
    key of a corresponding 'menu' and make that the current menu to operate on.

    The name of the entries to one menu-key now changed to the name `entries`.

    We also extract the `title` of one (sub)menu in order to show more
    information in the `print_menu`-function.

    :param menudef: dict with menu definition
    """
    category = "root"
    while True:
        title = menudef[category]["title"]
        entries = menudef[category]["items"]
        print_menu(entries, title)
        choice = get_user_input(entries)
        _, command = entries[choice]
        # here is the 'submenu'-magic. Just change the dictionary key and go
        # on in the loop, so the chosen submenu will be handled.
        if isinstance(command, str):
            category = command
        else:
            command()


def main():
    # just some demonstration menu structure. We have two menus, the 'root'
    # menu and one submenu called 'submenu'. As second option in the 'submenu'
    # we can leave the menu back to the 'root'-menu.
    menu = {
        "root": {
            "title": "Hauptmenü",
            "items": (
                ("Hallo", hello), ("Python", python), ("Submenu", "submenu"),
                ("Exit", lambda: sys.exit(0))
            )
        },
        "submenu": {
            "title": "Submenü",
            "items": (
                ("Spezial", special),
                ("Zurück", "root"),
            )
        }
    }

    # make it so! :-)
    handle_menu(menu)


if __name__ == "__main__":
    main()
