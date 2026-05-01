# UV Active By UV Map And Texture Node Count
#
#     Coded by Lofty
#
#   To make the specified UV Map be the Active UV Map for all visible
#   objects with the specified UV Map count and Texture node count.
#   Be sure to set the values before running this script.
#   
#
import bpy

UV_active = 1       # 1 thru 8 is normal. If your version of Blender allows more, go for it.
UV_count = 1        # Must be at least 1. Must not be less than UV_active number.
TX_count = 0        # 0 or more is allowed.

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

countU = 0
countT = 0

for obj in bpy.context.visible_objects:
    if obj.type == 'MESH':
        countT += 1
        if len(obj.data.uv_layers) == UV_count:
            for slot in obj.material_slots:
                mat = slot.material
                tex_node_count = len(mat.node_tree.nodes) - 2
                if tex_node_count == TX_count:
                    obj.data.uv_layers[(UV_active - 1)].active = True
                    obj.data.uv_layers[(UV_active - 1)].active_render = True
                    countU += 1

print(f"{countU} UV Maps set for {countT} total objects")
