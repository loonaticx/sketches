from direct.showbase.ShowBase import ShowBase
from pathlib import Path
from tkinter.filedialog import askopenfilename
from panda3d.core import Filename
from panda3d.core import GraphicsOutput
from direct.gui.DirectGui import *
import sys, os

# We need to import the tkinter library to
# disable the tk window that pops up.
# We use tk for the file path selector.
import tkinter as tk
root = tk.Tk()
root.withdraw()

# Force high quality for our render
from panda3d.core import loadPrcFileData
loadPrcFileData('', 'default-antialias-enable 1')
loadPrcFileData('', 'framebuffer-multisample 1')

"""
Controls:
s = Take screenshot
o = toggle oobe/free camera
r = reload loaded textures
e = reset rotation
1 = toggle shirt
2 = toggle bottoms
3 = load dogs body
4 = load dogm body
5 = load dogl body
mouse wheel up = zoom in
mouse wheel down = zoom out
mouse3(middle mouse click) = reset zoom
left arrow = rotate negative heading
right arrow = rotate positive heading
up arrow = rotate positive pitch
down arrow = rotate negative pitch

"""

"""
Todo:
Add onscreen text that displays the offset (camers zoom, clothing rotation, etc.) <-- will be hidden in screenshots
"""


class previewClothing(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.fileName = "output" # Output file name
        self.fileFormat = ".png"
        self.topTex = None
        self.sleeveTex = None
        self.bottomTex = None
        self.loadedTextures = [None, None, None]
        self.shirtVisible = True
        self.bottomsVisible = True
        self.torso = None
        self.type = 'm'
        self.botType = 'shorts' # just shorts/skirt
        self.defaultCamPos = base.cam.getPos()
        base.camera.hide()
        self.i = 1
        self.defaultH = 190 # todo: hotkey to reset all transformations
        self.currentH = self.defaultH
        self.defaultP = 0
        self.currentP = self.defaultP
        
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
        self.accept('o', base.oobe)
        self.accept('r', self.reloadTextures)
        self.accept('e', self.defaultRotation)
        self.accept('wheel_up', self.zoomCamera, [0.1])
        self.accept('wheel_down', self.zoomCamera, [-0.1])
        self.accept('mouse2', self.defaultCam)
        self.accept('arrow_left', self.rotateClothingH, [-5])
        self.accept('arrow_left-repeat', self.rotateClothingH, [-5])
        self.accept('arrow_right', self.rotateClothingH, [5])
        self.accept('arrow_right-repeat', self.rotateClothingH, [5])
        self.accept('arrow_up', self.rotateClothingP, [5])
        self.accept('arrow_up-repeat', self.rotateClothingP, [5])
        self.accept('arrow_down', self.rotateClothingP, [-5])
        self.accept('arrow_down-repeat', self.rotateClothingP, [-5])
        self.accept('1', self.toggleShirt)
        self.accept('2', self.toggleBottoms)
        self.accept('3', self.loadBody, ['s', self.botType])
        self.accept('4', self.loadBody, ['m', self.botType])
        self.accept('5', self.loadBody, ['l', self.botType])
        #self.accept('b', self.torso.showTightBounds)

       
    """
    ("tt_a_chr_dgX_Y_torso_1000.egg")
    X = s, m, l
    Y = shorts, skirt
    """
    def loadBody(self, type='m', gender='shorts'): # default: dogM_shorts
        self.clearBody()
        self.type = type
        self.botType = gender
        torsoModel = loader.loadModel("tt_a_chr_dg{}_{}_torso_1000.egg".format(type, gender)) # can rename this later
        self.torso = torsoModel.getChild(0)
        self.torso.reparentTo(render)
        #print(self.torso)
        
        
        #torsoModel.hide()
        for node in self.torso.getChildren():
            if (node.getName() != 'torso-top')\
            and (node.getName() != "torso-bot")\
            and (node.getName() != 'sleeves'):
                node.stash()
        # note: Z-up
        self.torso.setPos(0.00, 4.69, -0.235)
        self.torso.setH(self.currentH)
        self.torso.setP(self.currentP)
        if(type == 'l'):
            self.torso.setPos(self.torso.getX(), self.torso.getY()+ 0.91, self.torso.getZ() - 0.46)
        self.torso.setTwoSided(True)
        #print(self.topTex)
        if self.topTex is not None:
            self.torso.find('**/torso-top').setTexture(self.loadedTextures[0], 1)
        if self.sleeveTex is not None:
            self.torso.find('**/sleeves').setTexture(self.loadedTextures[1], 1)
        if self.bottomTex is not None:
            self.torso.find('**/torso-bot').setTexture(self.loadedTextures[2], 1)
        
    def clearBody(self):
        if self.torso is not None:
            self.torso.removeNode()
            self.torso = None

 
    def changeBotType(self):
        if self.botType == 'shorts':
            self.botType = 'skirt'
        elif self.botType == 'skirt':
            self.botType = 'shorts'
        else:
            self.botType = 'shorts' # Should never hit this but have a failsafe
        self.loadBody(self.type, self.botType)

 
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
        
        self.loadSButton = DirectButton(text=("dogs"),
                 scale=0.05, pos=(1.6, 0, -0.4), parent=base.aspect2d, command=self.loadBody, extraArgs=['s'])
        self.loadMButton = DirectButton(text=("dogm"),
                 scale=0.05, pos=(1.6, 0, -0.5), parent=base.aspect2d, command=self.loadBody, extraArgs=['m'])
        self.loadLButton = DirectButton(text=("dogl"),
                 scale=0.05, pos=(1.6, 0, -0.6), parent=base.aspect2d, command=self.loadBody, extraArgs=['l'])
        self.changeGenderButton = DirectButton(text=("Change gender"),
                 scale=0.05, pos=(1.6, 0, -0.7), parent=base.aspect2d, command=self.changeBotType)
        
    def saveScreenshot(self):
        # intent: Image number would increment if the file already exists just so it doesn't overwrite
        self.newfileName = self.fileName
        if not (os.path.isfile(self.newfileName)): # wip
            self.newfileName = self.fileName+str(self.i)
            self.i +=1
        
        filename = self.newfileName +self.fileFormat
        base.win.saveScreenshot(Filename(filename))
        self.aspect2d.show()
        print("Screenshot saved! {}".format(filename))
        

    def reloadTextures(self):
        for tex in self.loadedTextures:
            if tex: tex.reload()
    
    # temporary until i have a better way to do this lol    
    def toggleShirt(self):
        if self.torso is None:
            return
        if (self.shirtVisible):
            self.torso.find('**/torso-top').hide()
            self.torso.find('**/sleeves').hide()
            self.shirtVisible = False
        else:
            self.torso.find('**/torso-top').show()
            self.torso.find('**/sleeves').show()
            self.shirtVisible = True
    
    def toggleBottoms(self):
        if self.torso is None:
            return
        if (self.bottomsVisible):
            self.torso.find('**/torso-bot').hide()
            self.bottomsVisible = False
        else:
            self.torso.find('**/torso-bot').show()
            self.bottomsVisible = True
    
    
    # Rotate clothing
        
    def rotateClothingH(self, value):
        self.currentH = self.torso.getH() + value
        self.torso.setH(self.currentH)
        
    
    def rotateClothingP(self, value):
        self.currentP = self.torso.getP() + value
        self.torso.setP(self.currentP)
        
    def defaultRotation(self):
        self.currentH = self.defaultH
        self.torso.setH(self.currentH)
        self.currentP = self.defaultP
        self.torso.setP(self.currentP)
        
    # Camera Modifiers
    def defaultCam(self):
        base.cam.setPos(self.defaultCamPos)
        
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

    def openSleeves(self):
        filename = self.browseForImage()
        if str(filename) == ".":
            return
        try:
            self.loadSleeveTexture(filename)
        except:
            print(str(filename) + " could not be loaded!")

    def openBottom(self):
        filename = self.browseForImage()
        if str(filename) == ".":
            return
        try:
            self.loadBottomTexture(filename)
        except:
            print(str(filename) + " could not be loaded!")
        

app = previewClothing()
app.run()
    