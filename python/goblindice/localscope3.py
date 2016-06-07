# define variable
hitpoints = 55


# define function
def drink_magic_potion():
    """manipulating hitpoints by making hitpoints global"""
    global hitpoints
    hitpoints = hitpoints * 2

# call the function
print("hitpionts before drinking", hitpoints)
drink_magic_potion()
print("hitpoints after drinking", hitpoints)
