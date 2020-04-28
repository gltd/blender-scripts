import bpy


def move(obj, move={}, **kwargs):
    obj.location.x += move.get("x", 0)
    obj.location.y += move.get("y", 0)
    obj.location.z += move.get("z", 0)


def center_selected_at_origin(obj, **kwargs):
    set_active(obj)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    unset_active(obj)
    # https://blender.stackexchange.com/questions/70098/how-to-move-an-objects-origin-to-the-center-of-its-bounding-box
    # obj.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")


def unset_active(obj):
    # bpy.context.active_object.select_set(False)
    bpy.data.objects[obj.name].select_set(False)


def set_active(obj):
    # https://blender.stackexchange.com/questions/38618/selecting-an-object-via-scripting-in-2020
    # to select the object in the 3D viewport,
    # this way you can also select multiple objects
    bpy.data.objects[obj.name].select_set(True)
