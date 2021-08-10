from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Filename
from panda3d.core import GraphicsOutput
from panda3d.core import CullFaceAttrib
from panda3d.core import NodePath
from direct.gui.DirectGui import *
import sys, os

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $DEV_P3D')
loadPrcFileData('', 'screenshot-extension png')

# Only uncomment if you know what this will do
# I recommend looking at my "pstats" demo if you're unsure what pstats will do
# loadPrcFileData('', 'want-pstats #t')

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
        self.collisionsEnabled = False
        self.collisionsExist = False
        self.SGMeterToggled = False
        self.tightboundsToggled = False
        self.boundsToggled = False
        self.frontfaceCullingEnabled = False
        self.vertexPaintingToggled = False
        self.flatteningEnabled = False
        self.occludersEnabled = False
        self.occluderExist = False
        self.modelNodesEnabled = False
        self.modelNodesExist = False
        self.XYZAxis = loader.loadModel("models/misc/xyzAxis.bam")
        self.showNode = NodePath()

        self.xyz = None


        # Todo later, might do this in a different script
        #self.bloomEnabled = False
        #self.HDREnabled = False
        #self.ambientOcclusionEnabled = False
        #self.cartoonInkEnabled = False
        #self.sRGBEnabled = False
        #self.invertedEnabled = False

        self.accept('o', base.oobe)

        self.loadGUI()

        self.accept('q', self.loadLastModel)
        self.accept('a', render.analyze)
        self.accept('w', self.listNodes)
        self.accept('r', self.resetCam)
        self.accept('c', self.clearScene)
        self.accept('s', base.screenshot)


        self.accept('1', base.toggleShowVertices)
        self.accept('2', base.toggleWireframe)
        self.accept('3', base.toggleTexture)
        self.accept('4', self.toggleVertexPainting)
        self.accept('5', base.toggleBackface)
        self.accept('6', self.toggleFrontfaceCulling)
        #self.accept('7', self.toggleTightBounds) # todo: fix
        self.accept('7', self.toggleCollisionNodes)
        self.accept('o', self.toggleOccluderNodes)
        self.accept('p', self.toggleModelNodes)


    def enableFlatten(self):
        if self.model is not None:
            self.accept('8', self.model.flattenLight)
            self.accept('9', self.model.flattenMedium)
            self.accept('0', self.model.flattenStrong)
            return True
        else:
            return False


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
        self.lastModelPath = file
        self.model = loader.loadModel(file)
        self.model.reparentTo(render)
        print("========================================")
        print("Loaded {}".format(file))
        if not self.flatteningEnabled:
            self.flatteningEnabled = self.enableFlatten()

    def loadLastModel(self):
        self.loadModel(self.lastModelPath)

    def resetCam(self):
        base.oobe()
        base.cam.setPosHpr(0, 0, 0, 0, 0, 0)
        base.oobe()

    def clearScene(self):
        if self.model is not None:
            self.model.removeNode()
            self.model = None
        if self.flatteningEnabled:
            self.ignore('8')
            self.ignore('9')
            self.ignore('0')
            self.flatteningEnabled = False
        if self.xyz is not None:
            self.xyz.removeNode()
            self.xyz = None

    def toggleVertexPainting(self):
        if not self.vertexPaintingToggled:
            render.setColor(1, 1, 1)
            self.vertexPaintingToggled = True
        else:
            render.clearColor()
            self.vertexPaintingToggled = False

    def toggleFrontfaceCulling(self):
        if not self.frontfaceCullingEnabled:
            render.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
            self.frontfaceCullingEnabled = True
        else:
            render.clearAttrib(CullFaceAttrib)
            self.frontfaceCullingEnabled = False


    def toggleTightBounds(self):
        if not self.tightboundsToggled or self.boundsToggled:
            for node in render.getChild(0).getChildren():
                node.showTightBounds()
            self.tightboundsToggled = True
            self.boundsToggled = False
        else:
            for node in render.getChild(0).getChildren():
                node.hideBounds()
            self.tightboundsToggled = self.boundsToggled = False

    def toggleCollisionNodes(self):
        if not self.collisionsEnabled:
            for node in render.findAllMatches('**/CollisionNode'):
                self.collisionsExist = True
                self.collisionsEnabled = True
                node.show()
                print("Found collision node: {}".format(node))
                print("Collisions enabled")
            if not self.collisionsExist:
                print("No collision nodes found.")
        else:
            render.findAllMatches('**/+CollisionNode').hide()
            self.collisionsEnabled = False
            print("Collisions disabled")

    def toggleOccluderNodes(self):
        if not self.occludersEnabled:
            for node in render.findAllMatches('**/+OccluderNode'):
                self.occluderExist = True
                self.occludersEnabled = True
                node.show() # i haven't seen an occluder node before so idk if they have any geom
                print("Found occluder node: {}".format(node))
                print("Occluders enabled")
            if not self.occluderExist:
                print("No occluder nodes found.")
        else:
            render.findAllMatches('**/+OccluderNode').hide()
            self.occludersEnabled = False
            print("Occluders disabled")

    # todo: figure out the deal going on with the cycle assertion error :|
    def toggleModelNodes(self):
        if not self.modelNodesEnabled:
            for node in render.findAllMatches('**/+ModelNode'):
                self.modelNodesExist = True
                self.modelNodesEnabled = True
                self.xyz = self.XYZAxis.instanceTo(node) #copyTo bad
                self.xyz.setPos(node.getPos())
                self.xyz.setHpr(node.getHpr())
                node.show() # most of the time there's no geometry.
                print("Found ModelNode: {} at pos:{} hpr:{}".format(node, node.getPos(), node.getHpr()))
                print("ModelNodes visible")
            if not self.modelNodesExist:
                print("No model nodes found.")
        else:
            render.findAllMatches('**/ModelNode').hide()
            for node in self.XYZAxis.getChildren():
                node.removeNode()
            self.xyz.removeNode()
            self.xyz = None
            self.modelNodesEnabled = False
            print("Model nodes disabled")

    def listNodes(self):
        if self.model is None:
            return # can't return nodes of something that doesn't exist
        print()
        print("-x-x-x-x-x-x-x-x-x-x-x-x-")
        self.model.ls()
        print("-x-x-x-x-x-x-x-x-x-x-x-x-")
        print()


app = generate()
app.run()