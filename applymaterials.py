# SPDX-License-Identifier: BSD-3-Clause
# Rodrigo Nascimento Hernandez

import unreal

asset_path = '/Game'
material_dir = '/landsmaterials'

actors = unreal.EditorLevelLibrary.get_all_level_actors()
for each in actors:
    label = each.get_actor_label()
    if 'Landscape' in label:
        matname = asset_path + material_dir + '/M_' + each.get_path_name().split(':')[0].split('.')[1]
        mat = unreal.EditorAssetLibrary.load_asset(matname)
        each.set_editor_property('landscapematerial', mat)
