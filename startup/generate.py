import bpy

# Note: haven't actually seen this work...
def add_uv_sphere(name="sad unnamed object"):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new("Basic_Sphere")
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

    bpy.ops.object.modifier_add(type="SUBSURF")
    bpy.ops.object.shade_smooth()
