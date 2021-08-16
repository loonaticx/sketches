# https://discourse.panda3d.org/t/visualize-scene-graph-python/27873
from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from direct.gui.DirectGui import *
import sys, os
import VisualizeScene

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $RESOURCE_DIR')

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()

class VisualizeDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        self.model = None
        vs = VisualizeScene.VisualizeScene()
        self.loadGUI()
        #vs.showSceneGraph(base.render)
        self.accept('1', vs.showSceneGraph, [base.render])

        # Sample usage
    def loadSample(self):
        child1 = [root.attach_new_node(f'child{i}') for i in range(10)]
        for child in child1:
            child.setPos(*np.random.rand(3))

        child2 = [child1[2].attach_new_node(f'child{i}') for i in range(5)]
        for child in child2:
            child.setHpr(*np.random.rand(3))

    def loadGUI(self):
        self.topButton = DirectButton(text=("Load model"),
                 scale=0.05, pos=(0, 0, -0.90), parent=base.aspect2d, command=self.loadFile)

    def browseModel(self):
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

    def clearScene(self):
        if self.model is not None:
            self.model.removeNode()
            self.model = None

app = VisualizeDemo()
app.run()