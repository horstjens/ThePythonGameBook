Goblin vs. punchbag
===================

about
-----

This page shows how to formulate an idea (combat calculation) as a series of instructions and code it using python3.

.. note:: Please help improving this tutorial!
   
   Do you found a typo or failure ? Do you have ideas to improve this tutorial? Please edit/comment this file directly at https://github.com/horstjens/ThePythonGameBook/blob/master/goblindice001.rst (you need an account at github.com to do so).

idea
----

.. figure:: /python/goblindice/goblindice001.png
   :alt: Flow Chart for goblindice001
   :height: 800px
   :align: right
   

Imagine a young goblin named "Grunty". He dreams of being a fearsome warrior one day. However, at the moment, he is rather unskilled and barely capable of handling a weapon. Grunty goes to the training place fighting against a punchbag or wooden testdummy.

Handling a weapon is no easy task, and Grunty will, despite his best efforts, not always land a blow. Sometimes he will miss.

Independent of the graphical representation (there is none yet), some combat mechanics must be formulated so that the computer can emulate a fight. 


Let us assume that -like a ``pen & paper`` role player- Grunty has a low basic chance of hitting the testdummy while swinging his weapon. We express that as a low integer (whole) like  3. A more skilled warrior would have an higher attack value. A line of python code saying just that would look like:

.. code-block:: python

       grunty_base_attack = 3 
       
The part left of the equal sign is called a ``variable`` (because some time in the future hopefully Gruntys attack value will increase) and the part right from the equal sign is called a value. In this case, an ``integer`` value because we use whole numbers (no decimal point). Decimal numbers (like 0.3) are called ``float`` values. Note that in python, variable names can not include a space (python would think those are two different commands) and therefore an underscore ``_`` is used. It is also possible to use :term:`camelCase` like:  ``gruntyAttack`` instead. By convention, all variable names begin with a lowercase character. 

But not every strike is the same for Grunty. Sometimes he has luck and performs a perfect attack, sometimes not. To reflect this variety, let us add some random values on top his base chance, to reflect the actual luck / skill / performance / difficulty of combat. To calculate the outcome of one single attack in a combat situation, some random value is added to the base attack value. In pen & paper role playing games, the player has usually to throw two dice and add the number of eyes rolled to the base attack value. 

.. code-block:: python

       attack_value = grunty_base_attack + random_integer_value

The resulting attack_value is now hopefully greater than the base attack value. Let it compare to a similar calculated defense value to see if Grunty scored a hit. 

Grunty is fighting against a punchbag or wooden testdummy: an easy-to-hit target. Assign it an extreme low defense value of 1, reflecting instrinct defense abilities like difficult-to-hit geometry and shape.

.. code-block:: python

       base_defense = 1

In actual combat, sometimes even an punchbag can get lucky... not by actual moving, but maybe the sun is behind him, blinding the attacker, maybe the wind and the rain work in his favor. So to calculate actual combat performance, some random value is added on top of the (low) base defense value, but less than for the attacker. It this example rolling only one die is allowed to be added to the base defense.

.. code-block:: python

       defense_value = base_defense + random_integer_value

The combat runs in several combat rounds:
In each combat round, the computer calculates the attack and defense values (using his random generator functions) and compares those two. If the attacking value is greater than the defending value, Grunty managed a hit on the testdummy. If both values are equal, Grunty manages a "glancing blow", a hit that does no damage. If the attack value is greater than the defense value, damage is calculated as a random number between 0 and 10. With dice, this could be calculated by rolling 2 dice and subtracting 2 from the sum of pips.

.. code-block:: python
       damage = random_integer_value

The damage is then substracted from the "Hitpoints" (also an integer number) of the testdummy, and the whole process is repeated until the testdummy has no hitpoints left.

The fresh, undamaged testdummy must start with an given number of hitpoints, say 200 hiptoints. Also it is interesting to know how many combat rounds Grunty needs to destroy the testdummy, so a combat round counter is needed and set to 0 before the game. 

.. code-block:: python
 
     testudmmy_hitpoints = 200
     combat_round_counter = 0    


Those instructions above are already a program (that is a set of instructions). To simulate Grunty's combat performance only those instructions, some dice and paper and pen to keep track of combat rounds and hitpoints are needed.

To let a computer do this task instead, knowlede of an additional  set of commands and concepts is necessary:

  * :term:`Variables`: numbers that can have different values over time, like the testdummys hitpoints or the round counter

  * :term:`Operators` to compare two variables

  * :term:`Control structures`:

     * a :term:`Conditional` ``if`` statement to decide what to do if the attack value is greater than the defense value

     * a :term:`Loop` to repeat the whole process as long as necessary

  * Some random generator :term:`functions`


Code
====


prerequesites
-------------

  * necessary:
  
    * python3 is installed
    * text editor can save python files ( like `goblindice001.py`)  
    * python3 interpreter can launch saved python file.
    
  * recommended:
  
    * python-friendly IDE like IDLE, Geany etc.
    * ability to read and type (touch typing) using the 10 finger system, instead of copy and paste
    * python shell to lookup commands, like IDLE or Ipython
    * executing python with filename as parameter from the command line ``python3 goblindice001.py``
    
source code
-----------  
   
.. literalinclude:: /python/goblindice/goblindice001.py
   :language: python
   :linenos:


output
------

Some example output::

  *** Round: 22 ***, target has 104 hitpoints
   Oh no! Grunty does not even hit his target 5 < 9
  *** Round: 23 ***, target has 104 hitpoints
  Grunty manages to nearly hit the target, but he makes no damage 9 = 9
  *** Round: 24 ***, target has 104 hitpoints
  Smack! Grunty hits his target with a most skilled attack: 6 > 4
  ...and inflicts 2 damage!
  *** Round: 25 ***, target has 102 hitpoints
  Oh no! Grunty does not even hit his target 6 < 9



code discussion
---------------

Some elements in this code may need explaining:


=========== ============================== =========================================================================================================================================================================================================================================================================================================================================================
line number term                           explanation
=========== ============================== =========================================================================================================================================================================================================================================================================================================================================================
 1 - 13     :term:`docstring`              Some multi-line text :term:`string` insinde triple-quotes ``"""``. If a docstring is the first statement in a file it is automatically stored in the global variable ``__doc__``. Docstrings are interpreted by python as something interested for humans only, like a :term:`comment`. Docstrings are not necessary, but nice to have.
14          ``import random``              To make use of any :term:`functon` in python's random module, it is necessary to import this module first. Later in this code functions of the random module will use the prefix ``random.``.
16          ``comment``                    Everything behind a ``#`` sign in python is a comment. Comments are useful for human eyes only and always ignored by Python.
17          ``assign``, ``inline comment`` The value of 3 is assigned to the variable ``grunty_attack``. (read it from right to left).  Note that the part right from the ``#`` sign is also a comment.
26          ``loop``, ``expresssion``      The ``while`` ``keyword`` indicates, together with the colon at the end of this line, the beginning of an ``indented code block``. This code block is repeated as long as the ``expression``right from ``while``remains ``True``.
27          ``increment``                  The value of the the ``variable`` ``combatround`` is incremented by 1. Because this is made even before some combat values are calculated, ``combatround`` was set to 0 before the while loop.
28          ``strings and numbers``        Another textstring is appended to the textstring variable ``logfile``. The starting new line sign (``\n``) is a so called ``escaped character``. Because ``combatround`` is of type integer, it can *not* be appended to the textstring ``logfile``. Therefore, ''combatround'' must first be converted into a string using the ``str()`` function.
29          ``format mini language``       Using Format String Syntax instead of the ``str`` function, the curly brackets are replaced by python with the expression inside the round brackets of ``.format()``. See https://docs.python.org/2/library/string.html
30          ``random.randint()``           The ``random.randint()`` function generates a (nearly) random integer between (including) the first (lower) and the second (higher) number in the round brackets. Writing instead random.randint(2,12)`` would be similar, but not the same. See page :ref: goblindice003 for more on this topic.
32          ``conditional``, ``if``        Like the ``while`` keyword, the ``if`` keyword need an expression and a colon and is followed by an ``idented code block``. This code block will only be executed if the  ``expression`` is ``True``. Note that it is allowed to write an inline-comment after the colon with the ``#`` sign. For python, the comment is ignored and the line ends with the colon.
33 - 34     ``strings``                    Note that the string in line 33 ends with an space and the string in line 34 does not begin with a new line. In fact, line 33 and line 34 can be written in one (very long) line. In this case, two seperate lines were written for layout reasons, to make no code line longer than 72 characters. See http://legacy.python.org/dev/peps/pep-0008/
34          ``format mini language``       The first pair of curly brackets get replaced by the first value inside ``.format()``, the second pair of curly brackets get replaced by the second value inside ``.format()`` and so on.
35          ``random.randint())``          Here, ``random.randint(2,12) could have been used instead, and would have resulted similary, but not exactly the same distribution of random values as this formula. See :ref: goblindice003 for more details.                          
36          ``decrement``                  Like the increment, this line could have been written as: ``testdummy_hitpoints -= testdummy_hitpoints - damage``. But why type more than necessary?
=========== ============================== =========================================================================================================================================================================================================================================================================================================================================================

pause

=========== ============================== ================================================================================================================================================================================================================================================================================================================================================================
line number term                           explanation
=========== ============================== ================================================================================================================================================================================================================================================================================================================================================================
38          ``elif``                       Each ``if`` code block can have many (including none) ``elif`` code blocks. Like the ``if`` keyword, the ``indented code block`` after elif will only be executed if the ``expression`` was False for all previous ``elif`` expressions as well as for the initial ``if`` and only if the current expression (right of ``elif``) is ``True``. 
38          ``equal test``                 Please note that the `==` operator is used to *test for equality*. The `=` operator assigns values. 
40          ``format mini language``       A special trick using ``.format()``: If the same variable is needed at several places inside a string, like in this case, it is possible to use the position number of the variable inside the curly bracket. Python always start counting with 0, so the first variable in the round brackets is referred as ``{0}``, the second variable as ``{1}`` and so on.
41          ``else``                       If the ``if`` and all ``elif`` expressions are ``False``, the ``idented code block`` behind the ``else:`` keyword is executed. The ``else:`` keyword itself is optional and need no expression behind it. 
44          ``indentation``                This line is *outside* the ``while block`` ! Take a close look at the previous line with the same indentation: It's line 26. That means that line 44 will only be  executed if the expression in line 26 becomes ``False``
46          ``empty line``                 There is no specific reason to let this line empty: it’s just to have a pretty layout of code. Python ignores empty lines.
47          ``print()``                    The ``print()`` keyword can output any variable to the screen. Note that since python version 3, ``print`` requires round brackets.
=========== ============================== ================================================================================================================================================================================================================================================================================================================================================================

next page:  functions! :ref: goblindice002 
