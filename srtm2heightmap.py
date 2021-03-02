# SPDX-License-Identifier: BSD-3-Clause
# Rodrigo Nascimento Hernandez
# Tested UE versions:
# 4.26.1

import os
from PIL import Image
import pathlib

# Adjust this factor relative to the real projection figure on the region of the globe you're working in.
# https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm
# You DONT need to set this factor (not used in calculations) if your input is a regular GeoTiff in a orthogonal projection (e.g. UTM)
METER_BY_DEGREE_FACTOR = 111000

def main():
	inputfile = input("Enter GeoTIFF file's full path (including file name and extension)\n")
	DIR_PATH = pathlib.Path(inputfile).parent.absolute()
	userchoicebackgroundimage = YN("Want to tile a background image too? (To be used as UE4 textures")
	if userchoicebackgroundimage is True:
		backgroundimagepath = input("Enter background GeoTIFF file's full path (to be used as UE4 textures)\n")
	print("Computing image ...\n")
	gdalinfo = os.popen("gdalinfo -stats " + inputfile).read().splitlines()

	START_LAT = None
	START_LONG = None
	PIXEL_SIZE = None
	for each in gdalinfo:
		line = each.strip().upper()
		if "PIXEL SIZE" in line:
			PIXEL_SIZE = float(line.split("(")[1].split(",")[0])
		if "ORIGIN =" in line:
			START_LONG = float(line.split("(")[1].split(",")[0])
			START_LAT = float(line.split("(")[1].split(",")[1].split(")")[0])

	userchoice = False
	if START_LAT is not None:
		userchoice = YN("Use Lat (" + str(START_LAT) + ") from image statistics origin coordinates for Level starting point?")
	if userchoice is False:
		START_LAT = float(input("Enter Latitude coordinate of Level starting point (e.g. -20.32453)\n"))

	userchoice = False
	if START_LONG is not None:
		userchoice = YN(
			"Use Long (" + str(START_LONG) + ") from image statistics origin coordinates for Level starting point?")
	if userchoice is False:
		START_LONG = float(input("Enter Longitude coordinate of Level starting point (e.g. -45.54623)\n"))

	userchoice = False
	if PIXEL_SIZE is not None:
		userchoice = YN(
			"Use Spatial Resolution (" + str(PIXEL_SIZE) + ") from image statistics for output X,Y scale calculation?")
	if userchoice is False:
		PIXEL_SIZE = float(input("Enter Spatial Resolution (pixel size) of the input image\n"))

	PIXEL_SIZE_IS_DEGREE = YN("Is above Spatial Resolution in decimal degrees? (Choose 'N' if in meters)")
	TILE_SIZE = float(input("Enter UE4 (tile) Level size aspect (Recommended sizes: 127, 253, 505, 1009, 2017, 4033, 8129)\n"))
	X_TILES_NUMBER = float(input("Enter desired X number of Level Tiles \n"))
	Y_TILES_NUMBER = float(input("Enter desired Y number of Level Tiles\n"))

	zspace = YN("Use entire UE4 Z range (-256 to 255.992) for Level/tiles?"
				" Will use only positive range otherwise ( 0 to 255.992)")
	if zspace is False:
		startrange = 32767
	else:
		startrange = 0

	print("Computing parameters ...\n")

	overallfile = os.path.join(DIR_PATH, "overall.tif")
	totalX = X_TILES_NUMBER * TILE_SIZE * PIXEL_SIZE
	totalY = Y_TILES_NUMBER * TILE_SIZE * PIXEL_SIZE
	xrange = START_LONG + totalX
	yrange = START_LAT - totalY
	command = "gdal_translate -projwin " + str(START_LONG) + " " + str(START_LAT) + " " + str(xrange) + " " + str(yrange) + " " \
			  + inputfile + " " + overallfile

	print("Computing image ...\n")
	result = os.popen(command).read().splitlines()
	print(result)

	maxminvals = getmaxminheight(overallfile)
	STATISTICS_MAXIMUM = float(maxminvals[0])
	STATISTICS_MINIMUM = float(maxminvals[1])

	userchoice = False
	if STATISTICS_MAXIMUM is not 0:
		userchoice = YN(
			"Use source Max pixel value (height = " + str(STATISTICS_MAXIMUM) + ") from selected region statistics "
				 "for output Z scale calculation?")
	if userchoice is False:
		STATISTICS_MAXIMUM = input("Enter image's real world Max height in meters\n")

	userchoice = False
	if STATISTICS_MINIMUM is not 0:
		userchoice = YN(
			"Use source Min pixel value (height = " + str(STATISTICS_MINIMUM) + ") from selected region statistics "
																		  "for output Z scale calculation?")
	if userchoice is False:
		STATISTICS_MINIMUM = input("Enter image's real world Min height in meters\n")

	overallfilescaled = os.path.join(DIR_PATH, "overallScaled.tif")
	print("Computing image ...\n")
	scalecommand = "gdal_translate -ot UInt16 -scale " + str(STATISTICS_MINIMUM) + " " + str(STATISTICS_MAXIMUM) + \
				   " " + str(startrange) + " 65535" + " " + overallfile + " " + overallfilescaled
	print(scalecommand)
	scaleproc = os.popen(scalecommand).read()
	print(scaleproc)

	tilespath = os.path.join(DIR_PATH, "customtiles")
	os.mkdir(tilespath)

	tilelist = []
	stepX = START_LONG
	stepY = START_LAT
	tilerange = TILE_SIZE * PIXEL_SIZE
	for eachY in range(0, int(Y_TILES_NUMBER)):
		if eachY < 10:
			eachY = "0" + str(eachY)
		for eachX in range(0, int(X_TILES_NUMBER)):
			if eachX < 10:
				eachX = "0" + str(eachX)
			coordsname = "tile_x" + str(eachX) + "_y" + str(eachY)
			tilename = coordsname + ".tif"
			texturename = "texture_" + coordsname + ".tif"
			tilelist.append(tilename)
			tilepath = os.path.join(tilespath, tilename)
			texturepath = os.path.join(tilespath, texturename)
			tilerangeX =  stepX + tilerange
			tilerangeY = stepY - tilerange
			command = "gdal_translate -projwin " + str(stepX) + " " + str(stepY) + " " + str(tilerangeX) + " " + str(
				tilerangeY) + " " + overallfilescaled + " " + tilepath
			print(command)
			tileproc = os.popen(command).read()
			print(tileproc)
			if userchoicebackgroundimage:
				command2 = "gdal_translate -ot Byte -scale 0 255 -projwin " + str(stepX) + " " + str(stepY) + " " + str(
					tilerangeX) + " " + str(
					tilerangeY) + " " + backgroundimagepath + " " + texturepath
				print(command2)
				textureproc = os.popen(command2).read()
				print(textureproc)
			stepX = stepX + tilerange
		stepX = START_LONG
		stepY = stepY - tilerange

	print("Computing images ...\n")

	isresizeimage = False
	at = False
	rsize = 0
	for image in tilelist:
		terraintiffpath = os.path.join(tilespath, image)
		texturetiffpath = os.path.join(tilespath, "texture_" + image)
		terrainpngfile = image.split(".")[0]+".png"
		texturepngfile = "texture_" + image.split(".")[0] + ".png"
		terrainpngpath = os.path.join(tilespath, terrainpngfile)
		texturepngpath = os.path.join(tilespath, texturepngfile)
		if userchoicebackgroundimage:
			im = Image.open(texturetiffpath)
			width, height = im.size
			if not ((width != 0) and (width & (width-1) == 0)): # Test for (is number a power of two)?
				if not at:
					at = True
					isresizeimage = YN("Texture images are (" + str(width) + "x" + str(height) + "), not power of two size. "
					 	"Want to resize texture files?\n" )
					if isresizeimage:
						rs = int(input("Enter a number to use for width and height. (power of two recommended e.g."
										  " 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192)\n"))
						rsize = (rs, rs)
				if isresizeimage:
					im = im.resize(rsize, resample=Image.BILINEAR)
			im.save(texturepngpath)
			os.remove(texturetiffpath)
		im = Image.open(terraintiffpath)
		im.save(terrainpngpath)
		os.remove(terraintiffpath)
		print("Computing image ...\n")

	if PIXEL_SIZE_IS_DEGREE:
		PIXEL_SIZE = PIXEL_SIZE * METER_BY_DEGREE_FACTOR

	REAL_WORLD_XY_TILE_LENGHT = TILE_SIZE * PIXEL_SIZE
	UE4_XY_SCALE = (REAL_WORLD_XY_TILE_LENGHT / (TILE_SIZE - 1)) * 100
	REAL_WORLD_HEIGHT_DIFFERENCE = float(STATISTICS_MAXIMUM) - float(STATISTICS_MINIMUM)

	if zspace:
		zfactorrange = 512
		HEIGHT_MID_POINT = STATISTICS_MINIMUM + (REAL_WORLD_HEIGHT_DIFFERENCE / 2.0)
	else:
		zfactorrange = 256
		HEIGHT_MID_POINT = STATISTICS_MINIMUM

	UE4_Z_SCALE =  (REAL_WORLD_HEIGHT_DIFFERENCE * 100.0) / zfactorrange #height in centimeters
	UE4_TILE_TEXTURE_SCALE = UE4_XY_SCALE / (REAL_WORLD_XY_TILE_LENGHT*100.0)


	print("=================================== OUTPUTS ====================================\n")
	print("XY_TILE_LENGHT: " + str(REAL_WORLD_XY_TILE_LENGHT))
	print("XY_TILE_LENGHT: " + str(REAL_WORLD_XY_TILE_LENGHT))
	print("STATISTICS_MAXIMUM (height): " + str(STATISTICS_MAXIMUM))
	print("STATISTICS_MINIMUM (height): " + str(STATISTICS_MINIMUM))
	print("Real World height difference: " + str(REAL_WORLD_HEIGHT_DIFFERENCE))
	print("Origin X: " + str(START_LONG))
	print("Origin Y: " + str(START_LAT))
	print("\n")
	print("=========================== UE4 importing parameters ===========================\n")
	print("UE4 X,Y Scale: " + str(UE4_XY_SCALE))
	print("UE4 Z Scale: " + str(UE4_Z_SCALE))
	print("Tile texture scale: " + str(UE4_TILE_TEXTURE_SCALE))
	print("Height point reference (m): " + str(HEIGHT_MID_POINT))
	print("\n")

def getmaxminheight(inputfile):
	gdalinfo = os.popen("gdalinfo -stats " + inputfile).read().splitlines()
	vals = [0,0]
	for each in gdalinfo:
		line = each.strip().upper()
		if "STATISTICS_MAXIMUM" in line:
			vals[0] = line.split("=")[1].strip()
		if "STATISTICS_MINIMUM" in line:
			vals[1] = line.split("=")[1].strip()
	return vals

def YN(question):
	startlatoption = False
	while startlatoption is False:
		userinput = input(question + "(Y/N)\n")
		if "N" in userinput.upper():
			startlatoption = True
			return False
		if "Y" in userinput.upper():
			startlatoption = True
			return True


if __name__=="__main__":
	main()
