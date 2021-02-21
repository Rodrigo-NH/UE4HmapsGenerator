# UE4HmapsGenerator (heightmaps generator)
## Unrel Engine 4 scripts to:
- Prepare and tile from SRTM (and others) DEM to UE heightmaps while keeping real world X,Y,Z proportions and metrics (UE u.u.) (srtm2heightmap.py)
- Create landscape textures and materials. (materialsgen.py)
- Assign landscape materials to tiles. (applymaterials.py)

Output example: https://www.youtube.com/watch?v=91U2XWXpHJk

## >srtm2heightmap.py<
Script that takes GeoTiff (and other GDAL valid file drivers, SRTM .hgt images e.g.) and generates UE4 hightmaps tiles and texture files. Script needs GDAL installed (No need to have GDAL python binds installed). On Windows the easiest way to install GDAL is [osgeo4w]
Also on Windows make sure you have appropriated sys environment sets, e.g.:

"GDAL_DATA C:\Program Files\GDAL\gdal-data"
"GDAL_DRIVER_PATH C:\Program Files\GDAL\gdalplugins"
"GDAL_VERSION 3.1.1"

Script will ask for all necessary parameters needed to take the input images, generate the tiles and generate/inform the necessary importing X,Y,Z UE4 scales.
It will generate a 'customtiles' directory and auxiliary files in the same directory as origin files are located. The image file to be used as landscape texture/materials is optional but if you use it, needs to be a georeferenced file as well in the same projection/EPSG as the DEM file.
Look the code for the 'METER_BY_DEGREE_FACTOR' variable, adjust as necessary depending the part of the globe you're working. This conversion is necessary as we need convert spatial resolution (pixel size) to a metric reference (meter) as UE4 workspace is a orthogonal world. It may be better using a DEM image already in a ortoghonal projection (e.g. UTM) as you don't need to adjust 'METER_BY_DEGREE_FACTOR', accordingly your final objectives.
This script was tested with [SRTM] DEMs but will accept other valid GeoTiff images.
Starting from raw SRTM images if you don't know how to answer the Y/N questions, answer (Y)es for all of them to get started.
[How to download SRTM]

The conventions used by the script are the following:

![Alt text](https://github.com/Rodrigo-NH/UE4HmapsGenerator/readmeassets/origin.jpg "Scene origin")

[Work in progress]

[How to download SRTM]: https://www.youtube.com/watch?v=0YPFegTcL4w
[SRTM]: https://www2.jpl.nasa.gov/srtm/
[osgeo4w]: https://trac.osgeo.org/osgeo4w/