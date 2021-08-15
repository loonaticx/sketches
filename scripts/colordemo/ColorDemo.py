"""
  Panda3D Color Demo
  Demonstrating setColor and setColorScale
  Author: Loonatic
  Date: 7/12/2021

  https://docs.panda3d.org/1.10/python/programming/render-attributes/tinting-and-recoloring

  setColorScale = This color will be modulated (multiplied) <-- for tinting
  setColor = If the model already had vertex colors, they will disappear - method is replacing those colors with a new one
"""

from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from panda3d.core import NodePath
from direct.gui.DirectGui import *
import sys, os

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $DEV_P3D')

# I can probably make this way better if I copy what I did for the explore script but w/e
class ColorDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.cam.setPos(0, -4, 0)
        self.np = NodePath()
        self.base = ShowBase
        self.defaultH = 35
        self.currentH = self.defaultH
        self.defaultP = 360
        self.currentP = self.defaultP
        self.colorR = 0.5
        self.colorG = 0.5
        self.colorB = 0.5
        self.colorA = 1
        base.setSceneGraphAnalyzerMeter(False)
        base.setFrameRateMeter(False)
        self.loadDemo()
        base.disableMouse()
        self.loadGUI()

        self.accept('1', self.toggleTexture)
        self.accept('2', self.clearColor)
        self.accept('3', self.clearColorScale)


        self.accept('arrow_left', self.rotateH, [-5])
        self.accept('arrow_left-repeat', self.rotateH, [-5])
        self.accept('arrow_right', self.rotateH, [5])
        self.accept('arrow_right-repeat', self.rotateH, [5])
        self.accept('arrow_up', self.rotateP, [5])
        self.accept('arrow_up-repeat', self.rotateP, [5])
        self.accept('arrow_down', self.rotateP, [-5])
        self.accept('arrow_down-repeat', self.rotateP, [-5])



    """
    cube.egg = Default primitive cube, no vertex color applied
    cube2.egg = Default primitive cube, but 5 (out of 6) faces have been applied vertex color.
    Two faces may look identical in color, one has no vertex painting applied & one has white vertex painting applied. Also double-sided.
    No material is set on either of these.
    """
    def loadDemo(self):
        cube1 = render.attachNewNode('cube1')
        cube2 = render.attachNewNode('cube2')
        cube3 = render.attachNewNode('cube3')
        cube4 = render.attachNewNode('cube4')
        self.cubeModel = loader.loadModel("cube.egg")
        self.cubeModel.reparentTo(cube1)
        self.cubeModel.setTexture(loader.loadTexture("tex.png"), 1)
        self.cubeModel.setPosHpr(-1.00, 1.45, 0.65, self.currentH, self.currentP, 0)
        self.cubeModel2 = self.cubeModel.copyTo(cube2)
        self.cubeModel2.setPosHpr(1.00, 1.45, 0.65, self.currentH, self.currentP, 0)


        self.cubeModel3 = loader.loadModel("cube2.egg")
        self.cubeModel3.reparentTo(cube3)
        self.cubeModel3.setTexture(loader.loadTexture("tex.png"), 1)
        self.cubeModel3.setPosHpr(-1.00, 1.45, -0.65, self.currentH, self.currentP, 0)
        self.cubeModel4 = self.cubeModel3.copyTo(cube4)
        self.cubeModel4.setPosHpr(1.00, 1.45, -0.65, self.currentH, self.currentP, 0)

    def loadGUI(self):
        buttonSpacing = 0.1
        buttonbase_xcoord = 0
        buttonbase_ycoord = -0.25

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

        # The reason why the 4th (alpha) slider doesn't do anything right now is because it is using RGB color mode & not RGBA
        self.buttonColorA = DirectSlider(value=self.colorA,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - buttonSpacing * 7),
                                  range=(0, 1),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeColorValue)

    def clearColorScale(self):
        self.cubeModel.clearColorScale()
        self.cubeModel3.clearColorScale()
        # Intentionally not resetting the values on color variables

    def clearColor(self):
        self.cubeModel2.clearColor()
        self.cubeModel4.clearColor()

    def changeColorValue(self):
        self.colorR = self.buttonColorR['value']
        self.colorG = self.buttonColorB['value']
        self.colorB = self.buttonColorG['value']
        self.colorA = self.buttonColorA['value']
        self.cubeModel.setColorScale(self.colorR, self.colorB, self.colorG, self.colorA)
        self.cubeModel2.setColor(self.colorR, self.colorB, self.colorG, self.colorA)
        self.cubeModel3.setColorScale(self.colorR, self.colorB, self.colorG, self.colorA)
        self.cubeModel4.setColor(self.colorR, self.colorB, self.colorG, self.colorA)

    # lazy, i know.

    def rotateH(self, value):
        self.currentH = self.currentH + value
        self.cubeModel.setH(self.currentH)
        self.cubeModel2.setH(self.currentH)
        self.cubeModel3.setH(self.currentH)
        self.cubeModel4.setH(self.currentH)

    def rotateP(self, value):
        self.currentP = self.currentP + value
        self.cubeModel.setP(self.currentP)
        self.cubeModel2.setP(self.currentP)
        self.cubeModel3.setP(self.currentP)
        self.cubeModel4.setP(self.currentP)

    def defaultRotation(self):
        self.currentH = self.defaultH
        self.cubeModel.setH(self.currentH)
        self.cubeModel2.setH(self.currentH)
        self.cubeModel3.setH(self.currentH)
        self.cubeModel4.setH(self.currentH)
        self.currentP = self.defaultP
        self.cubeModel.setP(self.currentP)
        self.cubeModel2.setP(self.currentP)
        self.cubeModel3.setP(self.currentP)
        self.cubeModel4.setP(self.currentP)


app = ColorDemo()
app.run()