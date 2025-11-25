# Select No Material
#
#   Coded by Lofty
#   To select all visible objects in the scene that have no materials.
#

import os
import bpy


if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

tallyO = 0
tallyT = 0

obj_select = []
print("***************************************************")

for obj in bpy.context.visible_objects:
    obj.select_set(False)
    if obj.type == 'MESH':
        mesh = obj.data
        tallyT += 1
        if len(mesh.materials) == 0:
            if obj not in obj_select:
                obj_select.append(obj)
for obj in obj_select:
    obj.select_set(True)
    tallyO += 1
    
print(f"{tallyO} objects selected. A total of {tallyT} objects processed.")
