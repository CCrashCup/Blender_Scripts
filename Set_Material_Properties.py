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
AlphaValue  = True
EmitPower   = True
BackFace    = True
BlendMode   = True

#
## Be sure to set the intended value(s) below, that you want for any properties flagged True above.
#

alpha_value = 1.0
alpha_value_count  = 0

emit_power  = 1.0
emit_power_count  = 0

back_face   = False
#back_face   = True
back_face_count = 0

blend_mode = 'OPAQUE'
#blend_mode = 'CLIP'
#blend_mode = 'HASHED'
#blend_mode  = 'BLEND'
blend_mode_count = 0

mat_list    = []
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat_list.append(slot.material)
                mat = slot.material
                nodes = mat.node_tree.nodes
                nodeB = nodes.get("Principled BSDF")
                if AlphaValue:
                    if not nodeB.inputs['Alpha'].links:
                        nodeB.inputs['Alpha'].default_value = alpha_value
                        alpha_value_count += 1
                if EmitPower:
                    nodeB.inputs['Emission Strength'].default_value = emit_power
                    emit_power_count += 1
                if BackFace:
                    mat.use_backface_culling = back_face
                    back_face_count += 1
                if BlendMode:
                    if nodeB.inputs['Alpha'].links or (not nodeB.inputs['Alpha'].links and AlphaValue):
                        mat.blend_method = blend_mode
                        blend_mode_count += 1

print("*****************************************************************************")
if AlphaValue:
    print(f"{alpha_value_count} materials had Emission Strength set to {alpha_value}.")
if BackFace:
    print(f"{emit_power_count} materials had Emission Strength set to {emit_power}.")
if BackFace:
    print(f"{back_face_count} materials had BackFace Culling set to {back_face}.")
if BlendMode:
    print(f"{blend_mode_count} materials had Alpha Blend Mode set to {blend_mode}.")
