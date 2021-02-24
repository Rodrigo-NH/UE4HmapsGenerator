## >UTMCoordinates.uasset< (Testing)
This blueprint is an actor that reports it's current map coordinates and height. It just apllies an offset to ActorLocation vector position based on your real world X,Y origin coordinates. Edit the blueprint and change 'UTM X origin', 'UTM Y origin' and 'Height mid point (m)' informed by srtm2heightmap.py. Works for UTM and possibly any other orthogonal projection.
P.S. If you choose (N)o to 'Use entire UE4 Z range (-256 to 255.992) for Level/tiles?' in srtm2heightmap.py then you need to use 'STATISTICS_MINIMUM (height)' value to fill 'Height mid point (m)' in the blueprint.

![UE blueprint](https://raw.githubusercontent.com/Rodrigo-NH/UE4HmapsGenerator/main/blueprints/UTMCoordinates.jpg)
