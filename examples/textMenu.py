# text menu for use inside games. demonstrate the use of Menu and Item class. see pygameMenu.py

class Item:

    def __init__(self, name="dummy", choices=[], cindex=0, rect=None) :
        """
        Menu Item. For use inside Menu.items list.
        """
        self.name = name
        self.choices = choices
        self.cindex = cindex
        self.rect = rect
 

class Menu:

    def __init__(self, name="root", items=[], rect=None):
        """
        Menu , a list of Menu Items.
        Every Submenu (except the 'root' main menu) get's automatically added an Item('back')
        """
        self.name = name
        self.items = items
        self.rect = rect
        # autoexec: add 'back' as first item if necessary
        self.add_back_item()

    def add_back_item(self):
        if self.name != "root":
            if "back" not in [i.name for i in self.items]:
                self.items.insert(0,Item("back"))

# create menus, begin with sub-sub menu and working the way up to root menu
# every menu except the "root" menu gets automatically addaed an 'back' Item
audiomenu = Menu(name="audio", items=[Item("sound volume"), Item("music volume")])
videomenu = Menu(name="video", items=[Item("fullscreen"), Item("screen resolution")])
settingsmenu = Menu(name="settings",items=[audiomenu, videomenu, Item(name="difficulty",choices=["easy", "medium", "hard", "ironman"],cindex=0)])
rootmenu = Menu("root", [Item("play"), Item("credits"), settingsmenu, Item("quit")])

history = [rootmenu]
while True:
    menu = history[-1]

    # ----- print history --------
    print("You are here:", ">".join([i.name for i in history]))
    # ----- print menu items -----
    for number, item in enumerate(menu.items):
        print(number, item.name,
              ">" if type(item) == Menu else 
              ": " + item.choices[item.cindex]
              if len(item.choices) > 0 else ""  )
    command = input("number or name >>>")
    itemnames = [i.name for i in menu.items]
    if command in itemnames:
        i = itemnames.index(command)
    elif command in [str(i) for i in range(len(menu.items))]:
        i = int(command)
    else:
        print("unacceptable command")
        continue
    # ---- data processing -----
    # jump into submenu? 
    if type(menu.items[i]) == Menu:
        history.append(menu.items[i])
        menu = menu.items[i]
        continue
    # jump back to previous menu
    print("name:", menu.items[i].name)
    if menu.items[i].name == "back":
        history.pop() # delete last entry
        if len(history) == 1:
            menu = rootmenu
        else:
            menu = history[-1]
        continue
    # -- change value of item ----
    if len(menu.items[i].choices) > 0:
        menu.items[i].cindex += 1
        if menu.items[i].cindex == len(menu.items[i].choices):
            menu.items[i].cindex = 0
        continue
    # -- selection was not a sub-menu---
    selection = menu.items[i].name
    print("your choice was:", selection)
    if selection == "quit":
        break
    elif selection == "play":
        print("playing a game.....")
    elif selection == "credits":
        print("*** (c) 2020 by Horst JENS ***")

        
print("bye-bye")
        
    
    
        
    

