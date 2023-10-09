# Add Gamma Node
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene, adding and connecting a
#   Gamma node before the Base Color of the BSDF. Set the 
#   default gamma_value desired.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

gamma_value = 2.2

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
                nodeG = mat.node_tree.nodes.new("ShaderNodeGamma")
                nodeG.inputs['Gamma'].default_value = gamma_value
                nodeG.location = (nodeC.location.x + 100), (nodeC.location.y)
                nodeC.location = (nodeC.location.x - 100), (nodeC.location.y)
                links.new(sockC,nodeG.inputs['Color'])
                links.new(nodeG.outputs['Color'],nodeB.inputs['Base Color'])
                count += 1
                mat_list.append(mat)

print("*****************************************************************************")
print(f"{count} materials got Gamma inserted.")
