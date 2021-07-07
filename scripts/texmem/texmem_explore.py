from direct.tkwidgets.MemoryExplorer import MemoryExplorer
from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Filename
from panda3d.core import GraphicsOutput
from direct.gui.DirectGui import *
import sys, os

from direct.showutil.TexMemWatcher import TexMemWatcher

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'show-buffers 1')

# https://docs.panda3d.org/1.10/python/reference/direct.showutil.TexMemWatcher#module-direct.showutil.TexMemWatcher

class driver(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        base.setSceneGraphAnalyzerMeter(True)
        #self.base.toggleTexMem(self)
        # Sometimes the texture memory viewer will crash on certain files
        self.TexMemWatcher = TexMemWatcher()
        self.accept('1', base.oobe)
        self.accept('2', base.oobeCull)
        base.bufferViewer.toggleEnable()
        
        self.loadGUI()
        # probably want to re-arrange this sometime
        self.accept('q', base.showCameraFrustum)
        self.accept('w', render.analyze)
        self.accept('e', self.resetCam)
        self.accept('r', self.clearScene)
        self.accept('t', base.toggleTexture)
        self.accept('y', base.toggleBackface)
        self.accept('u', base.printEnvDebugInfo)
        self.accept('i', self.sphere)
        self.accept('o', self.cube)

        
        #render.analyze()

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
    
    def graphicsLimit(self):
        self.TexMemWatcher.setLimit()
    
    def findLargestHole(self):
        print(self.TexMemWatcher.findLargestHole())
    
    def pipe(self):
        print(base.pipeList())
    
    def sphere(self):
        base.saveSphereMap(size=1024)
    
    def cube(self):
        base.saveCubeMap(size=1024)

app = driver()
app.run()