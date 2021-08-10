from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Filename
from panda3d.core import GraphicsOutput
from panda3d.core import TextureStage, TextureAttrib, TexGenAttrib
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

# todo: have slider to change texscale? <-- onscreen text for that
# https://docs.panda3d.org/1.10/python/programming/texturing/3d-textures#d-textures

# todo: learn about texture stages
# and texture projection
# https://docs.panda3d.org/1.10/python/programming/texturing/automatic-texture-coordinates

class demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.cam.setPos(0, -4, 0)
        self.base = ShowBase
        self.texScale = 0.2 # default
        self.texPosU = 0.44
        self.texPosV = 0.5
        self.texPosW = 0.2
        self.loadDemo()

        self.circleModel = loader.loadModel('btn/tt_m_gui_mat_nameShop.egg')
        self.loadGUI()


    def loadDemo(self):

        self.planeModel = loader.loadModel("plane.egg")
        self.planeModel.reparentTo(render)
        self.planeModel.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.planeModel.setTexProjector(TextureStage.getDefault(), render, self.planeModel)
        self.planeModel.setTexPos(TextureStage.getDefault(), self.texPosU, self.texPosV, self.texPosW)
        self.planeModel.setTexScale(TextureStage.getDefault(), self.texScale)
        self.planeModel.setPos(-4, 0, 0)
        self.planeModel.setTwoSided(True)

        self.cubeModel = loader.loadModel("cube.egg")
        self.cubeModel.reparentTo(render)
        self.cubeModel.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.cubeModel.setTexProjector(TextureStage.getDefault(), render, self.cubeModel)
        self.cubeModel.setTexPos(TextureStage.getDefault(), self.texPosU, self.texPosV, self.texPosW)
        self.cubeModel.setTexScale(TextureStage.getDefault(), self.texScale)
        self.cubeModel.setPos(4, 0, 0)

        self.sphereModel = loader.loadModel("spherehq.egg")
        self.sphereModel.reparentTo(render)
        self.sphereModel.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.sphereModel.setTexProjector(TextureStage.getDefault(), render, self.sphereModel)
        self.sphereModel.setTexPos(TextureStage.getDefault(), self.texPosU, self.texPosV, self.texPosW)
        self.sphereModel.setTexScale(TextureStage.getDefault(), self.texScale)

        tex = loader.load3DTexture("v2/cube_map_#.png")
        self.sphereModel.setTexture(tex)
        self.cubeModel.setTexture(tex)
        self.planeModel.setTexture(tex)

        self.printInfo()


    def loadGUI(self):
        titleHeight = 0.61
        textStartHeight = 0.45
        textRowHeight = 0.145
        leftMargin = -0.72
        buttonbase_xcoord = 0.45
        buttonbase_ycoord = 0.45
        button_image_scale = (0.7, 1, 1)
        button_textpos = (0, -0.02)
        options_text_scale = 0.052

        self.texScaleButton = DirectSlider(value=self.texScale,
                                          pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - textRowHeight * 4),
                                          thumb_relief=None, range=(0, 1), thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                          frameSize=(-0.5, 0.5, -0.08, 0.08),
                                          command=self.changeValue)

        self.texPosUButton = DirectSlider(value=self.texPosU,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - textRowHeight * 5),
                                  thumb_relief=None, range=(0, 1), thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeValue)

        self.texPosVButton = DirectSlider(value=self.texPosV,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - textRowHeight * 6),
                                  thumb_relief=None, range=(0, 1), thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeValue)

        self.texPosWButton = DirectSlider(value=self.texPosW,
                                  pos=(buttonbase_xcoord + 0.1, 0.0, buttonbase_ycoord - textRowHeight * 7),
                                  thumb_relief=None, range=(0, 1), thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                  frameSize=(-0.5, 0.5, -0.08, 0.08),
                                  command=self.changeValue)


    def changeValue(self):
        print(self.texScaleButton['value'])
        self.texScale = self.texScaleButton['value']
        self.texPosU = self.texPosUButton['value']
        self.texPosV = self.texPosVButton['value']
        self.texPosW = self.texPosWButton['value']

        self.planeModel.setTexPos(TextureStage.getDefault(), self.texPosU, self.texPosV, self.texPosW)
        self.planeModel.setTexScale(TextureStage.getDefault(), self.texScale)
        self.cubeModel.setTexPos(TextureStage.getDefault(), self.texPosU, self.texPosV, self.texPosW)
        self.cubeModel.setTexScale(TextureStage.getDefault(), self.texScale)
        self.sphereModel.setTexPos(TextureStage.getDefault(), self.texPosU, self.texPosV, self.texPosW)
        self.sphereModel.setTexScale(TextureStage.getDefault(), self.texScale)

    def printInfo(self):
        print("---------------------------------------")
        print("Number of Texture Stages")
        print(self.planeModel.findAllTextureStages())
        print("---------------------------------------")
        #print("write()")
        #print(self.planeModel.getNumTextureStages())
        #print("---------------------------------------")

app = demo()
app.run()