"""part of http://ThePythonGameBook.com
source code: 

https://github.com/horstjens/ThePythonGameBook/blob/master/
python/goblins/slowgoblins018.py

TODO: edit goblin with full goblin class,
      ask isinstance (str, float) for each attribute before editing
      show and change status ( active, training, healing...) for goblin
      #calculate stat sum
      #show stat sum
      manage team money
      manage items
      equip goblins
      

This demo is based on the submenu example
of  Christian Hausknecht, located at
https://github.com/Lysander/snippets/tree/master/Python/python-misc/simplemenus

and licensed under the gpl license. 

see https://github.com/Lysander/snippets/blob/master/Python/python-misc/simplemenus/submenu.py
for the original file 

"""
__license__ = 'gpl3' # see http://www.gnu.org/licenses/gpl.html'

import sys
import random

class Goblin(object):
    """demo class, goblins only have a name attribute
    and a unique number (managed by a class attribute)"""
    number = 0 # class attribute
    
    def __init__(self, name="anonymous goblin", **kwargs):
        """creates a new goblin instance
        every attribute can be overwritten with an argument like
        
        g = Goblin(attack = 33.2)
        
        this will overwrite the random self.attack attribute with 33.2
        """
        self.name = name
        # float values
        self.attack = random.gauss(Config.attack, 2)
        self.defense = random.gauss(Config.defense, 2)
        self.hitpoints = random.gauss(Config.hitpoints, 3) 
        self.fullhealth = self.hitpoints 
        # integer values 
        self.defense_penalty = 0
        #statistics
        self.damage_dealt = 0
        self.damage_received = 0
        self.wins = 0
        self.fights = 0
        # overwrite attributes if keywords were passed as arguments
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        # but do not mess around with number
        self.number = Goblin.number # access class attribute
        Goblin.number += 1 # prepare class attribute for next goblin
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
            average_value = Config.__getattribute__(Config,attr)
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
        """returns a string with the actual stats"""
        text=""
        for stat in filter(lambda x: "__" not in x, dir(self)):
            if "bound method" in str(self.__getattribute__(stat)):
                continue # ignore methods, only take attributes
            #print(stat)
            attr = self.__getattribute__(stat)
            #testing if attribute is string or int or float
            if isinstance(attr, int) or isinstance(attr, float):
                text+= "\n{:>20}: {:5.1f}".format (stat, attr)
            else:
                text+= "\n{:>20}: {}".format(stat, attr)
        return text


    
def integer_input(min_value,max_value, prompt=">", default=-1):
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
            print("please enter numbers between {} and {} only".format(
                min_value, max_value-1))
    
    
def info():
    """demo method"""
    print("this is some information")


def buy_goblin(team_number):
    """create goblin instance and add it to team"""
    new_name = input("please give the new goblin a nickname:")
    if new_name == "":
        new_name = "unnamed goblin"
    g = Goblin(new_name)
    gnr = g.number
    Config.teams[team_number][gnr] = g          # add new goblin to team
    key = "editgoblins{}".format(team_number)
    # add edit goblin menu entry
    Config.menu[key].append(["edit goblin {} ({})".format(new_name, gnr),
        lambda: edit_goblin(gnr, team_number)])
    print("You purchased {} for the team!".format(new_name))

def show_goblins(team_number):
    """print a list of all goblins in this team"""
    print("{} all goblins of team {} {}".format(16*"-",
        Config.team_names[team_number], 16*"-"))
    
    print("{:>20}:   attack   defense hitpoints     value".format(
        "attribute"))
    print("{:>20}: {:8.2f} {:8.2f} {:8.2f}".format("normal", 
          10,10,20))
    print("{:>20}".format("goblin (unique nr)"))
    for (gnr, goblin) in Config.teams[team_number].items():
        print("{:>15} ({:>2}): {:8.2f} {:8.2f} {:8.2f}   {:8.2f}".format(
            goblin.name, gnr, goblin.attack, goblin.defense,
            goblin.hitpoints, goblin.value))
    print(60*"-")


def rename_team(team_number):
    """rename teamnames in the teamnamces dict and in the menu dict"""
    new_name = input("please enter new name for team number {}: ".format(
        team_number))
    if new_name == "":
        print("nothing renamed")
        return
    Config.team_names[team_number] = new_name
    # change the submenu
    key = "team{0}".format(team_number)
    Config.menu[key][0][0] = "exit menu of team {} (team {})".format(new_name,
        team_number)
    # root menu entry for team 0 is 1, entry for team 1 is 2 ....
    Config.menu["root"][team_number+1][0] = "manage team {} (team {})".format(
        new_name, team_number)

def edit_goblin(number, team_number):
    """let the user change attributes of an individual goblin
    need goblins unique number and team number"""  
    #get goblin
    if not number in Config.teams[team_number]:
        print("no goblin with this number is in your team")
        return
    goblin = Config.teams[team_number][number]
    for stat in ["name", "attack", "defense", "hitpoints"]:
       pass
    old_name = goblin.name
    new_name = input("please enter the new name for goblin {}: ".format(
        goblin.name)) 
    if new_name == "":
        print("nothing changed")
        return
    goblin.name = new_name
    # change menu entry, search for old entry
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
    p = "\n".join(("Each goblins has a unique goblin number. You can",
        "see this number using the 'show all goblins' menu",
        "it is the number in round parentheses",
        "unique number of goblin you want to sell ?"))
    print(p)
    # Goblin.number (class attribute) - 1 is the hightest possible 
    # number of a goblin. It does not mean that this goblin still exist
    delnumber = integer_input(-1, Goblin.number,"(-1 is cancel) >")
    if delnumber == -1:
        print("sell action canceled")
        return
    # check if this goblin exist in the selected team
    if not  delnumber in Config.teams[team_number]:
        print("No goblin with this number exist in your team")
        return
    d = Config.teams[team_number].pop(delnumber) # d is the deleted goblin
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
        choice = integer_input(0,len(menu))
        _, command = menu[choice]       # the _ is a name vor a variable
        # here is the 'submenu'-magic. Just change the dictionary key and go
        # on in the loop, so the chosen submenu will be handled.
        if isinstance(command, str):
            category = command
        else:
            command()

class Config(object):
    """class to hold 'global' variables
    (all done as class instances)"""
    teams = {0: {}, 1:{}} # a dict of dicts
    team_names = {0: "team 0", 1:"team 1"}
    #  average values to create goblins and calculate their money value
    hitpoints = 20
    attack = 10
    defense = 10
    menu = {"root": [
                # to handle a function with parameters, use lambda:
                ["Exit the main menu", lambda: sys.exit(0)],
                # go to another submenu by writing the submenu name
                ["Manage team 0", "team0"],
                ["Manage team 1", "team1"],
                # call a function by writing the funciton name
                ["Show info", info]  ],
            "team0": [
                ["Exit menu of team 0", "root"],
                ["show all goblins", lambda: show_goblins(0)],
                ["buy goblin", lambda: buy_goblin(0)],
                ["rename team", lambda: rename_team(0)], 
                ["edit goblins", "editgoblins0"],
                ["sell goblin (number)", lambda: sell_goblin(0)],
                ["Show info... ", info] ],
            "team1": [
                ["Exit menu of team 1", "root"],
                ["show all goblins", lambda: show_goblins(1)],
                ["buy goblin", lambda: buy_goblin(1)],
                ["rename team", lambda: rename_team(1)], 
                ["edit goblins", "editgoblins1"],
                ["sell goblin (number)", lambda: sell_goblin(1)],
                ["Show info... ", info] ], 
            "editgoblins0": [
                ["Exit the edit goblins menu", "team0"],
                ["edit goblin Stinky (0)", lambda: edit_goblin(0,0)] ],
            "editgoblins1": [
                ["Exit the edit goblins menu", "team1"],
                ["edit goblin Grunty (1)", lambda: edit_goblin(1,1)] ]
            }

def main():
    """the main function of the game"""
    #teams = {0: {}, 1:{}} # a dict of dicts
    #team_names = {0: "team 0", 1:"team 1"}
    gob0 = Goblin("Stinky")
    gob0nr = gob0.number               # first goblin, his number is 0
    gob1 = Goblin("Grunty")
    gob1nr = gob1.number               # second goblin, his number is 1
    # inside each team dict, the goblin number is key, 
    # the goblin instance (the goblin himself) is the value
    Config.teams[0][gob0nr] = gob0 # Stinky joins team0
    Config.teams[1][gob1nr] = gob1 # Grunty joins team1
    
    
    handle_menu(Config.menu)

if __name__ == "__main__":
    main()
    
