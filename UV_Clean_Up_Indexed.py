# UV Clean Up Indexed
#
#   To keep the indexed UV Map and remove all the rest from selected objects.
#   Be sure to change the indx value to the correct UV Map number.
#   Valid index values for Blender are 0-7.
#   
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

indx = 6
countD = 0
countT = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        countT += 1
        max = len(obj.data.uv_layers) - 1
        ndx = max
        for uv in reversed(obj.data.uv_layers):
            if ndx != indx:
                obj.data.uv_layers.remove(obj.data.uv_layers[ndx])
                countD += 1
            ndx -= 1
print(f"{countD} maps deleted from {countT} total objects")
