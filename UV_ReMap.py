# UV ReMap
#
#     Coded by Lofty
#
#     This is a short script to walk through the materials for
#     every visible object in a scene and link the Vector input
#     of every Image Texture node to the Vector output of the
#     added/inserted Texture Coordinate node and Mapping node.
#
#     Be sure to set the Location, Rotation, and Scale values.
#
#     Note: Here is the layout template of the Image Texture Nodes.
#
#     ┌─────┐  ┌─────┐             ┌──────┐
#     │ TEX │  │ MAP │  6   3   0  │ BSDF │
#     │     │  │     │  7   4   1  │      │
#     │     │  │     │      5   2  │      │
#     └─────┘  └─────┘             └──────┘

import bpy

# Mapping Defaults

Loc_X = 0.0
Loc_Y = 0.0
Loc_Z = 0.0

Rot_X = 0.0
Rot_Y = 0.0
Rot_Z = 0.0

Sca_X = 1.0
Sca_Y = 1.0
Sca_Z = 1.0

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

count = 0
mat_list = []
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
# Switch the 2 lines below to alter the scope of the changes
#for obj in bpy.context.selected_objects:
for obj in bpy.context.visible_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat_list.append(slot.material)
                mat = slot.material
                nodeBP = mat.node_tree.nodes.get("Principled BSDF")
                nodeBP.location = (nodeBP.location.x - 10), (nodeBP.location.y)

                nodeMAP = mat.node_tree.nodes.new("ShaderNodeMapping")
                nodeMAP.location = (nodeBP.location.x - 1200), (nodeBP.location.y)
                nodeCOR = mat.node_tree.nodes.new("ShaderNodeTexCoord")
                nodeCOR.location = (nodeBP.location.x - 1500), (nodeBP.location.y)
                mat.node_tree.links.new(nodeCOR.outputs['UV'], nodeMAP.inputs['Vector'])

                nodeMAP.inputs["Location"].default_value[0] = Loc_X
                nodeMAP.inputs["Location"].default_value[1] = Loc_Y
                nodeMAP.inputs["Location"].default_value[2] = Loc_Z

                nodeMAP.inputs["Rotation"].default_value[0] = Rot_X
                nodeMAP.inputs["Rotation"].default_value[1] = Rot_Y
                nodeMAP.inputs["Rotation"].default_value[2] = Rot_Z

                nodeMAP.inputs["Scale"].default_value[0] = Sca_X
                nodeMAP.inputs["Scale"].default_value[1] = Sca_Y
                nodeMAP.inputs["Scale"].default_value[2] = Sca_Z

                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        mat.node_tree.links.new(nodeMAP.outputs['Vector'], node.inputs['Vector'])
                        count += 1

print("*****************************************************************************")
print(f"{count} texture nodes remapped")
print("*****************************************************************************")
