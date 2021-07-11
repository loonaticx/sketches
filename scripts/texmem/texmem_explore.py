from direct.tkwidgets.MemoryExplorer import MemoryExplorer
from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from direct.gui.DirectGui import *
import sys, os

from direct.showutil.TexMemWatcher import TexMemWatcher
from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $DEV_P3D')

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()
# todo: make tex mem watcher spawn in a larger window so it can crash less
# https://docs.panda3d.org/1.10/python/reference/direct.showutil.TexMemWatcher#module-direct.showutil.TexMemWatcher

class driver(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        self.defaultCamPos = base.cam.getPos()
        base.setSceneGraphAnalyzerMeter(True)
        #self.base.toggleTexMem(self)
        # WARNING: Sometimes the texture memory viewer will crash on certain files
        self.TexMemWatcher = TexMemWatcher()
        self.accept('1', base.oobe)
        self.accept('2', base.oobeCull)
        self.accept('3', base.showCameraFrustum)
        #self.accept('4', base.hideCameraFrustum)

        self.loadGUI()

        self.accept('a', render.analyze)
        self.accept('r', self.resetCam)
        self.accept('c', self.clearScene)
        self.accept('t', base.toggleTexture)


    def loadGUI(self):
        # Todo: figure out how to reposition buttons when window changes size
        #guiFrame = DirectFrame(frameColor=(0, 0, 0, 1),
        #              frameSize=(-1, 1, -1, 1),
        #              pos=(1, -1, -1))
        self.topButton = DirectButton(text=("Load model"),
                 scale=0.05, pos=(0, 0, -0.90), parent=base.aspect2d, command=self.loadFile)

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

    def resetCam(self):
        base.cam.setPos(self.defaultCamPos)

    def clearScene(self):
        if self.model is not None:
            self.model.removeNode()
            self.model = None


app = driver()
app.run()