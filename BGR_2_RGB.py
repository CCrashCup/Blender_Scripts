# BGR to RGB
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene, adding and connecting a
#   BGR2RGB conversion before the Base Color of the BSDF.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

new = True
try:
    node = bpy.context.active_object.material_slots[0].material.node_tree.nodes.new("ShaderNodeSeparateColor")
except:
    new = False
if new:
    bpy.context.active_object.material_slots[0].material.node_tree.nodes.remove(node)
    R = 'Red'
    G = 'Green'
    B = 'Blue'
    C = 'Color'
else:
    R = 'R'
    G = 'G'
    B = 'B'
    C = 'Image'


count = 0
mat_list = []
print("*****************************************************************************")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat = slot.material
                links = mat.node_tree.links
                for node in mat.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        nodeB = node
                nodeC = nodeB.inputs['Base Color'].links[0].from_node
                sockC = nodeB.inputs['Base Color'].links[0].from_socket
                if new:
                    nodeS = mat.node_tree.nodes.new("ShaderNodeSeparateColor")
                    nodeJ = mat.node_tree.nodes.new("ShaderNodeCombineColor")
                else:
                    nodeJ = mat.node_tree.nodes.new("ShaderNodeCombineRGB")
                    nodeS = mat.node_tree.nodes.new("ShaderNodeSeparateRGB")
                nodeJ.location = (nodeC.location.x + 100), (nodeC.location.y)
                nodeS.location = (nodeC.location.x - 100), (nodeC.location.y)
                nodeC.location = (nodeC.location.x - 400), (nodeC.location.y)
#                links.new(sockC,nodeS.inputs['Color'])
#                links.new(nodeS.outputs['Red'],nodeJ.inputs['Blue'])
#                links.new(nodeS.outputs['Green'],nodeJ.inputs['Green'])
#                links.new(nodeS.outputs['Blue'],nodeJ.inputs['Red'])
#                links.new(nodeJ.outputs['Color'],nodeB.inputs['Base Color'])
                links.new(sockC,nodeS.inputs[C])
                links.new(nodeS.outputs[R],nodeJ.inputs[B])
                links.new(nodeS.outputs[G],nodeJ.inputs[G])
                links.new(nodeS.outputs[B],nodeJ.inputs[R])
                links.new(nodeJ.outputs[C],nodeB.inputs['Base Color'])

                count += 1
                mat_list.append(mat)

print("*****************************************************************************")
print(f"{count} materials got converted.")
