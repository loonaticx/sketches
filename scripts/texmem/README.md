# Texture Memory Viewer Demo

``texmem_explore`` was my experimental script & includes a bunch of junk that's currently not related to texmem. I will clean it up later.

todo: add cool pictures and explanations and stuff

# Caveats

Panda's Texture Memory Viewer application can be a bit buggy. The program may crash when trying to open up various BAM/EGG files. As a workaround, I recommend upscaling the texture memory viewer window before opening a new model.

# Usage

Before running ``run.bat``, configure ``DEV_P3D`` to point to a directory with Toontown's resources (phase folders, extracted)
## Controls

Key | Usage
------------ | -------------
1 | Toggle OOBE (Out of body experience)
2 | Toggle OOBE culling
3 | Show the camera's frustum
a | Output info about the rendered scene
r | Reset camera position
c | Clear the loaded scene
t | Toggle textures

# Todo

- Figure out if there's a way to define the default window size for tex mem on launch.