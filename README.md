# Blender Scriptin

## Setup

Blender looks for packages in the `modules` directory.

In order to more easily use third-party modules, I'm using pyenv and symlinking the site-packages for my pyenc to the modules folder of this directory.

For instance:

```
ln -s ~/.pyenv/versions/blender-scripting_3.6.10/lib/python3.6/site-packages/* . 
```

## Example Usage

```
blender empties/2.8a.blend --background --python jwords_export.py 
```

where `empties/2.8a.blend` is a saved empty project for your system's version of Blender and `blender` is aliased to your system's Blender binary. On Macs, that might be:

```
/Applications/Blender.app/Contents/MacOS/Blender
```

## Development

Blender loads scripts inside `startup` as packages. You can import anything in `startup` in a `scripts` script. For instance, you can add `startup/foo.py` and inside `scripts/bar.py` you can:

```
import foo
```

## Jwords
* [ ] do 3d scans with kinect in windows, and then for each:
  * [ ] convert from windows program to gltf
  * [ ] import all gltf together in blender, apply transform, remesh and decimate modifiers, export to new gltf

