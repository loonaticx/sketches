from direct.showbase.ShowBase import ShowBase
from panda3d.core import GraphicsOutput
from panda3d.core import NodePath
from direct.gui.DirectGui import *
import ShaderManager
from panda3d.core import loadPrcFileData
loadPrcFileData('', 'model-path $RESOURCE_DIR')
loadPrcFileData('', 'default-antialias-enable 1')
loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'textures-power-2 0')

class generate(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        base.setBackgroundColor(0, 0, 0)
        self.model = None
        self.sm= ShaderManager.ShaderManager()
        self.shader = None
        self.quad = None
        self.quad2D = None
        self.accept('o', base.oobe)
        self.accept('1', self.hideQuad2D)
        self.accept('2', self.showQuad2D)
        self.accept('3', base.render2d.hide)
        self.accept('4', base.render2d.show)
        self.accept('5', base.render.hide)
        self.accept('6', base.render.show)
        self.accept('7', self.snapshot3D)
        self.accept('8', self.snapshot2D)


        self.accept('0', self.loadShader)
        self.loadDemoModel()
        self.loadDemoGUI()


    def loadDemoModel(self):
        self.model = loader.loadModel("models/environment.egg.pz")
        self.model.reparentTo(render)
        self.model.setZ(-2)

    # Render2D stuff that gets affected by Quad2D
    def loadDemoGUI(self):
        guiModel = 'models/frame'
        guiModel2 = 'models/tt_m_gui_mat_namePanel'
        guiNode = loader.loadModel(guiModel)
        self.__aimPad = DirectFrame(image=guiNode.find('**/frame'), relief=None, pos=(0.7, 0, -0.553333), scale=0.1)
        guiNode.removeNode()
        self.upButton = DirectButton(parent=self.__aimPad, image=((guiModel2, '**/arrowTopA_up')), relief=None, pos=(1, 0, 0.221717))
        self.downButton = DirectButton(parent=self.__aimPad, image=((guiModel2, '**/arrowTopB_up')), relief=None, pos=(1, 0, -0.210101), image_hpr=(0, 0, 180))

    def loadShader(self):
        self.shader = self.sm.initTestShader(base.aspect2d)
        self.quad = self.shader.getQuad()
        self.quad2D = self.shader.getQuad2D()

    def hideQuad2D(self):
        if self.shader is None:
            return
        self.quad2D.hide()
    def showQuad2D(self):
        if self.shader is None:
            return
        self.quad2D.show()


    def snapshot3D(self): # Snapshot the quad @ base.cam
        tex = self.shader.tex3d
        # tex.clearImage()
        # tex.setClearColor((0, 0, 0, 1))
        # tex.setFormat(Texture.F_rgba)
        print(tex.getNumComponents())
        base.graphicsEngine.extractTextureData(tex, base.win.gsg)
        tex.write("snapshot3d.png")

    def snapshot2D(self): # Snapshot the quad @ base.cam2d
        tex = self.shader.tex2d
        # tex.clearImage()
        # tex.setClearColor((0, 0, 0, 1))
        # tex.setFormat(Texture.F_rgba)
        print(tex.getNumComponents())
        base.graphicsEngine.extractTextureData(tex, base.win.gsg)
        tex.write("snapshot2d.png")




app = generate()
app.run()