# Texture Cutter
#
#       by Lofty
# Primary use is for dividing an image texture into
# individual image textures. This works on the principle
# that all cells in the texture may be unevenly spaced by
# any arbitrary sized dimensions. The arguments passed
# to it are the image file format and comma separated
# lists of row and column boundaries expressed in pixels.
#
# There is a partner app that is simpler to use.
# It is called Tex_Split.py
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
    print("arg 2 = Rows - Locations List")
    print("arg 3 = Columns - Locations List")
    print('Example: TexCut png "512,1024" "512,1024,1536,2048"')
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
    print(f"size_x = {size_x}\t size_y = {size_y}")

    top_y = 0
    for y in range(len(part_h)):
        top_x = 0
        for x in range(len(part_w)):
            outFile = outDir + "\\" + inFile[:-4] + f"_{y:02}-{x:02}.png"
            if part_w[x] > size_x:
                bot_x = size_x
            else:
                bot_x = part_w[x]
            if part_h[y] > size_y:
                bot_y = size_y
            else:
                bot_y = part_h[y]
            #print(f"x = {x}\t y = {y}\t top_x = {top_x}\t top_y = {top_y}\t bot_x = {bot_x}\t bot_y = {bot_y}")
            im_out = im_in.crop((top_x, top_y, bot_x, bot_y))
            im_out.save(outFile)
            top_x = part_w[x]
        top_y = part_h[y]
