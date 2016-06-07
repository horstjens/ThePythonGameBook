"""
dungeon003_utils.py: the useful ask function in a single file

example of a game dungeon to teach python programming to young students
introducing import of functions from modules

This code is part of ThePythonGameBook project, see http://ThePythonGameBook.com
"""
__author__ = "Horst JENS (horstjens@gmail.com, http://spielend-programmieren.at)"
__license__ = "GPL3, see http://www.gnu.org/licenses/gpl-3.0.html"


def ask(prompt, allowed=["a", "b", "i", "q"]):
    """force the player to choose one of the allowed answers and returns it"""
    while True:
        print(prompt)
        answer = input("Please type corresponding key and ENTER>")
        if answer in allowed:
            return answer
        print("Wrong answer. Possible answers are:", allowed)
