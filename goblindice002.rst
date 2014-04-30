goblin vs. goblin
=================

about
-----

This page shows how to make use of a function in a two player combat sim, how to pass parameters to a function and how to get return values from a function. This examples show how to use a function to avoid redundant code.

.. note:: Please help improving this tutorial!
   
   Do you found a typo or failure ? Do you have ideas to improve this tutorial? Please edit/comment this file directly at https://github.com/horstjens/ThePythonGameBook/blob/master/goblindice002.rst (you need an account at github.com to do so).

idea
----

.. figure:: /python/goblindice/goblindice002.png
   :alt: Flow Chart for goblindice001
   :height: 800px
   :align: right
   

Grunty the goblin did well against the testdummy and is now ready to fight his training partner, Stinky the monster. Stinky and Grunty differ somewhat: Stinky can attack faster and better and has more hitpoints than Grunty, but Grunty is better at defending himself:

.. code-block:: python

   grunty_attack = 4   # integer value 
   grunty_defense = 7
   grunty_hitpoints = 100
   stinky_attack = 8
   stinky_defense = 2
   stinky_hitpoints = 130

The combat rules have not not changed since the previous example. However, the code becomes more complicated: Stinky is faster and always strike first at Grunty. If Grunty has still hitpoints left after Stinkys attack, he can strike back. 

Because Grunty can not strike back without hitpoints, it is necessary
to test *inside* the ``while loop``, not only at the beginning, if
Grunty has enough hitpoints left. If he has not, Python should break out of the while loop. This is done with the ``break`` command.

.. code-block:: pyhton

   if grunty_hitpoints < 1:           
        break                        

The same combat machanic (calculating attack value, calculating defense value, calculating damage, subtracting damage from hitpoints) is now neccessary to do twice: once in each while loop for Stinky attacking Grunty, and a second time for Grunty striking back at Stinky. 

Writing the (nearly) same code twice is something a good programmer  avoids: such a redundant code is harder to maintain and more likely to get errors, because an edit in one part of the code is not always copied correctly to the second, nearly identical part of the code. 

A method to avoid duplicate code is to put the relevant code into a ``function``. This function can be ``called`` from different parts of the program and will (mostly) ``return`` some results to the calling program. It is also possible to pass paramters (sometimes called arguments) to the function.

In the flow chart you see the function as a seperate box at the right, and parameters and return values are represented by dotted lines. 

A function is always defined in python using the ``def`` keyword, with a free-to-choose function names and the parameters (if any) inside round brackets. The function definition ends with a colon ``:``. Code inside the function is indented, like always in python after a colon. If the function gives something back to the caller, it uses the ``return`` keyword. It is a good idea to give a function a docstring (in triple quotes) describing it's purpose:

.. code-block:: python

   def function_name(parameter1, paramter2):
       """docstring in triple quotes"""
       internal instructions inside the function
       return value1, value2
       
As can be seen here it is possible to pass several parameters to a function, and get several values from a funtion, by using a comma to seperate them. Note that paramters as well as ``return`` values are optional.

.. code-block:: python

   def naked_function():
       """has neither parameters, nor return values"""
       print("i do nothing")
       # the function ends here, without return keyword !

Scope of variables inside funcions
----------------------------------

Variables defined inside functions have an so called ``local scope``: Those variables exist only inside the function and can not be manipulated or read outside the function. If a function wants to pass a return value to the calling program, two steps are necessary:

  # The function caller must assign a variable to the result of the function or call the function inside another function
  
  # The function must return it's local value using the ``return`` keyword.
  
.. code-block:: python
   # define the function
   def ultimate_answer():
       """returns always 42"""
       return 42
       
    # calling the function
    # using a variable:
    
    answer = ultimate_answer()
    print(answer) # print 42
    
    # calling the function inside the print function without a variable:
    print(ultimate_answer()) # also print 42
    
There are two ways to cross the boundarys of local scope:

If a variable is defined in the program before the function is called,
the function can read *but not manipulate* this variable.
    
correct:

.. code-block:: python

    # define variable
    hitpoints = 55
    # define function
    def drink_magic_potion():
       """create local variable before manipulating"""
       localhitpoints = hitpoints * 2
       return localhitpoints
    # call the function
    print("hitpionts before drinking",hitpoints)
    hitpoints = drink_magic_potion()
    print("hitpoints after drinking", hitpoints)
   
output:

.. code-block:: python

   hitpionts before drinking 55
   hitpoints after drinking 110

incorrect:

.. code-block:: python

    # define variable
    hitpoints = 55
    # define function
    def drink_magic_potion():
       """try manipulating hitpoints without local variable"""
       hitpoints = hitpoints * 2
       return hitpoints
    # call the function
    print("hitpionts before drinking",hitpoints)
    hitpoints = drink_magic_potion()
    print("hitpoints after drinking", hitpoints)
   
output:
    
.. code-block:: python

    hitpionts before drinking 55
    Traceback (most recent call last):
    File "localscope2.py", line 10, in <module>
    hitpoints = drink_magic_potion()
    File "localscope2.py", line 6, in drink_magic_potion
    hitpoints = hitpoints * 2
    UnboundLocalError: local variable 'hitpoints' referenced before assignment

Finally, there is the option of ignoring local scope at all by declaring a variable as having global scope with the ``global`` keyword. Note that in this example the function needs neither paramters nor return values. 

.. code-block:: python
    
    # define variable
    hitpoints = 55
    # define function
    def drink_magic_potion():
       """manipulating hitpoints by making hitpoints global"""
       global hitpoints
       hitpoints = hitpoints * 2
    
    # call the function
    print("hitpionts before drinking",hitpoints)
    drink_magic_potion() 
    print("hitpoints after drinking", hitpoints)

output:

.. code-block:: python

    hitpionts before drinking 55
    hitpoints after drinking 110

In all ThePythonGameBook tutorials, ``global`` is avoided whenever possible.


Code
====

This code is more complex than in the previous example. Note that before printing the logfile, it is necessary to check who has won using an ``if else`` statement. 

.. note:: Warning

    If the defense values for both players are much higher than the attack values, it can happen that the program caluculate for a long time ("hangs") showing only a black screen. You can avoid this by ``break``ing out of the while loop if the ``combatround`` value becomes too high.

prerequesites
-------------

  * necessary:
  
    * python3 is installed
    
  * recommended:
  
    * python-friendly IDE like IDLE, Geany etc.
    * python shell to lookup commands, like idle or ipython
    
source code
-----------  
   
.. literalinclude:: /python/goblindice/goblindice002.py
   :language: python
   :linenos:


output
------

Some example output::

    *** Round: 31 *** Grunty has 2 hitpoints, Stinky has 10 hitpoints
     Oh no! Stinky does not even hit Grunty 13 < 16
     Oh no! Grunty does not even hit Stinky 10 < 13
    *** Round: 32 *** Grunty has 2 hitpoints, Stinky has 10 hitpoints
    Stinky manages to nearly to hit Grunty, but he makes no damage 14 = 14
     Smack! Grunty hits Stinky with a most skilled attack: 10 > 9
     ...and inflicts 8 damage!
    *** Round: 33 *** Grunty has 2 hitpoints, Stinky has 2 hitpoints
     Smack! Stinky hits Grunty with a most skilled attack: 20 > 11
     ...and inflicts 5 damage!
    - - - - - - - - - - - - - - - - - - - - 
    Victory for Stinky after 33 rounds




code discussion
---------------


=========== ============================== ========================================================================================================================================================================================================================================================================================================================
line number term                           explanation
=========== ============================== ========================================================================================================================================================================================================================================================================================================================
 1 - 13     :term:`docstring`              Docstring insinde triple-quotes ``"""``.
14          ``import random``              importing the random module to make the later use of the ``random.randint()`` function possible.
17 - 28     assign start values            Those start values are no global variables, but because they are defined before a function is called those start values can be *read* (but *not* manipulated) inside a function.
32          :term:`def`                    Define a functin named ``strike``. This functions need 4 arguments (comma seperated) or it will not work.
33 - 52     function body                  This `indented code block` belongs to the function and all variables declared inside a function have *local scope*. The code inside the function is basically identical with :ref:`goblindice001`
39 - 40     multi-line line                A line of instructions for Python can stretch over multiple physical lines as long as the python interpreter understand that the lines belong together. In this case, the opening round bracket at the end of line 39 and the closing bracket at the end of line 40 indicate that this is for Python one very long line.
52          return values                  The strike function returns 2 comma seperated values.
54          main loop                      From within this loop, the `strike` function will be called twice. Because Grunty's hitpoints are checked in line 64, it is only not really necessary to control Stinkys *and* Gruntys hitpoints at the beginning of this `while loop`. But in later versions, when introducing attack speed,  it may become necessary.
60 - 61     functoin call                  Because the `strike` function returns two values, two variables are needed to be assigned with those return values. Note that because the opening round bracket at the end of line 60, line 60 and line 61 are for python one single line.
64          loop control                   Grunty's hitpoints were last checked at the beginning of the while loop. Meanwhile, if Stinky's strike was sucessfull, Grunty has possible zero or less hitpoints and can not strike back. This is checked here, in the middle of the `while loop`.
65          :term:`break`                  This ``break`` command will break out of the current `indented code block` and the Pyhton program will resume at the next line with the same indentation (that is, no indentation) as the ``while`` command of line 54: line 71
72 - 75     `if else`                      In contrast to :ref:`goblindice001`, it is now not clear who the winner is so a new `if else` construct is necessary.
=========== ============================== ========================================================================================================================================================================================================================================================================================================================

next page: recursion ! :ref: goblindice003
