#
# Object Shade Reset
#
#   Coded by Lofty
# 
#   This script is used to walk through every selected object in a scene,
#   clearing any custom notmals data and then changing the object shading
#   based on the selected criteria.
#
import bpy
import math
from math import *

ASangle = 30        # AutoSmooth angle to use.
AutoSmooth = True   # If True, do AutoSmooth. If False, check Smooth.

Smooth = True       # If True and AutoSmooth is False, do Smooth. If both are False, do Flat.

Scount = 0

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode = 'OBJECT')

if AutoSmooth:
    bpy.ops.object.shade_smooth(use_auto_smooth = True)
elif Smooth:
    bpy.ops.object.shade_smooth(use_auto_smooth = False)
else:
    bpy.ops.object.shade_smooth(use_auto_smooth = False)
    bpy.ops.object.shade_flat()

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        if AutoSmooth:
            bpy.context.object.data.auto_smooth_angle = radians(ASangle)
        Scount += 1

print(f"Objects processed  = {Scount}")
