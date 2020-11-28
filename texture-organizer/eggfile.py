import os
import shutil
import sys
from pathlib import Path
from panda3d.egg import EggData
from panda3d.egg import EggTextureCollection
from panda3d.egg import EggFilenameNode
from panda3d.egg import EggTexture
import dupFinder
#from panda3d.egg import EggObject

"""
  Egg Texture Organizer
  Reads all *.egg files found in a directory, locates their textures via texpath,
  and puts them in their own respected folder. Useful when sorting out Pandora textures.
  If texture cannot be located, a dummy image replaces the texture file of the output instead.
  Author: Loonatic
  Date: 11/25/2020
"""


eggDir = os.getcwd()
eggOutputDir = "output\\"
errorImage = "./error.png"
verboseList = False
outputFile = True
eggFiles = {} # egg filename, proposed filepath
texList = []

for file in os.listdir(eggDir):
    if os.path.isfile(os.path.join(eggDir, file)):
        if not file.endswith(".egg"):
            continue
        eggFiles[str(file)] = str(os.path.splitext(file)[0])

# print(eggFiles)

# Will be used to sort models accordingly [unused for now]
# Should shorten the file name in the future so new folders can be made for each element
modelPrefixList = {
    "bugRoom": "bugroom_",
    "tt_m_ara_est_house_": "house_"
}

def getTextureList(eggFile):
    texSet = set([])
    for child in eggFile.getChildren():
        if not isinstance(child, EggTexture):
            continue
        texSet.add(child.getFilename().getFullpath())
    return texSet

def cloneTextureDirs(textureList, model):
    for texture in textureList:
        modelDir = os.path.join(eggOutputDir, eggFiles[model])
        if not Path(modelDir).is_dir():
            print("Creating directory for %s" % eggFiles[model])
            os.makedirs(modelDir)

        filepath = Path(texture)
        filecheck = Path(os.path.join(eggOutputDir, eggFiles[model], os.path.basename(filepath))) # Check if texture already exists

        if filecheck.is_file():
            # print("Warning: %s already exists!" % filecheck)
            continue

        if not filepath.is_file(): # Texture does not exist
            print("Warning: %s does not exist!" % filepath)
            shutil.copyfile(errorImage, filecheck)
            continue

        shutil.copyfile(filepath, filecheck)

#if outputFile:
#    if path.exists('texList.txt'):
#        os.remove('texList.txt')

with open('texList.txt', 'w+') as fp:
    pass

for model in eggFiles:
    egg = EggData()
    egg.read(model)
    texList = getTextureList(egg)
    cloneTextureDirs(texList, model)
    if verboseList:
        print(model, texList)
    if outputFile:
        with open('texList.txt', 'a') as f:
            print("%s\n%s\n" % (model, texList), file=f)


# Post migration
dirList = []
for dirs in os.listdir(os.path.join(eggDir, eggOutputDir)):
    dirList.append(os.path.join(eggDir, eggOutputDir, dirs))

#print(os.path.join(eggDir, eggOutputDir))

dupFinder.findDuplicates(dirList, verboseList)
