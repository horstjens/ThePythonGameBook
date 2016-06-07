#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       dragoncave.py
#
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

#def main():
#
#   return 0
#
#if __name__ == '__main__':
#   main()

# --- some functions, to be replaced by easygui-functions


def msgbox(msg="hi there", title="window title", button="ok", root=None, image=None):
    print title
    print msg


def inputbox(msg="huh?", title="window title", default="dunno nothing", root=None, image=None):
    print title
    return raw_input("msg", default)


def buttonbox(msg="choose a button", title="window title", choices=("one", "two", "three"), root=None, image=None):
    answer = "-1"
    while not answer.isdigit() or (answer < 0) or (answer > len(choices)):
        print title
        print msg
        print "type the number and hit ENTER:"
        for button in choices:
            print choices.index(button), button
            # each button has an index number, starting with 0
        answer = int(raw_input("Your choice:>"))
        print answer
    return choices[answer]  # return the text of the selected button

    # -----


gameOver = False

msg = """
You stand in the entry of the famous dragoncave. Your task is to steal
three dragon eggs and return alive. The dragoncave is haunted by the
mighty dragon and other dangers"""

title = "cave entry"
choices = ("leave the cave", "go deeper into the cave")
answer1 = buttonbox(msg, title, choices)
