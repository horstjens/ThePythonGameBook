"""part of http://ThePythonGameBook.com
source code:

https://github.com/horstjens/ThePythonGameBook/blob/master/
python/goblins/slowgoblins020.py

TODO:    #decrease defense for each counterstrike
         #team battles
         #gold for won battles / damage dealt
         #stats after combat
         #tail-recursion in re-roll (thanks to yipyip)
         #calculate_value (and editstats) improved (thanks to yipyip)
         #generic input function
         #fileoperation IOError


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
        self.victory = 0  # over all rounds
        self.streak = 0  # victories in this combat
        self.lastround = 0  # number of combatround whre goblin lost
        self.lost = 0
        self.fights = 0
        # overwrite attributes if keywords were passed as arguments
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        # but do not mess around with number
        self.number = Goblin.number  # access class attribute
        Goblin.number += 1  # prepare class attribute for next goblin
        # calculate value based on averages described in class Config
        self.value = self.calculate_value()

    def prepare_for_fight(self):
        """reset attributes like hitpoints, loot etc for each battle"""
        self.restore_health()  # restore full hitpoints
        self.fights += 1
        self.damage_received = 0  # clear for this battle
        self.damage_dealt = 0
        self.streak = 0  # enemys knocked out in one battle
        self.lastround = 0  # fighting until this round (if >0)
        self.loot = 0  # gold plundered from fallen enemys

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
        #value = 0.0
        #for attr in ["attack", "defense", "hitpoints"]:
        #    actual_value = self.__getattribute__(attr)
        #    average_value = Config.__getattribute__(Config,attr)
        #    diff = actual_value - average_value
        #    if diff < 0:
        #        sign = -1
        #    else:
        #        sign = 1
        #    value += sign * diff**2  # square the diff but keep the sign
        #return value
        ## code from yipyip
        ## (1,-1)[True] is the same as (1,-1)[1] = -1
        ## (1,-1)[False] is the same as (1,-1)[0] = 1
        diffs = (pts - cfg for pts, cfg in zip((self.attack, self.defense, self.hitpoints), (Config.attack, Config.defense, Config.hitpoints)))
        return sum((1, -1)[diff < 0] * diff**2 for diff in diffs)

    def restore_health(self):
        """restore original hitpoints"""
        self.hitpoints = self.fullhealth

    def report(self):
        """returns a string with all the actual stats"""
        text = ""
        for stat in filter(lambda x: "__" not in x, dir(self)):
            if "bound method" in str(self.__getattribute__(stat)):
                continue  # ignore methods, only take attributes
            # print(stat)
            attr = self.__getattribute__(stat)
            # testing if attribute is string or int or float
            if stat == "sleep":  # sleep is boolean
                text += "\n{:>20}: {}".format(stat, attr)
            elif isinstance(attr, int) or isinstance(attr, float):
                text += "\n{:>20}: {:5.1f}".format(stat, attr)
            else:
                text += "\n{:>20}: {}".format(stat, attr)
        return text

    def __repr__(self):
        """overwriting the representation method of a goblin object"""
        return "{:>15} ({:>2}): {:6.2f} {:6.2f} {:6.2f} {:6.2f} {}".format(
            self.name, self.number, self.attack, self.defense, self.hitpoints,
            self.value, self.sleep
        )


def generic_input(typ="int", prompt=">", default=0, minv=-9999999, maxv=9999999):
    """ask user and returns answer (of typ "int", "float", "text")"""
    while True:
        raw = input(prompt)
        if raw == "":
            return default
        if typ == "text":
            return raw
        try:
            if typ == "int":
                answer = int(raw)
                if minv <= answer <= maxv:
                    return answer
                else:
                    raise IndexError

            elif typ == "float":
                answer = float(raw)
                if minv <= answer <= maxv:
                    return answer
                else:
                    raise IndexError
        except (ValueError, IndexError):
            print("please enter numbers between {} and {}".format(minv, maxv))
            if typ == "float" and not "." in raw:
                print("use decimal point")


def info():
    """demo method"""
    print("this is some information")


def buy_goblin(team_number):
    """create goblin instance and add it to team"""
    # check money
    if Config.gold[team_number] <= 0:
        print("Your team has no gold! Sell some goblins first")
        return
    new_name = generic_input(typ="text", prompt="nickname for new goblin?", default="unnamed goblin")
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
    print("{:>20}:   att   def     hp   value  sleep".format("attribute"))
    print("{:>20}: {:6.2f} {:6.2f} {:6.2f}".format("normal", Config.attack, Config.defense, Config.hitpoints))
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
    print("{:>20}: {:6.2f} {:6.2f} {:6.2f} {:6.2f} {:>2}".format("sum", sumatt, sumdef, sumhp, sumval, sumsleep))
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
            new_value = generic_input("float", "new value ?", old_value, old_value)
        elif isinstance(attr, int):
            new_value = generic_input("int", "new value ?", old_value, old_value)
        elif isinstance(attr, str):
            new_value = generic_input("text", "new value ?", old_value)
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

            # display gold cost before attribute change and let user confirm
            # new value is always bigger than old value
            norm = Config.__getattribute__(Config, stat)
            # signed(delta_new_norm_)squared - signed(delta_old_norm)squared
            diffnew = new_value - norm  # delta new norm
            diffold = old_value - norm  # delta old norm
            pricenew = (1, -1)[diffnew < 0] * diffnew**2
            priceold = (1, -1)[diffold < 0] * diffold**2
            #if dnn >= 0:
            #    sdnns = dnn**2     # signed delta new norm squared
            #else:
            #    sdnns = -1 * dnn**2
            #if don >= 0:
            #    sdons = don**2    # signed delta old norm squared
            #else:
            #    sdons = -1 * don**2
            #price = sdnns - sdons
            price = pricenew - priceold
            print("This change would cost: {} gold".format(price))
            print("Your team has {} gold".format(Config.gold[team_number]))
            if price > Config.gold[team_number]:
                print("nothing changed, due to lack of gold")
                continue
            if generic_input("int", "accept? 0=cancel, 1=yes", 0, 0, 1) == 1:
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
    delnumber = generic_input("int", "(-1 is cancel) >", -1, -1, Goblin.number)
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
    sleepnumber = generic_input("int", "(-1 is cancel) >", -1, -1, Goblin.number)
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
        choice = generic_input("int", prompt="Your menu choice?", default=0, minv=0, maxv=len(menu) - 1)
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

    for stat in [
        "attack", "defense", "hitpoints", "value", "sleep", "victory", "lost",
        "fights", "damage_received", "damage_dealt"
    ]:
        statsum = {a: 0, b: 0}
        for x in [a, b]:
            for (gbnr, goblin) in Config.teams[x].items():
                statsum[x] += goblin.__getattribute__(stat)
        print("{:>20}: {:6.1f}   {} {:6.1f}".format(stat, statsum[a], sign(statsum[a], statsum[b], statsum[b])))


def clear_logfile(filename="combatlog.txt"):
    """overwrites the old combatlogfile with empty text"""
    try:
        with open('combatlog.txt', 'w') as logfile:
            logfile.write("---")
        print("combatlogfile cleared")
    except IOError:
        print("problems writing combatlog.txt")


def reroll(min_eyes, max_eyes, accu=0, depth=99):
    """a die that is allowed to re-roll when the max_eyes is thrown.
       return the sum of all throws minus 1 per max_eyes thrown.
       This allows very high results with a very small propability
       example:  6(=max eyes) + (reroll) 6 + 2 = (6-1)+(6-1)+2 =12
       see https://gist.github.com/yipyip/6205271 and
       tail-recursion for more information"""

    assert depth >= 0  # make sure that depth is not negative

    result = random.randint(min_eyes, max_eyes)
    if result < max_eyes or depth == 0:
        return accu + result
    return reroll(min_eyes, max_eyes, accu + result - 1, depth - 1)


def strike(attacker, defender, combatround, counterstrike=False):
    """attacker strikes at defender. The function changes the new
    hitpoints of the defender and returns a text String with the
    combat report.
    counterstrike (boolean) indicates that this is a counterattack
    or not.
    Each counterstrike (=being attacked) increases the defense penalty
    by one.
    """
    striketext = []  # a list of textlines !
    if counterstrike:
        t = "counterattack"
    else:
        t = "attack"

    rollAtt = reroll(1, 6)  # allowed to re-roll if a 6 is thrown
    rollDef = reroll(1, 6)
    scoreA = attacker.attack + rollAtt
    scoreD = defender.defense + rollDef - defender.defense_penalty
    striketext.append("{} rolls {}, {} rolls {}".format(attacker.name, rollAtt, defender.name, rollDef))
    if scoreA > scoreD:
        striketext.append("Sucessfull {0} !  ({1:.2f} > {2:.2f})".format(t, scoreA, scoreD))
        damage = scoreA - scoreD
        defender.hitpoints -= damage
        #statistics
        attacker.damage_dealt += damage
        defender.damage_received += damage
        striketext.append("...doing {0:.2f} damage.".format(damage))
        if defender.hitpoints <= 0:
            attacker.victory += 1
            attacker.streak += 1
            defender.lost += 1
            defender.lastround = combatround
            striketext.append("Victory for {}! {} goes down".format(attacker.name, defender.name))
            striketext.append(
                "This is victory {} for {}".format(attacker.victory, attacker.name) +
                " ( {} had {} ".format(defender.name, defender.victory) + " before he got down)"
            )
            striketext.append("{} wins {:.2f} gold for his team".format(attacker.name, defender.fullhealth * Config.loot))
            attacker.loot = defender.fullhealth * Config.loot
    else:
        striketext.append("The {0} failed... ({1:.2f} <= {2:.2f})".format(t, scoreA, scoreD))
    if counterstrike:
        attacker.defense_penalty += 1  # each counterstrike lowers defense
    return striketext


def combatround(a, b, number):
    """a round of combat between team a and team b.
    Each non-sleeping, alive (hp>0) goblin can make one stike against
    another goblin of the enemy team.
    Each attacked goblin (if he survive the attack) makes an counterstrike
    against his attacker, and get his defensepenalty increased by 1
    The effect is that many attack against a single victim are more
    likely to suceed, but remain dangerous for the attacker"""
    # reset all defense_penaltys to 0
    text = []  # a list of lines !
    for team in [a, b]:
        for goblin in Config.teams[team].values():
            goblin.defense_penalty = 0
    # randomize goblin.number to process combat order
    # TODO: give each goblin speed and initiative attributes
    order = list(range(Goblin.number))  # list of all goblin numbers
    random.shuffle(order)  # random ordering of those numbers
    for gnr in order:
        if gnr in Config.teams[a]:
            myteam = a
            enemyteam = b
        elif gnr in Config.teams[b]:
            myteam = b
            enemyteam = a
        else:
            continue  # non-existing goblin ( sold? )
        attacker = Config.teams[myteam][gnr]
        if attacker.sleep or attacker.hitpoints <= 0:
            continue
        # search random victim
        victimlist = [
            x
            for x in Config.teams[enemyteam].values()
            if ((x.sleep == False) and (x.hitpoints > 0))
        ]
        if len(victimlist) == 0:
            continue
        defender = random.choice(victimlist)
        text.append("--")
        text.append(
            "{} (nr {}) of team {} strikes".format(attacker.name, attacker.number, Config.team_names[a]) +
            " {} (nr {})  of team {}".format(defender.name, defender.number, Config.team_names[b])
        )
        text.append("{:<20}:  att    def      hp".format("  Strike!") + "    $  sleep def-penalty")
        text.append(str(attacker) + " {}".format(attacker.defense_penalty))
        text.append(str(defender) + " {}".format(defender.defense_penalty))
        text.extend(strike(attacker, defender, number, False))
        if defender.hitpoints > 0:
            text.append("  Counterstrike of {}!".format(defender.name))
            text.extend(strike(defender, attacker, number, True))
    return text


def fight(a=0, b=1):
    """let fight all non-sleeping, alive goblins in 2 teams versus
       each other until one team has no goblins left"""
    text = ["The big battle between team {} and team {} starts:".format(Config.team_names[a], Config.team_names[b])]
    for team in [a, b]:
        for goblin in Config.teams[team].values():
            if not goblin.sleep:
                goblin.prepare_for_fight()  # restore hitpoints to full etc
    battleround = 0
    while True:
        battleround += 1
        ateam = [x for x in Config.teams[a].values() if ((x.sleep == False) and (x.hitpoints > 0))]
        bteam = [x for x in Config.teams[b].values() if ((x.sleep == False) and (x.hitpoints > 0))]
        if len(ateam) > 0 and len(bteam) > 0:
            text.append("=======================")
            text.append("---Battle round {:>4} ---".format(battleround))
            text.append("alive: {} vs. {}".format(len(ateam), len(bteam)))
            text.append("--------------------------")
            text.extend(combatround(a, b, battleround))
        elif len(ateam) > 0:
            text.append("========================")
            text.append("team {} is victorious".format(Config.team_names[a]))
            text.append("========================")
            break
        elif len(bteam) > 0:
            text.append("========================")
            text.append("team {} is victorious".format(Config.team_names[b]))
            text.append("========================")
            break
        else:
            text.append("no victorous team ?")
            break
    # ---- battle over, print textlines
    text.append("=====--------- battle statistics -----------=====")
    lootsum = [0.0, 0.0]
    for t in [a, b]:
        text.append("------ team {} ----".format(Config.team_names[t]))
        tl = [x for x in Config.teams[t].values() if not x.sleep]
        text.append("{:>20}{:>7}{:>7}{:>7}{:>7}{:>7}".format("Name:", "dmg d", "dmg r", "lst r", "streak", "loot"))
        for goblin in tl:
            #text.append(str(goblin))
            text.append("{:>20}{:7.2f}{:7.2f}{:7.2f}{:7.2f}{:7.2f}".format(
                goblin.name, goblin.damage_dealt, goblin.damage_received,
                goblin.lastround, goblin.streak, goblin.loot
                )
            )
            lootsum[t] += goblin.loot
        text.append("===================================")
        text.append("team {} made a sum of {:.2f} gold in this battle".format(Config.team_names[t], lootsum[t]))
        Config.gold[t] += lootsum[t]

    for line in text:
        print(line)
    try:
        with open('combatlog.txt', 'a') as logfile:
            for line in text:
                logfile.write(line + "\n")
        print("combat log appended into file 'combatlog.txt'")
    except IOError:
        print("problem writing into file combatlog.txt")


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
    answer = input("please enter the attribute for sorting:>")
    if not answer in valid:
        print("sorry this was not a valid answer. nothing changed")
        return
    old = Config.sortorder[rank]
    Config.sortorder[rank] = answer
    print( "changed sortorder for rank {} from {} to {}".format(


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
    loot = 1  # 1 gold per hitpoint of  knocked out enemy

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
            ["Fight team vs team", fight],
            ["Clear combatlog.txt", clear_logfile],
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
