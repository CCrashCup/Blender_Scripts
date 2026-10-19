# Tally Objects By UV Map Count
#
#   Coded by Lofty
#   To tally all objects in the scene based on the number of UV Maps.
#
import bpy

if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='OBJECT')

t_size = 50             # Make this larger if needed (unlikely)

tally = [0] * t_size

tallyT = 0

print("*" * 40)

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        t_index = len(obj.data.uv_layers)
        tally[t_index] += 1
        tallyT += 1


for t_index in range(t_size):
    if tally[t_index] > 0:
        print(f"Objects with {t_index} UV Maps = {tally[t_index]}")

print(f"A total of {tallyT} objects examined.")
print("*" * 40)
