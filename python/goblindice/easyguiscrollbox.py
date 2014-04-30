"""display text output of goblindice004.py inside a tkinter text gui"""
import sys
import os.path 

try:
    import goblindice004 as goblin
    import easygui
except:
    print("Failure: sadly, the import of the easygui.py and/or"
          "goblindice004. py failed. Please make both files are "
          "inside a python path or copy both files into the same"
          "folder as this program.")
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


def playtester_gui():
    """gui to help fine-tune stats of monsters"""

    status, text = check_files("stinky200.gif", "grunty200.gif")
    print(text)
    if not status:              # the same as if status == False:
        sys.exit()
    
    
    m1 = goblin.Monster("Grunty",0.4, 0.7, 95) # name, att, def, hp
    m2 = goblin.Monster("Stinky",0.8, 0.3, 109)
    winnername, hp, rounds, log = goblin.combat_sim(m1,m2)
    
    victorimage = None
    if winnername == "Grunty":
        victorimage = "grunty200.gif"
    elif winnername == "Stinky":
        victorimage = "stinky200.gif"

    m1wins, m2wins, battles = 0, 0, 0
    battlerounds = []
    m1_hp = []
    m2_hp = []
    vtext = "\n\n no battles yet"
    log = ""
    while True:
        text = "\n battles: {}".format(battles)
        text += "\n\n{}\n{}".format(m1,m2)
        if battles > 0:
            text += "\n wins for {}: {} ({:.2f}%)".format(
               m1.name, m1wins, m1wins/battles * 100)
            text+=" ~hp: {:.1f}".format(sum(m1_hp)/len(m1_hp))
            text += "\n wins for {}: {} ({:.2f}%)".format(
               m2.name, m2wins, m2wins/battles * 100)
            text+=" ~hp: {:.1f}".format(sum(m2_hp)/len(m2_hp))
            text += "\nbattles: {}".format(battles)
            text+=" ~duration: {:.1f}".format(sum(battlerounds) /len(
                                              battlerounds))
                    
        action = easygui.buttonbox(text + vtext, "combat sim viewer",
                 ["log", "edit", "save", "+1 battle", "+10 battles",
                  "+100 battles", "quit"], image=victorimage)
        if action == "quit":
            break
        elif action == "log":
            if  battles == 0:
                easygui.msgbox("no battles yet !") 
                continue # jump to the top of the current (while) loop
            easygi.textbox(vtext, "combat log", log)
        elif action == "edit":
            pass
        elif action == "save":
            output = open("combat_statistic","a") # a: append 
            output.write("\n- - - - -\ntext")
            output.close()
        elif action == "+1 battle":
            pass
            
            
        if easygui.ccbox(text,"combat result", image=victorimage):
            easygui.textbox(vtext, "combat log", log)
        
if __name__=="__main__":
    playtester_gui()
