# Adjust Vertex Color (Color Attribute)
#
#     Coded by Lofty
#
#     This is a short script to walk through every selected object
#     in a scene and adjust the vertex color value.
#     Set the "VC" variable to the index you want.
#
import bpy

VC = "vc_1"

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')
    
count = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for slot in obj.material_slots:
            if slot.material:
                mat = slot.material
                mat.use_nodes = True
                nodes = mat.node_tree.nodes
                for node in nodes:
                    if node.type == 'VERTEX_COLOR':
                        node.layer_name = VC
                        count += 1

print(f"{count} Color Attribute nodes adjusted")
