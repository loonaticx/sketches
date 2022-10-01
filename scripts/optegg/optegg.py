"""
Optimize eggfiles a la EggData

Alternative to egg-trans
"""

from panda3d.core import *
from panda3d.egg import EggData
import sys, subprocess


dryrun = False
input = str(sys.argv[1])

def optEggData(input, dryrun=False):
    egg = EggData()
    egg.read(input) # Assumes input is a correct filepath
    print("Collapsed {} equivalent materials.".format(egg.collapseEquivalentMaterials()))
    print("Collapsed {} equivalent textures.".format(egg.collapseEquivalentTextures()))
    if egg.originalHadAbsolutePathnames():
        print("Eggfile contained absolute filepaths !!") # bad
    else:
        print("Eggfile contains relative filepaths.") # good

    # NOTE: the following function calls may possibly cause issues with exported models. Look here if things are acting funky!
    egg.recomputePolygonNormals()
    # egg.recomputeVertexNormals()
    print("Removing {} invalid primitives".format(egg.removeInvalidPrimitives(True)))
    print("Removing {} unused vertices".format(egg.removeUnusedVertices(True)))
    # print("Triangulated {} new triangles produced".format(egg.triangulatePolygons(8)))
    # Convert to tri strips
    # egg.meshTriangles(8)

    if not dryrun:
        egg.writeEgg(input)
        
def optEggTrans(input):
    subprocess.run(['egg-trans', input] + "-FtTcCN -tbnall -np -o" + [input])
    
optEggTrans(input)
