# UV Clean Up Named
#
#   Coded by Lofty
#   To keep the named UV Map and remove all the rest from selected objects.
#   Be sure to change the uv_keep value to the correct UV Map name.
#   
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

uv_keep = "uv_?"

countD = 0
countT = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        countT += 1
        for uv in reversed(obj.data.uv_layers):
            if uv.name != uv_keep:
                obj.data.uv_layers.remove(uv)
                countD += 1
print(f"{countD} maps deleted from {countT} total objects")
