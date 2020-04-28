import bpy
import bmesh
import os
import yaml
from gltf import import_gltf, write_gltf
from config import load_config
from obj import move, center_selected_at_origin
from modifiers import apply_modifiers


def import_transform(parent_dir=None, name=None, **kwargs):
    read_path = os.path.join(parent_dir, name)
    import_gltf(name, read_path)
    for obj in bpy.data.objects:
        transform(obj, **kwargs)


def import_transform_all(sources=[], **kwargs):
    for source in sources:
        import_transform(**source, **kwargs)


def transform(obj, transforms={}, **kwargs):
    if obj.type != "MESH":
        return
    center_selected_at_origin(obj, **kwargs)
    apply_modifiers(obj, modifiers=transforms.get("modifiers", {}), **kwargs)
    move(obj, move=transforms.get("move", {}), **kwargs)


if __name__ == "__main__":
    config = load_config("./configs/jwords.yaml")
    import_transform_all(**config)
    write_gltf(**config)
