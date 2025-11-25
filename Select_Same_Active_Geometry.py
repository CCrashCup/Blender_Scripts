# Select Same As Active Geometry
#
#   Coded by Lofty
#   To select all visible objects in the scene that are the same as the
#   currently active object based on vertex, edge, and polygon counts.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

tallyO = 0
tallyT = 0

holdActive = bpy.context.active_object
hA = holdActive.data

obj_select = []
print("***************************************************")

for obj in bpy.context.visible_objects:
    obj.select_set(False)
    if obj not in obj_select:
        if obj.type == 'MESH':
            mesh = obj.data
            tallyT += 1
            if len(mesh.vertices)  == len(hA.vertices) and \
               len(mesh.edges)     == len(hA.edges)    and \
               len(mesh.polygons)  == len(hA.polygons):
                obj_select.append(obj)
for obj in obj_select:
    obj.select_set(True)
    tallyO += 1
    
bpy.context.view_layer.objects.active = holdActive
print(f"{tallyO} objects selected. A total of {tallyT} objects examined.")

