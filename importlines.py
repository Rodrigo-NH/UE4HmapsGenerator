# SPDX-License-Identifier: BSD-3-Clause
# Rodrigo Nascimento Hernandez
# Tested UE versions:
# 4.26.1
# Blueprint: ImportLines

import sys
import json
import unreal

# ========================================= user inputs ===============================================================
# Change this path pointing to your gdal python bindings install dir
sys.path.append(r'C:\OSGeo4W64\apps\Python37\Lib\site-packages')
from osgeo import ogr
# Set project's relative path of the importlines BluePrint (e.g. in content folder->
importlines = unreal.EditorAssetLibrary().load_blueprint_class('/Game/ImportLines')
# Set shapefile path
shapefile = r'D:\UnrealEngine\curves\contour.shp'
# Set layer's feature name to read lines vertices Z values (height). Leave empty to not import any (Can use blueprint's 'Snap to Ground' custom event instead)
# If set to read Z values so you need to set 'Height point reference (m)' value also, calculated by 'srtm2heightmap.py'
featurename = ''
hpointreference = 572
# Set real world's UTM X,Y Origin (used in srtm2heightmap.py e.g.)
UTMx = 596441.4895549538
UTMy = 7918815.581869906
# Choose one of SplinePointType to be used on import
SplinePointType = unreal.SplinePointType.CURVE_CLAMPED
# SplinePointType = unreal.SplinePointType.CURVE_CUSTOM_TANGENT
# SplinePointType = unreal.SplinePointType.LINEAR
# SplinePointType = unreal.SplinePointType.CURVE
# SplinePointType = unreal.SplinePointType.CONSTANT
# ========================================= script work ===============================================================

ogr = ogr.Open(shapefile)
layer = ogr.GetLayer(0)
jsond = '{'
LINE = 0
for feat in layer:
    if featurename is '':
        zvalue = "0"
    else:
        zvalue = feat.GetField(featurename)
    geometry = feat.GetGeometryRef()
    dd = geometry.ExportToJson()
    jsond = jsond + '"LINE' + str(LINE) + '": [ { "zvalue": ' + str(zvalue) + ' }, ' + dd + '],'
    LINE += 1
jsond = jsond[:-1] + '}'
ldata = json.loads(jsond)
ed = unreal.EditorLevelLibrary
for key in ldata:
    zvalue = ldata[key][0]['zvalue']
    print(zvalue)
    line = ldata[key][1]['coordinates']
    if zvalue != 0:
        zvalue = (float(zvalue) - float(hpointreference)) * 100.0
    pi = 0
    for coord in line:
        xx = (float(coord[0]) - UTMx) * 100.0
        yy = (UTMy - float(coord[1])) * 100.0
        nv = unreal.Vector(x=xx, y=yy, z=zvalue)
        if pi == 0:
            rt = unreal.Rotator(roll=0.0, pitch=0.0, yaw=0.0)
            tblt = ed.spawn_actor_from_object(importlines, nv, rt, transient=True)
            splinename = tblt.get_name()
            ag = ed.get_all_level_actors_components()
            for each in ag:
                tlab = each.get_full_name()
                if splinename in tlab:
                    if 'SplineComponent' in tlab:
                        SPLINE = each
                        SPLINE.input_spline_points_to_construction_script = True
                        SPLINE.set_spline_point_type(0, SplinePointType, update_spline=True)
        else:
            SPLINE.add_spline_point_at_index(nv, pi, unreal.SplineCoordinateSpace.WORLD)
            SPLINE.set_spline_point_type(pi, SplinePointType, update_spline=True)
        pi += 1

    SPLINE.remove_spline_point(pi)
    SPLINE.update_spline()