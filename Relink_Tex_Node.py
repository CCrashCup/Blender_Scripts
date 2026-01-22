# Relink Texture Node
#
#     Coded by Lofty
#
#     This is a short script to walk through every selected object
#     in a scene and relink the connection to the Base Color input
#     of the Principled BSDF node from a specific Image Texture node.
#
#     Note: Here is the layout template of the Image Texture Nodes.
#
#                               ┌──────┐
#                9   6   3   0  │ BSDF │
#               10   7   4   1  │      │
#               11   8   5   2  │      │
#                               └──────┘
#
import bpy

offset_TC = 0

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

count = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                mat = slot.material
                nodeTC = mat.node_tree.nodes[0]
                for node in mat.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        nodeB = node
                    if node.type == 'TEX_IMAGE':
                        if offset_TC > 0:
                            offset = f'{offset_TC/1000}'[-4:]
                        else:
                            offset = "ture"
                        if offset == node.name[-4:]:
                            nodeTC = node
                if not nodeTC == mat.node_tree.nodes[0]:
                    mat.node_tree.links.new(nodeTC.outputs['Color'],nodeB.inputs['Base Color'])
                    count += 1

print(f"{count} texture node groups relinked")
