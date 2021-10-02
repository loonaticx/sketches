"""
  ShaderManager
  Wrapper class for all things shaders

  Notice: It is important to remember that you can only call setShader one at a time, meaning
  you cannot have multiple shaders called on top of each other, unless they are combined within the same shader file.

  Currently, ShaderManager & it's child [TestShader] are intialized and setup when the client starts.

"""
from direct.directnotify import DirectNotifyGlobal
from direct.filter.FilterManager import FilterManager
from direct.showbase import DConfig


class ShaderManager:
    notify = DirectNotifyGlobal.directNotify.newCategory('ShaderManager')

    def __init__(self):
        if DConfig.GetBool('textures-power-2', 1):
            # This is a workaround, if ^ is enabled, the game would only render in the bottom left corner of the window.
            self.notify.warning("Cannot be initialized with texture-power-2 config enabled.")
            return


        """
        The FilterManager constructor requires you to provide a window which is rendering a scene,
        and the camera which is used by that window to render the scene.
        These are henceforth called the 'original window' and the 'original camera.'

        At the very moment ShaderManager only supports postprocessing shaders, which may be the reason why 2d gui is wonky w/ shaders.
        It seems that FilterManager is used for post processing shaders...?
        """
        self.manager = FilterManager(base.win, base.cam)
        # self.manager2d = None
        self.manager2d = FilterManager(base.win, base.cam2d)
        self.notify.info("Initialized ShaderManager")

    # Test shader for reproducing the 2D problem
    def initTestShader(self, parent):
        import TestShader as ts
        return ts.TestShader(parent, self.manager, self.manager2d)



