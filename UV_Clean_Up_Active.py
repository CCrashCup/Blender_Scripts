# UV Clean Up Active
#
#   Coded by Lofty
#   To keep the active UV Map and remove all the rest from selected objects.
#   Be sure to select all the objects you want processed.
#   
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

countD = 0
countT = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        countT += 1
        uvs = [uv for uv in obj.data.uv_layers 
                if not uv.active_render]
        while uvs:
            obj.data.uv_layers.remove(uvs.pop())
            countD += 1
print(f"{countD} maps deleted from {countT} total objects")
