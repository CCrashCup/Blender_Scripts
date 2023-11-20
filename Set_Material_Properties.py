# Set Material Properties
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene and change various properties.
#   This is an expansion of Set Blend Mode.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

# Properties to set must be True otherwise False
BlendMode   = False
BackFace    = True

#
## Be sure to set the intended value(s) below, that you want for any properties flagged True above.
#

#blend_mode = 'OPAQUE'
#blend_mode = 'CLIP'
#blend_mode = 'HASHED'
blend_mode  = 'BLEND'
blend_mode_count = 0

#back_face   = False
back_face   = True
back_face_count = 0

mat_list    = []
print("*****************************************************************************")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat_list.append(slot.material)
                mat = slot.material
                nodes = mat.node_tree.nodes
                nodeB = nodes.get("Principled BSDF")
                if BlendMode:
                    if nodeB.inputs['Alpha'].links:
                        mat.blend_method = blend_mode
                        blend_mode_count += 1
                if BackFace:
                        mat.use_backface_culling = back_face
                        back_face_count += 1

print("*****************************************************************************")
if BlendMode:
    print(f"{blend_mode_count} materials had Alpha Blend Mode set.")
if BackFace:
    print(f"{back_face_count} materials had BackFace Culling set.")
