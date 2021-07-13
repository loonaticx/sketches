import os
import shutil
import sys
from tkinter.filedialog import askopenfilename

from pathlib import Path
from panda3d.egg import EggData
from panda3d.egg import EggVertexUV
from panda3d.egg import EggVertex
from panda3d.egg import EggVertexPool
from panda3d.egg import EggTexture

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()

"""
it would be cool if we were able to 3d plot down
the vertexes within an egg file
but i have no fucking clue how that will turn out LMAO
"""

class epic():
    def __init__(self):
        self.egg = EggData()
        self.loadFile()
        list = self.getUVList(self.egg)
        self.setupGraph(list)

    def setupGraph(self, pointsList): #pointsList is LPoint2d
        for point in pointsList:
            #plt.plot(np.array([point[0], point[1]]))
            plt.scatter(point[0], point[1])
        plt.grid(True)
        plt.savefig("test.png")
        plt.title(self.egg.egg_filename)
        plt.show()

    def getUVList(self, eggFile):
        uvList = []
        # Some models don't get pass through the vertexPool check
        # so the UVs for smaller models don't get picked up
        for vertexPool in eggFile.getChildren():
            if not isinstance(vertexPool, EggVertexPool):
                continue
            for vertex in vertexPool:
                if not vertex.hasUv():
                    continue
                uvList.append(vertex.getUv()) #matplotlib lol
        return uvList

    def browseModel(self):
        path = Path(askopenfilename(filetypes = (
            ("Panda3D Model Files", "*.egg"),
            ("EGG", "*.egg"))))
        return path

    def loadFile(self):
        filename = self.browseModel()
        if str(filename) == ".":
            return
        try:
            self.egg.read(filename)
        except:
            print(str(filename) + " could not be loaded!")




app = epic()

