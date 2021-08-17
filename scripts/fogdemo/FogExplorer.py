"""
  Panda3D Color Explorer
  Explore & modify models using setColor and setColorScale
  Author: Loonatic
  Date: 7/12/2021

  https://docs.panda3d.org/1.10/python/programming/render-attributes/tinting-and-recoloring

  setColorScale = This color will be modulated (multiplied) <-- for tinting
  setColor = If the model already had vertex colors, they will disappear - method is replacing those colors with a new one

  TLDR: setColorScale = keep vertex painting, setColor = remove vertex painting
"""

from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from direct.gui.DirectGui import *
import sys, os
import ToontownFogManager

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $RESOURCE_DIR')

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()
class FogExplorer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        self.defaultCamPos = base.cam.getPos()
        self.fog = ToontownFogManager.ToontownFogManager()
        self.fog.setFog(render)

        self.fogMode = [0] # default we will use Exponential

        self.colorR = 1
        self.colorG = 1
        self.colorB = 1

        self.expDensity = 0.5
        self.linRange_Onset = 0.5
        self.linRange_Opacity = 0.5
        base.setSceneGraphAnalyzerMeter(False)

        self.buttonSpacing = 0.1
        self.buttonbase_xcoord = -1.4
        self.buttonbase_ycoord = -0.20

        self.buttonList = []
        self.buttonExpDensity = None
        self.loadFogModifiers()

        self.loadGUI()
        self.addAuxButtons()

        self.accept('c', self.clearScene)
        self.accept('t', self.toggleTexture)


    def loadGUI(self):
        self.topButton = DirectButton(text=("Load model"),
                 scale=0.05, pos=(0, 0, -0.90), parent=base.aspect2d, command=self.loadFile)


        self.buttonColorR = DirectSlider(value=self.colorR,
                                pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 4),
                                range=(0, 1),
                                frameSize=(-0.5, 0.5, -0.08, 0.08),
                                command=self.changeColorValue)

        self.buttonColorB = DirectSlider(value=self.colorG,
                                  pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 5),
                                  range=(0, 1),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeColorValue)

        self.buttonColorG = DirectSlider(value=self.colorB,
                                  pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 6),
                                  range=(0, 1),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeColorValue)

        self.buttonColorMode = [
        DirectRadioButton(text='Linear Fog', variable=self.fogMode, value=[2],
                        scale=0.05, pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 4), command=self.addAuxButtons),
        DirectRadioButton(text='Exponential Fog (Squared)', variable=self.fogMode, value=[1],
                        scale=0.05, pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 3), command=self.addAuxButtons),
        DirectRadioButton(text='Exponential Fog', variable=self.fogMode, value=[0],
                        scale=0.05, pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 2), command=self.addAuxButtons)
        ]
        for button in self.buttonColorMode:
            button.setOthers(self.buttonColorMode)

    def loadFogModifiers(self):
        self.buttonExpDensity = DirectSlider(value=self.expDensity,
                                pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 1),
                                range=(0, 0.01),
                                frameSize=(-0.5, 0.5, -0.08, 0.08),
                                command=self.changeDensity)
        self.buttonExpDensity.hide()

        self.buttonLinearRange_Onset = DirectSlider(value=self.linRange_Onset,
                            pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 2),
                            range=(0, 0.1),
                            frameSize=(-0.5, 0.5, -0.08, 0.08),
                            command=self.setLinearRange)
        self.buttonLinearRange_Onset.hide()

        self.buttonLinearRange_Opacity = DirectSlider(value=self.linRange_Opacity,
                        pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.buttonSpacing * 1),
                        range=(0, 0.1),
                        frameSize=(-0.5, 0.5, -0.08, 0.08),
                        command=self.setLinearRange)
        self.buttonLinearRange_Opacity.hide()


    def addAuxButtons(self):
        self.removeAuxButtons()
        self.fog.setFogMode(self.fogMode[0])
        if self.fogMode[0] == 0 or self.fogMode[0] == 1: # Exponential
            self.buttonExpDensity.show()
            self.buttonList.append(self.buttonExpDensity)
        else:
            self.buttonLinearRange_Onset.show()
            self.buttonLinearRange_Opacity.show()
            self.buttonList.append(self.buttonLinearRange_Onset)
            self.buttonList.append(self.buttonLinearRange_Opacity)


    def removeAuxButtons(self):
        for btn in self.buttonList:
            btn.hide()
            self.buttonList.remove(btn)

    def changeDensity(self):
        self.expDensity = self.buttonExpDensity['value']
        self.fog.setDensity(self.expDensity)

    def setLinearRange(self):
        self.linRange_Onset = self.buttonLinearRange_Onset['value']
        self.linRange_Opacity = self.buttonLinearRange_Opacity['value']
        self.fog.setLinearRange(self.linRange_Onset, self.linRange_Opacity)


    def changeColorValue(self):
        self.colorR = self.buttonColorR['value']
        self.colorG = self.buttonColorB['value']
        self.colorB = self.buttonColorG['value']
        self.fog.setColor(self.colorR, self.colorG, self.colorB)



    def browseModel(self):
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


app = FogExplorer()
app.run()