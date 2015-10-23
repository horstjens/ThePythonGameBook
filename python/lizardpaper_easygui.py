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

#### warum kann ich nicht from lizardpaper import game, startmenu machen und die funktionien output, ask und askname überschreiben ???
#### wenn ich es mache werde trotzdem die funkoinen ask etc. von lizardpaper ausgeführt, nicht die neuen easygui-funktionnen

import random
try:
    import easygui
except:
    raise UserWarning("Please make sure easygui.py is in the same folder")


    # general purpose functions from lizardpaper, replaced with easygui functions
def output(msg):
    easygui.msgbox(msg)  # python 2.x: use "print msg" instead "print(msg)"


def ask(msg="Your answer please:", choices=["yes", "no"]):
    return easygui.buttonbox(msg, "your answer:", choices)


def askname(msg="please enter your name"):
    return easygui.enterbox(msg)  # python2.x: use "raw_input" instead "input"


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
    output(msg)
    mode = "x"
    mode = ask("press c for classic variant (rock, paper, scissors) \n"  \
               "press n for new variant (rock, paper, scissors, lizard, Spock \n", ["c","n"])
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
        things["o"] = "Spock"

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
            "o": ("paper disproves Spock", "Spock is disproved by paper"),
            "r": ("paper covers rock", "rock is enveloped by paper")
        },
        "o": {
            "s": ("Spock smashes scissors", "scissors are smashed by Spock"),
            "r": ("Spock vaporizes rock", "rock is vaporized by Spock")
        },
        "l": {
            "p": ("lizard eats paper", "paper is eaten by lizard"),
            "o": ("lizard poisons Spock", "Spock is poisoned by lizard")
        }
    }

    question = "What do you play ? \n"
    for thingy in things.keys():
        question += thingy + ": " + things[thingy] + "\n"
    #question += "\n please press one of the keys listed above and ENTER \n"
    mainloop = True
    rounds = 0
    # ------ generating players --------
    players = {}  # name, nature, thing, points # a dict cointaining dicts ...
    while True:
        output(
            "At the moment, this game has %i players. Minimum to start a game is 2 players."
            % len(players)
        )
        if len(players.keys()) > 0:
            output("-- list of players in the game --")
            for player in players.keys():
                output(
                    "name: %s  type: %s" % (player, players[player]["nature"])
                )
        output("----")
        playername = askname(
            "please type in the name of a new player and press ENTER \n"
            "press only ENTER to start the game \n"
        )
        if playername == "":
            break  # exit
        natureOfPlayer = ask(
            "is this player a (h)uman or a (c)omputer ?", ["h", "c"]
        )
        players[playername] = {
            "nature": natureOfPlayer,
            "thing": "xxx",
            "points": 0
        }  # add player to dictionary
    if len(players) < 2:
        output("you need at least 2 players to start a game. Bye !")
        return "too few players"

    while mainloop:  # ----------- the game loop ------------
        output(" ---- rounds played: %i ----- " % rounds)
        for player in players.keys():
            if players[player]["nature"] == "h":  # human
                playerthing = ""
                output("******** player %s, it is your turn ! *******" % player)
                playerthing = ask(question, tuple(things.keys()))  # asking the player for rock, paper etc..
                players[player]["thing"] = playerthing  # adding answer to dict (inside a dict)
            else:  # computer player
                players[player]["thing"] = random.choice(tuple(things.keys()))  # computerthing
        rounds += 1

        for player in players.keys():  # --- output ----
            playerthing = players[player]["thing"]
            output("The coice of player %s is: %s " % (player, playerthing))
        for player in players.keys():  # ---- calculate winner
            output("...calculating points for player %s..." % player)
            playerthing = players[player]["thing"]
            for enemy in players.keys():
                if player != enemy:
                    enemything = players[enemy]["thing"]
                    output(
                        "%s of %s versus %s of %s" % (
                            things[playerthing], player, things[enemything],
                            enemy
                        )
                    )
                    if playerthing == enemything:
                        output("this is a draw (0 points)")
                    elif enemything in wintext[playerthing].keys():
                        players[player]["points"] += 1
                        output(
                            "%s (+1 point)" %
                            wintext[playerthing][enemything][0]
                        )  # victory
                    else:
                        output(
                            "%s (no point)" %
                            wintext[enemything][playerthing][1]
                        )  # loose
        output("====== result (round %i) =======" % rounds)  #------ summary -------
        for player in players.keys():
            output("points: %i for %s" % (players[player]["points"], player))
        output("------ next round -------")
        playMore = ask("press c to continue, q to quit", ["c", "q"])
        if playMore == "q":
            mainloop = False
        #print "\n\n\n" # three empty lines
    output("bye-bye")
    return 0  # (computerpoints, playerpoints)


if __name__ == '__main__':
    startmenu()
