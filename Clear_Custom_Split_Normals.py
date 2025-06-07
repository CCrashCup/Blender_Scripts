# Clear Custom Split Normals
#
#     Coded by Lofty
#
#     This is a short script to walk through the selected objects
#     in a scene and clear the Custom Split Normals.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

count = 0
print("*****************************************************************************")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        count += 1

print("*****************************************************************************")
print(f"{count} Custom Split Normals cleared.")
