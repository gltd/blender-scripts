import bpy
import os


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


def export_gltf(filepath, **kwargs):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=kwargs.get("export_format", "GLTF_SEPARATE"),
        ui_tab=kwargs.get("ui_tab", "GENERAL"),
        export_copyright=kwargs.get("export_copyright", ""),
        export_image_format=kwargs.get("export_image_format", "NAME"),
        export_texture_dir=kwargs.get("export_texture_dir", ""),
        export_texcoords=kwargs.get("export_texcoords", True),
        export_normals=kwargs.get("export_normals", True),
        export_draco_mesh_compression_enable=kwargs.get(
            "export_draco_mesh_compression_enable", False
        ),
        export_draco_mesh_compression_level=kwargs.get(
            "export_draco_mesh_compression_level", 6
        ),
        export_draco_position_quantization=kwargs.get(
            "export_draco_position_quantization", 14
        ),
        export_draco_normal_quantization=kwargs.get(
            "export_draco_normal_quantization", 10
        ),
        export_draco_texcoord_quantization=kwargs.get(
            "export_draco_texcoord_quantization", 12
        ),
        export_draco_generic_quantization=kwargs.get(
            "export_draco_generic_quantization", 12
        ),
        export_tangents=kwargs.get("export_tangents", False),
        export_materials=kwargs.get("export_materials", True),
        export_colors=kwargs.get("export_colors", True),
        export_cameras=kwargs.get("export_cameras", False),
        export_selected=kwargs.get("export_selected", False),
        export_extras=kwargs.get("export_extras", False),
        export_yup=kwargs.get("export_yup", True),
        export_apply=kwargs.get("export_apply", False),
        export_animations=kwargs.get("export_animations", True),
        export_frame_range=kwargs.get("export_frame_range", True),
        export_frame_step=kwargs.get("export_frame_step", 1),
        export_force_sampling=kwargs.get("export_force_sampling", True),
        export_nla_strips=kwargs.get("export_nla_strips", True),
        export_def_bones=kwargs.get("export_def_bones", False),
        export_current_frame=kwargs.get("export_current_frame", False),
        export_skins=kwargs.get("export_skins", True),
        export_all_influences=kwargs.get("export_all_influences", False),
        export_morph=kwargs.get("export_morph", True),
        export_morph_normal=kwargs.get("export_morph_normal", True),
        export_morph_tangent=kwargs.get("export_morph_tangent", False),
        export_lights=kwargs.get("export_lights", False),
        export_displacement=kwargs.get("export_displacement", False),
        will_save_settings=kwargs.get("will_save_settings", False),
        check_existing=kwargs.get("check_existing", True),
        filter_glob=kwargs.get("filter_glob", "*.glb;*.gltf"),
    )


def write_gltf(write={}, **kwargs):
    write_dir = os.path.join(write.get("parent_dir"), write.get("name"))
    os.makedirs(write_dir, exist_ok=True)
    write_path = os.path.join(write_dir, "main")
    export_gltf(write_path)
