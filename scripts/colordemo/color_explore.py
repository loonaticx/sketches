from direct.tkwidgets.MemoryExplorer import MemoryExplorer
from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from direct.gui.DirectGui import *
import sys, os

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $DEV_P3D')

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()
# TLDR: setColorScale = vertex painting, setColor = no vertex painting
class driver(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        self.defaultCamPos = base.cam.getPos()

        self.colorScale = [1] # default we will use setColorScale

        self.colorR = 1
        self.colorG = 1
        self.colorB = 1
        self.colorA = 1
        base.setSceneGraphAnalyzerMeter(False)

        self.loadGUI()

        self.accept('c', self.clearScene)
        self.accept('t', self.toggleTexture)


    def loadGUI(self):
        self.topButton = DirectButton(text=("Load model"),
                 scale=0.05, pos=(0, 0, -0.90), parent=base.aspect2d, command=self.loadFile)

        buttonSpacing = 0.1
        buttonbase_xcoord = -1.4
        buttonbase_ycoord = -0.20


        self.buttonColorR = DirectSlider(value=self.colorR,
                                pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 4),
                                range=(0, 1),
                                frameSize=(-0.5, 0.5, -0.08, 0.08),
                                command=self.changeColorValue)

        self.buttonColorB = DirectSlider(value=self.colorG,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 5),
                                  range=(0, 1),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeColorValue)

        self.buttonColorG = DirectSlider(value=self.colorB,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 6),
                                  range=(0, 1),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeColorValue)

        self.buttonColorA = DirectSlider(value=self.colorA,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 7),
                                  range=(0, 1),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeColorValue)

        # todo maybe make this a radio button instead
        self.buttonColorMode = [
        DirectRadioButton(text='setColorScale', variable=self.colorScale, value=[1],
                        scale=0.05, pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 3), command=self.changeColorValue),
        DirectRadioButton(text='setColor', variable=self.colorScale, value=[0],
                        scale=0.05, pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 2), command=self.changeColorValue)
        ]
        for button in self.buttonColorMode:
            button.setOthers(self.buttonColorMode)

    def changeColorValue(self):
        self.colorR = self.buttonColorR['value']
        self.colorG = self.buttonColorB['value']
        self.colorB = self.buttonColorG['value']
        self.colorA = self.buttonColorA['value']
        if self.colorScale[0]:
            for node in render.getChildren():
                node.clearColor()
                node.setColorScale(self.colorR, self.colorB, self.colorG, self.colorA)
        else:
            for node in render.getChildren():
                node.clearColorScale()
                node.setColor(self.colorR, self.colorB, self.colorG, self.colorA)

    def browseModel(self):
    # does direct.showbase.Loader.loadModel support any of the normal model types like obj/fbx?
        path = Path(askopenfilename(filetypes = (
            ("Panda3D Model Files", "*.egg;*.bam"),
            ("EGG", "*.egg"),
            ("BAM", "*.bam"))))

        return path

    def loadFile(self):
        filename = self.browseModel()
        if str(filename) == ".":
            return
        try:
            self.loadModel(filename)
        except:
            print(str(filename) + " could not be loaded!")

    def loadModel(self, file: str):
        self.clearScene()
        self.model = loader.loadModel(file)
        self.model.reparentTo(render)
        print("========================================")
        print("Loaded {}".format(file))


    def clearScene(self):
        if self.model is not None:
            self.model.removeNode()
            self.model = None


app = driver()
app.run()