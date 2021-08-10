from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Shader

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
        self.accept("1", self.enableShader)



    def loadDemo(self):

        self.shader = Shader.load(Shader.SL_GLSL,
                       vertex="shader.vert",
                       fragment="shader.frag")

        self.cubeModel = loader.loadModel("cube.egg")
        self.cubeModel.reparentTo(render)

        tex = loader.loadTexture("rainbow.png")
        self.cubeModel.setTexture(tex)



    def enableShader(self):
        self.cubeModel.setShader(self.shader)

app = demo()
app.run()