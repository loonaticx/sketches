from panda3d.core import *
import sys

input = sys.argv[1]
mode = sys.argv[2]
mode = int(mode)

newfile = str(input).replace(".egg", ".bam")

loader = Loader.getGlobalPtr()
node = loader.loadSync(input)

if mode == 0:
    bam_normal = NodePath(node)
    bam_normal.writeBamFile(newfile)
elif mode == 3:
    bam_light = NodePath(node)
    bam_light.flattenLight()
    bam_light.writeBamFile(newfile)
elif mode == 2:
    bam_med = NodePath(node)
    bam_med.flattenMedium()
    bam_med.writeBamFile(newfile)
elif mode == 1:
    bam_strong = NodePath(node)
    bam_strong.flattenStrong()
    bam_strong.writeBamFile(newfile)
else:
    print("Invalid mode")
