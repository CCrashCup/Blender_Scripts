# Delete Mesh by UV
#
#   Coded by Lofty
#   To delete selected objects with fewer than a specified number of UV maps
#   Change the "minimum" value to fit your criteria.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

minimum = 4
countD = 0
countT = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        countT += 1
        if len(obj.data.uv_layers) < minimum:
            bpy.data.objects.remove(obj)
            countD += 1
print(f"{countD} objects deleted out of {countT} total")
