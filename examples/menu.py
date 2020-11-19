#generic menu for pygame, with optional (no-pygame) text  mode

import pygame
import random



class Menu:

    def __init__(self, 
                 menudict,
                 choicedict = {},
                 cursortext="-->",  
                 startIndex = 0,
                 cycle_up_down=False,
                 menuname="root",
                 cursorTextList = ["=-->", "-=->", "--=>"],
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
                 helptextcolor = (0,0,0),
                 helptextfontsize = 15,

                 ) -> str:
        """menudict is a dict of menupoints, with menupointname as key and list of menupoints as values
        the root key must be called 'root'. If not present, a "quit" entry will autmatically added to the root values.
        Each submenu must have its own key with values. If not present, a "back" entry will automatically added to
        each submenu values.
        If a selected value is the same as a key of a submenu, the menu will jump to the submenu.
        choicedict is a dict with the menupoint as key and a list of possible values to change/toggle. The current
        choice will appended as text to the menupoint
        The default value will in a choicedict will always be the first value of the list of possible values

        example:
        menudict = {
            "root": ["play", "options", "quit"]                       # root menu
            "options": ["graphic", "turn sound:", "music volume:"]      # sub menu
            "graphic": ["resolution 800x600", "resolution 1024x800"]  # sub-sub menu
        valuedict = {"turn sound:": ["on", "off"],
                     "music volume:": ["off", "silent", "medium", "loud"]}
        }
        ---- generic parameters ----
        :rtype: object
        :param menudict:
        :param choicedict:
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
        :param helptextcolor:
        :param helptextfontsize:
        """
        # --- testing ---
        if type(menudict) != dict:
            raise ValueError("menudict is not a dict")
        vtypes = [type(v) is list for v in menudict.values()]
        if False in vtypes:
            raise ValueError("each value in menudict must be a list")
        if "root" not in menudict:
            raise ValueError("menudict must have an root entry")
        if menuname not in menudict:
            raise ValueError("menuname must be a key of valuedict (usually: 'root')")
        # --- add quit to main menu if necessary ---
        if "quit" not in menudict["root"]:
            menudict["root"].append("quit")
        # --- add "back" to each submenu if necessary ----
        for k in menudict.keys():
            if k != "root":
                v = menudict[k]
                if not "back" in v:
                    menudict[k].append("back")

        # --- start

        self.menudict = menudict
        self.cursortext = cursortext

        self.cycle_up_down = cycle_up_down
        self.i = startIndex
        self.menuname = menuname
        self.history = [] # traceback
        #---- pygame variables
        self.cursorSprite = cursorSprite
        self.cursorTextList = cursorTextList
        self.cursorAnimTime = cursorAnimTime
        self.menutime = menutime # age of menu in seconds
        self.background = background # pygame surface to blit
        self.screen = screen
        self.screenrect = self.screen.get_rect()
        self.textcolor = textcolor # black
        self.clock = pygame.time.Clock()
        self.fps = 400
        #self.fontsize = fontsize
        #self.fontname = fontname
        self.font = pygame.font.SysFont(name=fontname, size=fontsize, bold=True, italic=False)
        self.yspacing = yspacing # pixel vertically between text lines
        self.helptextheight = helptextheight # pixel distance to top border of window, to display helptext
        self.helptextcolor = helptextcolor
        self.helptextfontsize = helptextfontsize
        self.helptextfont = pygame.font.SysFont(name=fontname, size=helptextfontsize, bold=True)
        # ------
        self.anim = 0


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

    def pygame_run(self):
        # calcualte best position for menu (to not recalculate each sub-menu)
        width, height, entries = self.calculate_all_dimensions()
        if width > self.screenrect.width:
            print("warning: fontsize too big or menuentries too long or screen width too small:" + str(menupoints))
        if height > self.screenrect.height - self.helptextheight:
            print("warning: fontsize / helptext too big or too many menuentries or screen height too small" + str(menupoints))
        dy = height / entries

        #    srcolling = True
        # else:
        #    scrolling = False
        # x =  s
        # center menu on screen, calculate topleft position for menu
        x = self.screenrect.width // 2 - width // 2
        y = self.helptextheight + (self.screenrect.height-self.helptextheight) // 2 - height // 2
        running = True
        while running:
            # clock
            milliseconds = self.clock.tick(self.fps)  #
            seconds = milliseconds / 1000
            self.menutime += seconds

            # ---------- clear all --------------
            self.screen.blit(self.background, (0, 0))
            # pygame.display.set_icon(self.icon)
            t = f"menu: {self.menuname} Navigate with Up/Down/Enter/Backspace"
            pygame.display.set_caption(t)
            # ----- write helptext on top ----
            wh, yh = write(self.screen, t, 10, 0, self.helptextcolor, self.helptextfont, origin="topleft")
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

            # ---------------------------------
            # ----------- writing on screen ----------
            menupoints = self.menudict[self.menuname]
            for i, entry in enumerate(menupoints):
                if i == self.i:
                    write(self.screen, cursortext, x - maxcursordistance + cursordistance, y + dy * i ,
                               cursorcolor, self.font, origin="topright")
                # -----------
                write(self.screen, entry, x, y + dy * i,
                           self.textcolor, self.font, origin="topleft")
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # ------- pressed and released key ------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            return "quit"
                    if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        self.i -= 1
                        if self.i < 0:
                            if self.cycle_up_down:
                                self.i = len(menupoints) - 1
                            else:
                                self.i = 0
                        #print("i", self.i)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        self.i += 1
                        if self.i >= len(menupoints):
                            if self.cycle_up_down:
                                self.i = 0
                            else:
                                self.i = len(menupoints) - 1
                    if event.key == pygame.K_BACKSPACE:
                        if self.menuname != "root":
                            self.menuname = self.history.pop()
                            self.i = 0
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        selection = menupoints[self.i]
                        print("selected:", selection)
                        if selection in self.menudict.keys():
                            self.history.append(self.menuname)
                            self.menuname = selection
                            self.i = 0
                        elif selection == "back":
                            self.menuname = self.history.pop()  # remove last item
                            self.i = 0
                        #elif selection == "quit":
                        else:
                            return selection
            # ---------- end of event handler -----
            # --- special sprites ---
            # self.menusprites.update(seconds)
            # self.menusprites.draw(self.screen)
            #-------- update screen -------------
            pygame.display.flip()



    def text_run(self):
        """for testing a menu without pygame"""
        print("self:", self, self.__dict__)

        while True:
            menupoints = self.menudict[self.menuname]
            for i, entry in enumerate(menupoints):
                if i==self.i:
                    print(self.cursortext, end="")
                else:
                    print(" "* len(self.cursortext), end="")
                print(entry)
            command = input("d for down, u for up or just enter>>>")
            if command == "":
                selection = menupoints[self.i]
                print("selected:", selection)
                if selection in self.menudict.keys():
                    self.history.append(self.menuname)
                    self.menuname = selection
                    self.i = 0
                elif selection == "back":
                    self.menuname = self.history.pop() # remove last item
                    self.i = 0
                else:
                    return selection
            elif command == "d":
                self.i += 1
            elif command == "u":
                self.i -= 1
            if self.i < 0:
                if self.cycle_up_down:
                    self.i = len(menupoints) - 1
                else:
                    self.i = 0
            elif self.i >= len(menupoints):
                if self.cycle_up_down:
                    self.i = 0
                else:
                    self.i = len(menupoints)-1

class Viewer:
    width: int
    height: int
    screenrect: pygame.Rect
    font = None
    menu = None

    def __init__(self, width=800, height=600):
        # ---- pygame init
        pygame.init()
        Viewer.width = width
        Viewer.height = height
        self.setup_screen(width, height)
        self.run()

    def setup_screen(self, width, height):
        Viewer.screenrect = pygame.Rect(0, 0, width, height)
        self.screen = pygame.display.set_mode(
            (width, height), pygame.DOUBLEBUF
        )
        self.background = pygame.Surface((width, height))
        self.background.fill((255, 255, 255))

        #print("Screen:", self.screen, self.screen.get_rect())


    def run(self):
        # create a menu, save it into a variable, manipulate it after creation
        m1 = Menu(
            menudict={"root":["play","options","help", "credits"],
                      "options":["sound", "graphic"],
                      "sound":["toggle music: on", "toggle sound: on"],
                      "graphic":["toggle fullscreen: on", "screen resolution"],
                      #"screen resolution": [], # will be added later by code
                      "credits":["graphic artist", "sound artist", "coding", "design", "testing"],
                      "help": ["how to play", "modding" ]
                      },
            cycle_up_down=True,
            textcolor=(0,0,222),
            screen=self.screen,
            background=self.background,
            menuname="root",
            startIndex=0,
        )
        # how to edit menuentry AFTER creating menu
        reslist = pygame.display.list_modes(flags=pygame.FULLSCREEN)
        # reslist is in horrible format: [(x1,y1),(x2,y2)...] with many double entries
        # create a set (without double entries) of strings and convert into a list
        res = [] # {(x,y) for (x,y) in reslist} # empty list
        for (x,y) in reslist:
            if (x,y) not in res:
                res.append((x,y))
        res = [str(x)+"x"+ str(y) for (x,y) in res]
        #res = list({str(x) +"x"+str(y) for (x,y) in reslist})
        # sort this list
        #print(res)
        m1.menudict["screen resolution"] = res
        # you must in this case MANUALLY append an "back" entry
        m1.menudict["screen resolution"].append("back")


        # ---main loop
        while True:
            # get a command from the menu. All code must be handled here inside your game loop.
            # the menu save is persistant as
            command = m1.pygame_run()

            if command == "play":
                ## start game code here
                print("playing a game...")

            # change screen resolution
            if command in res:
                # change the screen resolution
                x,y = int(command.split("x")[0]), int(command.split("x")[1])
                pygame.display.set_mode((x,y))
                self.setup_screen(x,y)
                m1.screen = self.screen
                m1.background = self.background

            if command == "quit":
                break
        # -----
        pygame.quit()


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



if __name__ == "__main__":
    # to test without pygame:
    # m = Menu({"root":    ["play", "options", "credits"],
    #           "options": ["graphic", "sound"],
    #           "graphic": ["toggle fullscreen"]
    #          })
    # m.textrun()
    # test with pygame
    Viewer(800,600)



