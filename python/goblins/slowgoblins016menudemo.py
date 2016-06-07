"""part of http://ThePythonGameBook.com
source code:

https://github.com/horstjens/ThePythonGameBook/blob/master/
python/goblins/slowgoblins016menudemo.py

menu demo

This demo is a nearly identical copy of the simplemenu tutorial
of  Christian Hausknecht, located at
https://github.com/Lysander/snippets/tree/master/Python/python-misc/simplemenus

and licensed under the gpl license.

see https://github.com/Lysander/snippets/blob/master/Python/python-misc/simplemenus/submenu.py
for the original file

"""
__license__ = 'gpl3'  # see http://www.gnu.org/licenses/gpl.html'

import sys


class Goblin(object):
    """demo class, goblins only have a name attribute"""

    def __init__(self, name="anonymous goblin"):
        self.name = name


def integer_input(min_value, max_value, prompt=">", default=-1):
    """ask and returns an integer between min_value and max_value"""
    while True:
        try:
            choice = int(input(prompt))
            if choice == "":
                choice = default
            if min_value <= choice < max_value:
                return choice
            else:
                raise IndexError
        except (ValueError, IndexError):
            print("please enter numbers between {} and {} only".format(min_value, max_value - 1))


def info():
    """demo method"""
    print("this is some information")


def rename_team(team_number):
    """rename teamnames in the teamnamces dict and in the menu dict"""
    # hier kommt nicht der neue name
    new_name = input("please enter new name for team number {}: ".format(team_number))
    if new_name == "":
        print("nothing renamed")
        return
    team_names[team_number] = new_name
    # change the submenu
    key = "team{0}".format(team_number)
    menu[key][0][0] = "exit menu of team {} (team {})".format(new_name, team_number)
    # root menu entry for team 0 is 1, entry for team 1 is 2 ....
    menu["root"][team_number + 1][0] = "manage team {} (team {})".format(new_name, team_number)


def buy_goblin(team_number):
    """create goblin instance and add it to team"""
    new_name = input("please give the new goblin a nickname:")
    if new_name == "":
        new_name = "not yet nicknamed goblin"
    teams[team_number].append(Goblin(new_name))
    print("You purchased {} for the team!".format(new_name))


def show_goblins(team_number):
    """print a list of all goblins in this team"""
    print("------- all goblins of team {} ------".format(team_names[team_number]))
    for goblin in teams[team_number]:
        print(goblin.name)
    print("--------------------------")

# -------------------------- Christan's Code ----------------


def print_menu(menu):
    """
    Function that prints our menu items. It adds an numeric index to each
    item in order to make that the choosebale index for the user.

    :param menu: tuple with menu definition
    """
    # start numbering the items with number 0
    for index, item in enumerate(menu, 0):
        print("{}  {}".format(index, item[0]))


def handle_menu(menudef):
    """
    Core function of our menu system. It handles the complete process of
    printing the menu, getting the user input and calling the corresponding
    function.

    We recognize if a 'submenu' is called by comparing the type of the second
    parameter of our entry item. If that is a string, we interpret that as the
    key of a corresponding 'menu' and make that the current menu to operate on.

    :param menudef: dict with menu definition
    """
    category = "root"
    while True:
        # Hint: 'menu' does not name the complete menu-structure (the dict)
        # but instead it just refenrences the entries for one dictionary-key.
        # And those we can call just 'menu'. Perhaps 'entries' would have been
        # a better name, but that would have broken the parameter naming of
        # the tow other functions.
        menu = menudef[category]
        print_menu(menu)
        choice = integer_input(0, len(menu))
        _, command = menu[choice]  # the _ is a name vor a variable
        # here is the 'submenu'-magic. Just change the dictionary key and go
        # on in the loop, so the chosen submenu will be handled.
        if isinstance(command, str):
            category = command
        else:
            command()


if __name__ == "__main__":
    teams = {0: [], 1: []}
    team_names = {0: "team 0", 1: "team 1"}
    teams[0].append(Goblin("Stinky"))
    teams[1].append(Goblin("Grunty"))
    menu = {
        "root": [
            # to handle a function with parameters, use lambda:
            ["Exit the main menu", lambda: sys.exit(0)],
            # go to another submenu by writing the submenu name
            ["Manage team 0", "team0"],
            ["Manage team 1", "team1"],
            # call a function by writing the funciton name
            ["Show info", info]
        ],
        "team0": [
            ["Exit menu of team 0", "root"],
            ["show goblins", lambda: show_goblins(0)],
            ["buy goblin", lambda: buy_goblin(0)],
            ["rename team", lambda: rename_team(0)],
            ["Show info... ", info]
        ],
        "team1": [
            ["Exit menu of team 1", "root"],
            ["showgoblins", lambda: show_goblins(1)],
            ["buy goblin", lambda: buy_goblin(1)],
            ["rename team", lambda: rename_team(1)],
            ["Show info... ", info]
        ]
    }

    handle_menu(menu)
