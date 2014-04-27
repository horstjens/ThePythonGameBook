Goblin vs. testdummy
====================

about
-----

This page shows how to formulate an idea (combat calculation) as a series of instructions and code it using python3.

idea
----

.. figure:: /python/goblindice/goblindice001.png
   :alt: Flow Chart for goblindice001
   :height: 800px
   :align: right
   

Imagine a young goblin named "Grunty". He dreams of being a fearsome warrior one day. However, at the moment, he is rather unskilled and barely capable of handling a weapon. Grunty goes to the training place and fight a wooden testdummy to train his fighting skills.

Handling a weapon is no easy task, and Grunty will, despite his best efforts, not always land a blow. Sometimes he will miss.

How Grunty looks is not the focus of this tutorial (yet). For this first example let us create some game (combat) mechanics using the Python programming language.





Let us assume that Grunty has a low basic chance of hitting the testdummy while swinging his weapon, like only 3 hits for every ten strikes. This can be written as a fraction: 3/10 or 0.3 or 30% - that's a bit less than every third strike.


But not every strike is the same for Grunty. Sometimes he has luck and performs a perfect attack, sometimes not. To reflect this variety, let us add some luck on top his base chance, like a random decimal number (a so called :term:`float`) between Zero and One. 
The formula for Gruntys attack is therefore:

.. code-block:: python

       attack_value = base_attack + random_float_value

Note that the resulting attack value can be larger then 1, everytime when the random value is larger than 0.7. The attack value can never be smaller than 0.3 for Grunty.

Grunty is fighting against a wooden, unmovable testdummy. The testdummy is easy to hit: 9 times out of 10 an attacker can calculate to land an hit on the testdummy. Let us describe this value as base defense value for the testdummy (1/10 or 0.1 or 10%), and add to that an random float value between 0 and 1:

.. code-block:: python

       defense_value = base_defense + random_float_value

The combat runs in several combat rounds:
Each round, the computer calculates the attack and defense values (using his random generator) and compares those two. If the attacking value is greater than the defending value, Grunty managed a hit on the testdummy. But how much damage did he inflict ? The damage is calculated seperately, by a random whole number (:term:`integer`) bewteen 1 and 10: 

.. code-block:: python
       damage = random_integer_value

The damage is then substracted from the "Hitpoints" (also an integer number) of the testdummy, and the whole process is reapeated until the testdummy has no hitpoints left.

The fresh, undamaged testdummy must start with an given number of hitpoints, say 200 hiptoints. Also it is interesting to know how many combat rounds Grunty needs to destroy the testdummy, so a combat round counter is needed and set to 0 (you will soon see why) before the game.

.. code-block:: python
 
     testudmmy_hitpoints = 200
     combat_round_counter = 0    




If you have read the instructions above you have basically read a program (that is a set of instructions) and you could now simulate Gruntys combat performance by using those instructions, paper and pen to keep track of combat rounds and hitpoints, and some sort of random generators (for whole numbers you could roll a dice or randomly open a book and read the page number. For float values you could use a method like touching a ruler with a pen behind your back and reading the value of where the pen touched - or by simply making the numbers up in your mind).

To let a computer do this task instead, a set of commands and concepts is necessary:

:term:`Variables`: numbers that can have different values over time, like the testdummys hitpoints or the round counter

:term:`Operators` to compare two variables

:term:`Control structures`:

a :term:`Conditional` ("if") statement to decide what to do if the attack value is greater than the defense value

a :term:`Loop` to repeat the whole process as long as necessary

Some random generator :term:`functions`


Code
====


prerequesites
-------------
  * necessary:
  
    * python3 installed
    * text editor can save python files ( like `goblindice001.py`)  
    * python3 interpreter can launch saved python file.
    
  * recommended:
  
    * python-friendly IDE like IDLE, Geany etc.
    * ability to read and type (blind typing) using the 10 finger system, instead of copy and paste
    * python shell to lookup commands
    * executing python with filename as parameter from the command line `python3 goblindice001.py`)
    
source code
-----------  
   
bbbb


.. literalinclude:: /python/goblindice/goblindice001.py
   :language: python
   :linenos:

code discussion
---------------

Some elements in this code may need explaining:


=========== ================= ================================================================================================================================================================================================================================================================================================
line number term              explanation
=========== ================= ================================================================================================================================================================================================================================================================================================
 1 - 9      ``import random`` Some multi-line text :term:`string` insinde triple-quotes ``"""``. Because the text ist not assigned to any variable, it is inter preted by python as something interested for humans only, like a :term:`comment`. Docstrings at the beginning of the code are not necessary, but nice to have.
11          bla bla blabla    abc def ghi jkl etc. usw.
=========== ================= ================================================================================================================================================================================================================================================================================================


+--------------+---------------------+-----------------------------------------------------------------+
| Line numbers | term                | explanation                                                     |
+==============+=====================+=================================================================+
| 1-9          | :term:`docstring`   | Some multi-line text :term:`string` in triple-quotes ``"""``.   |
|              |                     | Because the text ist not assigned to any variable, it is inter- |
|              |                     | preted by python as something interested for humans only, like  |
|              |                     | a :term:`comment`. Docstrings at the beginning of the code are  |
|              |                     | not necessary, but nice to have.                                |        
+--------------+---------------------+-----------------------------------------------------------------+
| 11           | ``import random``   | To make use of any :term:`functon` in pythons random module,    |
|              |                     | it is necessary to import this module first. Later in this code |
|              |                     | functions of the random module will use the ``.random`` prefix. |
+--------------+---------------------+-----------------------------------------------------------------+
| 13           | ``comment``         | Everything behind a ``#`` sign in python is a comment. Comments |
|              |                     | are useful for human eyes only and mostly ignored by Python.    |
+--------------+-------------------- +-----------------------------------------------------------------+
| 14           | ``assignement``,    | The value of 0.3 is assigned to the variable ``grunty_attack``  |
|              | ``inline comment``  | (You best read it from right to left). Python knows that this   | 
|              |                     | is a float because of the assigned decimal point value.         |
|              |                     | Note that the part right from the ``#`` sign is also a comment  |
+--------------+---------------------+-----------------------------------------------------------------+
| 23           | ``loop``            | The line starts with the ``while`` keyword and ends with an     |
|              |                     | colon. All following, idented lines (line 24 until line 41)     |
|              |                     | are building a code block, and this block is repeated a as long |
|              |                     | as the ``condition`` right next to ``while`` remains ``True``.  |
+--------------+---------------------+-----------------------------------------------------------------+
| 24           | ``increment``       | The variable ``combatround`` is incremented by 1. This is the   |
|              |                     | reason that the variable was set to 0 before.                   |
+--------------+---------------------+-----------------------------------------------------------------+
| 25           | ``string format``,  | The textstring variable ``logfile`` is incremented, meaning     |
|              | ``\n``,             | another textstring ist appended to it. The appending textstring |
|              | ``new line``        | starts with a new line ``\n`` and use the ``.format()`` method  |
|              |                     | to mix numbers and text inside a text string: Each pair of      |
|              |                     | curly brackets ``{}`` is replaced by python with a text         |
|              |                     | representation of the variable inside the ``format()`` call.    |
|              |                     | example: if ``combatround has the value ``1`` the output of the |
|              |                     | logfile will be: ``Round: 1 *** The testdummy``.                | 
+--------------+---------------------+-----------------------------------------------------------------+



.. [#] Do yourself a favor and really type in the code with your fingers, not just use copy & paste. The point is that you train yourself to type code. While typing, you have a better chance to think about the code and learn keywords, and you also will make some mistakes, like spelling errors. If you make mistakes, the code will not start. That is a good thing, because it allows you learn from your mistakes and avoid them in the future. 
   A well trained monkey may use copy and paste, but he will not learn about coding. Neither will you. 
