## >UTMCoordinates.zip< (Testing)
This blueprint is an actor that reports it's current map coordinates and height. It just apllies an offset to ActorLocation vector position based on your real world X,Y origin coordinates. Edit the blueprint and change 'UTM X origin', 'UTM Y origin' and 'Height point reference (m)' informed by >srtm2heightmap.py<. Works for UTM and possibly any other orthogonal projection.
![UE blueprint](https://raw.githubusercontent.com/Rodrigo-NH/UE4HmapsGenerator/main/blueprints/UTMCoordinates.jpg)
## >ImportLines.zip<
Blueprint to be used in conjunction with >importlines.py<