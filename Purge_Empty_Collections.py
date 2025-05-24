# Purge Empty Collections from Outliner
#
#   Coded by Lofty
#   To delete Collections with no objects in them.
#   Change LOG_NAMES to True to get a list in the console.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

LOG_NAMES = False

def find_empty_groups():
    empty_groups = []
    print(f"{len(bpy.data.collections)} Total Collections.")
    for group in bpy.data.collections:
        if group.name == "Collection":
            continue
        if not group.all_objects:
            empty_groups.append(group)
    return empty_groups

empty_groups = find_empty_groups()

if empty_groups:
    print(f"{len(empty_groups)} Empty collections deleted.")
    for group in empty_groups:
        if LOG_NAMES:
            print(group.name)
        bpy.data.collections.remove(group)
else:
    print("No empty groups found.")
