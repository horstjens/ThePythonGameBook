# useful tools and functions

def colornames(max_lenght_of_name = 6):
    """
    return a list of short colornames without numbers in the name
    requires that pygame is initialized
    requires that pygame.colordict is imported
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


def write(
        background,
        text,
        x=50,
        y=150,
        color=(0, 0, 0),
        font= None,
        origin="topleft",
):
    """blit text on a given pygame surface and returns the width and height of the text in pixel
    requires that pygame is initialized

    :param background:  pygame surface
    :param text:  text to blit
    :param int x: x-position of text
    :param int y: y-position of text
    :param color: tuple (red, green, blue)
    :param font: pygame font object
    :param origin: anchor of (x,y). Must be on of those: "center", "topleft", "topcenter", "topright", "centerleft", "centerright",
                                "bottomleft", "bottomcenter", "bottomright"
    :return: width, height in pixel
    """
    #if font_size is None:
    #    font_size = 24
    #font = pygame.font.SysFont(font_name, font_size, bold)
    if font is None:
        font=pygame.font.SysFont("mono", 24, True),
    width, height = font.size(text)
    surface = font.render(text, True, color)

    if origin == "center" or origin == "centercenter":
        background.blit(surface, (x - width // 2, y - height // 2))
    elif origin == "topleft":
        background.blit(surface, (x, y))
    elif origin == "topcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "topright":
        background.blit(surface, (x - width, y))
    elif origin == "centerleft":
        background.blit(surface, (x, y - height // 2))
    elif origin == "centerright":
        background.blit(surface, (x - width, y - height // 2))
    elif origin == "bottomleft":
        background.blit(surface, (x, y - height))
    elif origin == "bottomcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "bottomright":
        background.blit(surface, (x - width, y - height))
    return width, height
