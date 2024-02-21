# UV Map Adjust
#
#   Coded by Lofty
#
#   This is a short script to center and scale the UV Map
#   for all the visible objects in the scene.
#   Select or set the "scale" variable that works for your project.
#   (Very specialized, results will vary.)
#
import bpy

#scale = 0.0004875       # Armored Core 6
scale = 0.000975        # Gundam Breaker Mobile

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

print("********************************************************************************")

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.visible_objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.context.area.ui_type = 'UV'
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(scale, scale, 1.0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, use_accurate=True)
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.transform.translate(value=(0.5, 0.5, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.object.editmode_toggle()
        obj.select_set(False)
        bpy.context.area.ui_type = 'TEXT_EDITOR'
