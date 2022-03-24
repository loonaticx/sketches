from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Filename
from panda3d.core import GraphicsOutput
from direct.gui.DirectGui import *
import sys, os

from panda3d.core import loadPrcFileData

loadPrcFileData('', 'model-path $RESOURCE_DIR')

# We need to import the tkinter library to disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk

root = tk.Tk()
root.withdraw()


# https://docs.panda3d.org/1.10/python/reference/direct.showutil.TexMemWatcher#module-direct.showutil.TexMemWatcher

class generate(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        # Just in case we have these enabled in the config...
        base.setFrameRateMeter(False)
        base.setSceneGraphAnalyzerMeter(False)

        self.accept('o', base.oobe)

        self.loadGUI()

        self.accept('a', render.analyze)
        self.accept('r', self.resetCam)
        self.accept('c', self.clearScene)
        self.accept('t', base.toggleTexture)
        self.accept('b', base.toggleBackface)

        self.accept('1', self.sphere)
        self.accept('2', self.cube)
        self.accept('3', self.screenshot)

    def loadGUI(self):
        self.topButton = DirectButton(
            text = ("Load model"),
            scale = 0.05,
            pos = (0, 0, -0.90),
            parent = base.aspect2d,
            command = self.loadFile
        )

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

    """
    saveSphereMap(self, namePrefix='spheremap.png', defaultFilename=0, source=None, camera=None, size=256, cameraMask= 0111 1111 1111 1111 1111 1111 1111 1111, numVertices=1000, sourceLens=None)
    ** source = base.win [current window]
    ** camera = self.camera
    ** sourcelense = self.camLens
    ** cameraMask = cameraMask = PandaNode.getAllCameraMask()


    https://docs.panda3d.org/1.10/python/reference/direct.showbase.ShowBase#direct.showbase.ShowBase.ShowBase.saveSphereMap
    https://docs.panda3d.org/1.10/python/_modules/direct/showbase/ShowBase#ShowBase.saveSphereMap

    This works much like saveCubeMap(), and uses the graphics API's hardware cube-mapping ability to get a 360-degree view of the world.
    But then it converts the six cube map faces into a single fisheye texture, suitable for applying as a static environment map (sphere map).

    For eye-relative static environment maps, sphere maps are often preferable to cube maps because they require only a single texture and because they are supported on a broader range of hardware.

    Returns The filename if successful, or None if there is a problem.
    """

    def sphere(self, imgsize = 1024):
        base.saveSphereMap(namePrefix = "spheremap1-allverts.png", size = imgsize)
        base.saveSphereMap(namePrefix = "spheremap2-200verts.png", size = imgsize, numVertices = 200)
        base.saveSphereMap(namePrefix = "spheremap-10verts.png", size = imgsize, numVertices = 10)

    """
    saveCubeMap(self, namePrefix='cube_map_#.png', defaultFilename=0, source=None, camera=None, size=128, cameraMask= 0111 1111 1111 1111 1111 1111 1111 1111, sourceLens=None)[source]
    Similar to screenshot(), this sets up a temporary cube map Texture which it uses to take a series of six snapshots of the current scene, one in each of the six cube map directions. This requires rendering a new frame.

    Unlike screenshot(), source may only be a GraphicsWindow, GraphicsBuffer, or DisplayRegion; it may not be a Texture.

    Camera should be the node to which the cubemap cameras will be parented. The default is the camera associated with source, if source is a DisplayRegion, or base.camera otherwise.

    The filename if successful, or None if there is a problem.
    """

    def cube(self):
        base.saveCubeMap(size = 1024)


app = generate()
app.run()
