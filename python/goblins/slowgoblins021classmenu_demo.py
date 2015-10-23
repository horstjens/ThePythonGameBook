"""part of http://ThePythonGameBook.com
source code:

https://github.com/horstjens/ThePythonGameBook/blob/master/
python/goblins/slowgoblins021classmenu_demo.py

TODO:     +better remove submenu
          +dynamic finsh method

some code is based on the menudemo of  Christian Hausknecht, located at
https://github.com/Lysander/snippets/tree/master/Python/python-misc/simplemenus

and licensed under the gpl license.

see https://github.com/Lysander/snippets/blob/master/Python/python-misc/simplemenus/classmenu.py
for the original file

"""

import sys
import itertools  # from itertools import chain

#
# Create some little demo functions that does not have any sensefull
# functionality but printing some stuff.
#


def make_some_foo_func(s):
    """just some demonstration functions"""

    def func():
        print(s)

    return func


hello, python, nothing, special = list(
    make_some_foo_func(s)
    for s in (
        "Hello World!", "Python rocks!", "Nothing to do yet...",
        "Wow! So special we must put it into a subsubmenu..."
    )
)


class Menu:
    """
    Class that represents and handles a complete menu system all in once.

    Each menu class can...

        ... print out the (current) menu
        ... handle the user input
        ... run in an event-loop, that handles the complete menu based
            workflow.

    It provides the `finish`-method, which adds automatically all needed
    'Exit'-entries to each (sub)menu, so building up a menu is not so much
    typing.

    To avoid recursion, we use the `context`-attribute of the Menu-class. The
    current menu-object is always bound to this attribute. As we can combine
    arbitrary menu objects (via the `append_submenu`-method) we must keep
    the current working menu accessible to operate only in one object, the
    'root'-object.
    """

    def __init__(self, title):
        self.title = title
        self.items = []
        self.context = self

    def __repr__(self):
        return "Menu({})".format(self.title)

    def __str__(self):
        head = ("", "-" * len(self.title), "{}".format(self.title), "-" * len(self.title))
        entries = ("{} {} {}".format(index, "+" if isinstance(entry[1], Menu) else " ", entry[0]) for index, entry in enumerate(self, 0))
        return "\n".join(itertools.chain(head, entries))

    def __getitem__(self, key):
        """
        Nice to have method for providing the iterable "interface". So you can
        access any menu item via an index or loop over all entries using
        `for` :-)
        """
        return self.items[key]

    def append(self, text, func):
        """
        Appends a menu entry to `self.items`.

        :param text: string with entry description
        :param func: callable that will be called if chosen
        """
        self.items.append((text, func))

    def insert(self, text, func):
        """
        insert a menu entry at position 0 to `self.items`.

        :param text: string with entry description
        :param func: callable that will be called if chosen
        """
        self.items.insert(0, (text, func))

    def remove(self, text):
        """
        remove a menu entry

        :param text: string with entry description
        """
        for (t, f) in self.items:
            if t == text:
                break
        else:
            print("did not found text")
            return
        self.items.remove((t, f))

    def append_submenu(self, other):
        """
        Appends a submenu entry to the menu. That can be a complex branch
        of menu-objects.

        :param other: Menu object, that represents a complete submenu-branch.
        """
        self.items.append((other.title, other))

    def remove_submenu(self, title):
        """removes complete submenu entry and tree"""
        pass  # not necessary ?

    def finish(self, text="Exit"):
        """
        Nice helper method that computes all needed 'Exit'-items for each
        submenu and the 'final' 'Exit'-item at the main-menu, which is simply
        any string.

        All other exit-items are menu objects of the corresponding parent-menu.

        The algorithm implements a breadth-first search for handling this task.

        only useable once for a new menu, not later for a dynamic menu

        :param text: string with the text of the 'Exit'-item.
        """
        #self.items.append((text, "#exit"))
        self.items.insert(0, (text, "#exit"))
        stack = [(self, None)]
        while stack:
            menu, parent = stack.pop()
            for _, command in menu:
                if isinstance(command, Menu):
                    stack.append((command, menu))
            if menu is not self:
                #menu.append("{} -> {}".format(text, parent.title), parent)
                menu.insert(
                    "{} -> go back to {}".format(text, parent.title), parent
                )

    def get_user_input(self):
        while True:
            try:
                choice = int(input("Your choice?: "))  #- 1
                if -1 <= choice < len(self.context.items):
                    return choice
                else:
                    raise IndexError
            except (ValueError, IndexError):
                print("please enter numbers from 0 to {} only".format(len(self.context.items) - 1))

    def run(self):
        """
        Core method to handle a menu. This invokes a loop that handles all
        menu tasks as long as the main menu is exited by the user.
        """
        while True:
            print(self.context)
            choice = self.get_user_input()
            _, command = self.context[choice]
            if isinstance(command, Menu):
                self.context = command
            elif isinstance(command, str):
                return
            else:
                command()


class Game(object):
    def __init__(self):

        self.teams = []

        self.menu = Menu("main menu")
        self.menu.append("hello", hello)  # call function outside class
        self.menu.append("python", python)
        self.menu.append("greetings", self.greetings)  # call method
        self.menu.append("new team", self.newteam)
        self.menu.append("kill team", self.killteam)

        sub = Menu("Sub menu")
        sub.append("action", nothing)

        # ... or to create menu objects that we can later on
        subsub = Menu("Subsub menu")
        subsub.append("Special", special)
        # ... easily add to another menu as submenu
        sub.append_submenu(subsub)

        another_sub = Menu("Another sub menu")
        another_sub.append("more action", nothing)
        # wait a second, we do not need that... we have `menu.finish()`!
        #another_sub.append("Back", menu)

        self.menu.append_submenu(sub)
        self.menu.append_submenu(another_sub)

        # create 'Exit'-entries automatically - nice to have this :-)
        # saves a lot of typing... :-)))
        self.menu.finish()

        # shake it!
        self.menu.run()

    def greetings(self):
        print("i send you greetings from within the game class")

    def newteam(self):
        nt = input("please enter name for new team \n:>")
        self.teams.append(nt)
        self.menu.append("manage team {}".format(nt), lambda: self.manage(nt))
        sub = Menu("submenu for team {}".format(nt))
        # sadly i can NOT use finish here, because finish was already used
        sub.append("Exit --> go back to main menu", self.menu)
        sub.append("Special", special)

        self.menu.append_submenu(sub)

    def killteam(self):
        kt = input("please enter name for team to delete \n:>")
        self.teams.remove(kt)
        self.menu.remove("manage team {}".format(kt))
        self.menu.remove("submenu for team {}".format(kt))

    def manage(self, teamname):
        print("You are such a manager of team {}! what a boss..".format(teamname))


if __name__ == "__main__":
    #main()
    g = Game()
