# UV Map Adjust
#
#   Coded by Lofty
#
########## NOTE: This workaround might not be needed as the ripper improves.
#                I have started using the [UV_ReMap.py](https://github.com/CCrashCup/Blender_Scripts/edit/main/UV_ReMap.py) script instead of this one.
#
#   This is a script to center and scale the Active Render UV Map
#   for all the visible objects in the scene.
#   Select or set the "scale" variable that works for your project.
#   (Very specialized, results will vary.)
#
import bpy

#X_scale = 0.0004875           # Armored Core 6
#Y_scale = 0.0004875           # Armored Core 6
#X_center = 0.5                # Armored Core 6
#Y_center = 0.5                # Armored Core 6

#X_scale = 0.0004925           # Dark Souls III
#Y_scale = 0.0004925           # Dark Souls III
#X_center = 0.504925           # Dark Souls III
#Y_center = 0.5                # Dark Souls III
 
#X_scale = 0.000975            # Gundam Breaker Mobile
#Y_scale = 0.000975            # Gundam Breaker Mobile
#X_center = 0.5                # Gundam Breaker Mobile
#Y_center = 0.5                # Gundam Breaker Mobile

#X_scale = 0.001               # Lost: Via Domus
#Y_scale = 0.001               # Lost: Via Domus
#X_center = 0.5                # Lost: Via Domus
#Y_center = 0.5                # Lost: Via Domus

X_scale = 0.000244140625      # War Thunder's CDK
Y_scale = 0.000244140625      # War Thunder's CDK
X_center = 0.4999             # War Thunder's CDK - Have had to adjust these for different rips.
Y_center = 0.5045             # War Thunder's CDK - Should be 0.5 for both. Your results might vary.


FLIP = False


# These don't seem to be accurately consistent across all objects/materials
#X_scale = 0.00388935
#X_scale = 0.00387             # Arma 3 from NR 1.7.1 rip / needs FLIP
#Y_scale = 0.003885            # Arma 3 from NR 1.7.1 rip / needs FLIP
#X_center = 0.5                # Arma 3 from NR 1.7.1 rip / needs FLIP
#X_center = 0.4975             # Arma 3 from NR 1.7.1 rip / needs FLIP
#Y_center = 0.498125           # Arma 3 from NR 1.7.1 rip / needs FLIP
#Y_center = 0.500125           # Arma 3 from NR 1.7.1 rip / needs FLIP
#FLIP = True

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

print("********************************************************************************")

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.visible_objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if len(bpy.context.object.data.uv_layers) > 0:
            for uv in bpy.context.object.data.uv_layers:
                if uv.active_render:
                    uv.active = True
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.context.area.ui_type = 'UV'
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.snap_cursor(target='ORIGIN')
            bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
            bpy.ops.transform.resize(value=(X_scale, Y_scale, 1.0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, use_accurate=True)
            if bpy.app.version < (3, 6, 0):
                bpy.ops.transform.translate(value=(X_center, Y_center, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
            else:
                bpy.ops.transform.translate(value=(X_center, Y_center, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
            if FLIP:
                bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))
            bpy.ops.object.mode_set(mode = 'OBJECT')
            obj.select_set(False)
            bpy.context.area.ui_type = 'TEXT_EDITOR'




