import bpy


def apply_remesh(obj, **kwargs):
    remesh_modifier = obj.modifiers.new("RemeshMod", "REMESH")
    remesh_modifier.octree_depth = kwargs.get("octree_depth", 12)
    remesh_modifier.scale = kwargs.get("scale", 0.025)
    remesh_modifier.use_smooth_shade = kwargs.get("use_smooth_shade", True)
    remesh_modifier.use_remove_disconnected = kwargs.get(
        "use_remove_disconnected", True
    )
    bpy.ops.object.modifier_apply(modifier=remesh_modifier.name)


def apply_decimate(obj, **kwargs):
    decimate_modifier = obj.modifiers.new("DecimateMod", "DECIMATE")
    decimate_modifier.ratio = kwargs.get("ratio", 0.01)
    decimate_modifier.use_collapse_triangulate = kwargs.get(
        "use_collapse_triangulate", True
    )
    bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)


def apply_modifiers(obj, modifiers={}, **kwargs):
    if modifiers.get("remesh"):
        apply_remesh(obj, **modifiers["remesh"])
    if modifiers.get("decimate"):
        apply_decimate(obj, **modifiers["decimate"])
