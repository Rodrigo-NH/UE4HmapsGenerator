# UE4HmapsGenerator (heightmaps generator)
## Unreal Engine 4 scripts to:
- Prepare and tile from SRTM (and others) DEM to UE heightmaps while keeping real world X,Y,Z proportions and metrics (UE u.u.) (>srtm2heightmap.py<)
- Create landscape textures and materials. (>materialsgen.py<)
- Assign landscape materials to tiles. (>applymaterials.py<)

Output example: https://www.youtube.com/watch?v=91U2XWXpHJk

## >srtm2heightmap.py<
Script that takes GeoTiff (and other GDAL valid file drivers, SRTM .hgt images e.g.) and generates UE4 hightmaps tiles and texture files. Script needs GDAL installed (No need to have GDAL python binds installed). On Windows the easiest way to install GDAL is [osgeo4w]
Also on Windows make sure you have appropriated sys environment sets, e.g.:

- "GDAL_DATA C:\Program Files\GDAL\gdal-data"
- "GDAL_DRIVER_PATH C:\Program Files\GDAL\gdalplugins"
- "GDAL_VERSION 3.1.1"

Script will ask for all necessary parameters needed to take the input images, generate the tiles and generate/inform the necessary importing X,Y,Z UE4 scales.
It will generate a 'customtiles' directory and auxiliary files in the same directory as origin files are located. The image file to be used as landscape texture/materials is optional but if you use it, needs to be a georeferenced file as well in the same projection/EPSG as the DEM file.
Look the code for the 'METER_BY_DEGREE_FACTOR' variable, adjust as necessary depending the part of the globe you're working. This conversion is necessary as we need convert spatial resolution (pixel size) to a metric reference (meter) as UE4 workspace is a orthogonal world. It may be better using a DEM image already in a ortoghonal projection (e.g. UTM) as you don't need to adjust 'METER_BY_DEGREE_FACTOR', accordingly your final objectives.
This script was tested with [SRTM] DEMs but will accept other valid GeoTiff images.
Starting from raw SRTM images if you don't know how to answer the Y/N questions, answer (Y)es for all of them to get started.
[How to download SRTM]

The conventions used by the script are the following:

![Scene origin](https://raw.githubusercontent.com/Rodrigo-NH/UE4HmapsGenerator/main/readmeassets/origin.JPG)

The script will detect the most top left coordinates as the origin coordinates for the tiles extraction. Script will ask if user wants to use the detected origin coordinates or indicate alternative coordinates somewhere in the scene to be used as origin for tiles extraction.

![UE import screen](https://raw.githubusercontent.com/Rodrigo-NH/UE4HmapsGenerator/main/readmeassets/ueimportscreen.jpg)

You can use the script to produce a single tile and import directly in landscape mode. If importing tiles in world composition mode, make sure option 'Flip Tile Y Coordinate' is not selected. Either way, use the X,Y,Z scales calculated by the script in the importing screen. Take care to not select texture 'texture_' files but only the heightmaps png files;

## >materialsgen.py<

This script will import the texture files, create and set the materials for each tile. Copy this script under your UE project '/content' folder, edit and change the 'inputdir' and 'UE4_TILE_TEXTURE_SCALE' variables accordingly and run in the UE4 project instance (e.g. File->Execute Python Script).
After importing all textures the resulting blueprint for each tile material will be like:

![UE blueprint](https://raw.githubusercontent.com/Rodrigo-NH/UE4HmapsGenerator/main/readmeassets/blueprint.jpg)

## >applymaterials.py<

This script simply apply the texture materials in the corresponding tiles/levels.

[How to download SRTM]: https://www.youtube.com/watch?v=0YPFegTcL4w
[SRTM]: https://www2.jpl.nasa.gov/srtm/
[osgeo4w]: https://trac.osgeo.org/osgeo4w/