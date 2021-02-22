# SPDX-License-Identifier: BSD-3-Clause
# Rodrigo Nascimento Hernandez

import unreal
import os
import pathlib

inputdir = r'D:\MA\GIS\UE4\kingsvalley\customtiles' # Enter directory where tiled texture files are stored
asset_path = '/Game'
material_dir = '/landsmaterials'
# Change to your Z scale calculated by srtm2heightmap.py
UE4_TILE_TEXTURE_SCALE = 0.003952569169960475

# Scan for texture files
texturepaths = []
for file in os.listdir(inputdir):
    if file.startswith("texture_") and file[-4:].upper() == '.PNG':
        texturepaths.append(os.path.join(inputdir, file))

# import textures and set in memory textures reference
data = unreal.AutomatedAssetImportData()
data.set_editor_property('destination_path', asset_path + material_dir)
data.set_editor_property('filenames', texturepaths)
textures = unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(data)

# set used tools
assetTools = unreal.AssetToolsHelpers.get_asset_tools()
mf = unreal.MaterialFactoryNew()

for texture in textures:
    texturename = texture.get_name()
    matname = 'M_' + texturename.split('texture_')[1]

    # Create the new material and set property
    matobj = assetTools.create_asset(matname, asset_path + material_dir, unreal.Material, mf)
    matobj.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_DEFAULT_LIT)

    # Create texturesample expression, constant expression, make connections and set texture asset origin
    texturesample = unreal.MaterialEditingLibrary.create_material_expression(matobj,unreal.MaterialExpressionTextureSample,-384,-200)
    specularzero = unreal.MaterialEditingLibrary.create_material_expression(matobj,unreal.MaterialExpressionConstant,-200,-100)
    unreal.MaterialEditingLibrary.connect_material_property(texturesample, 'rgb', unreal.MaterialProperty.MP_BASE_COLOR)
    unreal.MaterialEditingLibrary.connect_material_property(specularzero, '', unreal.MaterialProperty.MP_SPECULAR)
    texturesample.texture = texture

    # Create TextureCoordinate expression, set scales and connect
    coordexpression = unreal.MaterialEditingLibrary.create_material_expression(matobj,unreal.MaterialExpressionTextureCoordinate,-550,-200)
    coordexpression.set_editor_property('utiling', UE4_TILE_TEXTURE_SCALE)
    coordexpression.set_editor_property('vtiling', UE4_TILE_TEXTURE_SCALE)
    unreal.MaterialEditingLibrary.connect_material_expressions(coordexpression, '', texturesample, 'uvs')

    # Optional save the assets as soon as possible. Shaders must be compiled etc.
    # May be more comfortable leave this commented, wait all shaders compiles in editor and just press 'save all' in editor
    # textureref = asset_path + material_dir + '/' + texturename
    # matref = asset_path + material_dir + '/' + matname
    # unreal.EditorAssetLibrary.save_asset(textureref)
    # unreal.EditorAssetLibrary.save_asset(matref)

