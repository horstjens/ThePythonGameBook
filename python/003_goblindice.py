#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt


import random 

# this example uses classes to store the propertys of the goblins,
# introduces the __main__ function and handles user-input
# with the raw_input() function





class Goblin(object):
    """goblin with name, and other individual values"""
    def __init__(self):
        """standard out-of-the-cave goblin, alter values after creation"""
        self.name = "Dummy"
        self.hitpoints = 50
        self.wins = 0
        self.min_damage = 1
        self.max_damage = 6
        self.min_speed = 1
        self.max_speed = 7  
        
    def report(self, description=True):
        """print out all attributes
        with or without description (column header)
        right-align all for 20 chars."""
        if description:
            msg = "{0:>15} : {1:>15} \n".format("class",self.__class__.__name__ )
        else:
            msg = "{0:>15} \n".format(self.__class__.__name__)
        for x in self.__dict__.keys():
            if description:
                msg+= "{0:>15} : {1:>15} \n".format(x, self.__dict__[x])
            else:
                msg+= "{0:>15} \n".format(self.__dict__[x])
        return msg
    
    def modify(self):
        """allow the user to modify all values of this Goblin"""
        newName = False
        print self.report()
        for x in  self.__dict__.keys():
            new = raw_input("{0}: {1} (Enter=accept)>".format(x, self.__dict__[x]))
            if new != "":
                if x == "name":            # accept everything as name
                    self.__dict__[x] = new
                    print "name changed into {0}".format(new)
                    newName = True         # modify menu 
                else:                      # accept only numbers
                    if new.isdigit():
                        self.__dict__[x] = new
                        print "new value accepted"
                    else:
                        print "new value rejected because not a number"
        print "--- i print now the new values"
        print self.report()  
        if newName:
            return self.name
        else:
            return None


intro = """
---- Introduction -------
Two goblins, Grunty and Stinky, play the traditional game of 
Goblin Dice Duel

The rules a very simple. Each goblin throws a die and is 
allowed to hit the other goblin on the head with a club as often
as the number of eyes on his throwed die. This is called damage.

As each goblins has an individual number of hitpoints (how much damage
he can suffer) the last gobling standing is the winner.

Note that dice in the goblin cave are made out of bones and are not 
six-sided as the dice you may know. 
Each dice has a minimal value (number of eyes) and a maximal value. 

To find out if weak and smart goblins beat dumb and strong goblins more 
often than not, it is necessary to observe thousands of games
"""

stinky = Goblin() # create stinky with default values
stinky.name = "Stinky" # adapt some values of Stinky the Goblin
stinky.min_damage = 3
stinky.max_damage = 4
stinky.min_speed = 4
stinky.max_speed = 9

grunty = Goblin() # create Grunty with default values
grunty.name = "Grunty" # adapt some values of Grunty
grunty.max_damage = 7
grunty.max_speed = 7
grunty.hitpoints = 60


menuitems = [] # empty list
menuitems.append("read introduction")           # 0
menuitems.append("view and compare goblins")    # 1
menuitems.append("modify Stinky")               # 2
menuitems.append("modify Grunty")               # 3
menuitems.append("make many fights")            # 4
menuitems.append("quit")                        # 5

def compare(leftGoblin, rightGoblin):
    
    # make a list of lines with description and values:
    leftLines = leftGoblin.report(True).splitlines() 
    # make a list of lines with only values, no description
    rightLines = rightGoblin.report(False).splitlines() 
    msg = ""
    for lineNumber in range(len(leftLines)):
        msg += "{0} vs. {1} \n ".format(leftLines[lineNumber], rightLines[lineNumber] )
    return msg



def menu(menuitems):
    while True: # endless menu loop
        for item in menuitems:
            print menuitems.index(item), item
        while True: # endless user input loop
            wish = raw_input("your choice (and Enter):")  
            if wish.isdigit():
                if int(wish) >= 0 and int(wish) < len(menuitems):
                    break # break the endless user input loop
        print "your wish was %i: %s" % (int(wish), menuitems[int(wish)])
         
        if int(wish) == 0: 
            print intro 
        elif int(wish) == 1:  # compare goblins
            msg = compare(stinky, grunty)
            print msg
        elif int(wish) == 2:  # modify Stinky (and menu entry)
            newname = stinky.modify()
            if newname != None:
                menuitems[2] = "modify " + newname     
        elif int(wish) == 3:  # modify Grunty (and menu entry)
            newname = grunty.modify()
            if newname != None:
                menuitems[3] = "modify " + newname
        elif int(wish) == 4:  # fight !
            while True:       #endless user input loop
               amount = raw_input("how many fights (Enter)")
               if amount.isdigit():
                   if int(amount) >0:
                       break  # correct answer
            many_games(stinky, grunty, int(amount)) 
        elif int(wish)==5:     
            break             # break out of the menu loop
         
def firstStrike(leftGoblin, rightGoblin):
    """this recursive function computes the faster of 2 Goblins"""
    leftSpeed = random.randint(leftGoblin.min_speed, leftGoblin.max_speed)
    rightSpeed = random.randint(rightGoblin.min_speed, rightGoblin.max_speed)
    print "both Goblins try to strike each other..."
    if leftSpeed == rightSpeed:
        print "but both are equal fast {0}:{1}".format(leftSpeed, rightSpeed)
        return firstStrike(leftGoblin, rightGoblin) # recursion !
    elif leftSpeed > rightSpeed:
        print "{0} is faster ({1}:{2}) and strikes first !".format(leftGoblin.name, leftSpeed, rightSpeed)
        return leftGoblin
    else:
        print "{0} is faster ({1}:{2}) and strikes first !".format(rightGoblin.name, rightSpeed, leftSpeed)
        return rightGoblin
        
def strike(attacker, defender):
    """the attacker strikes against the defender"""
    damage = random.randint(attacker.min_damage, attacker.max_damage)
    defender.hitpoints -= damage
    print "{0} strikes against {1} and causes {2} damage." \
          "({3} hitpoints left)".format(attacker.name, defender.name,
                                       damage, defender.hitpoints)
                                      
                        

def combat(leftGoblin, rightGoblin):
    """a function that takes 2 goblins (class instances)
       let them fight and returns the winning goblin"""
    

    combatround = 0 # the word "round" is a reserved keyword in python
    print "saving hitpoints..."
    
    original_hp_left = leftGoblin.hitpoints
    original_hp_right = rightGoblin.hitpoints
     
    while leftGoblin.hitpoints > 0 and rightGoblin.hitpoints > 0:
        combatround += 1 # increase the combat round counter
        print " ----- combat round %i -------" % combatround
        # who attacks first ?
        firstStriker = firstStrike(leftGoblin, rightGoblin)
        if firstStriker == leftGoblin:
            # leftGoblin strikes first
            strike(leftGoblin, rightGoblin)
            if rightGoblin.hitpoints <= 0:
                break
            else:
                print "{0} strikes back !".format(rightGoblin.name)
                strike(rightGoblin, leftGoblin)
        elif firstStriker == rightGoblin:
            # rightGoblin strikes first
            strike(rightGoblin, leftGoblin)
            if leftGoblin.hitpoints <= 0:
                break
            else:
                print "{0} strikes back !".format(leftGoblin.name)
                strike(leftGoblin, rightGoblin)
        else:
            print "no first strike ??"
    #----- end of loop ----
    print "=================================="
    if leftGoblin.hitpoints > 0:
        print "{0} is the winner !".format(leftGoblin.name)
        leftGoblin.wins += 1
        print "restoring original hitpoints"
        leftGoblin.hitpoints = original_hp_left
        rightGoblin.hitpoints = original_hp_right
        return leftGoblin 
    else:
        print "{0} is the winner !".format(rightGoblin.name)
        rightGoblin.wins += 1
        print "restoring original hitpoints"
        leftGoblin.hitpoints = original_hp_left
        rightGoblin.hitpoints = original_hp_right
        return rightGoblin
        
def many_games(leftGoblin, rightGoblin, number_of_fights=1000):
    """calls the combat function 1000 times"""
    print "setting wins to zero"
    leftGoblin.wins = 0
    rightGoblin.wins = 0     
    for fight in range(number_of_fights):
        print "fight number %i" % fight
        winner = combat(leftGoblin, rightGoblin)
        
    print "==============================="
    print " * * * end results * * * "
    print "==============================="
    print "{0} wins: {1}  vs. {2} wins: {3}".format(leftGoblin.name,
           leftGoblin.wins, rightGoblin.name, rightGoblin.wins)
    

if __name__ == "__main__":
    menu(menuitems)
               
        
        
    


