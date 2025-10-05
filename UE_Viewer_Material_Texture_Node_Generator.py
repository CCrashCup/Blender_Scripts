# UE Viewer Material Texture Node Generator
#
#   Coded by Lofty
#
#   Adds texture nodes and connects them based on the material names.
#   This is oriented toward Unreal Engine extracted assets.
#   WIP
#   At present, it might save you a lot of manual work, but there is a
#   lot of inconsistency in the files. Not sure how much more I will chase this.
#

import os
import bpy

### Need to copy/paste the full path to the umodel output "Game" folder into 'base_path'.
### Need to copy/paste the full sub folder path to the .psk(x) and .mat files into 'modl_path'.
### Every back slash "\" needs to be doubled or turned into single forward slashes "/".
### Examples: "C:/MyFiles/" or "C:\\MyFiles\\"
### Because of this, you can only do one folder at a time, which is good, because it can be a little slow.
### Doing it in sections is safer as well, since Blender still crashes sometimes.

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

base_path = "D:/Solar Ash/"

modl_path = "/Game/Characters/NPCs/Engineer/"

material_path_table = ["/Game/Common/Materials/",
                       "/Game/Common/Materials/Textures/",
                       "/Game/Common/Materials/StandardMaterials/",
                       "/Engine/EngineMaterials/",
                       "/Game/Props/LightFixtures/", ]

props_ext = ".props.txt"
mat_ext   = ".mat"

def build_path(matl_name):
    
    retn_path = modl_path + matl_name
    bilt_path = base_path + retn_path + props_ext
    if not os.path.isfile(bilt_path):
        for mpt_path in material_path_table:
            retn_path = mpt_path + matl_name
            bilt_path = base_path + retn_path + props_ext
            if os.path.isfile(bilt_path):
                break
    return(retn_path)

    
def build_array(matl_path):
    
    matl_path_table = []

    props_path = base_path + matl_path + props_ext
    props_file = open(props_path, "r")
    aline = props_file.readline()
    if "Parent = MaterialInstanceConstant'" in aline:
        return(None)
    if "Parent = Material3'" in aline:
        beg_ndx = aline.find("'") + 1
        end_ndx = aline.rfind("'")
        add_path = os.path.splitext(aline[beg_ndx:end_ndx])[0]
        add_table = build_array(add_path)
        if len(add_table) > 0:
            for adt in add_table:
                if adt not in matl_path_table:
                    matl_path_table.append(adt)

    props_file.close()
    props_file = open(props_path, "r")        
    isTABL = False
    srch_strng = ["TextureParameterValues[",
                  "ParameterValue = Texture2D'",
                  "ReferencedTextures[",
                  "] = Texture2D'",
                  "Materials[",
                  "] = Material", ]

    for aline in props_file:
        if srch_strng[0] in aline[0:len(srch_strng[0])] \
        or srch_strng[2] in aline[0:len(srch_strng[1])] \
        or srch_strng[4] in aline[0:len(srch_strng[2])]:
            beg_ndx = aline.find("[") + 1
            end_ndx = aline.rfind("]")
            if int(aline[beg_ndx:end_ndx]) > 0:
                isTABL = True
            break

    if isTABL:
        for aline in props_file:
            if (srch_strng[1] in aline)                            \
            or (srch_strng[2] in aline and srch_strng[3] in aline) \
            or (srch_strng[4] in aline and srch_strng[5] in aline):
                beg_ndx = aline.find("'") + 1
                end_ndx = aline.rfind("'")
                mpath = os.path.splitext(aline[beg_ndx:end_ndx])[0]
                if mpath not in matl_path_table:
                    matl_path_table.append(mpath)

    props_file.close()
    return(matl_path_table)

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

count = 0
countO = 0
countT = 0
isBSDF = False
isTEX = False
isNORM = False
isDIFF = False
isHOLD = False
doNOODLE = True
table_size = 0
path_table = []
mat_list = []

### Change which line you use, based on what you want.
#for obj in bpy.data.objects:			# Entire scene
for obj in bpy.context.selected_objects:	# Only selected objects
    if obj.type == 'MESH':
        count += 1
        for slot in obj.material_slots:
            if slot.material:
                if slot.material in mat_list:
                    continue
                mat_list.append(slot.material)
                matl = slot.material
                matl.use_nodes = True
                isBSDF = False
                isTEX = False
                isNORM = False
                for node in matl.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        nodeBP = node
                        nodeBP.location = (nodeBP.location.x - 10), (nodeBP.location.y)
                        isBSDF = True
                    if node.type == 'TEX_IMAGE':
                        isTEX = True
                if isTEX == False:
                    countT += 1
                    matlname = os.path.splitext(slot.material.name)[0]
                    matlpath = build_path(matlname)
                    table_size = 0
                    path_table = build_array(matlpath)
                    if path_table:
                        table_size = len(path_table)
                    if "_Glass_" in matlname or "skylight" in matlname:
                        slot.material.blend_method = 'BLEND'
                        nodeBP.inputs['Alpha'].default_value = 0.75
                    mpath = base_path + matlpath + mat_ext
                    if os.path.isfile(mpath):
                        locX = 800
                        locY = 0
                        outnoodle = "Color"
                        innoodle = "Base Color"
                        isDIFF = False
                        mfile = open(mpath, "r")
                        doNOODLE = True
                        countO = 0
                        for aline in mfile:
                            pref_file = aline.splitlines()[0].rsplit("=")[1]
                            pref_path = base_path + matlpath + pref_file
                            if table_size > 0:
                                for path in path_table:
                                    tail = path.find(pref_file)
                                    if tail > -1:
                                        pref_path = base_path + path
                                        break
                            tpath = pref_path + ".tga"
                            if not os.path.isfile(tpath):
                                tpath = pref_path + ".png"
                            if not os.path.isfile(tpath):
                                tpath = pref_path + ".dds"
                            if not os.path.isfile(tpath):
                                continue
                            if os.path.isfile(tpath):
                                if "Diffuse=" in aline:
                                    if "_ddn" in aline:
                                        nodeNM = matl.node_tree.nodes.new(type='ShaderNodeNormalMap')
                                        nodeNM.location = (nodeBP.location.x - 600), (nodeBP.location.y - 1200)
                                        matl.node_tree.links.new(nodeNM.outputs['Normal'],nodeBP.inputs['Normal'])
                                        outnoodle = "Color"
                                        innoodle = "Color"
                                        locX = nodeNM.location.x - 300
                                        locY = nodeNM.location.y
                                        nodeACT = nodeNM
                                    else:
                                        outnoodle = "Color"
                                        innoodle = "Base Color"
                                        locX = nodeBP.location.x - 900
                                        locY = nodeBP.location.y + 600
                                        isDIFF = True
                                        isHOLD = True
                                        nodeACT = nodeBP
                                elif "Normal=" in aline:
                                    nodeNM = matl.node_tree.nodes.new(type='ShaderNodeNormalMap')
                                    nodeNM.location = (nodeBP.location.x - 600), (nodeBP.location.y - 1200)
                                    matl.node_tree.links.new(nodeNM.outputs['Normal'],nodeBP.inputs['Normal'])
                                    outnoodle = "Color"
                                    innoodle = "Color"
                                    locX = nodeNM.location.x - 300
                                    locY = nodeNM.location.y
                                    isNORM = True
                                    nodeACT = nodeNM
                                elif "SpecPower=" in aline:
                                    outnoodle = "Color"
                                    innoodle = "Specular"
                                    locX = nodeBP.location.x - 900
                                    locY = nodeBP.location.y - 300
                                    nodeACT = nodeBP
                                elif "Emissive=" in aline:
                                    outnoodle = "Color"
                                    innoodle = "Emission"
                                    locX = nodeBP.location.x - 900
                                    locY = nodeBP.location.y - 600
                                    nodeACT = nodeBP
                                elif "Opacity=" in aline:
                                    outnoodle = "Color"
                                    innoodle = "Alpha"
                                    slot.material.blend_method = 'BLEND'
                                    locX = nodeBP.location.x - 900
                                    locY = nodeBP.location.y - 600
                                    nodeACT = nodeBP
                                elif "Other[" in aline:
                                    if "T_MacroVariation" in aline:
                                        continue
                                    if "_AO" in aline:
                                        nodeMR = matl.node_tree.nodes.new(type='ShaderNodeMixRGB')
                                        nodeMR.location = (nodeBP.location.x - 300), (nodeBP.location.y + 300)
                                        matl.node_tree.links.new(nodeMR.outputs['Color'],nodeBP.inputs['Base Color'])
                                        nodeMR.blend_type = 'MULTIPLY'
                                        nodeMR.inputs['Fac'].default_value = 0.7
                                        if isDIFF:
                                            matl.node_tree.links.new(nodeHLD.outputs['Color'],nodeMR.inputs['Color1'])
                                        outnoodle = "Color"
                                        innoodle = "Color2"
                                        locX = nodeMR.location.x - 600
                                        locY = nodeMR.location.y
                                        nodeACT = nodeMR
                                    elif "_rough" in aline:
                                        outnoodle = "Color"
                                        innoodle = "Roughness"
                                        locX = nodeBP.location.x - 600
                                        locY = nodeBP.location.y - 600
                                        nodeACT = nodeBP
                                    elif "_m" in aline:
                                        outnoodle = "Color"
                                        innoodle = "Metallic"
                                        locX = nodeBP.location.x - 900
                                        locY = nodeBP.location.y
                                        nodeACT = nodeBP
                                    elif "_b" in aline:
                                        nodeBM = matl.node_tree.nodes.new(type='ShaderNodeBump')
                                        nodeBM.location = (nodeBP.location.x - 300), (nodeBP.location.y - 900)
                                        matl.node_tree.links.new(nodeBM.outputs['Normal'],nodeBP.inputs['Normal'])
                                        if isNORM:
                                            matl.node_tree.links.new(nodeNM.outputs['Normal'],nodeBM.inputs['Normal'])
                                        outnoodle = "Color"
                                        innoodle = "Height"
                                        locX = nodeBM.location.x - 600
                                        locY = nodeBM.location.y
                                        nodeACT = nodeBM
                                    else:
                                        if isDIFF:
                                            doNOODLE = False
                                        outnoodle = "Color"
                                        innoodle = "Base Color"
                                        locX = -1500
                                        locY = 600 + (countO * -300)
                                        countO += 1
                                        isDIFF = True
                                        isHOLD = True
                                        nodeACT = nodeBP

                                nodeTI = matl.node_tree.nodes.new(type='ShaderNodeTexImage')
                                nodeTI.location = (locX), (locY)
                                if doNOODLE:
                                    matl.node_tree.links.new(nodeTI.outputs[outnoodle],nodeACT.inputs[innoodle])
                                doNOODLE = True
                                nodeTI.image = bpy.data.images.load(tpath)
                                if isHOLD:
                                    nodeHLD = nodeTI
                                    isHOLD = False
                        mfile.close()

                    else:
                        apath = base_path + modl_path + matlname + ".tga"
                        if not os.path.isfile(apath):
                            apath = base_path + modl_path + matlname + ".png"
                        if not os.path.isfile(apath):
                            apath = base_path + modl_path + matlname + ".dds"
                        if os.path.isfile(apath):
                            outnoodle = "Color"
                            innoodle = "Base Color"
                            locX = 800
                            locY = 0
                            nodeACT = nodeBP
                            nodeTI = matl.node_tree.nodes.new(type='ShaderNodeTexImage')
                            nodeTI.location = (nodeBP.location.x - locX), (nodeBP.location.y - locY)
                            matl.node_tree.links.new(nodeTI.outputs[outnoodle],nodeACT.inputs[innoodle])
                            nodeTI.image = bpy.data.images.load(apath)

print("*******************************************************************************")
print(f"{countT} texture node groups relinked out of {count} mesh(es).")

