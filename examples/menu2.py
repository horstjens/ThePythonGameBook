#generic menu for pygame

import pygame
import pygame.colordict
from typing import NamedTuple, Sequence, Optional, Any
import random



class Item(NamedTuple):
    name: str = "dummy item"
    choices: Sequence = []
    default_index: int = 0
    rect: Any = None

class Menu(NamedTuple):
    name: str = "root"
    items: Sequence = []
    rect: Any = None


class Viewer:
    width: int
    height: int
    screenrect: pygame.Rect
    screen = None
    background = None
    font = None
    menu = None

    def __init__(self, width=800, height=600):
        # ---- pygame init
        pygame.init()
        Viewer.width = width
        Viewer.height = height
        self.setup_screen(width, height)
        #self.run()

    def setup_screen(self, width, height, backgroundcolor=(255,255,255)):
        Viewer.screenrect = pygame.Rect(0, 0, width, height)
        Viewer.screen = pygame.display.set_mode(
            (width, height), pygame.DOUBLEBUF
        )
        Viewer.background = pygame.Surface((width, height))
        Viewer.background.fill(backgroundcolor)


class PygameMenu:

    def __init__(self,
                 rootmenu,
                 cursortext="-->",
                 startIndex = 0,
                 cycle_up_down=False,
                 menuname="root",
                 cursorTextList = ["→  ", "-→ ", "--→"],
                 cursorAnimTime = 550,
                 cursorSprite=None,
                 menutime=0,
                 textcolor=(0,0,225),
                 background=None,
                 screen=None,
                 fontsize=24,
                 fontname="mono",
                 yspacing=10,
                 helptextheight = 100,
                 helptextcolor1 = (0,0,0),
                 helptextcolor2=(0, 200, 200),
                 helptextfontsize = 15,

                 ) :
        """menudict
        ---- generic parameters ----
        :rtype: object
        :param rootmenu:  includes all submenus, choices and default_values for choices
        :param cursortext:
        :param startIndex:
        :param cycle_up_down:
        :param menuname:
        --- pygame parameters ---
        :param cursorSprite:
        :param cursorTextList:
        :param cursorAnimTime:
        :param menutime:
        :param textcolor:
        :param background:
        :param screen:
        :param fontsize:
        :param fontname:
        :param yspacing:
        :param helptextheight:
        :param helptextcolor1:
        :param helptextcolor2:
        :param helptextfontsize:
        """
        # --- testing ---
        #if type(menudict) != dict:
        #    raise ValueError("menudict is not a dict")
        #if type(choicesdict) != dict:
        #    raise ValueError("choicedict is not a dict")
        #vtypes = [type(v) is list for v in menudict.values()]
        #if False in vtypes:
        #    raise ValueError("each value in menudict must be a list")
        #vtypes = [type(v) is list for v in choicesdict.values()]
        #if False in vtypes:
        #    raise ValueError("each value in choicedict must be a list")
        #if "root" not in menudict:
        #    raise ValueError("menudict must have an root entry")
        #if menuname not in menudict:
        #    raise ValueError("menuname must be a key of valuedict (usually: 'root')")
        # TODO search for orhpaned menu keys
        # --- add quit to main menu if necessary ---
        #if "quit" not in rootmenu.items:
        #    rootmenu.items.append("quit")
        # --- add "back" to each submenu if necessary ----
        #for k in rootmenu.items:
        #
        #            menudict[k].append("back")

        # --- start

        self.rootmenu = rootmenu
        self.cursortext = cursortext
        self.cycle_up_down = cycle_up_down
        self.i = startIndex
        self.menu = rootmenu
        self.history = [] # traceback
        #---- pygame variables
        self.cursorSprite = cursorSprite
        self.cursorTextList = cursorTextList
        self.cursorAnimTime = cursorAnimTime
        self.menutime = menutime # age of menu in seconds
        self.background = Viewer.background # pygame surface to blit
        self.screen = Viewer.screen
        self.screenrect = self.screen.get_rect()
        self.textcolor = textcolor # black
        self.clock = pygame.time.Clock()
        self.fps = 400
        self.fontsize = fontsize
        self.fontname = fontname
        #self.font = pygame.font.SysFont(name=fontname, size=fontsize, bold=True, italic=False)
        self.yspacing = yspacing # pixel vertically between text lines
        self.helptextheight = helptextheight # pixel distance to top border of window, to display helptext
        self.helptextcolor1 = helptextcolor1
        self.helptextcolor2 = helptextcolor2
        self.helptextfontsize = helptextfontsize
        #self.helptextfont = pygame.font.SysFont(name=fontname, size=helptextfontsize, bold=True)
        # ------
        self.anim = 0
        #self.choicesdict = choicesdict
        #self.create_defaults()

    @property
    def font(self):
        """read only attribute, influened by fontname and fontsize"""
        return pygame.font.SysFont(name=self.fontname, size=self.fontsize, bold=True, italic= False)

    @property
    def helptextfont(self):
        """read only attribute, influened by fontname and helptextfontsize"""
        return pygame.font.SysFont(name=self.fontname, size=self.helptextfontsize, bold=True, italic=False)

    def create_defaults(self):
        """call this after you manually changed the choicesdict"""
        self.indexdict = {k: 0 for k in self.choicesdict.keys()}  # index for each cuttently selected choice
        # write meaningful default values for menusettings (if it exist)
        #if "menusettings" in self.menudict:



    def calculate_all_dimensions(self):
        self.screenrect = self.screen.get_rect()
        maxwidth = 0
        maxheight = 0
        maxentries = 0
        for k in self.menudict:
            width, height = self.calculate_dimensions(self.menudict[k])
            entries = len(self.menudict[k])
            maxwidth = max(maxwidth, width)
            maxheight = max(maxheight, height)
            maxentries = max(maxentries, entries)
        return maxwidth, maxheight, maxentries

    def calculate_dimensions(self, menupointlist):
        maxwidth = 0
        totalheight = 0
        for entry in menupointlist:
            #print("entry", entry)
            width, height = self.font.size(entry)
            maxwidth = max(maxwidth, width)
            totalheight += height
        return maxwidth, totalheight + self.yspacing * (len(menupointlist) - 1)

    def blit_helptext(self, selection):
        """blit the helptext on top of the screen, using different colors"""
        t1 = "current menu: "
        t2 = f"{self.menuname}"
        t3 = " current selection: "
        t4 = f"{selection}"
        t5 = "Navigate: "
        t6 = "[\u2191]/[\u2193]/[Backspace]"
        t7 = " Accept: "
        t8 = "[Enter]"
        t9 = " Change: "
        t10= "[Space]/[\u2190]/[\u2192]"

        pygame.display.set_caption(t1)
        # ----- write helptext on top ----
        x = 10
        y = 0
        xh, yh = write(self.screen, t1, x, y, self.helptextcolor1, self.helptextfont, origin="topleft")
        x += xh
        xh, yh = write(self.screen, t2, x, y, self.helptextcolor2, self.helptextfont, origin="topleft")
        x += xh
        xh, yh = write(self.screen, t3, x, y, self.helptextcolor1, self.helptextfont, origin="topleft")
        x += xh
        xh, yh = write(self.screen, t4, x, y, self.helptextcolor2, self.helptextfont, origin="topleft")
        y += yh  # new line
        x = 10
        xh, yh = write(self.screen, t5, x, y, self.helptextcolor1, self.helptextfont, origin="topleft")
        x += xh
        xh, yh = write(self.screen, t6, x, y, self.helptextcolor2, self.helptextfont, origin="topleft")
        x += xh
        xh, yh = write(self.screen, t7, x, y, self.helptextcolor1, self.helptextfont, origin="topleft")
        x += xh
        xh, yh = write(self.screen, t8, x, y, self.helptextcolor2, self.helptextfont, origin="topleft")
        x += xh
        # ---- only if current menupoint has choices ----
        if selection in self.choicesdict:
            # --- write helptext to change choices ---
            xh, yh = write(self.screen, t9, x, y, self.helptextcolor1, self.helptextfont, origin="topleft")
            x += xh
            xh, yh = write(self.screen, t10, x, y, self.helptextcolor2, self.helptextfont, origin="topleft")
            #x += xh
            y += yh
            x = 0

            t11 = " values: {}".format(" ".join(self.choicesdict[selection]))
            xh, yh = write(self.screen, t11, x, y, self.helptextcolor1, self.helptextfont, origin="topleft")


        x = 10
        y += yh
        # ready for next line

    def cursor_up(self, menupoints):
        # move cursor up to previous menupoint
        self.i -= 1
        if self.i < 0:
            if self.cycle_up_down:
                self.i = len(menupoints) - 1
            else:
                self.i = 0

    def cursor_down(self, menupoints):
        # move cursor down to next menupoint
        self.i += 1
        if self.i >= len(menupoints):
            if self.cycle_up_down:
                self.i = 0
            else:
                self.i = len(menupoints) - 1

    def run(self):
        # calcualte best position for menu (to not recalculate each sub-menu)
        #width, height, entries = self.calculate_all_dimensions()
        #if width > self.screenrect.width:
        #    print("warning: fontsize too big or menuentries too long or screen width too small:" )
        #if height > self.screenrect.height - self.helptextheight:
        #    print("warning: fontsize / helptext too big or too many menuentries or screen height too small" )
        #dy = height / entries

        #    srcolling = True
        # else:
        #    scrolling = False
        # x =  s
        # center menu on screen, calculate topleft position for menu
        #cx = self.screenrect.width // 2 - width // 2
        #cy = self.helptextheight + (self.screenrect.height-self.helptextheight) // 2 - height // 2
        cx = 100
        cy = 100
        dy = 25
        running = True
        while running:
            # clock
            milliseconds = self.clock.tick(self.fps)  #
            seconds = milliseconds / 1000
            self.menutime += seconds

            #print("self menu:", self.menu)
            #print("items:", self.menu.items)
            #print("loop:")
            #for x, i in enumerate(self.menu.items):
            #    print(x,i)
            #    print(i.name)
            #print("end of loop")
            #print("strings:",[i for i in self.menu.items])
            # ---------- clear all --------------
            self.screen.blit(self.background, (0, 0))
            # pygame.display.set_icon(self.icon)
            menupoints = [p for p in self.menu.items]
            selection = self.menu.items[self.i] # self.menudict[self.menuname][self.i]
            #self.blit_helptext(selection)
            #print("selection", selection.name)

            # ------- cursor animation --------
            # bounce coursor from left to right:
            maxcursordistance = 20
            ## first value is animation time (lower is slower), second value is travel distance of Curosr
            #cursordistance = (self.menutime * 20) % 50
            anim = int((self.menutime * 1.5 ) % len(self.cursorTextList))
            cursortext = self.cursorTextList[anim]
            cursordistance = 0
            # cursor color:
            #r,g,b = self.textcolor
            #r += random.randint(-140,140)
            #g += random.randint(-140,140)
            #b += random.randint(-140,140)
            #r = max(0, min(255,r))
            #g = max(0, min(255,g))
            #b = max(0, min(255,b))
            #cursorcolor = (r,g,b)
            cursorcolor = self.textcolor

            # ----------current menupoints and selection ------
            #menupoints = self.menudict[self.menuname]
            #selection = menupoints[self.i]
            menupoints = [p.name for p in self.menu.items]
            selection = self.menu.items[self.i].name  # self.menudict[self.menuname][self.i]
            # ----------- writing on screen ----------

            # ------- write cursor --------
            for i, entry in enumerate(menupoints):
                if i == self.i:
                    write(self.screen, cursortext, cx - maxcursordistance + cursordistance, cy + dy * i ,
                               cursorcolor, self.font, origin="topright")
                # ----------- write entry ---
                write(self.screen, entry, cx, cy + dy * i, self.textcolor, self.font, origin="topleft")
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # ------- pressed and released key ------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            return "quit"
                    if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        self.cursor_up(menupoints)

                        #print("i", self.i)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        self.cursor_down(menupoints)

                    if event.key == pygame.K_BACKSPACE:
                        if self.menuname != "root":
                            self.menuname = self.history.pop()
                            self.i = 0
                    if event.key in (pygame.K_SPACE, pygame.K_RIGHT, pygame.K_PLUS, pygame.K_KP_PLUS):
                        if selection in self.choicesdict:
                            # change value +
                            self.indexdict[selection] += 1
                            if self.indexdict[selection] >= len(self.choicesdict[selection]):
                                self.indexdict[selection] = 0

                    if event.key in (pygame.K_LEFT, pygame.K_MINUS, pygame.K_KP_MINUS):
                        if selection in self.choicesdict:
                            # change value +
                            self.indexdict[selection] -= 1
                            if self.indexdict[selection] < 0:
                                self.indexdict[selection] =  len(self.choicesdict[selection]) -1

                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        #selection = menupoints[self.i]
                        #print("selected:", selection)
                        if selection in self.menudict.keys():
                            self.history.append(self.menuname)
                            self.menuname = selection
                            self.i = 0
                        elif selection == "back":
                            self.menuname = self.history.pop()  # remove last item
                            self.i = 0
                        #elif selection == "quit":
                        elif selection in self.choicesdict:
                            # ---- return value of entry + choicesdict/chosendict value -----
                            return selection + " " + self.choicesdict[selection][self.indexdict[selection]]
                        else:
                            return selection
            # ---------- end of event handler -----
            # --- special sprites ---
            # self.menusprites.update(seconds)
            # self.menusprites.draw(self.screen)
            #-------- update screen -------------
            pygame.display.flip()


def colornames(max_lenght_of_name = 6):
    """return a list of short colornames without numbers in the name"""
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
    """blit text on a given pygame surface (given as 'background')
    the origin is the alignment of the text surface
    origin can be 'center', 'centercenter', 'topleft', 'topcenter', 'topright', 'centerleft', 'centerright',
    'bottomleft', 'bottomcenter', 'bottomright'
    -> width, height
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


def main():

    Viewer(800, 600) # makes pygame.init
    # list of some colors
    colors = colornames()
    # list of possible video resolutions without double entries
    reslist = list(set(pygame.display.list_modes(flags=pygame.FULLSCREEN)))
    reslist.sort()
    # reslist is in horrible format: [(x1,y1),(x2,y2)...] with many double entries
    # create a set (without double entries) of strings and convert into a list


    audiomenu = Menu(name="audio", items=[
        Item("sound effects", choices=["on", "off"], default_index=0),
        Item("music", choices=["on", "off"], default_index=0),
    ])
    videomenu = Menu(name="video", items=[
        Item("fullscreen", choices=["on", "off"], default_index=0),
        Item("screen resolution", choices=reslist, default_index=4)
    ])
    settingsmenu = Menu(name="settings", items=[
        audiomenu,
        videomenu,
        Item("fontsize_small", choices=range(8,50,2), default_index=3),
        Item("fontsize_big", choices=range(8,50,2), default_index=8),
        Item("color_background", choices=colors, default_index = -2),
        Item("color_small_font1", choices=colors, default_index = 3),
        Item("color_small_font2", choices=colors, default_index = 7),
        Item("color_big_font", choices=colors, default_index = 4),
    ])
    rootmenu = Menu(name="root", items=[Item("play"), Item("credits"), settingsmenu, Item("quit")])


    Viewer.menu1 = PygameMenu(rootmenu )


    # ---- main loop ----
    running = True
    while running:
        # get a command from the menu. All code must be handled here inside your game loop.
        # the menu save is persistant as
        command = Viewer.menu1.run()
        print("menu command is:", command)
        print("---all choice values:---")
        #for k in m1.choicesdict:
        #    print(k, "is set to", m1.choicesdict[k][m1.indexdict[k]])

        # ---- excecute commands ----
        if command == "play":
            ## start game code here
            print("playing a game...")
        # execute a bunch of commands if one of the menusettings points was accepted with ENTER
        elif Viewer.m1.menuname == "settings":
            # it was one of the subcommands of "
            m1.background.fill(m1.choicesdict["backgroundcolor:"][m1.indexdict["backgroundcolor:"]])
            m1.textcolor = m1.choicesdict["textcolor1:"][m1.indexdict["textcolor1:"]]
            m1.helptextcolor1 = m1.choicesdict["textcolor2:"][m1.indexdict["textcolor2:"]]
            m1.helptextcolor2 = m1.choicesdict["textcolor3:"][m1.indexdict["textcolor3:"]]
            m1.fontsize = int(m1.choicesdict["fontsize1:"][m1.indexdict["fontsize1:"]])
            m1.helptextfontsize = int(m1.choicesdict["fontsize2:"][m1.indexdict["fontsize2:"]])

        elif command == "screen resolution":
            pass
            # change screen resolution
            #if command in res:
            # change the screen resolution
            #x, y = int(command.split("x")[0]), int(command.split("x")[1])
            #pygame.display.set_mode((x, y))
            #self.setup_screen(x, y)
            ## m1.screen = self.screen
            #m1.background = self.background

        elif command == "quit":
            running = False
            #break
        # -----
    # -------------------------
    print("end of mainloop")
    pygame.quit()






if __name__ == "__main__":
    main()