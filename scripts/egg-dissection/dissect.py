
from panda3d.egg import *

global uvNames
uvNames = set()

def traverseEgg(egg):
    global uvNames
    for child in egg.getChildren():
        if isinstance(child, EggGroup):
            # print(f"found an EggGroup: {child.getName()}")
            traverseEgg(child)
        if isinstance(child, EggTextureCollection):
            print(child.getTextures())
        if isinstance(child, EggTexture):
            print(f"found an EggTexture: {child}")
            print(f"texgen = {child.getTexGen()}\nname: {child.getFilename()}")
            uvName = child.getUvName()
            if uvName:
                #print(f"found a uvName: {uvName} from model {egg.egg_filename} with EggTexture {child.getName()}")
                uvNames.add(uvName)
        if isinstance(child, EggVertexPool):
            # print(f"found an EggVertexPool: {child.getName()}")
            for vpoolchild in child:  # should only contain EggVertexes
                pass
        
model = "model.egg"
egg = EggData()
egg.read(model)
traverseEgg(egg)
