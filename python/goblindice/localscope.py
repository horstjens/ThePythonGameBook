# define variable
hitpoints = 55


# define function
def drink_magic_potion():
    """manipulate hitpoints directly"""
    localhitpoints = hitpoints * 2
    return localhitpoints
# call the function
print("hitpionts before drinking", hitpoints)
hitpoints = drink_magic_potion()
print("hitpoints after drinking", hitpoints)
