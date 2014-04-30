"""display text output of goblindice004.py inside a tkinter text gui"""
import sys
import os.path 
import goblindice004 

try: 
    import easygui
except:
    print("Failure: sadly, the import of the easygui was not "
          "sucessfull. please install easygui correctly inside a"
          "python path or copy the file easygui.py into the same"
          "folder as this program. Download easygui at"
          "http://easygui.sourceforge.net/")
    sys.exit()
    

stinky_found = os.path.isfile("stinky200.gif")
grunty_found = os.path.isfile("grunty200.gif")

if stinky_found and grunty_found:
    print("both image files found. have a nice game")
else:
    print("Please make sure both files stinky200.gif and grunty200.gif"
          " are inside the same folder as this program"
          "status: stinky200.gif: {} grunty200.gif: {}".format(
          stinky_found, grunty_found))
    #sys.exit() #continue, but without graphic


log = goblindice004.combat_sim()


if "Victory for Grunty" in log:
    victorimage = "grunty200.gif"
    vtext = "Grunty wins again !"
else:
    victorimage = "stinky200.gif"
    vtext = "Another victory for Stinky!"
text = vtext + "\nDo you wish to see the combat log?"
if easygui.ccbox(text,"combat result", image=victorimage):
    easygui.textbox(vtext, "combat log", log)
    
