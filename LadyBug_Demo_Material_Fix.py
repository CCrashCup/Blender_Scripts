# LadyBug Demo Material Fix
#
#     Coded by Lofty
#
#     This is a short script to walk through the materials for
#     every selected object in a scene and link the connections
#     from the specified Image Texture nodes to the inputs of the
#     Principled BSDF node, and add/insert a Normal Map node
#     with conversion as needed. Made for the AMD LadyBug Demo.
#     https://www.guru3d.com/download/amd-ladybug-directx-11-demo
#
#     Note: Here is the layout template of the Image Texture Nodes.
#
#                               ┌──────┐
#                9   6   3   0  │ BSDF │
#               10   7   4   1  │      │
#               11   8   5   2  │      │
#                               └──────┘

import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

position_T0 = 0     # Texture not used
position_T1 = 1     # Texture Color
position_T2 = 2     # Texture is only correct for the ladybug mesh. It should be connected by hand.
position_T3 = 3     # Texture Roughness
position_T4 = 4     # Texture Normal
position_T5 = 5     # Texture not used


count = 0
mat_list = []
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat = slot.material
                mat_list.append(slot.material)
                try:
                    nodeBP = mat.node_tree.nodes.get("Principled BSDF")
                except:
                    continue
                nodeBP.location = (nodeBP.location.x - 10), (nodeBP.location.y)

                countT = 0
                nodeTC = nodeTC = nodeTN = None
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        if node.name[-4:] == f'{position_T1/1000}'[-4:]:
                            nodeTC = node
                        elif node.name[-4:] == f'{position_T3/1000}'[-4:]:
                            nodeTC = node
                        elif node.name[-4:] == f'{position_T4/1000}'[-4:]:
                            nodeTN = node
                        else:           # Collect extra nodes out of the way
                            node.location = (nodeBP.location.x + (300 + (countT * 50))), (nodeBP.location.y - (300 + (countT * 50)))
                            countT += 1
#
                if nodeTC:
                    nodeTC.location = (nodeBP.location.x - 1500), (nodeBP.location.y - 85)
                    mat.node_tree.links.new(nodeTC.outputs['Color'], nodeBP.inputs['Base Color'])

                    if nodeTR:
                        nodeTRI = mat.node_tree.nodes.new("ShaderNodeInvert")
                        nodeTRI.location = (nodeBP.location.x - 300), (nodeBP.location.y - 299)
                        mat.node_tree.links.new(nodeTRI.outputs['Color'], nodeBP.inputs['Roughness'])

                        nodeTR.image.colorspace_settings.name = 'Non-Color'
                        nodeTR.image.alpha_mode = 'CHANNEL_PACKED'
                        nodeTR.location = (nodeBP.location.x - 900), (nodeBP.location.y - 350)
                        mat.node_tree.links.new(nodeTR.outputs['Color'], nodeTRI.inputs['Color'])
                    #
                    ## Baby Poop Normal Map Conversion
                    #
                    if nodeTN:
                        nodeNM = mat.node_tree.nodes.new("ShaderNodeNormalMap")
                        nodeNM.location = (nodeBP.location.x - 300), (nodeBP.location.y - 603)
                        mat.node_tree.links.new(nodeNM.outputs['Normal'], nodeBP.inputs['Normal'])

                        nodeNCC = mat.node_tree.nodes.new("ShaderNodeCombineColor")
                        nodeNCC.location = (nodeBP.location.x - 600), (nodeNM.location.y)
                        mat.node_tree.links.new(nodeNCC.outputs['Color'], nodeNM.inputs['Color'])

                        nodeNSCBI = mat.node_tree.nodes.new("ShaderNodeInvert")
                        nodeNSCBI.location = (nodeBP.location.x - 900), (nodeBP.location.y - 745)
                        mat.node_tree.links.new(nodeNSCBI.outputs['Color'], nodeNCC.inputs['Blue'])

                        nodeNSC = mat.node_tree.nodes.new("ShaderNodeSeparateColor")
                        nodeNSC.location = (nodeBP.location.x - 1200), (nodeBP.location.y - 659)
                        mat.node_tree.links.new(nodeNSC.outputs['Red'], nodeNCC.inputs['Red'])
                        mat.node_tree.links.new(nodeNSC.outputs['Green'], nodeNCC.inputs['Green'])
                        mat.node_tree.links.new(nodeNSC.outputs['Blue'], nodeNSCBI.inputs['Color'])

                        nodeTN.image.colorspace_settings.name = 'Non-Color'
                        nodeTN.image.alpha_mode = 'CHANNEL_PACKED'
                        nodeTN.location = (nodeBP.location.x - 1500), (nodeNM.location.y)
                        mat.node_tree.links.new(nodeTN.outputs['Color'], nodeNSC.inputs['Color'])

                    count += 1

print("*****************************************************************************")
print(f"{count} texture node groups relinked")
