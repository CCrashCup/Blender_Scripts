# Connect - Adjust Alpha
#
#   Coded by Lofty
#   This is a short script to walk through the materials for
#   every selected object in a scene, connecting the "Alpha"
#   of the Image Texture node connected to the "Base Color"
#   of the Principled BSDF to the "Alpha" of the BSDF.
#   Also modify the Image Texture node Alpha to be Channel-Packed.
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
                try:
                    nodeB = nodes.get("Principled BSDF")
                except:
                    continue
                try:
                    nodeT = nodeB.inputs['Base Color'].links[0].from_node
                except:
                    continue
                if not nodeB.inputs['Alpha'].is_linked:
                    links.new(nodeT.outputs['Alpha'],nodeB.inputs['Alpha'])
                if nodeT.image:
                    nodeT.image.alpha_mode = 'CHANNEL_PACKED'
                count += 1
                mat_list.append(mat)

print("*****************************************************************************")
print(f"{count} materials got Alpha adjusted.")
