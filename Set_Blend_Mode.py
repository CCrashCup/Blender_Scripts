# Set Blend Mode
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene and change the Blend Mode
#   to blend_mode value for each material with an Alpha input.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

#blend_mode = 'OPAQUE'
#blend_mode = 'CLIP'
#blend_mode = 'HASHED'
blend_mode = 'BLEND'

count = 0
mat_list = []
print("*****************************************************************************")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat_list.append(slot.material)
                mat = slot.material
                nodes = mat.node_tree.nodes
                nodeB = nodes.get("Principled BSDF")
                if nodeB.inputs['Alpha'].links:
                    mat.blend_method = blend_mode
                    count += 1

print("*****************************************************************************")
print(f"{count} materials alpha adjusted.")
