# useful tools and functions

def colornames(max_lenght_of_name = 6):
    """
    return a list of short colornames without numbers in the name
    requires that pygame is initialized
    """
    colornames = []
    for colorname in pygame.colordict.THECOLORS:
        if len(colorname) > max_lenght_of_name:
            continue
        # test if any number 0-9 is in the colorname
        result = [str(x) in colorname for x in range(10)]
        if any(result):
            continue
        colornames.append(colorname)
    return colornames