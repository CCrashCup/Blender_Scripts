# Adjust Solid Color (Solid Display Color)
#
#     Coded by Lofty
#
#     This is a short script to walk through every selected object
#     in a scene and adjust the solid color value.
#     Set the "SC" variable to the color value you want.
#     Or make up your own color.
#
import bpy

sc_blue = (0.1, 0.1, 0.8, 1.0)
sc_green = (0.1, 0.8, 0.1, 1.0)
sc_red = (0.8, 0.1, 0.1, 1.0)
sc_yellow = (0.8, 0.8, 0.0, 1.0)

SC = sc_blue

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')
    
count = 0

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        obj.active_material.diffuse_color = SC
        count += 1

print(f"{count} Objects Display Color adjusted")
