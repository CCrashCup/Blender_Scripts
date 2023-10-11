# Material Colate - Mesh Join - Merge By Distance
#
#     Coded by Lofty
#     This is a script to colate Materials by Texture,
#     Join the Meshes for each Material,
#     Very specialized, results may vary.
#

import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

#
## Trim the materials
#

mapping = {}

for material in bpy.data.materials:
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                texture = node.image
                if texture not in mapping:
                    mapping[texture] = []
                mapping[texture].append(material)
    else:
        texture = None
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material == material:
                        if slot.texture and slot.texture.type == 'IMAGE':
                            texture = slot.texture.image
                        break
                if texture:
                    break
        
        if texture:
            if texture not in mapping:
                mapping[texture] = []
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
                            except:
                                print("------------------------------------")
                                continue
#            print(obj)                 # for debugging
#            print(mat)                 # for debugging
            try:
                bpy.data.materials.remove(mat)
            except:
                print("++++++++++++++++++++++++++++++++++++")
                continue

#
## Join meshes with same material
#

if bpy.ops.object.select_all.poll():
    bpy.ops.object.select_all(action='DESELECT')

while bpy.context.visible_objects:
    for obj in bpy.context.visible_objects:
        if obj.type == 'MESH':
            break
#    print(obj)                 # for debugging
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if bpy.ops.object.select_linked.poll():
        bpy.ops.object.select_linked(type='MATERIAL')
    if bpy.ops.object.join.poll():
        bpy.ops.object.join()
    if bpy.ops.object.editmode_toggle.poll():
        bpy.ops.object.editmode_toggle()
    if bpy.ops.mesh.select_all.poll():
        bpy.ops.mesh.select_all(action='SELECT')
    if bpy.ops.mesh.remove_doubles.poll():
        bpy.ops.mesh.remove_doubles()
    if bpy.ops.object.editmode_toggle.poll():
        bpy.ops.object.editmode_toggle()
    obj.hide_set(True)

for obj in bpy.context.scene.objects:
    obj.hide_set(False)

print("********************************************************************************")
