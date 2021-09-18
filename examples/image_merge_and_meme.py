#!/usr/bin/env python3
"""
Concatenate multiple images (selected in filemanager or passed as command line argument or choosed by gui)
and optional write a text on it
recommended to use as right-click-script with linux file manager Caja / Nautilus
    ubuntu (nautilus):
        put the script in ~/.local/share/nautilus/scripts and make the script executable
    ubuntu mate (caja):
        put the script in ~/.config/caja/scripts  and make the script executable
    right-click some images in file-manager, then choose scripts -> image_merge_and_meme.py

you can also pass filenames as command line arguments when calling this script:

python3 image_merge_and_meme *.jpg

or you can call this python file without any command line arguments and use only the gui

see blog post: https://note.nkmk.me/en/python-pillow-basic/
see PIL documentation: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#text-anchors
linux fonts are installed in /usr/share/fonts/truetype ...
needs installed:
pysimplegui
pil (pillow)

"""

import PIL.Image
import PIL.ImageDraw 
import PIL.ImageFont 
import PySimpleGUI as sg
import time
#import os
import sys

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
PREVIEW_SIZE = (640,400)
WINDOW_SIZE = (960,800)
def generate_time_stamp(datestamp=True, timestamp=True):
    """creating an datestamp/timestamp string to act as a suffix for the filename"""
    # time.localtime() gives this struct:
    # time.struct_time(tm_year=2021, tm_mon=8, tm_mday=19, tm_hour=12, tm_min=45, tm_sec=51, tm_wday=3, tm_yday=231, tm_isdst=1)
    result_string = ""
    if datestamp:
        result_string += f"_{time.localtime().tm_year}{time.localtime().tm_mon:02}{time.localtime().tm_mday:02}"
    if timestamp:
        result_string += f"_{time.localtime().tm_hour:02}{time.localtime().tm_min:02}{time.localtime().tm_sec:02}"
    return result_string

def splitme(x):
    """gives back a as-quadratic-as-possible list of list
    :param x:int = number of items (images)
    4-> [[0,1], [2,3]]
    5-> [[0], [1,2], [3,4]]
    6-> [[0,1],[2,3], [4,5]]
    7-> [[0], [1,2,3], [4,5,6]
    8-> [[0,1], [2,3,4], [5,6,7]]
    9-> [[0,1,2], [3,4,5], [6,7,8]]
    ...
    """
    result = []
    i = 0
    #divider = find_divider(x)
    root = x**0.5
    if root == int(root):
        for row in range(int(root)):
            line = []
            for col in range(int(root)):
                line.append(i)
                i += 1
            result.append(line)
        return result
    smallroot = int(root)
    bigroot = int(root + 1)
    if abs(x - smallroot**2) < abs(bigroot**2-x):
        bestroot = smallroot
        # first line
        line = list(range(0, x- bestroot**2))
        result.append(line)
        i = len(line)
        # other lines
        for row in range(bestroot):
            line = []
            for col in range(bestroot):
                line.append(i)
                i += 1
            result.append(line)
        return result
    else:
        bestroot = bigroot
        line = list(range(bestroot - (bestroot**2 - x)))
        i = len(line)
        result.append(line)
        for row in range(bestroot-1):
            line = []
            for col in range(bestroot):
                line.append(i)
                i += 1
            result.append(line)
        return result


def get_concat_h_multi_resize(im_list, resample=PIL.Image.BICUBIC):
    """concatenate images horizontally. see https://note.nkmk.me/en/python-pillow-basic/"""
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = PIL.Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=PIL.Image.BICUBIC):
    """concatenate images vertically. see https://note.nkmk.me/en/python-pillow-basic/"""
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = PIL.Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def get_concat_tile_resize(im_list_2d, resample=PIL.Image.BICUBIC):
    """create big images from list of lists of images, see  https://note.nkmk.me/en/python-pillow-basic/"""
    im_list_v = [get_concat_h_multi_resize(im_list_h, resample=resample) for im_list_h in im_list_2d]
    return get_concat_v_multi_resize(im_list_v, resample=resample)

def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    """merge images horizontally, leaving blank the leftover see  https://note.nkmk.me/en/python-pillow-basic/"""
    dst = PIL.Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v_blank(im1, im2, color=(0, 0, 0)):
    """merge images vertically, leaving blank the leftover, see https://note.nkmk.me/en/python-pillow-basic/"""
    dst = PIL.Image.new('RGB', (max(im1.width, im2.width), im1.height + im2.height), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def create(filenames = None, horizontal = True, vertical = False, outputfilename="result.jpg", memetext=None,
           fontsize=12, fontcolor=None, fontfile="/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
           make_tiles = False):
    """
    saves an merged image, add text to it and saves a smaller png preview image as well

    :param horizontal: to merge images in a row
    :param vertical:   to merge images in a column
    :param outputfilename:  outputfilename. Shall NOT be "preview.png"
    :param memetext: multi-line text or None
    :param fontsize: fontsize of meme text
    :param fontcolor:  fontcolor (hex) of meme text
    :param fontfile:  path to fontfile for meme text
    :param make_tiles: programs try to arrange images in rows and columns
    :returns: image width, image height
    """
    if filenames is None:
        raise ValueError("no filenames passed")
    sg.PopupQuick("merging images, please wait...", auto_close_duration=1)
    #for path in os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').splitlines():
    #    filenames.append(path)

    images = []
    # create pil image objects and store them in the list 'images'
    for one_filename in filenames:
        try:
            im = PIL.Image.open(one_filename)
        except:
            sg.PopupError("could not open:" + one_filename)
            continue
        images.append(im)

    if horizontal:
        im = get_concat_h_multi_resize([*images])
    elif vertical:
        im = get_concat_v_multi_resize([*images])
    elif make_tiles: # make as quadratic as possible
        ranklist = splitme(len(images))
        im_list = [[images[rank] for rank in line] for line in ranklist]
        im = get_concat_tile_resize(im_list)
    # make text
    if memetext is not None and len(memetext.strip()) > 0  :
        draw = PIL.ImageDraw.Draw(im)
        ##draw.line((0, im.height, im.width, 0), fill=(255, 0, 0), width=8)
        ##draw.rectangle((100, 100, 200, 200), fill=(0, 255, 0))
        ##draw.ellipse((250, 300, 450, 400), fill=(0, 0, 255))
        font = PIL.ImageFont.truetype(fontfile, fontsize)
        x = im.width // 2  # find middle pixel coordinate of image
        y = im.height // 2
        draw.multiline_text(xy=(x,y),
                            anchor="mm",     # mm means middle (vertical) and middle (horizontal). see documentation https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#text-anchors
                            text=memetext,
                            fill = fontcolor,
                            font=font,
                            align="center")
    # finally, save to disk
    im.save(outputfilename)  # big picture
    im2 = im.resize(size=PREVIEW_SIZE)
    im2.save("preview.png")  # small preview png 640x400
    return im.width, im.height # return dimension of big picture


def main(filelist=[]):
    """
    pysimplegui menu.
    from pysimplegui cookbook  https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-pattern-1a-one-shot-window-the-simplest-pattern
    """
    ## nautilus right-click pass all selected file/foldernames as command line arguments!
    if len(filelist) > 0:
        goodlist = []
        #remove everything that has no extension
        for name in filelist:
            if "." not in name :
                #print("has no dot:", name)
                continue
            # remove everything that has no valid image extension
            extension = name.split(".")[-1]
            if extension.lower() not in IMAGE_EXTENSIONS:
                print("unknown extension in", name)
                continue
            goodlist.append(name)
        filelist = goodlist
        #im = None



    left_part = sg.Column(layout=[
              [sg.Text("meme text :")],
              [sg.Multiline(key="memetext", size=(50,5), default_text="hello\nmy\nlove")],
              [sg.ColorChooserButton("select text color:", target="hexcolor", key="color"),
               sg.InputText(key="hexcolor", size=(10,1), default_text="#FF0000")],
              [sg.Text("font size:"),
               sg.Slider(range=(10,1000), default_value=120,key="fontsize", orientation="h", size=(35,15))],
              [sg.Button("select font file", key="font"), sg.InputText(key="fontfile", size=(35,1), default_text="/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"),],
              [sg.Text("output filename:"),  sg.InputText(key='outputfilename', default_text="merged_image.jpg", size=(50,1)),],
              [sg.Text("add suffix to filename:"),
               sg.Checkbox(text="_YYYY_MM_DD", default=False, key="suffix_date"),
               sg.Checkbox(text="_hh_mm_ss", default=True, key="suffix_time")],
              [sg.Button(button_text="Create!", bind_return_key=True, key="ok"), sg.Button(button_text="Quit", key="cancel")],
              ])
    right_part = sg.Column(layout=[
        [sg.Text("image filenames:"), sg.Button("add image file:", key="add_imagefile")],
        #                   [sg.Text("zweite Zeile")],
        [sg.Listbox(values=[filename.split("/")[-1] for filename in filelist], size=(65,13), key="imagefilenames",enable_events=True,  )],
        [sg.Text("selected file:"),
         sg.Button("\u2191", key="move_up", disabled=True),
         sg.Button("\u2193", key="move_down", disabled=True),
         sg.Button("remove", key="remove", disabled=True)],
        [sg.Text('layout: merge (concatenate) images:')],
        [sg.Radio("horizontal", default=True, group_id="hv", key="horizontal"),
         sg.Radio("vertical", default=False, group_id="hv", key="vertical"),
         sg.Radio("quadratic", default=False, group_id="hv", key="quadratic"),
         ],
        ], vertical_alignment="top", element_justification="left"
    )
    layout = [
        [left_part, sg.VerticalSeparator(), right_part],
        [sg.Text("preview of:"), sg.Text(text = "<no image created yet>", key="previewtext", size=(100,1))],
        [sg.Image(filename=None,
                  key="preview",
                  size=PREVIEW_SIZE,
                  pad=((WINDOW_SIZE[0]-PREVIEW_SIZE[0])/2,0))],
              ]

    window = sg.Window('Window Title', layout, size=WINDOW_SIZE)
    while True:
        event, values = window.read()
        # file-entry buttons enable/disable?
        if len(values["imagefilenames"]) > 0:
            window["move_up"].update(disabled = False)
            window["move_down"].update(disabled=False)
            window["remove"].update(disabled=False)
        else:
            window["move_up"].update(disabled=True)
            window["move_down"].update(disabled=True)
            window["remove"].update(disabled=True)

        # --------- event handler ----
        if event == sg.WINDOW_CLOSED or event=="cancel":
            break # end of GUI loop
        elif event in ["move_up", "move_down", "remove"]:
            if values["imagefilenames"] is None or len(values["imagefilenames"]) == 0:
                print("no action because of: empty list or no item selected")
                continue
            name = values["imagefilenames"][0]
            #i = [filename.split("/")[-1] for filename in filelist].index(values["imagefilenames"][0])
            #print("i", i, "name:", name)
            #print("Widget:", window.Element('imagefilenames').Widget.curselection() )
            index = window.Element('imagefilenames').Widget.curselection()[0]
            print("index:", index, "fillist", filelist)
            if event == "move_up":
                if index > 0:
                    filelist.insert(index - 1, filelist.pop(index))  # moving up
                    index -= 1
                else:
                    print("already at top position")
            elif event == "move_down":
                if  index <= len(filelist):
                    filelist.insert(index + 2, filelist[index])
                    filelist.pop(index)
                    index += 1
                else:
                    print("already at last position")
            elif event == "remove":
                filelist.pop(index)
            # update listbox entries, generated from filelist
            window["imagefilenames"].update(values= [filename.split("/")[-1] for filename in filelist],
                                            set_to_index=index)

        elif event == "add_imagefile":
            # let user choose an file to add to filelist
            newfile = sg.PopupGetFile(message="select imagefile(s) to add", title="choose file",
                                      multiple_files=True)
            if newfile is None:
                continue # cancel this operation
            # newfile can contain a single filename or a string of multiple filenames seperated by semicolon (;)
            if ";" in newfile:
                for one_new_file_name in newfile.split(";"):
                    filelist.append(one_new_file_name)
            else:
                filelist.append(newfile)
            window["imagefilenames"].update(values = [filename.split("/")[-1] for filename in filelist])
        elif event == "font":
            window["fontfile"].update(sg.popup_get_file(message="select true type font:",
                              title="choose folder and file",
                              default_path="/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
                              initial_folder="/usr/share/fonts/truetype/freefont/",
                              ))
        elif event == "ok": # create image
            # quadratic needs at minimum 4 images:
            if values["quadratic"] and len(filelist) < 4:
                sg.PopupError("I need a minimum of 4 images to arrange quadratic")
                continue
            output_name = ""
            timestampstring = generate_time_stamp(values["suffix_date"], values["suffix_time"]) # can be ""
            if values["outputfilename"] is None or len(values["outputfilename"]) == 0:
                if timestampstring == "":
                    sg.PopupError("please enter an outputfilename or enable date/time suffix")
                    continue
                output_name = timestampstring + ".jpg"
            elif "." not in values["outputfilename"]:
                # check if ouputfilename is has an extension
                output_name = values["outputfilename"] + timestampstring + ".jpg"
            else:
                left_part = "".join(values["outputfilename"].split(".")[:-1]) # the part before the last dot
                right_part = values["outputfilename"].split(".")[-1] # the part after the last dot
                output_name = left_part + timestampstring + "." + right_part

            width, height = create(
                   filenames =filelist,
                   horizontal=values["horizontal"],
                   vertical=values["vertical"],
                   memetext=values["memetext"],
                   fontsize=int(values["fontsize"]),
                   fontfile = values["fontfile"],
                   outputfilename=output_name,
                   fontcolor=values["hexcolor"],
                   make_tiles = values["quadratic"])
            sg.PopupOK(f"images created:\npreview.png: {PREVIEW_SIZE[0]}x{PREVIEW_SIZE[1]} pixel\n{output_name}: {width} x {height} pixel")
            window["preview"].update(filename="preview.png", size=(800, 600))
            window["previewtext"].update(value=f"{output_name} dimension: {width} x {height} pixel")

    window.close()


if __name__ == "__main__":
    # sys.argv[0] is always the name of the python program itself
    main(sys.argv[1:]) # pass all other arguments to main (empty list if is passed if no arguments are given)





