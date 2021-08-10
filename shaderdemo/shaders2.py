from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Shader
from panda3d.core import NodePath
from direct.gui.DirectGui import *
import sys, os
from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $RESOURCE_DIR')
loadPrcFileData('', 'default-antialias-enable 1')
loadPrcFileData('', 'framebuffer-multisample 1')
#loadPrcFileData('', 'want-pstats #t')
# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()


class generate(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        self.lastModelPath = ""
        self.showNode = NodePath()
        self.shader_rainbowGradient = Shader.load(Shader.SL_GLSL,
                    vertex="tt_sha_render_rainbowgrad.vert",
                    fragment="tt_sha_render_rainbowgrad.frag")

        self.shader_rainbow = Shader.load(Shader.SL_GLSL,
                    vertex="tt_sha_render_rainbow.vert",
                    fragment="tt_sha_render_rainbow.frag")

        self.shader_downsample = Shader.load(Shader.SL_GLSL,
            vertex="hdr_scene.vert.glsl",
            fragment="hdr_scene.frag.glsl")

        self.shader_fxaa = Shader.load(Shader.SL_GLSL,
            vertex="fxaa.vert.glsl",
            fragment="fxaa.frag.glsl")

        self.shader_drunk = Shader.load(Shader.SL_GLSL,
            vertex="tt_sha_render_drunk.vert",
            fragment="tt_sha_render_drunk.frag")

        self.accept('o', base.oobe)

        self.loadGUI()

        # Just in case we have these enabled in the config...
        base.setFrameRateMeter(False)
        base.setSceneGraphAnalyzerMeter(False)


        self.accept('a', render.analyze)
        self.accept('r', self.resetCam)
        self.accept('c', self.clearScene)
        self.accept('s', base.screenshot)


        self.accept("1", self.enableShader)
        self.accept("2", self.enableShader1)
        self.accept("3", self.enableShader2)
        self.accept("4", self.enableShader3)
        self.accept("0", self.enableShader0)



    def loadGUI(self):
        self.topButton = DirectButton(text=("Load model"),
                 scale=0.05, pos=(0, 0, -0.90), parent=base.aspect2d, command=self.loadFile)

    def browseModel(self):
        path = Path(askopenfilename(filetypes = (
            ("Image Files", "*.egg;*.bam"),
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

    def resetCam(self):
        base.oobe()
        base.cam.setPosHpr(0, 0, 0, 0, 0, 0)
        base.oobe()

    def clearScene(self):
        if self.model is not None:
            self.model.removeNode()
            self.model = None

    def enableShader0(self):
        self.model.setShader(self.shader_drunk)

    def enableShader(self):
        self.model.setShader(self.shader_rainbowGradient)

    def enableShader1(self):
        self.model.setShader(self.shader_rainbow)

    def enableShader2(self):
        self.model.setShader(self.shader_downsample)

    def enableShader3(self):
        self.model.setShader(self.shader_fxaa)


app = generate()
app.run()