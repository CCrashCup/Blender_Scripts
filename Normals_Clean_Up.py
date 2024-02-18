# Normals Clean Up
#
#   Coded by Lofty from the code of "marbs" in a StackExchange post referred by @flyingsaucer.
#   You may select the entire mesh, or a partial area, that contains errant face normals.
#   This will hopefully detect the errant normals and then, optionally, flip them for you.
#   If you set the variable "auto_Flip" to False then the object will remain in Edit Mode
#   with the errant faces selected.
#   If you set the variable "do_Snap" to False then the reference will be World Origin
#   instead of Object Origin.
#   Be sure to check the box for Face Orientation in the Overlays menu so you can watch.  
#   It can be complex, where multiple passes are needed, with different options active.
#
import bpy
import bmesh
import mathutils

auto_Flip = True        # Flip the calculated faces (otherwise just leave them selected).
do_Snap = True          # Snap the Cursor to the current object's origin.

#allow = 0.0001         # Greater than zero
allow = 0               # This value can be adjusted to get more or fewer faces that are angled.
#allow = -0.0001        # Less than zero

print("=======================================")

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode = 'OBJECT')

obj = bpy.context.active_object

faces=[]
if obj and obj.type == 'MESH':
    mesh = bpy.context.active_object
    # Get selected faces
    selected_faces = [f.index for f in mesh.data.polygons if f.select]
    # Loop through the selected faces.
    for face_index in selected_faces:
        face = mesh.data.polygons[face_index]
        normal = face.normal
        if do_Snap:
            view_location = mathutils.Vector((0.0, 0.0, 0.0))       # Force view_location to Object Origin
        else:
        # Get location of the current 3d view.
            area = next(area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D')
            view_location = area.spaces.active.region_3d.view_matrix.inverted().translation
        # Calculate the dot product with the normal.
        dot_product = normal.dot(view_location - face.center)
        if do_Snap:
            if dot_product >= allow:
                faces.append(face_index)
        else:
            if dot_product <= allow:
                faces.append(face_index)

                
    # Deselect all faces
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    # Reselect only the inverted faces.
    for face in faces:
        obj.data.polygons[face].select = True

    if do_Snap:
        bpy.context.area.ui_type = 'VIEW_3D'        # Required for Snap to work
        bpy.ops.view3d.snap_cursor_to_active()
        bpy.context.area.ui_type = 'TEXT_EDITOR'    # Reset back to normal
    bpy.ops.object.mode_set(mode = 'EDIT')
    if auto_Flip:
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode = 'OBJECT')
    if do_Snap:
        bpy.context.area.ui_type = 'VIEW_3D'        # Required for Snap to work
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.context.area.ui_type = 'TEXT_EDITOR'    # Reset back to normal
else:
    print("No mesh object currently selected.")
