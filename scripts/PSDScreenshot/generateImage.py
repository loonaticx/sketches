"""
This method isn't the most robust way but it works. (edit: it kind of sucks a lot)
First, we'll toggle off the texture(s) to get only the vertex painting, extract that as an image.
Then we'll toggle back on the texture(s) but set the models color to remove the vertex painting, then extract that as an image.
The first image would have to be overlayed on top of the second image using the "Multiply" overlay

I don't know why but it's just extremely difficult to take different images since it seems like the code is running too fast before getting to process the change.
I tried adding in a task manager but the delay is manual since it also doesn't want to behave as intended. :v
"""
# https://photoshop-python-api.readthedocs.io/en/master/examples.html

from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import *
from direct.gui.DirectGui import *
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

        self.fileName = "image"
        self.fileFormat = ".png"
        self.showNode = NodePath()
        self.textureToggled = False
        #self.base.toggleTexMem(self)
        self.accept('o', base.oobe)

        self.loadGUI()

        # Just in case we have these enabled in the config...
        base.setFrameRateMeter(False)
        base.setSceneGraphAnalyzerMeter(False)


        self.accept('a', render.analyze)
        self.accept('r', self.resetCam)
        self.accept('c', self.clearScene)
        self.accept('s', self.test) # Hacky b/c hiding and showing in same method no work
        self.accept('s-up', self.setupTasks)


    def test(self):
        self.aspect2d.hide()
        base.toggleTexture()


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

    def saveScreenshot(self, type):
        filename = self.fileName + "_" +  type + self.fileFormat
        base.win.saveScreenshot(Filename(filename))
        print("Screenshot saved! {}".format(filename))

    def doScreenshot(self, task):
        self.saveScreenshot("shading")
        return task.done

    def doScreenshotAgain(self, task):
        self.saveScreenshot("flat")
        return task.done

    def fixScene(self, task):
        print(task)
        if task.name == "fix1":
            print("Toggling textures")
            base.toggleTexture()
        if self.model.getColor() == (1, 1, 1, 1):
            print("Fixing color")
            self.model.clearColor()
        if task.name == "fix2":
            self.aspect2d.show()
        return task.done


    def setupTasks(self):
        # i hate this
        #base.toggleTexture()
        taskMgr.doMethodLater(1, self.doScreenshot, 'ss1', sort=1)
        #taskMgr.doMethodLater(2, self.delay, 'delay1', sort=2)
        taskMgr.doMethodLater(2, self.fixScene, 'fix1', sort=3)
        taskMgr.doMethodLater(4, self.clear, 'clearpls', sort=4)
        taskMgr.doMethodLater(5, self.doScreenshotAgain, 'ss2', sort=5) # should i change over to uponDeath instead of this
        #taskMgr.doMethodLater(self.delay, 'delay3', sort=6)
        taskMgr.doMethodLater(7, self.fixScene, 'fix2', sort=7)

    def delay(self, task):
        if task.time < 2.0:
            return task.again
        print("Delay over")
        return task.done

    def clear(self, task):
        self.model.setColor(1, 1, 1, 1) # setting the last value to 0 does some VERY weird things.....



app = generate()
app.run()