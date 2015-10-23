"""scrollbox to display text in a vertical scrollable window

source: http://stackoverflow.com/questions/17657212/
        how-to-code-the-tkinter-scrolledtext-module
note:   easygui.textbox does the same, but is not included in python
"""

import tkinter as tk
import tkinter.scrolledtext as tkst
# make sure goblindice003.py is is in the same folder as this program
import goblindice003 as goblin

window = tk.Tk()
frame1 = tk.Frame(master=window, bg='#808000')
frame1.pack(fill='both', expand='yes')
editArea = tkst.ScrolledText(master=frame1, wrap=tk.WORD, width=80, height=40)
editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# Adding some text, to see if scroll is working as we expect it
editArea.insert(tk.INSERT, goblin.combat_sim())
window.mainloop()
