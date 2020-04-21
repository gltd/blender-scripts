import bpy
import bmesh
import os

"""POA: find . -name '*.blend' -exec blender {} --background --python jwords_export.py"""


def export_gltf(filepath, **kwargs):
    print(f"exporting {filepath}")
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=kwargs.get('export_format', 'GLTF_SEPARATE'),
        ui_tab=kwargs.get('ui_tab', 'GENERAL'),
        export_copyright=kwargs.get('export_copyright', ""),
        export_image_format=kwargs.get('export_image_format', 'NAME'),
        export_texture_dir=kwargs.get('export_texture_dir', ""),
        export_texcoords=kwargs.get('export_texcoords', True),
        export_normals=kwargs.get('export_normals', True),
        export_draco_mesh_compression_enable=kwargs.get(
            'export_draco_mesh_compression_enable', False),
        export_draco_mesh_compression_level=kwargs.get(
            'export_draco_mesh_compression_level', 6),
        export_draco_position_quantization=kwargs.get(
            'export_draco_position_quantization', 14),
        export_draco_normal_quantization=kwargs.get(
            'export_draco_normal_quantization', 10),
        export_draco_texcoord_quantization=kwargs.get(
            'export_draco_texcoord_quantization', 12),
        export_draco_generic_quantization=kwargs.get(
            'export_draco_generic_quantization', 12),
        export_tangents=kwargs.get('export_tangents', False),
        export_materials=kwargs.get('export_materials', True),
        export_colors=kwargs.get('export_colors', True),
        export_cameras=kwargs.get('export_cameras', False),
        export_selected=kwargs.get('export_selected', False),
        export_extras=kwargs.get('export_extras', False),
        export_yup=kwargs.get('export_yup', True),
        export_apply=kwargs.get('export_apply', False),
        export_animations=kwargs.get('export_animations', True),
        export_frame_range=kwargs.get('export_frame_range', True),
        export_frame_step=kwargs.get('export_frame_step', 1),
        export_force_sampling=kwargs.get('export_force_sampling', True),
        export_nla_strips=kwargs.get('export_nla_strips', True),
        export_def_bones=kwargs.get('export_def_bones', False),
        export_current_frame=kwargs.get('export_current_frame', False),
        export_skins=kwargs.get('export_skins', True),
        export_all_influences=kwargs.get('export_all_influences', False),
        export_morph=kwargs.get('export_morph', True),
        export_morph_normal=kwargs.get('export_morph_normal', True),
        export_morph_tangent=kwargs.get('export_morph_tangent', False),
        export_lights=kwargs.get('export_lights', False),
        export_displacement=kwargs.get('export_displacement', False),
        will_save_settings=kwargs.get('will_save_settings', False),
        check_existing=kwargs.get('check_existing', True),
        filter_glob=kwargs.get('filter_glob', "*.glb;*.gltf")
    )


def apply_remesh(obj, **kwargs):
    remesh_modifier = obj.modifiers.new('RemeshMod', 'REMESH')
    remesh_modifier.octree_depth = kwargs.get('octree_depth', 12)
    remesh_modifier.scale = kwargs.get('scale', .025)
    remesh_modifier.use_smooth_shade = kwargs.get('use_smooth_shade', True)
    remesh_modifier.use_remove_disconnected = kwargs.get('use_remove_disconnected', True)
    bpy.ops.object.modifier_apply(modifier=remesh_modifier.name)


def apply_decimate(obj, **kwargs):
    decimate_modifier = obj.modifiers.new('DecimateMod', 'DECIMATE')
    decimate_modifier.ratio = kwargs.get('ratio', .01)
    decimate_modifier.use_collapse_triangulate = kwargs.get(
        'use_collapse_triangulate', True)
    bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)


def apply_modifiers(obj, remesh=None, decimate=None):
    if remesh:
        apply_remesh(obj, **remesh)
    if decimate:
        apply_decimate(obj, **decimate)


def import_gltf(name, object_directory):
    gltf_filename = f"{name}.gltf"
    raw_gltf_filepath = os.path.join(object_directory, gltf_filename)
    try:
        bpy.ops.import_scene.gltf(filepath=raw_gltf_filepath)
    except RuntimeError:
        # i wasn't consistent with the filenames. live and learn.
        print(f"Couldn't find: {raw_gltf_filepath}, will try alternative.")
        rm = f"_{object_directory.split('_')[-1]}"
        fixed_filename = raw_gltf_filepath.split("/")[-1].replace(rm, "")
        fixed_filepath = os.path.join(object_directory, fixed_filename)
        print(f"Importing {fixed_filepath}")
        bpy.ops.import_scene.gltf(filepath=fixed_filepath)


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


def write(name, read_parent_dir, write_path, **kwargs):
    read_path = os.path.join(read_parent_dir, name)
    import_gltf(name, read_path)
    for obj in bpy.data.objects:
        print("NAME", obj.name)
        if obj.type != "MESH":
            continue
        apply_modifiers(obj, **kwargs)
        full_write_directory = os.path.join(
            write_path, name.replace(".gltf", ""))
        os.makedirs(full_write_directory, exist_ok=True)
        filepath = os.path.join(full_write_directory, name)
        export_gltf(filepath)


def write_all(read_parent_dir, write_parent_dir, **kwargs):
    for name in os.listdir(read_parent_dir):
        if name in skip:
            continue
        write(name, read_parent_dir, write_parent_dir, **kwargs)


def add_uv_sphere(name="sad unnamed object"):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new('Basic_Sphere')
    # mesh.name = name
    basic_sphere = bpy.data.objects.new("Basic_Sphere", mesh)

    # Add the object into the scene.
    bpy.context.collection.objects.link(basic_sphere)

    # Select the newly created object
    bpy.context.view_layer.objects.active = basic_sphere
    basic_sphere.select_set(True)

    # Construct the bmesh sphere and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
    bm.to_mesh(mesh)
    bm.free()

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.ops.object.shade_smooth()


if __name__ == "__main__":
    skip = ['.DS_Store']
    read_parent_dir = "/Users/jak/Desktop/15pm/jwords/jwords-captures/exports/"
    write_parent_dir = "/Users/jak/Desktop/15pm/jwords/gltf-hack/"
    # write_all(read_parent_dir, write_parent_dir)
    name = "Scan3D_20200304204207_repaired"
    kwargs = {
        # "remesh": {
        #     "octree_depth": 5,
        # },
        "decimate": {
            "ratio": .1
        }
    }
    
    # add_uv_sphere(name="surface")
    write(name, read_parent_dir, write_parent_dir, **kwargs)
