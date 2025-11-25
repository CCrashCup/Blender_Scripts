# Select By Texture Count
#
#   Coded by Lofty
#   To select all visible objects in the scene that have the
#   specified number of Image Texture nodes in their Materials.
#
import bpy

tex_count = 3             # Change to fit your criteria.

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

tallyO = 0
tallyT = 0

obj_select = []
print("***************************************************")

for obj in bpy.context.visible_objects:
    obj.select_set(False)
    if obj not in obj_select:
        if obj.type == 'MESH':
            countN = 0
            for slot in obj.material_slots:
                if slot.material:
                    mat = slot.material
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            countN += 1
            tallyT += 1
            if countN == tex_count:
                obj_select.append(obj)
for obj in obj_select:
    obj.select_set(True)
    tallyO += 1
    
print(f"{tallyO} objects selected. A total of {tallyT} objects examined.")

