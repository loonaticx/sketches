import os
import shutil
import sys
from pathlib import Path
from panda3d.egg import EggData
from panda3d.egg import EggTextureCollection
from panda3d.egg import EggFilenameNode
from panda3d.egg import EggTexture
import dupFinder

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
eggFiles = {}  # egg filename, proposed filepath
texList = []

for file in os.listdir(eggDir):
    if os.path.isfile(os.path.join(eggDir, file)):
        if not file.endswith(".egg"):
            continue # We only want egg files
        eggFiles[str(file)] = str(os.path.splitext(file)[0])


def getTextureList(eggFile):
    texSet = set([])
    for child in eggFile.getChildren():
        if not isinstance(child, EggTexture):
            continue
            # todo: could returning texset here be more optimal?
            # Textures are only referenced on top after the comment, shouldnt be anywhere else
        texSet.add(child.getFilename().getFullpath())
    return texSet


def cloneTextureDirs(textureList, model):
    modelDir = os.path.join(eggOutputDir, eggFiles[model])
    if not Path(modelDir).is_dir():
        print("Creating directory for %s" % eggFiles[model])
        os.makedirs(modelDir)
        # Copy the model file to the new directory
        # todo: make this an option/bool
        modelpath = Path(model)
        outputModelDir = Path(os.path.join(eggOutputDir, eggFiles[model], os.path.basename(
            modelpath)))
        shutil.copyfile(model, outputModelDir)

    for texture in textureList:
        filepath = Path(texture)
        filecheck = Path(os.path.join(eggOutputDir, eggFiles[model], os.path.basename(
            filepath)))  # Check if texture already exists

        fileroot = Path(os.path.join(eggOutputDir, eggFiles[model]))

        if filecheck.is_file():
            # print("Warning: %s already exists!" % filecheck)
            # Should only be triggered if script is ran twice
            continue

        if not filepath.is_file():  # Texture does not exist in maps folder
            print("Warning: %s does not exist!" % filepath)
            shutil.copyfile(errorImage, filecheck)
            continue

        shutil.copyfile(filepath, filecheck)

# if outputFile:
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
