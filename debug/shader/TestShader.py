"""
Note: Filters won't work properly if textures-power-2 is enabled or set to True

"""
from panda3d.core import TransparencyAttrib as ta
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import Shader
from panda3d.core import Texture

class TestShader:
    notify = DirectNotifyGlobal.directNotify.newCategory('TestShader')

    def __init__(self, parent, manager, manager2d=None): # parent=aspect2d
        self.parent = parent
        self.manager = manager
        self.manager2d = manager2d
        self.visible = False
        self.quad = None
        self.quad2d = None
        self.vertexShader = "shaders/base.vert"
        self.fragmentShader = "shaders/chromatic-abberation.frag"
        self.enabled = True
        self.tex2d = None
        self.tex3d = None
        self.loaded = self.setupShader()

    def setupShader(self):
        """
        Sets up the vertex and fragment shaders
        """
        shader = Shader.load(Shader.SLGLSL, self.vertexShader, self.fragmentShader)

        if shader is not None:
            colortex = Texture()  # Create an empty Texture object
            # quad is a GeomNode (NodePath) known as filter-base-quad
            self.quad = self.manager.renderSceneInto(colortex=colortex)  # Render-to-texture our scene (3D)
            self.quad.setShader(shader) # Load shaders
            #self.quad.setShaderInput("colorTexture", colortex) # Pass our rendered scene texture for the shader to process
            self.quad.setShaderInput("enabled", (self.enabled, self.enabled))
            #self.quad.setShaderInput("render2d", (0, 0))
            #self.quad.setTransparency(ta.MAlpha, 1)
            self.tex3d = colortex
            # 2D texture #
            if self.manager2d is not None:
                colortex2d = Texture()
                colortex2d.setClearColor((0, 0, 0, 0))
                self.quad2d = self.manager2d.renderSceneInto(colortex=colortex2d) # renderQuad doesn't do anything?
                self.quad2d.setShader(shader)
                #self.quad2d.setShaderInput("colorTexture", colortex2d)
                self.quad2d.setShaderInput("enabled", (self.enabled, self.enabled))
                #self.quad2d.setShaderInput("render2d", (0, 0))
                self.quad2d.setTransparency(ta.MAlpha, 1)
                self.tex2d = colortex2d
            self.notify.info('Loaded default shader')
            return True
        else:
            self.notify.warning('Cannot load default shader!')
            return False

    def getTex2D(self):
        return self.tex2d

    def getTex3D(self):
        return self.tex3d

    def getQuad(self):
        return self.quad

    def getQuad2D(self):
        return self.quad2d

