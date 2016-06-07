#       lizardpaper.py
#       Copyright 2012 Horst JENS <horst.jens@spielend-programmieren.at>
#       This program is part of ThePythonGameBook ,
#       see http://ThePythonGameBook.com for more information.
#       Check the newest version of this file at Github.com:
#       https://github.com/horstjens/ThePythonGameBook/blob/master/python/lizardpaper.py
#
#       tested with python3
#
#       This source code is licensed under the
#       GNU General Public License, Free Software Foundation
#       http://www.gnu.org/licenses/gpl
#

## irgendein fehler mit keys

import random


# general purpose functions, to be replaced later by a graphical user interface
def output(msg):
    print(msg)


def ask(msg="Your answer please:", choices=["yes", "no"]):
    """gives the user a list of choices to answer. Choices must have different first chars"""
    while True:
        print(msg)
        print("Please type one of those answers (without the quotes) and press ENTER:")
        print(choices)
        print("or")
        firstchars = []
        # see if there are choices larger than one char
        maxlength = 1
        for item in choices:
            if len(item) > maxlength:
                maxlength = len(item)
        if maxlength > 1:
            for item in choices:
                firstchars.append(item[0])
            print(tuple(firstchars))
        answer = input(">")
        if answer in choices or answer in firstchars:
            break
    return answer[0]


def askname(msg="please enter your name"):
    return input(msg)


def startmenu():
    msg = "\n"
    msg += "\n*** Welcome !***"
    msg += "\nplease choose between a classic game of 'rock, paper, scissors'"
    msg += "\nor a game of the newer variant 'rock, paper, scissors, lizard, Spock' "
    msg += "\n"
    msg += "\nsee Wikipedia for game rules and more information:"
    msg += "\nhttp://en.wikipedia.org/wiki/Rock_paper_scissors"
    msg += "\nhttp://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-spock"
    msg += "\n"
    #output(msg)
    mode = ask(msg + "press c for classic variant (rock, paper, scissors) \n"  \
               "press n for new variant (rock, paper, scissors, lizard, Spock \n", ["classic","new"])
    if mode == "c":
        game("classic")
    elif mode == "n":
        game("new")


def game(mode="classic"):
    """rock paper scissor lizard spock
    mode can be new or classic"""
    # { key: human-readable key description }
    things = {"r": "rock", "s": "scissors", "p": "paper"}
    if mode == "new":  # expand only for new version
        things["l"] = "lizard"
        things["m"] = "mister Spock"

        # { victor : { victim : (victorytext loosertext) }}
    wintext = {
        "r": {
            "s": ("rock crushes scissors", "scissors is crushed by rock"),
            "l": ("rock crushes lizard", "lizard is crushed by rock")
        },
        "s": {
            "p": ("scissors cut paper", "paper is cut by scissors"),
            "l":
            ("scissors decapitate lizard", "lizard is decapitated by scissors")
        },
        "p": {
            "o": (
                "paper disproves mister Spock",
                "mister Spock is disproved by paper"
            ),
            "r": ("paper covers rock", "rock is enveloped by paper")
        },
        "m": {
            "s": (
                "mister Spock smashes scissors",
                "scissors are smashed by mister Spock"
            ),
            "r":
            ("mister Spock vaporizes rock", "rock is vaporized by mister Spock")
        },
        "l": {
            "p": ("lizard eats paper", "paper is eaten by lizard"),
            "o": ("lizard poisons Spock", "Spock is poisoned by lizard")
        }
    }

    #question = "What do you play ? \n"
    #for thingy in things.keys():
    #    question += thingy + ": " + things[thingy] + "\n"
    #question += "\n please press one of the keys listed above and ENTER \n"
    mainloop = True
    rounds = 0
    # ------ generating players --------
    players = {}  # name, nature, thing, points # a dict cointaining dicts ...
    while True:
        msg = "At the moment, this game has %i players. Minimum to start a game is 2 players. \n" % len(players)
        if len(players.keys()) > 0:
            msg += "-- list of players in the game --\n"
            for player in players.keys():
                msg += "name: %s  type: %s \n" % (player, players[player]["nature"])
        msg += "----\n"
        playername = askname(msg + "please type in the name of a new player and press ENTER \npress only ENTER to start the game \n")
        if playername == "":
            break  # exit
        natureOfPlayer = ask("is this player %s a human or a computer ?" % playername, ["human", "computer"])
        players[playername] = {
            "nature": natureOfPlayer,
            "thing": "xxx",
            "points": 0
        }  # add player to dictionary
    if len(players) < 2:
        output("you need at least 2 players to start a game. Bye !")
        return "too few players"

    while mainloop:  # ----------- the game loop ------------
        output(" ---- rounds played: %i ----- \n" % rounds)
        for player in players.keys():
            if players[player]["nature"] == "h":  # human
                playerthing = ""
                msg = "******** player %s, it is your turn ! ******* \n" % player
                playerthing = ask(msg + "What do you play ? \n", tuple(things.values()))  # asking the player for rock, paper etc..
                players[player]["thing"] = playerthing  # adding answer to dict (inside a dict)
            else:  # computer player
                players[player]["thing"] = random.choice(tuple(things.keys()))  # computerthing
        rounds += 1

        msg = ""
        for player in players.keys():  # --- output ----
            playerthing = players[player]["thing"]
            msg += "The coice of player %s is: %s \n" % (player, playerthing)
        for player in players.keys():  # ---- calculate winner
            msg += "...calculating points for player %s...\n" % player
            playerthing = players[player]["thing"]
            for enemy in players.keys():
                if player != enemy:
                    enemything = players[enemy]["thing"]
                    msg += "%s of %s versus %s of %s \n" % (things[playerthing], player, things[enemything], enemy)
                    if playerthing == enemything:
                        msg += "this is a draw (0 points) \n"
                    elif enemything in wintext[playerthing].keys():
                        players[player]["points"] += 1
                        msg += "%s (+1 point) \n" % wintext[playerthing][enemything][0]  # victory
                    else:
                        msg += "%s (no point) \n" % wintext[enemything][playerthing][1]  # loose
        msg += "====== result (round %i) =======\n" % rounds  #------ summary -------
        for player in players.keys():
            msg += "points: %i for %s \n" % (players[player]["points"], player)
        msg += "------ next round -------\n\n"
        playMore = ask(msg + "continue or quit ?", ["continue", "quit"])
        if playMore == "q":
            mainloop = False
        #print "\n\n\n" # three empty lines
    output("bye-bye")
    return 0  # (computerpoints, playerpoints)


if __name__ == '__main__':
    startmenu()
