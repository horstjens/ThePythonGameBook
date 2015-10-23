#This game is part of The Python-Game-Book
# TODO: equipped weapon for monster does not affect combat stat ?
# TODO: seperate IO from other code
# TODO: detect empty list_items for use, drop, equip etc
# TODO: give monster armor and weapons
# TODO: encumberance or cancel fight after 100 rounds
# TODO: cancel for every menu
# TODO: create random armors and weapons
# TODO: monsters corpses spawn loot
# TODO: history of slain enemys ( room 0?)
# TODO: game won condition
# TODO: monsters can pick up/drop weapons
# TODO: armor and weapons can shatter

import random
import sys
#import logging

if sys.version_info[0] < 3:
    print("this script need python3. You are using python 2 or lower.")
    sys.exit()

#logging.basicConfig(filename='horst.log',level=logging.DEBUG)


class Game(object):
    """
    holds all information for a game. Later it may be
    possible to load / save different games
    """
    number = 0

    def __init__(self):
        self.number = Game.number
        Game.number += 1
        self.rooms = {}  # dictionary of rooms, key is room number
        self.items = {}  # dictionary of items, key is item number
        self.monsters = {}  # dictionary of monsters, key is monster number
        self.players = []  # dictionary of players, key is player number, value = monsternumber
        self.effects = {}  # dictionary of effects (for items), key is effect name


class Monster(object):
    number = 1  # number 1 should be reserved for player

    def __init__(
        self,
        game,
        where=0,
        adjective="",
        description="",
        boss=False,
        carrier=False
    ):
        self.number = Monster.number
        Monster.number += 1
        game.monsters[self.number] = self  # add monster into game dict
        self.adjective = adjective
        self.location = where  # room number
        self.description = description
        self.hitpoints = random.randint(5, 15)
        self.player = False
        self.carrier = carrier  # can carry items ?
        self.attack = 10 + random.randint(-2, 2)
        self.defense = 10 + random.randint(-2, 2)
        self.speed = 10 + random.randint(-2, 2)
        self.damage = 3 + random.randint(-2, 2)
        self.armor = 3 + random.randint(-2, 2)
        self.agressive = False
        self.slots = {
            "head": 1,
            "body": 1,
            "hand": 2,
            "finger": 2,
            "neck": 1,
            "feet": 2
        }  # only one magic ring per ring-finger
        if description == "":
            if boss:
                self.adjective = random.choice(
                    (
                        "deadly", "fantastic", "creepy", "ugly", "epic"
                    )
                )
                self.description = random.choice(
                    (
                        "dragon", "cave drake", "sea serpent", "gorgon",
                        "giant beetle", "arch druid"
                    )
                )
                self.hitpoints *= 5
                self.attack += random.randint(2, 7)
                self.defense += random.randint(2, 7)
                self.speed += random.randint(2, 7)
            else:
                self.adjective = random.choice(
                    (
                        "weak", "boring", "tired", "cheap", "old"
                    )
                )
                self.description = random.choice(
                    (
                        "goblin", "ork", "troll", "mice", "rat", "dwarf",
                        "spider"
                    )
                )

    def info(self):
        txt = "Monster number {}: {} {} with {} hitpoints\n".format(
            self.number, self.adjective, self.description, self.hitpoints
        )
        if self.carrier:
            txt += "This monster can carry items\n"
        return txt

    def inspect(self, game):
        return "{}\n{:2}\n{:2}\n{:2}\n{:2}\n{:2}".format(
            self.description, self.hitpoints, self.attack, self.defense,
            self.speed, self.damage, self.armor
        )

    def list_items(
        self,
        game,
        active_only=False,
        wearable_only=False,
        passive_only=False,
        magic_only=False
    ):
        return []  #TODO: give monsters armor and weapons

    def leftcol(self):
        #return "name      \nhitpoints \nattack    \ndefense   \nspeed     \ndamage    \narmor     \n"
        return "\n\n\n\n\n\n\n"

    def calculate_values(self, game):
        """calculate all bonus and malus from equipped weapons and armors toward combat stats.
        returns dict with combat values"""
        values = {
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "damage": self.damage,
            "armor": self.armor
        }
        items = self.list_items(game, True, True, False, False)
        for i in items:
            values["attack"] += game.items[i].attackbonus
            values["defense"] += game.items[i].defensebonus
            values["speed"] += game.items[i].speedbonus
            values["damage"] += game.items[i].damagebonus
            values["armor"] += game.items[i].armorbonus
        return values


class Player(Monster):
    #playernumber = 1
    def __init__(self, game, where=0, name="hero"):
        """need game instance.
        """
        Monster.__init__(self, game, where, carrier=True)
        game.players.append(self.number)  # add my monsternumber to game.players
        self.playerindex = len(game.players) - 1
        self.name = name
        self.player = True
        self.description = "player"  # overwrite monster
        self.adjective = "human"  # overwrite monster
        #self.inventory = [] # list of itemnumbers (player carry items)
        self.maxcarry = 35  # kg
        self.carry = 0  # current mass of all carried items in kg
        self.damage += random.randint(1, 5)
        self.armor += random.randint(1, 5)
        self.speed += random.randint(1, 5)
        self.weapon = None
        #self.armor = None
        #self.loaction = where # start room number

    def show_inventory(self, game, itemnumberlist):

        txt = ""
        txt += "\n==== Your inventory ====\n"
        for itemnumber in itemnumberlist:
            i = game.items[itemnumber]

            if not game.items[itemnumber].active:
                e = "rucksack"
            else:
                e = "(equipped)"
            txt += "{}...{}...{} kg {}\n".format(
                itemnumber, game.items[itemnumber].description,
                game.items[itemnumber].mass, e
            )

        txt += "You're currently carrying {:.2f} kg, that is {:.2f}% of your capacity".format(
            self.carry, (self.carry / self.maxcarry) * 100
        )
        return txt

    def list_items(
        self, game, active_only, wearable_only, passive_only, magic_only
    ):
        """returns list of itemnumber
        of the items in the inventory of the player"""
        txt = ""
        items = []
        for itemnumber in game.items:
            i = game.items[itemnumber]
            if i.location == -self.number:
                if active_only and not i.active:
                    continue
                if passive_only and i.active:
                    continue
                if magic_only and not i.is_magic:
                    continue
                if wearable_only and not i.is_weapon and not i.is_armor:
                    continue
                items.append(itemnumber)
                #txt += game.items[itemnumber].description
        return items

    def pickup_item(self, game):
        txt, items = game.rooms[self.location].list_items(game)
        if len(items) > 0:
            output("please select item number to pick up\n")
            output(txt)
            i = select_number(items)
            m = game.items[i].mass
            if m > self.maxcarry:
                return "You fail to pick up this item. Reason: You can only carry {} kg. \n and try to pick up {} kg. Become stronger and try again!".format(
                    self.maxcarry, m
                )
            elif m + self.carry > self.maxcarry:
                return "You fail to pick up this item. Reason: You already carry {} kg. Picking up {} would exceed your max. carry capacity of {} kg. Drop some items first or become stronger!".format(
                    self.carry, m, self.maxcarry
                )
            else:
                game.items[i].location = -self.number  # negative monster number
                self.carry += m
                return "You now carry items for a total weight of {} kg".format(
                    self.carry
                )

        else:
            return "this room has no items so there is nothing to pick up\n"

    def drop_item(self, game):
        items = self.list_items(game, False, False, False, False)  # do not drop equipped items
        if len(items) > 0:
            output(self.show_inventory(game, self.list_items(game, False, False, False, False)))
            output("select itemnumber to drop\n")
            i = select_number(items)
            if game.items[i].never_drop:
                return "you can not drop this item, sorry! Try another item"
            game.items[i].location = self.location  # drop item in my room
            self.carry -= game.items[i].mass  # update player
            return "you drop the {} to the floor\n".format(game.items[i].description)
        else:
            return "you carry no items so you can drop nothing\n"

    def use_item(self, game):
        """launch effect of magic item (must be in inventory)"""
        items = self.list_items(game, False, False, False, True)
        if len(items) > 0:
            output(self.show_inventory(game, self.list_items(game, False, False, False, True)))
            output("select itemnumber to use/equip\n")
            i = select_number(items)
            if game.items[i].effect == None:
                return "this item has no effect/is not equippable"
            txt = ""
            game.items[i].charges -= 1
            if game.items[i].charges == 0:
                # destroy item (move to room 0)
                game.items[i].location = 0
                txt += "while using the effect, the item has destroyed itself\n"
            txt += game.effects[game.items[i].effect].action(game, victim=self.number)
            return txt
        else:
            return "you carry no magic items so you can use nothing"

    def inspect(self, game):
        """all you ever wanted to know about yourself, but was too afraid to ask"""
        txt = ""
        weapontext = ""
        armortext = ""
        items = self.list_items(game, True, False, False, False)
        for i in items:
            if game.items[i].is_weapon:
                weapontext += game.items[i].description + " and "
            elif game.items[i].is_armor:
                armortext += game.items[i].description + ", "
        if weapontext == "":
            weapontext = "no weapon"
        else:
            weapontext = weapontext[:-5]  # remove last 5 chars
        if armortext == "":
            armortext = "no armor"
        else:
            armortext = armortext[:-2]  # remove last 2 chars
        txt += "you are a {} with {} hitpoints wielding ".format(self.description, self.hitpoints)
        txt += "{} and wearing: {}\n".format(weapontext, armortext)
        attr = self.calculate_values(game).keys()
        #left = self.leftcol().splitlines()
        #right = self.inspect().splitlines()
        v = self.calculate_values(game)
        total = v.values()
        base = []
        for k in attr:
            base.append(self.__getattribute__(k))
        both = zip(attr, base, total)
        txt += "  attribute base  eqip   tmp.effect    total\n"
        for pair in both:
            txt += "{:>10}: {:>2}   {:>2}                    {:>2}\n".format(pair[0], pair[1], pair[2] - pair[1], pair[2])
        return txt

    def equip(self, game):
        """ask user of itemnumber to wear/wield/remove"""
        items = self.list_items(game, False, True, False, False)
        txt = "Please select number of item to wield/wear/equip.\n If item is already equipped, it will be put back in the inventory\n"
        for itemnumber in items:
            i = game.items[itemnumber]
            if i.active:
                d = "currently equipped"
            else:
                d = "in inventory"
            txt += "{}.....{}....({})\n".format(i.number, i.description, d)
        output(txt)
        select = select_number(items)
        i = game.items[select]
        i.active = not i.active  # toggle active status
        if i.active:
            output("You wield/wear {}".format(i.description))
        else:
            output("You moved {} into your inventory".format(i.description))

    def nextAction(self, game):
        """ask the user to select only one of many options"""
        output("please select your next action:")
        cd = game.rooms[self.location].connectiondict(game)  #cd = connectiondict
        txt = ""
        for roomnumber in cd:
            txt += "{:2}........goto {}\n".format(roomnumber, cd[roomnumber])
        txt += "i,s,m,r...inspect (i)nventory/(s)elf/(m)onsters/(r)oom\nd,p.......(d)rop/(p)ick up item\n"
        txt += "e.........(e)quip/remove armor or weapon\n"
        txt += "u.........(u)se magic item\n"
        txt += "f.........(f)ight monsters\n"
        txt += "please type number/char and press ENTER or q and ENTER to (q)uit\n"
        # generate valid answerlist:
        chars = ("i", "d", "p", "u", "f", "s", "q", "m", "r", "e")
        answers = []
        for roomnumber in cd:
            answers.append(str(roomnumber))
        answers.extend(chars)
        output(txt)
        answer = select_answer(answers)
        if not answer in chars:
            # room change
            # automatic damage if there is still a monster
            txt = ""
            for monster in game.rooms[self.location].local_monsters(game, self.number):
                txt += "While you {} like a coward, {} attacks you from behind for double damage !\n".format(
                    "flee" if self.hitpoints > 0 else "die", monster.description
                )
                damage = monster.damage * 2
                txt += "You loose {} hitpoints! ({} hitpoints left) \n".format(damage, self.hitpoints - damage)
                self.hitpoints -= damage
                if self.hitpoints < 1:
                    txt += "You are dead!! \n"
            if txt != "":
                output(txt)
            self.location = int(answer)
        elif answer == "q":
            #sys.exit()
            self.location = 0  # teleport player out of game
        elif answer == "i":
            output(self.show_inventory(game, self.list_items(game, False, False, False, False)))
        elif answer == "e":
            self.equip(game)  # output inside equip function
        elif answer == "r":
            output(game.rooms[self.location].info(game, short=False))
        elif answer == "d":
            output(self.drop_item(game))
        elif answer == "p":
            output(self.pickup_item(game))
        elif answer == "u":
            output(self.use_item(game))
        elif answer == "s":
            output(self.inspect(game))
        elif answer == "m":
            for monster in game.monsters.values():  # iterate directly over all monsters
                if monster.location == self.location and monster.number != self.number:
                    left = self.leftcol().splitlines()
                    middle = self.inspect(game).splitlines()
                    right = monster.inspect(game).splitlines()
                    total = zip(left, middle, right)
                    for t in total:
                        output(t[0] + ": " + t[1] + "  vs.  " + t[2])
        elif answer == "f":
            output("you fight one of the monsters in this room !")
            #for monsternumber in [monsternumber for monsternumber in game.monsters if game.monsters[monsternumber].location == self.location]:
            txt = ""
            for monster in game.monsters.values():
                if monster.location == self.location:
                    if self.hitpoints > 0 and monster.number != self.number:
                        txt += "---- combat versus {} ----\n".format(monster.description)
                        txt += combat(game, self, monster)
                        if self.hitpoints > 0:
                            txt += "====== Victory !!! ========"
                            monster.location = 0  # move deat monster in the void
                            # todo: loot
                            # create item: corpse
                            Item(
                                g, self.location, "corpse of killed monster", 70
                            )
                            break
                        else:
                            txt += "----==== you loose ====----"
                            break
            else:
                txt += "there are no (more) monsters to fight in this room"
            output(txt)


class Item(object):
    number = 1

    def __init__(self, game, where=0, description="", mass=-1, effect=None, charges=1):
        """need game instance. primary key of all items is the unique
        item number, so that you can have several items with the same
        name"""
        self.number = Item.number
        Item.number += 1
        game.items[self.number] = self  # add item into game dict
        self.effect = effect
        if self.effect:
            self.is_magic = True
        else:
            self.is_magic = False
        self.charges = charges  # how many times you can use this effect before item is destroyed
        self.location = where  # positive values are room number,
        # negative values refer to monster(!) number possesing this item
        self.description = description
        self.active = False  # is item currently worn or equipped by someone ?
        self.is_weapon = False
        self.is_armor = False
        self.never_drop = False  # forbid to drop this item
        if mass == -1:
            self.mass = round(random.randint(1, 30))
        else:
            self.mass = mass
        if self.description == "":
            self.description = random.choice(
                (
                    "small healing potion", "medium healing potion", "gold",
                    "paper", "towel", "restaurant bill", "teleport pill",
                    "piece of junk"
                )
            )
            if self.description == "medium healing potion":
                self.effect = "heal5"
                self.is_magic = True
            elif self.description == "medium healing potion":
                self.effect = "heal10"
                self.is_magic = True
            elif self.description == "teleport pill":
                self.effect = "randomteleport"
                self.is_magic = True

    def info(self, game):
        txt = "Item Number {}: ".format(self.number)
        txt += self.description + "\n"
        #if self.location >= 0:
        #   #txt +="\n current location: room {}, {}".format(self.location, game.rooms[self.location].description)
        #else:
        #    txt += "\n currently carried by {}".format(game.monsters[self.location*-1].description)
        #return txt


class Weapon(Item):
    def __init__(
            self, game, where=0, description="", mass=-1, effect=None, charges=1, oneHand=True, twoHand=False,
            length=0.1, attackbonus=0, defensebonus=0, damagebonus=0, speedbonus=0, armorbonus=0, quality=.5
    ):
        Item.__init__(self, game, where, description, mass, effect, charges)
        self.is_weapon = True  # overwrite value False from Item.__init__
        self.one_hand = oneHand
        self.two_hand = twoHand
        self.length = length  # lenght of melee weapon in meter
        self.attackbonus = attackbonus
        self.defensebonus = defensebonus
        self.damagebonus = damagebonus
        self.speedbonus = speedbonus
        self.armorbonus = armorbonus
        self.quality = quality

    def unequip(self, game, who):
        """un-wield a weapon and put it back in the inventory"""
        pass

    def equip(self, game, who):
        """wield a weapon. un-wield previous selected weapon"""
        pass


class Armor(Item):
    def __init__(
        self, game, where=0, description="", mass=-1, effect=None, charges=1, encumberance=0, attackbonus=0,
        defensebonus=0, damagebonus=0, speedbonus=0, armorbonus=0, slot="body", quality=0.5
    ):
        Item.__init__(self, game, where, description, mass, effect, charges)
        self.slot = slot
        self.is_armor = True
        self.encumberance = encumberance
        self.attackbonus = attackbonus
        self.defensebonus = defensebonus
        self.damagebonus = damagebonus
        self.speedbonus = speedbonus
        self.armorbonus = armorbonus
        self.quality = quality

    def unequip(self, game, who):
        """remove armor and put it back in inventory"""
        pass

    def equip(self, game, who):
        """wear armor. remove any previous armor in this armor slot and
        put it back in inventory"""
        pass


class Effect(object):
    """generic instant " magic" effect for items like key (connection between rooms,
       teleport effect, gain healt effect etc."""

    def __init__(self, game, name, function, description="", arg1=0, arg2=0, success=.5):
        #victim 0 means the effect is targeted at the player (monsternumber 0)
        self.name = name
        self.function = function
        self.description = description
        self.success = success  # probability .5 means it has a chance of 50% to work correct
        #self.victim = victim # if the effect is aimed at somebody
        # -1 means the effect is targeted at the first player
        #self.roomnumber=roomnunmber # if the effect is in a certain room only
        self.arg1 = arg1  # reserve
        self.arg2 = arg2  # reserve
        self
        game.effects[self.name] = self

    def action(self, game, victim=-1):
        """gives effect to monster with monsternumber == victim"""
        # successchance
        luck = random.random()  # TODO: add players evocation ability here
        if luck > self.success:
            return "Item FAIL ! bad luck, the item/effect refuses to work. try again ?"
        if self.function == "teleport":
            if self.arg1 != 0:
                # teleport into specific room number
                target = self.arg1
            else:
                # random teleport
                while True:
                    target = random.choice(list(game.rooms.keys()))
                    if target != 0:  # anywhere but the void room
                        break
            game.monsters[victim].location = target
            return "the teleport effect works ! Victim is transported by magic into room number {}".format(
                target
            )
        elif self.function == "heal":
            game.monsters[victim].hitpoints += self.arg1
            return "healing effect works! gained {} hitpoints".format(self.arg1)
        elif self.function == "key":
            # right key, wrong room ?
            if game.monsters[victim].location != self.arg1:
                return "you can not find a lock to use with this key here. maybe in another room ?"
            game.rooms[self.arg1].connections.append(self.arg2)
            return "you open a formerly closed door!"
        elif self.function == "carry":
            game.monsters[victim].maxcarry += self.arg1
            return "you can now carry {} kg. more!".format(self.arg1)
        else:
            return "unknow effect worked correctly"


class Room(object):
    number = 0

    def __init__(
        self, game, name="", description="", connections=[], explored=False,
        itemchances=[0.5, 0.25, 0.1], monsterchances=[0.3, 0.2, 0.1, 0.05], bosschances=[0.0], hint=""
    ):
        """need game instance"""
        self.number = Room.number  # void room has number 0
        game.rooms[self.number] = self  # add room into game dict
        Room.number += 1
        self.explored = explored  # True or False
        self.name = name
        self.hint = hint  # description of room if still unexplored
        self.description = description
        self.connections = connections
        self.itemchances = itemchances
        self.monsterchances = monsterchances
        self.bosschances = bosschances

        # create items
        for chance in self.itemchances:
            if random.random() < chance:
                newItem = Item(game, self.number)  # create item in this room

        # create monsters
        for chance in self.monsterchances:
            if random.random() < chance:
                newMonster = Monster(game, self.number)  # create monster in this room
        # create boss(es)
        for chance in self.bosschances:
            if random.random() < chance:
                newMonster = Monster(game, self.number, boss=True)

    def inspect_monsters(self, game, playermonsternumber):
        monstercounter = 0
        txt = ""
        player = game.monsters[playermonsternumber]
        for monster in game.monsters.values():  # iterate directly over all monsters
            if monster.location == self.number and monster.number != playermonsternumber:  # each monster in this room but not the player himself
                monstercounter += 1
                left = player.leftcol().splitlines()
                middle = player.inspect(game).splitlines()
                right = monster.inspect(game).splitlines()
                total = zip(left, middle, right)
                for t in total:
                    txt += t[0] + ": " + t[1] + "  vs.  " + t[2] + "\n"
        if monstercounter == 0:
            return "There are no monsters in this room"
        else:
            return txt

    def local_monsters(self, game, playermonsternumber):
        monsters = []
        for monster in game.monsters.values():  # iterate directly over all monsters
            if monster.location == self.number and monster.number != playermonsternumber:
                monsters.append(monster)
        return monsters

    def list_items(self, game):
        """return string with itemnumbers and item description
        as well as list of itemnumbers"""
        txt = "items in this room:\n"
        items = []
        for itemnumber in game.items:
            if game.items[itemnumber].location == self.number:
                txt += "{}....{}\n".format(itemnumber, game.items[itemnumber].description)
                items.append(itemnumber)
        return txt, items

    def connectiondict(self, game):
        """returns a dict with connections from this room.
        key is room number, value is room description (or "unknown",
        depending if the room is yet bo be explored"""
        namesdict = {}  # temp list of room names
        for c in self.connections:
            if game.rooms[c].explored:
                namesdict[c] = game.rooms[c].name
            else:
                namesdict[c] = "unknown room " + game.rooms[c].hint
        return namesdict

    def info(self, game, short=True):
        """return string with all information about this room"""
        txt = "Room number {}: {}\n".format(self.number, self.name)
        txt += self.description + "\n"
        # items ?
        txt2 = ""
        itemcounter = 0
        for itemnumber in game.items:
            if game.items[itemnumber].location == self.number:
                itemcounter += 1
                if itemcounter > 1:
                    txt2 += ", "
                txt2 += game.items[itemnumber].description
        if itemcounter > 0:
            txt += "You see {} item(s) here: \n".format(itemcounter) + txt2
        else:
            txt += "This room has no items."
        # doors
        txt += "\nYou see {} door(s) and ".format(len(self.connections))
        # monsters ?
        monstercounter = 0
        txt2 = ""
        for monsternumber in game.monsters:
            if game.monsters[monsternumber].location == self.number:
                if not game.monsters[monsternumber].player:
                    monstercounter += 1
                    txt2 += game.monsters[monsternumber].info()
        if monstercounter > 0:
            txt += "{} monster(s) here:\n".format(monstercounter)
            txt += txt2
        else:
            txt += "no monsters in this room, fortunately.\n"
        if short:
            return "You are in Room {}: {}. You see {} doors, {} items and {} monsters".format(
                self.number, self.name, len(self.connections), itemcounter,
                monstercounter
            )
        return txt

#--------- battle math -----------


def swing(game, attacker, defender):
    """single combat action and damage calculation"""
    av = attacker.calculate_values(game)  # av...AtackerValues
    dv = defender.calculate_values(game)  # dv...DefenderValues
    attack_dice = opendice()  # default=2
    defend_dice = opendice()
    damage_dice = opendice(1)  # only one dice
    armor_dice = opendice(1)  # only one dice
    attack_value = av["attack"] + attack_dice
    defend_value = dv["defense"] + defend_dice
    damage_value = av["damage"] + damage_dice
    armor_value = dv["armor"] + armor_dice
    #armor_value = armor_dice
    damage = damage_value - armor_value
    txt = ""
    # hit at all ?
    if attack_value > defend_value:
        txt += "{} hit {} ({}+{}>{}+{})".format(
            attacker.description, defender.description, av["attack"], attack_dice, dv["defense"], defend_dice
        )
        # armor penetration ?
        if damage_value > armor_value:
            txt += " for {} damage ({}+{}-{}-{})\n".format(
                damage, av["damage"], damage_dice, dv["armor"], armor_dice
            )
            defender.hitpoints -= damage
        else:
            txt += " but makes no damage ({}+{}<{}+{})\n".format(
                av["damage"], damage_dice, dv["armor"], armor_dice
            )
    else:
        txt += "{} misses ({}+{}<{}+{})\n".format(
            attacker.description, av["attack"], attack_dice, dv["defense"], defend_dice
        )
    return txt


def combat(game, a, b):
    """combat between two monsters,
    one of them is usually the player"""
    # first strike ?
    txt = ""
    combatround = 1
    while a.hitpoints > 0 and b.hitpoints > 0:
        txt += "--- round {} ---:\n".format(combatround)
        combatround += 1
        speed_a = a.calculate_values(game)["speed"] + opendice()
        speed_b = b.calculate_values(game)["speed"] + opendice()
        if speed_a > speed_b:
            txt += "first strike! " + swing(game, a, b)
            if b.hitpoints > 0:
                txt += "risposte: " + swing(game, b, a)
        else:
            txt += "first strike! " + swing(game, b, a)
            if a.hitpoints > 0:
                txt += "risposte: " + swing(game, a, b)
    return txt


    #------------- generic functions ------
    # this function use print, replace later with gui commands
def output(txt):
    """can be later replaced by gui or graphical output"""
    print(txt)


def select_number(list_of_numbers):
    """The player select *one* number of a list of numbers"""
    answer = ""
    while ((not answer.isdecimal()) or int(answer) not in list_of_numbers):
        answer = input("Please type selected number and press ENTER: ")
    return int(answer)


def select_answer(list_of_answers):
    """The player select *one* char out of a list"""
    answer = ""
    while not answer in list_of_answers:
        answer = input(">>>")
    return answer


def opendice(number_of_dices=2, number_of_sides=6):
    """a dice that re-rolls if the highest number is rolled."""
    if number_of_dices < 1 or number_of_sides < 2:
        return 1  # stupid arguments
    sum = 0
    for dice in range(number_of_dices):
        while True:
            roll = random.randint(1, number_of_sides)
            if roll == number_of_sides:
                sum += (number_of_sides - 1)
            else:
                sum += roll
                break
    return sum

    # create a game instance


g = Game()

# ---------- rooms ---------
# add rooms with  description and connections.
# Each room will have a unique number and add himself to game
# syntax: Room(game, roomname, description, connections...)
# room 0 ....... is the "exit from the game" room
Room(g, "end of the world (game over)", [], explored=True)
# room number 1 .... starting lobby
descr = """The room where your adventure starts. If you
go to the room number 0, the game is over"""

Room(g, "starting lobby", descr, [0, 2], explored=True)
# this is a one-way connection from room1 to room0 !
# room number 2 .... first room
Room(g, "first room", "a boring room with many doors", [1, 3, 4, 5])
# room number 3 ..... storage room
Room(g, "storage room", "you see shelfs, empty boxes and a lot of dust and debris", [2, 4], itemchances=[0.6, 0.4, 0.33])
# room number 4 ..... gear room
Room(g, "gear room", "a room full of stuff", [2, 3], itemchances=[1.0, 1.0, 0.7, 0.7])
# room number 5
Room(g, "npc room", "a ladder leads from here to the roof (7)", [2, 7, 8], monsterchances=[1.0])
# room number 6 ..... secret room
Room(g, "secret room", "this is where the monsters dump loot and treasures", [9], itemchances=[1.0, 1.0, 0.8, 0.5, 0.4])
# room number 7 .... roof
Room(g, "roof", "you can jump from here directly into the boss room (9)", [5, 9], hint="(roof)")
# room number 8 .... barrier (blocks path to boss room)
descr = """a mighty magical one-way barrier blocks your path into the
nearby boss room. Maybe there is another way into the boss room?"""

Room(g, "barrier room", descr, [5], hint="(magic light)")
# room number 9 .... boss room
# the boss room has 1 to 6 minions and 1 to 3 bosses
descr = "you smell blood. You can go from here throug the barrier (8). There is also a closed secret door. if you use a key, it may open."
Room(g, "boss chamber", descr, [8], monsterchances=[1.0, 0.9, 0.8, 0.5, 0.5, 0.5], bosschances=[1.0, 0.15, 0.05], hint="(boss chamber)")

# ----------- effects ----------
Effect(g, "randomteleport", "teleport")
Effect(g, "hometeleport", "teleport", arg1=1)
Effect(g, "heal5", "heal", arg1=5)
Effect(g, "heal10", "heal", arg1=10)
Effect(g, "heal15", "heal", arg1=15)
Effect(g, "heal50", "heal", arg1=50)
Effect(g, "open secret door", "key", arg1=9, arg2=6, success=1.0)  # connect room 9 to room 6
Effect(g, "poison10", "heal", arg1=-10)
Effect(g, "fullheal", "heal", arg1=50)
Effect(g, "curse", "heal", arg1=-50, success=0.75)
Effect(g, "carry5", "carry", arg1=5)
Effect(g, "carry10", "carry", arg1=10, success=1.0)
Effect(g, "carry15", "carry", arg1=15, success=1.0)
Effect(g, "carry50", "carry", arg1=50, success=1.0)

# ---------- items ------------
# syntax: Item(game, where, description, mass, effect, workshowmanytimes)
Item(g, 1, "blue fearsome chicken feather", 0.1, "hometeleport")
Item(g, 1, "red fearsome chicken feather", 0.2, "hometeleport")
Item(g, 5, "yellow mockingbird feather", 0.1, "randomteleport")
Item(g, 2, "black mockingbird feather", 0.1, "randomteleport")
Item(g, 3, "pink mockingbird feather", 0.1, "randomteleport")
Item(g, 4, "potion of instant healing", 0.25, "heal15")
Item(g, 1, "small healing potion", 0.25, "heal5")
Item(g, 3, "big wheel of cheese", 0.50, "heal5", 5)  # works 5 times
Item(g, 1, "key to secret door", 0.5, "open secret door", -1)  # works always
Item(g, 6, "bottle of holy water", 0.5, "heal50")
Item(g, 7, "Full health potion", 0.50, "fullheal")
Item(g, 2, "Cursed pill", 0.10, "curse")
Item(g, 3, "small backpack", 0.0, "carry5")
Item(g, 5, "medium backpack", 0.0, "carry10")
Item(g, 7, "big backpack", 0.0, "carry15")
Item(g, 6, "super big backpack of doom", 0.0, "carry50")

# -------- weapons ------
w = Weapon(g, 1, "wooden training sword", 3, length=1.0, attackbonus=3, defensebonus=2, damagebonus=1)
Weapon(g, 1, "wooden shield", 6, defensebonus=5, armorbonus=2)  # shield is a weapon !

Armor(g, 1, "leather cap", 2, slot="head", armorbonus=1)

#Daniels code monster

m = Monster(g, 1, "ugly", "troll")
m.hitpoints = 50
w = Weapon(g, -m.number, "epic bow")
w.attackbonus = 50
w.active = True

# --------- Player ------------
p = Player(g, where=1)  # create player in room 1
# ---- default gear for player ---------
shirt = Armor(g, -p.number, "peasant robes", 1, slot="boy", armorbonus=1)
shirt.active = True
p.carry = 1
#fist = Weapon(g,-p.number,"fists (unarmed combat)",0, length=0.0, attackbonus=-1)
#fist.never_drop = True
#fist.active = True

# main loop
turns = 1
while p.location != 0 and p.hitpoints > 0:
    output("----- turn: {} -----".format(turns))
    if not g.rooms[p.location].explored:
        output("You explore a new room!")
        g.rooms[p.location].explored = True  # explore this room
    output(
        "You have {} hitpoints left:\n{}".format(
            p.hitpoints, g.rooms[
                p.location
            ].info(g)
        )
    )
    p.nextAction(g)
    turns += 1
output("\n==================\n")
output("Thank you for playing. Have a nice real life")
