# Image Extension
#
#   Coded by Lofty
#   This is a short script to walk through every object in a scene
#   and change all image texture file name extensions. The initial
#   purpose is for pointing at files converted from .DDS to another
#   format like .PNG.
#   Change the source extension "from_ext" to fit your old image file type.
#   Change the target extension "to_ext" to fit your new image file type.
#   The "name" and the "filepath" are both changed to avoid confusion.
#   The "name" is for Blender internal reference only and does not
#   change any external file names.
#   The script will work even if you have not yet converted the files,
#   but you will then need to "Find Missing Files" after the conversion.
#
import os
import bpy

from_ext = ".dds"
to_ext = ".png"

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')
    
count = 0

for image in bpy.data.images:
    opath = bpy.data.images[count].filepath
    oname = bpy.data.images[count].name
    if not (os.path.splitext(oname)[1] == from_ext):
        oname = os.path.splitext(oname)[0]
    if opath > "":
        if os.path.splitext(oname)[1] == from_ext:
            npath = os.path.splitext(opath)[0] + to_ext
            nname = os.path.splitext(oname)[0] + to_ext
            bpy.data.images[count].filepath = npath
            bpy.data.images[count].name = nname
    count += 1

print("*****************************************************************************")
print(f"{count} image names processed.")
