import bpy
import os

skip = ['.DS_Store']
read_directory = "/Users/jak/Desktop/15pm/jwords/jwords-captures/exports/"
write_directory = "/Users/jak/Desktop/15pm/jwords/objs-for-mesh-instances/"

for name in os.listdir(read_directory):
    if name in skip:
        continue
    object_directory = os.path.join(read_directory, name)
    gltf_filename = f"{name}.gltf"
    raw_gltf_filepath = os.path.join(object_directory, gltf_filename)
    print(f"importing filepath {raw_gltf_filepath}")
    try:
        bpy.ops.import_scene.gltf(filepath=raw_gltf_filepath)
    except RuntimeError:
        # i wasn't consistent with the filenames. live and learn.
        print(f"Failed on: {raw_gltf_filepath}")
        # continue
        rm = f"_{object_directory.split('_')[-1]}"
        fixed_filename = raw_gltf_filepath.split("/")[-1].replace(rm, "")
        fixed_filepath = os.path.join(object_directory, fixed_filename)
        bpy.ops.import_scene.gltf(filepath=fixed_filepath)
    obj_filepath = os.path.join(write_directory,f"{name}.obj")
    print(f"writing obj to {obj_filepath}")
    bpy.ops.export_scene.obj(filepath=obj_filepath)


    # blend_filename = f"{name}.blend"
    # write_filepath = os.path.join(write_directory, blend_filename)
    # bpy.ops.wm.save_as_mainfile(filepath=write_filepath)
