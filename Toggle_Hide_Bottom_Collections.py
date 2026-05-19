# Toggle Hide Bottom Collections
#
#   coded by Lofty
#
#   Walks the Collection tree and hides any that don't have 
#   any nested Collections. Useful for when you want to look
#   at the contents of individual Collections without having
#   to manually hide all the others.
#
import bpy

# Set True or False then run.
TOGGLE = True

LIST = []

# Get LayerCollections - Recursive
def get_layer_children_recursive(p):
    LIST.append(p)
    for c in p.children:
        if c.rna_type.name == "Collection":
            LIST.append(c)
        get_layer_children_recursive(c) 

get_layer_children_recursive(bpy.context.scene.view_layers[0].layer_collection)

for c in [*set(LIST)]:
    if c.name != "Scene Collection":
        if not len(c.children):
            # Icon - Eye = Viewport
            c.hide_viewport = TOGGLE
# Other options that can also be toggled.
            # Icon - Checkbox = Isolation + Collapse
#            c.exclude = TOGGLE
            # Icon - Cursor = Item Selectability
#            bpy.data.collections[str(c.name)].hide_select = TOGGLE
            # Icon - Camera = Render Visibility
#            bpy.data.collections[str(c.name)].hide_render = TOGGLE
