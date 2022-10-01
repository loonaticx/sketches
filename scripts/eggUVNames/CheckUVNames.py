"""
Use this to check for models with non-empty UVMap names (known to cause issues)
"""

import os

from panda3d.core import loadPrcFileData
loadPrcFileData("", "notify-level-linmath error")

from panda3d.egg import *

global uvNames
uvNames = set()
global problematicUV
problematicUV = False


def traverseEgg(egg):
    global uvNames
    global problematicUV
    for child in egg.getChildren():
        if isinstance(child, EggGroup):
            # print(f"found an EggGroup: {child.getName()}")
            traverseEgg(child)
        if isinstance(child, EggTexture):
            # print(f"found an EggTexture: {child.getName()}")
            uvName = child.getUvName()
            if uvName:
                print(f"found a uvName: {uvName} from model {egg.egg_filename} with EggTexture {child.getName()}")
                problematicUV = True
                uvNames.add(uvName)
                # Clear foo from <Scalar> uv-name { foo }
                child.clearUvName()
        if isinstance(child, EggVertexPool):
            # print(f"found an EggVertexPool: {child.getName()}")
            for vpoolchild in child:  # should only contain EggVertexes
                for uvName in uvNames:
                    uv = vpoolchild.modifyUvObj(uvName)
                    if uv:
                        # print(f"found uv {uvName}")
                        # Clear foo from <UV> foo { ... }
                        uv.setName('')



selectedPhases = ['3', '3.5', '4', '5', '5.5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
allFiles = []
modelFiles = {}
verbose = False

for phase in selectedPhases:
    if not os.path.exists('phase_%s' % phase):
        continue
    for root, _, files in os.walk('phase_%s' % phase):
        for file in files:
            if not file.endswith(".egg"):  # Input file
                continue
            # print("Adding %s" % file)
            file = os.path.join(root, file)
            allFiles.append(file)

resourceDir = os.getcwd()
for file in allFiles:
    if os.path.isfile(os.path.join(resourceDir, file)):
        if not file.endswith(".egg"):
            continue  # We only want egg files
        modelFiles[str(file)] = str(os.path.splitext(file)[0])


for model in modelFiles.items():
    problematicUV = False
    egg = EggData()
    egg.read(model[0])
    traverseEgg(egg)
    #print(f"Loaded model: {model}")
    # Uncomment to re-write out the egg file
    # if problematicUV:
        # egg.writeEgg(model[0])
