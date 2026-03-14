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

count_S = 0
count_T = 0
print("*****************************************************************************")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        count_T += 1
        bpy.context.view_layer.objects.active = obj
        try:
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        except:
            count_S -= 1
        count_S += 1

print("*****************************************************************************")
print(f"{count_S} Custom Split Normals cleared.")
print(f"{count_T} Total Meshes.")
