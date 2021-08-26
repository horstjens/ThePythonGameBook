#!/usr/bin/env python3

# recursive goes down all folders
# and renames all image files with a _h or _v or _q suffix, depending on their geometry (vertical or horziontal or quadratic orientation)
# also writes image dimension as suffix
import os
#import os.path
import PIL.Image
import sys
import PySimpleGUI as sg

DIMENSION_PREFIX = "_d"
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]


def rename_files(startfolderlist=[]):
	"""rename recursive (go in each (sub)folder) all image files with suffix (width x height)
		and '_q' or  '_v' or '_h' for quadratic, vertical or horizontal orientation  """
	## if this script is executed by right-click from ubuntu file manager (nautilus/caja) then all
	## selected files / folders are passed as command line arguments!

	# only ask by gui for start folder if python script is called without command line arguments

	here = os.getcwd()
	if startfolderlist is None or len(startfolderlist) == 0:
		startfolder = sg.PopupGetFolder(message="please select start folder to recursive rename all image files",
										default_path=here,
										initial_folder=here,
										)
		if startfolder is None:
			# startfolder can now be None if user clicked on Cancel button
			return
		startfolderlist.append(startfolder)

	# iterate over all passed startfolders
	counter = 0
	for startfolder in startfolderlist:
		# starfolder can now be some crazy text if user entered text manually or by command line argument
		# check if starfolder is a file -> use directory of file as startfolder
		if os.path.isfile(startfolder):
			pathname, filename = os.path.split(startfolder)
			if pathname == "":
				pathname = here
			startfolder = pathname
			sg.PopupOK(f"got a filename, will use the folder instead: {startfolder}")

		if (startfolder is None) or (not os.path.isdir(startfolder)):
				#sg.PopupError("cancel operation because: invalid startfolder ")
				continue
		sg.PopupOK("processing:" + startfolder)

		#if startfolder is None:
		#	# check if script was invoked by richt-click from file manager nautilus / caja with selected path
		#	filelist = []
		#	for path in os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').splitlines():
		#		filelist.append(path)
		#	sg.PopupOK(f"got right click from file-manager: {filelist}")
		#return
		# check if startfolder is a path

		for path, dirs, files in os.walk(startfolder):  # current dir
			for one_file in files:
				extension = one_file.split(".")[-1]
				filename = one_file.split(".")[-2]
				if extension.lower() in IMAGE_EXTENSIONS:
					if "_" in filename:
						#print("filenmaE:", filename)
						if filename.split("_")[-1].lower() in ["h","v", "q"]:
							print(filename + extension, "already processed?")
							continue
					# open image in pil
					try:
						with PIL.Image.open(os.path.join(path, one_file)) as img:
							width = img.width
							height = img.height
					except:
						print("i could not open as image:", path, one_file)
						continue
					print("processing:", path, one_file, width, height)
					suffix = "q" # quadratic
					if int(width) > int(height):
						suffix = "h" # horizontal
					elif int(width) < int(height):
						suffix = "v" # vertical

					os.rename(src= os.path.join(path, one_file),
							  dst= os.path.join(path, filename + f"{DIMENSION_PREFIX}{width}x{height}_{suffix}.{extension}"))
					counter += 1
	sg.Popup(f"I renamed {counter} files", auto_close_duration=1)

if __name__ == "__main__":
	# print(sys.argv)
	# sys.argv[0] is always the name of the python program itself
	rename_files(sys.argv[1:]) # pass all arguments except the python program name
