"""part of http://ThePythonGameBook.com
source code:

https://github.com/horstjens/ThePythonGameBook/blob/master/
python/goblins/slowgoblins019.py

TODO:    #compare teams of goblins
         #change sort order
         #sort compare tables by column (attribute)
         #toggle sleep for each goblin
         #check money when buying new goblins

some code is based on the menudemo of  Christian Hausknecht, located at
https://github.com/Lysander/snippets/tree/master/Python/python-misc/simplemenus

and licensed under the gpl license.

see https://github.com/Lysander/snippets/blob/master/Python/python-misc/simplemenus/submenu.py
for the original file

for usage of operator.attrgetter, see:
http://wiki.python.org/moin/HowTo/Sorting/
"""
__license__ = 'gpl3'  # see http://www.gnu.org/licenses/gpl.html'

import sys
import random
import operator


class Goblin(object):
    """demo class, goblins only have a name attribute
    and a unique number (managed by a class attribute)"""
    number = 0  # class attribute

    def __init__(self, name="anonymous goblin", **kwargs):
        """creates a new goblin instance
        every attribute can be overwritten with an argument like
        g = Goblin(attack = 33.2)
        this will overwrite the random self.attack attribute with 33.2
        """
        self.name = name
        self.attack = random.gauss(Config.attack, 2)  # float values
        self.defense = random.gauss(Config.defense, 2)
        # always create an goblin with twice the "normal" hitpoints
        # to make him cost real money
        self.hitpoints = random.gauss(Config.hitpoints * 2, 3)
        self.fullhealth = self.hitpoints
        self.defense_penalty = 0  # integer value
        self.sleep = False  # boolean
        # statistics
        self.damage_dealt = 0
        self.damage_received = 0
        self.wins = 0
        self.fights = 0
        # overwrite attributes if keywords were passed as arguments
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        # but do not mess around with number
        self.number = Goblin.number  # access class attribute
        Goblin.number += 1  # prepare class attribute for next goblin
        # calculate value based on averages described in class Config
        self.value = self.calculate_value()

    def calculate_value(self):
        """calculates a 'value' of the goblin based on att, def and hp.
        Formula:
        1.) compare attack, defense and hitpoints with the average
        values found in class Config.
        2.) take the difference between actual attribute and average
        3.) square the difference but keep the sign
        4.) build a sum of those squared differences
        Effect should be that a few big differences from the "norm" cost
        a lot more gold than many small differences"""
        value = 0.0
        for attr in ["attack", "defense", "hitpoints"]:
            actual_value = self.__getattribute__(attr)
            average_value = Config.__getattribute__(Config, attr)
            diff = actual_value - average_value
            if diff < 0:
                sign = -1
            else:
                sign = 1
            value += sign * diff**2  # square the diff but keep the sign
        return value

    def restore_health(self):
        """restore original hitpoints"""
        self.hitpoints = self.fullhealth

    def report(self):
        """returns a string with all the actual stats"""
        text = ""
        for stat in filter(lambda x: "__" not in x, dir(self)):
            if "bound method" in str(self.__getattribute__(stat)):
                continue  # ignore methods, only take attributes
            #print(stat)
            attr = self.__getattribute__(stat)
            #testing if attribute is string or int or float
            if stat == "sleep":  # sleep is boolean
                text += "\n{:>20}: {}".format(stat, attr)
            elif isinstance(attr, int) or isinstance(attr, float):
                text += "\n{:>20}: {:5.1f}".format(stat, attr)
            else:
                text += "\n{:>20}: {}".format(stat, attr)
        return text

    def __repr__(self):
        """overwriting the representation method of a goblin object"""
        return "{:>15} ({:>2}): {:8.2f} {:8.2f} {:8.2f}   {:8.2f}  {}".format(
            self.name, self.number, self.attack, self.defense, self.hitpoints,
            self.value, self.sleep
        )


def integer_input(prompt=">", default=-1, minv=-9999999, maxv=9999999):
    """ask and returns an integer between min_value and max_value"""
    while True:
        try:
            choice = int(input(prompt))
            if choice == "":
                choice = default
            if minv <= choice <= maxv:
                return choice
            else:
                raise IndexError
        except (ValueError, IndexError):
            print("please enter numbers between {} and {} only".format(minv, maxv))


def float_input(prompt=">", default=0, minv=-9999999, maxv=9999999):
    """ask and returns an float value from the user"""
    answer_ok = False
    while not answer_ok:
        answer = input(prompt)
        if answer == "":
            return default
        try:
            newvalue = float(answer)
            if minv <= newvalue <= maxv:
                answer_ok = True
            else:
                raise IndexError
        except (ValueError, IndexError):
            print("integer or float with decimal point please")
            print("enter value between {} and {}".format(minv, maxv))
    return newvalue


def text_input(prompt=">", default=""):
    """text input function that always returns a text an can handle
    default values if the user only type the ENTER key"""
    new_value = input(prompt)
    if new_value == "":
        return default
    else:
        return new_value


def info():
    """demo method"""
    print("this is some information")


def buy_goblin(team_number):
    """create goblin instance and add it to team"""
    #check money
    if Config.gold[team_number] <= 0:
        print("Your team has no gold! Sell some goblins first")
        return
    new_name = input("please give the new goblin a nickname:")
    if new_name == "":
        new_name = "unnamed goblin"
    g = Goblin(new_name)
    gnr = g.number
    Config.teams[team_number][gnr] = g  # add new goblin to team
    Config.gold[team_number] -= g.value  # deduct gold for buying
    key = "editgoblins{}".format(team_number)
    # add edit goblin menu entry
    Config.menu[key].append(["edit goblin {} ({})".format(new_name, gnr), lambda: edit_goblin(gnr, team_number)])
    print("You purchased {} for the team!".format(new_name))


def show_goblins(team_number):
    """print a list of all goblins in this team and the team gold
    also sum all stats (att, def, hitpoints, value) for the team"""
    print("{} team {} gold: {:6.2f} {}".format(20 * "-", Config.team_names[team_number], Config.gold[team_number], 20 * "-"))
    print("{:>20}: attack   defense hitpoints     value  sleep".format("attribute"))
    print("{:>20}: {:8.2f} {:8.2f} {:8.2f}".format("normal", Config.attack, Config.defense, Config.hitpoints))
    print("{:>20}{}".format("--goblin (unique nr)", 46 * "-"))
    sumatt, sumdef, sumhp, sumval, sumsleep = 0, 0, 0, 0, 0
    sortlist = []
    for (gnr, goblin) in Config.teams[team_number].items():
        sortlist.append(goblin)
    for goblin in sorted(
        sortlist,
        key=operator.attrgetter(Config.sortorder[0], Config.sortorder[1], Config.sortorder[2]),
        reverse=Config.reverse
    ):
        print(goblin)  # this calls self.__repr__ of Goblin instance
        sumatt += goblin.attack
        sumdef += goblin.defense
        sumhp += goblin.hitpoints
        sumval += goblin.value
        sumsleep += goblin.sleep  # True count as 1, False as 0
    print(66 * "=")
    print("{:>20}: {:8.2f} {:8.2f} {:8.2f}   {:8.2f} {:>2}".format("sum", sumatt, sumdef, sumhp, sumval, sumsleep))
    print(66 * "-")


def rename_team(team_number):
    """rename teamnames in the teamnamces dict and in the menu dict"""
    new_name = input("please enter new name for team number {}: ".format(team_number))
    if new_name == "":
        print("nothing renamed")
        return
    Config.team_names[team_number] = new_name
    # change the submenu
    key = "team{0}".format(team_number)
    Config.menu[key][0][0] = "exit menu of team {} (team {})".format(new_name, team_number)
    # root menu entry for team 0 is 1, entry for team 1 is 2 ....
    Config.menu["root"][team_number + 1][0] = "manage team {} (team {})".format(new_name, team_number)


def edit_goblin(number, team_number):
    """let the user change attributes of an individual goblin
    need goblins unique number and team number"""
    #get goblin
    if not number in Config.teams[team_number]:
        print("no goblin with this number is in your team")
        return
    goblin = Config.teams[team_number][number]
    print("current values for this goblin:", goblin.report())
    print("please enter the new (>0) values for name, att, def and hp:")
    namechange = False
    old_name = goblin.name
    for stat in ["name", "attack", "defense", "hitpoints"]:
        attr = goblin.__getattribute__(stat)
        old_value = attr
        print("old value (Enter to accept) for {} is: {}".format(stat, old_value))
        if isinstance(attr, float):
            new_value = float_input("new value ?", old_value, old_value)
        elif isinstance(attr, int):
            new_value = integer_input("new value ?", old_value, old_value)
        elif isinstance(attr, str):
            new_value = text_input("new value ?", old_value)
        else:
            print("unknown attribute error")  # boolean ?
            raise ValueError
        if new_value == old_value:
            print("nothing changed")
            continue
        if stat == "name":
            goblin.name = new_value
            namechange = True
        else:
            # display gold cost before and let user confirm
            # new value is always bigger than old value
            norm = Config.__getattribute__(Config, stat)
            # signed(delta_new_norm_)squared - signed(delta_old_norm)squared
            dnn = new_value - norm  # delta new norm
            don = old_value - norm  # delta old norm
            if dnn >= 0:
                sdnns = dnn**2  # signed delta new norm squared
            else:
                sdnns = -1 * dnn**2
            if don >= 0:
                sdons = don**2  # signed delta old norm squared
            else:
                sdons = -1 * don**2
            price = sdnns - sdons
            print("This change would cost: {} gold".format(price))
            print("Your team has {} gold".format(Config.gold[team_number]))
            if price > Config.gold[team_number]:
                print("nothing changed, due to lack of gold")
                continue
            if integer_input("accept? 0=cancel, 1=yes", 0, 0, 1) == 1:
                goblin.__setattr__(stat, new_value)
                print("changed {} from {} to {}".format(stat, old_value, new_value))
                Config.gold[team_number] -= price
            else:
                print("nothing changed because user canceled")
    # ---- end of for loop ----
    # if new name, change menu entry, search for old entry
    if namechange:
        new_name = goblin.name
        key = "editgoblins{}".format(team_number)
        subkey = "edit goblin {} ({})".format(old_name, number)
        newkey = "edit goblin {} ({})".format(new_name, number)
        for entry in Config.menu[key]:
            if entry[0] == subkey:
                entry[0] = newkey
                break
        else:
            print("error.. i did not found the correct menu entry")


def sell_goblin(team_number):
    """ask user for goblins unique number and delete this goblin
       from team and delete corresponding edit goblin menu entry"""
    # create prompt
    p = "\n".join(
        (
            "Each goblins has a unique goblin number. You can",
            "see this number using the 'show all goblins' menu",
            "it is the number in round parentheses",
            "unique number of goblin you want to sell ?"
        )
    )
    print(p)
    # Goblin.number (class attribute) - 1 is the hightest possible
    # number of a goblin. It does not mean that this goblin still exist
    delnumber = integer_input("(-1 is cancel) >", -1, -1, Goblin.number)
    if delnumber == -1:
        print("sell action canceled")
        return
    # check if this goblin exist in the selected team
    if not delnumber in Config.teams[team_number]:
        print("No goblin with this number exist in your team")
        return
    d = Config.teams[team_number].pop(delnumber)  # d is the deleted goblin
    Config.gold[team_number] += d.value  # add gold for selling goblin
    print("Goblin {} sold".format(d.name))
    #remove editmenu entrys
    key = "editgoblins{}".format(team_number)
    subkey = "edit goblin {} ({})".format(d.name, delnumber)
    for entry in Config.menu[key]:
        if entry[0] == subkey:
            Config.menu[key].remove([entry[0], entry[1]])
            break
    else:
        print("error.. i did not found the correct menu entry")


def toggle_sleep(team_number):
    """ask user for goblin number and toggle sleep status"""
    # create prompt
    p = "\n".join(
        (
            "Each goblins has a unique goblin number. You can",
            "see this number using the 'show all goblins' menu",
            "it is the number in round parentheses",
            "unique number of goblin you want sleep/wake up ?"
        )
    )
    print(p)
    sleepnumber = integer_input("(-1 is cancel) >", -1, -1, Goblin.number)
    if sleepnumber == -1:
        print("toggle sleep action canceled")
        return
    # check if this goblin exist in the selected team
    if not sleepnumber in Config.teams[team_number]:
        print("No goblin with this number exist in your team")
        return
    g = Config.teams[team_number][sleepnumber]
    g.sleep = not g.sleep  # toggle sleep
    print("Sleep status of Goblin {}({}) changed to {}".format(g.name, g.number, g.sleep))


def print_menu(menu):
    """print visible menu points. menu is the key in the giant menu
    dict so that the corresponding (sub) menu is printed-
    see original code and tutorial of Christian Hausknecht
    https://github.com/Lysander/snippets/tree/master/Python/python-misc/simplemenus
    """
    # start numbering the items with number 0
    for index, item in enumerate(menu, 0):
        print("{}  {}".format(index, item[0]))


def handle_menu(menudef):
    """ print menu, ask for action, userinput, does action, print menu
    menudef is the menu structure ( giant dict )
    see original code and tutorial of Christian Hausknecht
    https://github.com/Lysander/snippets/tree/master/Python/python-misc/simplemenus
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
        choice = integer_input(default=0, minv=0, maxv=len(menu) - 1)
        _, command = menu[choice]  # the _ is a name vor a variable
        # here is the 'submenu'-magic. Just change the dictionary key and go
        # on in the loop, so the chosen submenu will be handled.
        if isinstance(command, str):
            category = command
        else:
            command()


def sign(a, b):
    """compares a with b and returns a "<","=" or ">" sign """
    if a < b:
        return "<"
    elif a > b:
        return ">"
    else:
        return "="


def compare_teams(a, b):
    """printing comparasion table for two teams"""
    print("-----------------------------")
    print("comparing team {} ({}) with team {} ({})".format(Config.team_names[a], a, Config.team_names[b], b))
    print("{:>20}: {:6.1f}   {} {:6.1f}".format("gold", Config.gold[a], sign(Config.gold[a], Config.gold[b]), Config.gold[b]))
    print("{:>20}: {:6.1f}   {} {:6.1f}".format("goblins", len(Config.teams[a]), sign(len(Config.teams[a]), len(Config.teams[b])), len(Config.teams[b])))

    for stat in ["attack", "defense", "hitpoints", "value", "sleep"]:
        statsum = {a: 0, b: 0}
        for x in [a, b]:
            for (gbnr, goblin) in Config.teams[x].items():
                statsum[x] += goblin.__getattribute__(stat)
        print("{:>20}: {:6.1f}   {} {:6.1f}".format(stat, statsum[a], sign(statsum[a], statsum[b]), statsum[b]))


# funcitons for sorting
def display_sortorder():
    print("the current sortorder is:")
    print(Config.sortorder)
    print("reverse: ", Config.reverse)


def toggle_reverse():
    Config.reverse = not Config.reverse
    print("changed reverse to ", Config.reverse)


def sort(rank):
    """ask the user for a keyword and manipulates Config.sortorder"""
    valid = ["attack", "defense", "hitpoints", "value", "name", "sleep"]
    print("The keyword for sorting must be one of those words:")
    print(valid)
    print("(without the brackets, quotes and commas)")
    answer = text_input("please enter the attribute for sorting:>")
    if not answer in valid:
        print("sorry this was not a valid answer. nothing changed")
        return
    old = Config.sortorder[rank]
    Config.sortorder[rank] = answer
    print("changed sortorder for rank {} from {} to {}".format(rank, old, answer))


class Config(object):
    """class to hold various 'global' variables until a clean place to
    store those variables is found. (all done as class instances)"""
    teams = {0: {}, 1: {}}  # a dict of dicts
    gold = {0: 500, 1: 500}  # inital design points for each team
    team_names = {0: "team 0", 1: "team 1"}
    #  average values to create goblins and calculate their money value
    hitpoints = 10  # it's twice that number in reality to make goblins expensive
    attack = 10
    defense = 10
    sortorder = ["attack", "defense", "hitpoints", "value"]
    reverse = False
    menu = {
        "root": [
            # to handle a function with parameters, use lambda:
            ["Exit the main menu", lambda: sys.exit(0)],
            # go to another submenu by writing the submenu name
            ["Manage team 0", "team0"],
            ["Manage team 1", "team1"],
            # call a function by writing the funciton name
            ["Compare teams", lambda: compare_teams(0, 1)],
            ["Show info", info]
        ],
        "team0": [
            ["Exit menu of team 0", "root"],
            ["show all goblins", lambda: show_goblins(0)],
            ["buy goblin", lambda: buy_goblin(0)],
            ["rename team", lambda: rename_team(0)],
            ["edit goblins", "editgoblins0"],
            ["sell goblin (number)", lambda: sell_goblin(0)],
            ["toggle sleep for goblin (number)", lambda: toggle_sleep(0)],
            ["Change sort order", "sortorder"], ["Show info... ", info]
        ],
        "team1": [
            ["Exit menu of team 1", "root"],
            ["show all goblins", lambda: show_goblins(1)],
            ["buy goblin", lambda: buy_goblin(1)],
            ["rename team", lambda: rename_team(1)],
            ["edit goblins", "editgoblins1"],
            ["sell goblin (number)", lambda: sell_goblin(1)],
            ["toggle sleep for goblin (number)", lambda: toggle_sleep(1)],
            ["Change sort order", "sortorder"], ["Show info... ", info]
        ],
        "editgoblins0": [
            ["Exit the edit goblins menu", "team0"],
            ["edit goblin Stinky (0)", lambda: edit_goblin(0, 0)]
        ],
        "editgoblins1": [
            ["Exit the edit goblins menu", "team1"],
            ["edit goblin Grunty (1)", lambda: edit_goblin(1, 1)]
        ],
        "sortorder": [
            ["Exit the sortorder menu", "root"],
            ["display sort order", display_sortorder],
            ["toogle reverse sorting", toggle_reverse],
            ["edit first sort key", lambda: sort(0)],
            ["edit second sort key", lambda: sort(1)],
            ["edit third sort key", lambda: sort(2)],
            ["edit fourth sort key", lambda: sort(3)]
        ]
    }


def main():
    """the main function of the game"""
    gob0 = Goblin("Stinky")
    gob0nr = gob0.number  # first goblin, his number is 0
    gob1 = Goblin("Grunty")
    gob1nr = gob1.number  # second goblin, his number is 1
    # inside each team dict, the goblin number is key,
    # the goblin instance (the goblin himself) is the value
    Config.teams[0][gob0nr] = gob0  # Stinky joins team0
    Config.teams[1][gob1nr] = gob1  # Grunty joins team1
    # adjust the gold for each team to reflect buying the first goblin
    Config.gold[0] -= gob0.value
    Config.gold[1] -= gob1.value
    # start the menu, start the game
    handle_menu(Config.menu)


if __name__ == "__main__":
    main()
