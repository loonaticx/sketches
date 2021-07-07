from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from panda3d.core import Filename
from panda3d.core import GraphicsOutput
from direct.gui.DirectGui import *

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()

# Force high quality for our render
from pandac.PandaModules import loadPrcFileData
loadPrcFileData('', 'default-antialias-enable 1')
loadPrcFileData('', 'framebuffer-multisample 1')

"""
Controls:
s = Take screenshot
o = oobe (buggy rn sadge)
r = reload loaded textures
"""

"""
Todo:
Torso only frame,
Bottom only frame too,
m and f body types,
different body types
maybe show back of outfit on the right side
Add onscreen text that displays the offset (camers zoom, clothing rotation, etc.)
"""


class previewClothing(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.fileName = "output.png" # Output file namee
        self.topTex = None
        self.sleeveTex = None
        self.bottomTex = None
        self.loadedTextures = [None, None, None]
        self.defaultCamPos = base.cam.getPos()
        
        # Just in case we have these enabled in the config...
        base.setFrameRateMeter(False)
        base.setSceneGraphAnalyzerMeter(False)
        
        base.disableMouse()

        self.loadBody()
        self.loadGUI()
        """
        If you want to change the default outfit texture (not desat), you can either
        change the texture path of the egg model(s) itself, or, alternatively, you can
        directly call to load specific textures, e.g.:
            self.loadTopTexture("path/to/texture.png")
        """
       
        self.accept('s', self.aspect2d.hide) # Hacky b/c hiding and showing in same method no work
        self.accept('s-up', self.saveScreenshot)
        self.accept('o', self.freeCam)
        self.accept('r', self.reloadTextures)
        self.accept('wheel_up', self.incrementCam)
        self.accept('wheel_down', self.decrementCam)
        self.accept('mouse2', self.defaultCam)
        self.accept('arrow_left', self.decrementH)
        self.accept('arrow_left-repeat', self.decrementH)
        self.accept('arrow_right', self.incrementH)
        self.accept('arrow_right-repeat', self.incrementH)
        #self.accept('b', self.torso.showTightBounds)

       

    """
    ("tt_a_chr_dgX_shorts_torso_1000.egg")
    X = s, m, l
    """
    def loadBody(self): # todo: args decide what body type to use
        torsoModel = loader.loadModel("tt_a_chr_dgm_shorts_torso_1000.egg") # can rename this later
        self.torso = torsoModel.getChild(0)
        self.torso.reparentTo(render)
        
        

        #torsoModel.hide()
        for node in self.torso.getChildren():
            if (node.getName() != 'torso-top')\
            and (node.getName() != "torso-bot")\
            and (node.getName() != 'sleeves'):
                node.stash()

        self.torso.setPosHprScale(0.00, 4.69, -0.235, 190.30, 0.00, 0.00, 1.00, 1.00, 1.00)
        self.torso.setTwoSided(True)

        
        
    def loadGUI(self):
        # Todo: figure out how to reposition buttons when window changes size
        #guiFrame = DirectFrame(frameColor=(0, 0, 0, 1),
        #              frameSize=(-1, 1, -1, 1),
        #              pos=(1, -1, -1))
        self.topButton = DirectButton(text=("Change Top"),
                 scale=0.05, pos=(-1.6, 0, -0.4), parent=base.aspect2d, command=self.openTop)
        self.sleeveButton = DirectButton(text=("Change Sleeve"),
                 scale=0.05, pos=(-1.6, 0, -0.5), parent=base.aspect2d, command=self.openSleeves)
        self.shortsButton = DirectButton(text=("Change Bottoms"),
                 scale=0.05, pos=(-1.6, 0, -0.6), parent=base.aspect2d, command=self.openBottom)

        
    def saveScreenshot(self):
        base.win.saveScreenshot(Filename(self.fileName))
        self.aspect2d.show()
        
    def freeCam(self):
        base.oobe()

    def reloadTextures(self):
        for tex in self.loadedTextures:
            if tex: tex.reload()
    
    def incrementH(self):
        self.rotateClothingH(1)
    
    def decrementH(self):
        self.rotateClothingH(-1)
    
    def rotateClothingH(self, value):
        self.torso.setH(self.torso.getH() + value)
    
    
    # Camera Modifiers
    def defaultCam(self):
        base.cam.setPos(self.defaultCamPos)
    
    def incrementCam(self):
        self.zoomCamera(0.1)
    
    def decrementCam(self):
        self.zoomCamera(-0.1)
    
    def zoomCamera(self, value):
        base.cam.setPos(base.cam.getX(), base.cam.getY() + value, base.cam.getZ())
    ###
        
    def browseForImage(self):
        path = Path(askopenfilename(filetypes = (
            ("Image Files", "*.jpg;*.jpeg;*.png;*.psd;*.tga"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("PNG", "*.png"),
            ("Photoshop File", "*.psd"),
            ("Targa", "*.tga"))))

        return path

    def loadTopTexture(self, file: str):
        tex = loader.loadTexture(file)
        self.topTex = file
        self.loadedTextures[0] = tex
        self.torso.find('**/torso-top').setTexture(tex, 1)

    def loadSleeveTexture(self, file: str):
        tex = loader.loadTexture(file)
        self.sleeveTex = file
        self.loadedTextures[1] = tex
        self.torso.find('**/sleeves').setTexture(tex, 1)

    def loadBottomTexture(self, file: str):
        tex = loader.loadTexture(file)
        self.bottomTex = file
        self.loadedTextures[2] = tex
        self.torso.find('**/torso-bot').setTexture(tex, 1)

    def openTop(self):
        filename = self.browseForImage()
        if str(filename) == ".":
            return
        try:
            self.loadTopTexture(filename)
        except:
            print(str(filename) + " could not be loaded!")
            messagebox.showerror("Error", "Unable to load texture: " + str(filename))

    def openSleeves(self):
        filename = self.browseForImage()
        if str(filename) == ".":
            return
        try:
            self.loadSleeveTexture(filename)
        except:
            print(str(filename) + " could not be loaded!")
            messagebox.showerror("Error", "Unable to load texture: " + str(filename))

    def openBottom(self):
        filename = self.browseForImage()
        if str(filename) == ".":
            return
        try:
            self.loadBottomTexture(filename)
        except:
            print(str(filename) + " could not be loaded!")
            messagebox.showerror("Error", "Unable to load texture: " + str(filename))
        

app = previewClothing()
app.run()
    