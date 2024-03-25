# Set Alpha Properties
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene and change various properties.
#   Be sure to adjust all settings before running.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

# Properties to set must be True otherwise False
AlphaConnect  = False
AlphaValue    = False
BlendMode     = False
#
## Be sure to set the intended value(s) below, that you want for any properties flagged True above.
#

alpha_connect_count  = 0

alpha_value = 1.0
alpha_value_count  = 0

#blend_mode = 'OPAQUE'
#blend_mode = 'CLIP'
#blend_mode = 'HASHED'
blend_mode  = 'BLEND'
blend_mode_count = 0


mat_list    = []
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat_list.append(slot.material)
                mat = slot.material
                links = mat.node_tree.links
                nodes = mat.node_tree.nodes
                nodeB = nodes.get("Principled BSDF")
                if AlphaConnect:
                    if not nodeB.inputs['Alpha'].is_linked:
                        nodeT = nodeB.inputs['Base Color'].links[0].from_node
                        links.new(nodeT.outputs['Alpha'],nodeB.inputs['Alpha'])
                        alpha_connect_count += 1
                if AlphaValue:
                    if not nodeB.inputs['Alpha'].is_linked:
                        nodeB.inputs['Alpha'].default_value = alpha_value
                        alpha_value_count += 1
                if BlendMode:
                    if nodeB.inputs['Alpha'].is_linked or (not nodeB.inputs['Alpha'].is_linked and AlphaValue):
                        mat.blend_method = blend_mode
                        blend_mode_count += 1

print("*****************************************************************************")
if AlphaConnect:
    print(f"{alpha_connect_count} materials had Alpha connected.")
if AlphaValue:
    print(f"{alpha_value_count} materials had Alpha set to {alpha_value}.")
if BlendMode:
    print(f"{blend_mode_count} materials had Alpha Blend Mode set to {blend_mode}.")
