import bpy

def reset_scene():
    # Select objects by type
    for o in bpy.context.scene.objects:
        # if o.type == 'MESH':
        o.select_set(True)
        # else:
        # o.select_set(False)

    # Call the operator only once
    bpy.ops.object.delete()

    # Save and re-open the file to clean up the data blocks
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)


