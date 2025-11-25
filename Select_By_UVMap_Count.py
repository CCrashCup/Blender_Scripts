# Select By UV Map Count
#
#   Coded by Lofty
#   To select all visible objects in the scene that have the specified number of UV Maps.
#
import bpy

uv_count = 8		# Change to fit your criteria

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
            if len(obj.data.uv_layers) == uv_count:
                obj_select.append(obj)
            tallyT += 1

for obj in obj_select:
    obj.select_set(True)
    tallyO += 1
    
print(f"{tallyO} objects selected. A total of {tallyT} objects examined.")
