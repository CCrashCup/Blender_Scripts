# UV Clear
#
#   To remove all the UV Maps from selected objects.
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
        max = len(obj.data.uv_layers) - 1
        ndx = max
        for uv in reversed(obj.data.uv_layers):
            obj.data.uv_layers.remove(obj.data.uv_layers[ndx])
            countD += 1
            ndx -= 1
print(f"{countD} maps deleted from {countT} total objects")
