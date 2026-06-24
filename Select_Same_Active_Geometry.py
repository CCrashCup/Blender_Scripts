# Select Same As Active Geometry
#
#   Coded by Lofty
#   To select all visible objects in the scene that are the same as the
#   currently active object based on vertex, edge, and polygon counts.
#   Optionally include a UV Map compare. Set UV_TEST to True or False.
#   Optionally select only the duplicates. Set DUPES_ONLY to True or False.
#
import bpy

UV_TEST = False
DUPES_ONLY = False

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

def compare_uvs(obj1, obj2, tolerance=1e-5):
    
    if not obj1 or not obj2 or obj1.type != 'MESH' or obj2.type != 'MESH':
        return False
    uv_data1 = obj1.data.uv_layers.active.data
    uv_data2 = obj2.data.uv_layers.active.data
    if len(uv_data1) != len(uv_data2):
        return False
    for i, (loop1, loop2) in enumerate(zip(uv_data1, uv_data2)):
        if (loop1.uv - loop2.uv).length > tolerance:
            return False
    return True


tallyO = 0
tallyT = 0

holdActive = bpy.context.active_object
hA = holdActive.data
bpy.context.view_layer.objects.active = None

obj_select = []
print("***************************************************")

for obj in bpy.context.visible_objects:
    obj.select_set(False)
    if obj not in obj_select:
        if obj.type == 'MESH':
            tallyT += 1
            if obj == holdActive and DUPES_ONLY:
                continue
            mesh = obj.data
            if len(mesh.vertices)  == len(hA.vertices) and \
               len(mesh.edges)     == len(hA.edges)    and \
               len(mesh.polygons)  == len(hA.polygons):
                if UV_TEST:
                    if compare_uvs(holdActive, obj):
                        obj_select.append(obj)
                else:
                    obj_select.append(obj)
for obj in obj_select:
    obj.select_set(True)
    tallyO += 1
    
if not DUPES_ONLY:
    bpy.context.view_layer.objects.active = holdActive
print(f"{tallyO} objects selected. A total of {tallyT} objects examined.")

