from panda3d.core import *

input = "input.egg"

loader = Loader.getGlobalPtr()
node = loader.loadSync(input)

bam_normal = NodePath(node)
bam_normal.writeBamFile("output_normal.bam")

bam_light = NodePath(node)
bam_light.flattenLight()
bam_light.writeBamFile("output_light.bam")

bam_med = NodePath(node)
bam_med.flattenMedium()
bam_med.writeBamFile("output_medium.bam")

bam_strong = NodePath(node)
bam_strong.flattenStrong()
bam_strong.writeBamFile("output_strong.bam")
