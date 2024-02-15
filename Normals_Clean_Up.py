# Normals Clean Up
#
#   Coded by Lofty from the code of "marbs" in a StackExchange post referred by @flyingsaucer.
#   You may select the entire mesh, or a partial area, that contains errant face normals.
#   This will hopefully detect the errant normals and then, optionally, flip them for you.
#   If you set the variable "auto_flip" to False then the object will remain in Edit Mode
#   with the errant faces selected.
#   Be sure to check the box for Face Orientation in the Overlays menu so you can watch.  
#
import bpy
import bmesh
import mathutils

auto_flip = True

print("=======================================")

allow = 0
# Set to object mode.
if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode = 'OBJECT')

# Get the active object
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
#       Original code below. Replaced.
        # Get location of the current 3d view.
#        area = next(area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D')
#        view_location = area.spaces.active.region_3d.view_matrix.inverted().translation
        view_location = mathutils.Vector((0.0, 0.0, 0.0))       # Force view_location to Object Origin
        # modify the view location so that it is at (0,0,0) and calculate 
        # the dot product with the normal.
        dot_product = normal.dot(view_location - face.center)
#       Original code below. Replaced.
        # If the dot product is negative then this is a 'red' face.
#        if dot_product < allow:
        if dot_product >= allow:
            faces.append(face_index)
                
    # Deselect all faces
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

    # Reselect only the inverted faces.
    for face in faces:
        obj.data.polygons[face].select = True

    bpy.context.area.ui_type = 'VIEW_3D'        # Required for Snap to work
    bpy.ops.view3d.snap_cursor_to_active()
    bpy.context.area.ui_type = 'TEXT_EDITOR'    # Reset back to normal
    bpy.ops.object.mode_set(mode = 'EDIT')
    if auto_flip:
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.area.ui_type = 'VIEW_3D'        # Required for Snap to work
    bpy.ops.view3d.snap_cursor_to_center()
    bpy.context.area.ui_type = 'TEXT_EDITOR'    # Reset back to normal
else:
    print("No mesh object currently selected.")
