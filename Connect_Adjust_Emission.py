# Connect - Adjust Emission
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene, connecting the Base Color
#   of the BSDF to the Emission of the BSDF.
#   Also modify the Emission Strength to the value desired.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

emit_power_old = 1.0
emit_power_new = 0.2

count = 0
mat_list = []
print("*****************************************************************************")
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material not in mat_list:
                mat = slot.material
                links = mat.node_tree.links
                nodes = mat.node_tree.nodes
                nodeB = nodes.get("Principled BSDF")
                nodeT = nodeB.inputs['Base Color'].links[0].from_node
                if bpy.app.version < (4, 0, 0):
                    if not nodeB.inputs['Emission'].is_linked:
                        links.new(nodeT.outputs[0],nodeB.inputs['Emission'])
                else:
                    if not nodeB.inputs['Emission Color'].is_linked:
                        links.new(nodeT.outputs[0],nodeB.inputs['Emission Color'])
                if nodeB.inputs["Emission Strength"].default_value == emit_power_old:
                    nodeB.inputs["Emission Strength"].default_value = emit_power_new
                count += 1
                mat_list.append(mat)

print("*****************************************************************************")
print(f"{count} materials got Emission adjusted.")
