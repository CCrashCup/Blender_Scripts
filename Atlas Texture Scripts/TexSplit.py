# Texture Splitter
#
#       by Lofty
# Primary use is for dividing an Atlas texture into
# individual image textures. This works on the principle
# that all cells in the Atlas are evenly spaced by
# standard power-of-2 sized dimensions. The arguments
# passed to it are the Atlas image file format and the
# number of rows and the number of columns.
#
# There is a partner app allowing more flexibility.
# It is called Tex_Cut.py
#
import os, sys
import glob
from PIL import Image

outDir = "New"

i = 0
for s in sys.argv:
    i += 1
if not (i == 4):
    print("arg 1 = Input Filetype")
    print("arg 2 = Rows - Vertical Divisions")
    print("arg 3 = Columns - Horizontal Divisions")
    print("Example: TexSplit png 2 4")
    print(" ")
    sys.exit("** EXIT - Argument count error.**")

i = 0
for s in sys.argv:
    if i > 0:
        print(f"sys.argv[{i}] = {sys.argv[i]}")
    i += 1

try:
    os.makedirs(outDir)
except FileExistsError:
    pass

glbsrch = "*." + sys.argv[1]
part_h_list = sys.argv[2].split(',')
part_h = [int(s) for s in part_h_list]
part_w_list = sys.argv[3].split(',')
part_w = [int(s) for s in part_w_list]

for inFile in glob.glob(glbsrch, recursive=False):
    print(f"Processing file: {inFile}")
    im_in = Image.open(inFile)

    size_x, size_y = im_in.size
    size_w = size_x / part_w[0]
    size_h = size_y / part_h[0]
    
    for y in range(part_w[0]):
        for x in range(part_h[0]):
            outFile = outDir + "\\" + inFile[:-4] + f"_{y:02}-{x:02}.png"
            top_x = x * size_w
            top_y = y * size_h
            bot_x = top_x + size_w
            bot_y = top_y + size_h
            #print(f"x = {x}\t y = {y}\t top_x = {top_x}\t top_y = {top_y}\t bot_x = {bot_x}\t bot_y = {bot_y}")
            im_out = im_in.crop((top_x, top_y, bot_x, bot_y))
            im_out.save(outFile)
