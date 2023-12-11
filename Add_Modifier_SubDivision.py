# Add Modifier - Subdivision
#
#   Hide any objects you don't want processed.
#   Be sure to set the level values.
#   Since the meshes might first need cleaning,
#   Merge By Distance has been included.
#   You may need to set the MBD value.
#   
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

sdiv_lev = 2
sdiv_rend_lev = 2
MBD = 0.0001            # Change Merge By Distance value as needed

countT = 0

for obj in bpy.context.visible_objects:
    if obj.type == 'MESH':
        countT += 1
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.remove_doubles(threshold = MBD)
        bpy.ops.object.editmode_toggle()
        obj.modifiers.new("Subdivision", 'SUBSURF')
        obj.modifiers["Subdivision"].levels = sdiv_lev
        obj.modifiers["Subdivision"].render_levels = sdiv_rend_lev

print(f"{countT} total objects modified.")
