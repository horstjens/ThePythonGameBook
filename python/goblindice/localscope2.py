# define variable
hitpoints = 55


# define function
def drink_magic_potion():
    """try to direct manipulating hitpoints"""
    hitpoints = hitpoints * 2
    return hitpoints
# call the function
print("hitpionts before drinking", hitpoints)
hitpoints = drink_magic_potion()
print("hitpoints after drinking", hitpoints)
