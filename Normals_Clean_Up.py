# Normals Clean Up
#
#   Coded by Lofty from the code of "marbs" in a StackExchange post referred by @flyingsaucer.
#   A single mesh is normally selected for processing, but multiple meshes can be selected.
#
#   You may select all faces of the mesh, or a partial area, that contains errant face normals.
#   The object's origin may be relocated to give a different angle and a different result.
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
from mathutils import Vector

auto_Flip = True        # Flip the calculated faces (otherwise just leave them selected).
do_Snap = True          # Snap the Cursor to the current object's origin.

#allow = 0.0001         # Greater than zero
allow = 0               # This value can be adjusted to get more or fewer faces that are angled.
#allow = -0.0001        # Less than zero

print("=======================================")

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode = 'OBJECT')


obj_list = []
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        if obj not in obj_list:
            obj_list.append(obj)

bpy.ops.object.select_all(action='DESELECT')
for obj in obj_list:
    obj.select_set(True)
    ORG_SET = False
    if obj.location == mathutils.Vector((0.0, 0.0, 0.0)):
        ORG_SET = True
#
## First pass
#
    if obj and obj.type == 'MESH':
        if ORG_SET:
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        # Select all faces
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')

        bm = bmesh.from_edit_mesh( bpy.context.object.data )

        # Reference selected face indices
        bm.faces.ensure_lookup_table()
        selFaces = [ f.index for f in bm.faces if f.select ]

        # Calculate the average normal vector
        avgNormal = Vector()
        for i in selFaces: avgNormal += bm.faces[i].normal
        avgNormal = avgNormal / len( selFaces )

        # Calculate the dot products between the average an each face normal
        dots = [ avgNormal.dot( bm.faces[i].normal ) for i in selFaces ]

        # Reversed faces have a negative dot product value
        reversedFaces = [ i for i, dot in zip( selFaces, dots ) if dot < 0 ]

        # Deselect all faces and (later) only select flipped faces as indication of change
        for f in bm.faces: f.select = False
        bm.select_flush( False )

        for i in reversedFaces:
            bm.faces[i].select = True
            bm.faces[i].normal_flip()  # Flip normal

        bm.select_flush( True )
        bpy.ops.object.mode_set(mode = 'OBJECT')
#
## Second pass
#
        faces=[]
        mesh = obj
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
        if auto_Flip:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
        if do_Snap:
            bpy.context.area.ui_type = 'VIEW_3D'        # Required for Snap to work
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.context.area.ui_type = 'TEXT_EDITOR'    # Reset back to normal
        if ORG_SET:
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    obj.select_set(False)
#
## Reset Selection back to before
#
for obj in obj_list:
    obj.select_set(True)
