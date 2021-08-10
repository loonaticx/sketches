from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import *
from direct.gui.DirectGui import *
import sys, os
from direct.filter.FilterManager import FilterManager
from PIL import Image
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

# https://docs.panda3d.org/1.10/python/programming/render-to-texture/generalized-image-filters#extracting-more-information-from-the-scene
# ?????????

class generate(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        self.lastModelPath = ""
        self.showNode = NodePath()
        self.manager = FilterManager(base.win, base.cam)
        self.p = PNMImage()
        #self.base.toggleTexMem(self)
        self.accept('o', base.oobe)

        self.loadGUI()

        # Just in case we have these enabled in the config...
        base.setFrameRateMeter(False)
        base.setSceneGraphAnalyzerMeter(False)


        self.accept('a', render.analyze)
        self.accept('r', self.resetCam)
        self.accept('c', self.clearScene)
        self.accept('s', base.screenshot)
        self.accept('1', self.renderScene)






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

    def renderScene(self):
        tex = Texture()
        atex = Texture()
        dtex = Texture()
        self.manager.renderSceneInto(colortex=tex, auxtex=atex, depthtex=dtex)
        #self.manager.renderQuadInto(depthtex=dtex, colortex=tex)
        #self.manager.resizeBuffers()
        imgArr = tex.getRamImageAs("RGBA")
        #self.p.read(imgArr)
        print(imgArr)
        #im = Image.fromarray(imgArr)
        #im.save("h.png")



app = generate()
app.run()