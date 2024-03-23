# Material Colate
#
#     Coded by Lofty
#     Partially based on code by Erik Marberg.
#     This is a script to colate Materials by Texture.
#

import bpy
import os

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode = 'OBJECT')

#
## Scan the materials
#

countU = 0
countD = 0

mapping = {}

for material in bpy.data.materials:
    print("Material = ", material.name)
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                tex01 = os.path.splitext(node.image.name )[0]
                ext02 = os.path.splitext(tex01 )[1]
                if ext02 == "":
                    texture = node.image.name
                else:
                    texture = tex01
                print("....Texture = ", texture)
                if texture not in mapping:
                    mapping[texture] = []
                if material not in mapping[texture]:
                    mapping[texture].append(material)

for texture, materials in mapping.items():
    if len(materials) > 1:
        main_material = materials[0]
        for mat in materials[1:]:
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for poly in obj.data.polygons:
                        if obj.material_slots[poly.material_index].material == mat:
                            try:
                                obj.material_slots[poly.material_index].material = main_material
                                countU += 1
                            except:
                                print("----------- Replace Error ----------")
                                print("Object       = ", obj.name)
                                print("    Main Mat = ", main_material.name)
                                print("    Material = ", mat.name)
                                print("    Texture  = ", texture)
                                continue
            try:
                bpy.data.materials.remove(mat)
                countD += 1
            except:
                print("+++++++++++ Remove Error +++++++++++")
                print("    Material = ", mat.name)
                continue

print("********************************************************************************")
print(f"{countU} object materials updated.")
print(f"{countD} orphan materials deleted.")
