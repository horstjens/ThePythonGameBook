"""
gui to edit and test monster attributes and combats

Name:             combatsim.py 
purpose           show menu and gui using easygui, show passing of
                  parameters to and from functions, show passing of 
                  class instances, introduce lists and dictionarys
edit this code:   https://github.com/horstjens/ThePythonGameBook/
                  blob/master/python/goblindice/combatsimviewer.py
edit tutorial:    https://github.com/horstjens/ThePythonGameBook/
                  blob/master/goblindice004.rst                  
main project:     http://ThePythonGameBook.com
Author:           Horst JENS, horst.jens@spielend-programmieren.at
Licence:          gpl, see http://www.gnu.org/licenses/gpl.html
"""
import sys
import os.path

try:
    import goblindice004 as goblin
    import easygui
except:
    print(
        "Failure: sadly, the import of the easygui.py and/or"
        "goblindice004. py failed. Please make both files are "
        "inside a python path or copy both files into the same"
        "folder as this program."
    )
    sys.exit()


def check_files(*filenames):
    """"check if files exist in the same folder as this program.
    filenames must be passed as comma seperated parameters"""
    txt = ""
    for filename in filenames:
        ok = True
        if os.path.isfile(filename):
            txt += "\n{} exist".format(filename)
        else:
            txt += "\n{} not found"
            ok = False
    return ok, txt


def clean():
    """return fresh values for playtester_gui"""
    return 0, 0, 0, [], [], [], "\n\n no battles yet", ""


def make_txt(m1, m2, m1_wins, m2_wins, m1_hp, m2_hp, battles, battlerounds):
    """make textstring for main menu"""
    text = "\n{}\n{}\n".format(m1, m2)
    if battles > 0 and len(m1_hp) > 0:
        text += "\nVictorys for {}: {} ({:.2f}%)".format(
            m1.name, m1_wins, m1_wins / battles * 100
        )
        text += " ~hp: {:.1f}".format(sum(m1_hp) / len(m1_hp))
        #text+="\nwins: " + int(100 * m1_wins/battles)*"V"
    if battles > 0 and len(m2_hp) > 0:
        text += "\nVictorys for {}: {} ({:.2f}%)".format(
            m2.name, m2_wins, m2_wins / battles * 100
        )
        text += " ~hp: {:.1f}".format(sum(m2_hp) / len(m2_hp))
        #text+="\nwins: " + int(100 * m1_wins/battles)*"V"
    if battles > 0:
        text += "\n\nbattles: {} ~duration: {:.1f}".format(
            battles, sum(battlerounds) / len(battlerounds)
        )
    return text


def show_log(battles, vtext, log):
    if battles == 0:
        easygui.msgbox("no battles yet !")
        return  # do nothing and return
    easygui.textbox(vtext, "combat log", log)  # show box and return


def edit_monsters(m1, m2):
    while True:  # loop until Cancel or having valid values
        # easygui.multenterbox(text, titles, fieldls, values)
        values = easygui.multenterbox(
            "Please edit carefully", "edit monster stats", (
                "Monster1: name (text)", "Monster1: attack (float)",
                "Monster1: defense (float)", "Monster1: hitpoints (integer)",
                "Monster2: name (text)", "Monster2: attack (float)",
                "Monster2: defense (float)", "Monster2: hitpoints (integer)"
            ), (
                m1.name, m1.attack, m1.defense, m1.hitpoints, m2.name,
                m2.attack, m2.defense, m2.hitpoints
            )
        )
        if values == None or None in values:
            easygui.msgbox("nothing changed: empty value or Cancel")
            break  # break out of the  edit loop
        else:
            try:
                m1 = goblin.Monster(
                    values[0], float(values[1]), float(values[2]),
                    int(values[3])
                )
                m2 = goblin.Monster(
                    values[4], float(values[5]), float(values[6]),
                    int(values[7])
                )
            except:
                easygui.msgbox("Invalid value. Please try again")
                continue  # repeat editing
            break  # no problems detected:
    return m1, m2  # return the changed monster instances


def savefile(oldtext, text):
    filename = easygui.filesavebox()  # return None if user click Cancel
    if filename == None:
        return  # user selected Cancel
    output = open(filename, "a")  # a: append
    output.write("\n- - - - -\n{}\n{}".format(oldtext, text))
    output.close()


def fight(
    action, calc_buttons, m1, m2, battles, battlerounds, m1_wins, m1_hp,
    m2_wins, m2_hp, picdict
):
    potency = calc_buttons.index(action)  # rank of button
    for x in range(10**potency):  # fight 1,10,100 times
        winner, hp, rounds, log = goblin.combat_sim(m1, m2)
        battles += 1
        battlerounds.append(rounds)
        if winner == m1.name:
            m1_wins += 1
            m1_hp.append(hp)
        else:
            m2_wins += 1
            m2_hp.append(hp)
        m1.hitpoints = m1.fullhealth  # restore original hp !
        m2.hitpoints = m2.fullhealth
    vtext = "\n\n\n"
    vtext += "{} wins after {} rounds having {} hp left".format(
        winner, rounds, hp
    )
    if winner in picdict:
        victorimage = picdict[winner]
    else:
        victorimage = None
    # \ as last char of a line indicate python to continue in next line
    return battles, battlerounds, m1_wins, m1_hp, m2_wins, m2_hp, \
           vtext, victorimage, log


def playtester_gui():
    """gui to help fine-tune stats of monsters"""

    status, text = check_files("stinky200.gif", "grunty200.gif")
    if not status:  # the same as if status == False:
        sys.exit()

    m1 = goblin.Monster("Grunty", 0.4, 0.7, 95)  # name, att, def, hp
    m2 = goblin.Monster("Stinky", 0.8, 0.3, 109)

    victorimage = None
    picdict = {"Grunty": "grunty200.gif", "Stinky": "stinky200.gif"}

    m1_wins, m2_wins, battles, battlerounds, m1_hp, m2_hp, \
        vtext, log = clean() # set valuues to zero / empty
    oldtext = ""

    calc_buttons = ["+1 battle", "+10 battles", "+100 battles", "1000", "10000"]
    buttonlist = ["log", "clear", "edit", "save"]
    buttonlist.extend(calc_buttons)  # append each calcbutton to the list
    buttonlist.append("quit")  # append one single elemet

    while True:
        text = make_txt(
            m1, m2, m1_wins, m2_wins, m1_hp, m2_hp, battles, battlerounds
        )
        action = easygui.buttonbox(
            oldtext + text + vtext,
            "combat sim viewer",
            buttonlist,
            image=victorimage
        )
        if action == "quit":  # --------menu handler-----------
            break
        elif action == "log":
            show_log(battles, vtext, log)
        elif action == "clear":
            m1wins, m2wins, battles, battlerounds, m1_hp, m2_hp, \
                vtext, log = clean()
            text, oldtext, victorimage = "", "", None
        elif action == "edit":
            m1, m2 = edit_monsters(m1, m2)
            oldtext = text + "\n" + "- - - " * 10 + "\n"
            m1_wins, m2_wins, battles, battlerounds, m1_hp, \
               m2_hp, vtext, log = clean()
        elif action == "save":
            savefile(oldtext, text)
        elif action in calc_buttons:  # fight !
            battles, battlerounds, m1_wins, m1_hp, m2_wins, m2_hp, \
                vtext, victorimage, log=fight(action,calc_buttons,m1,m2,
                battles, battlerounds, m1_wins, m1_hp, m2_wins, m2_hp,
                picdict)


if __name__ == "__main__":
    playtester_gui()
