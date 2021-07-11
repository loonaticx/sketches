from direct.tkwidgets.MemoryExplorer import MemoryExplorer
from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData

# Set this to true (1) to compress textures as they are loaded into texture memory, if the driver supports this.
# Default is 0
loadPrcFileData('', 'compressed-textures 0')

# Set this true (1) to ask the graphics driver to compress textures, rather than compressing them in-memory first.
# Depending on your graphics driver, you may or may not get better performance or results by setting this true.
# Default is 0
loadPrcFileData('', 'driver-compress-textures 0')

# If you set this true, the screen will flash with textures drawn in a special mode that shows the mipmap detail level and texture size for each texture.
# Textures will be drawn in blue for mipmap level 0, yellow for mipmap level 1, and red for all higher mipmap levels.
# Brighter colors represent larger textures.
# Default is 0
loadPrcFileData('', 'gl-show-texture-usage 0')

# https://docs.panda3d.org/1.10/python/programming/texturing/texture-compression

class driver(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        base.cam.setPos(0, -7, 1)

        modelFile = 'demo_model/demo_rings.egg'
        self.modelDemo = loader.loadModel(modelFile)
        self.modelDemo.reparentTo(render)
        base.setSceneGraphAnalyzerMeter(True)
        self.base.toggleTexMem(self)
        self.accept('1', self.modifyTextures)
        self.accept('2', self.modifyTexture2048)
        self.accept('3', self.modifyTexture4096)
        self.accept('a', render.analyze)


        """
        Technically, we have a total of 3 + 1 textures initially loaded.
        Because we are using Panda's Scene Graph Analyzer meter (and possibly the fps meter),
        Panda will load a 256x256 font texture that will take up approx 64.0 Kb of memory.
        render.analyze() does not account for this texture.
        """

        # If we run this at runtime, the texture memory viewer won't
        # pick up the 3 initial textures. It will only display the overriding texture.
        # However, there will still 4 textures loaded in memory. (67.0 KiB active, 123 KiB total)
        # self.modifyTextures()
        render.analyze()

    def modifyTextures(self):
        for node in self.modelDemo.getChildren():
            # 32 x 32 texture, will take up 3.0 kb of texture memory. (Uncompressed)
            node.setTexture(loader.loadTexture('demo_model/texture3.jpg'), 1)

    ### WARNING: Make sure your tex mem viewer window is large enough for the following methods or it will crash :( ###
    ## The program may get unstable with these methods ##

    def modifyTexture2048(self):
        # 2048 x 2048 texture, will take up 12.0 MB of texture memory. (Uncompressed)
        self.modelDemo.findAllMatches('**/ring_top')\
            .setTexture(loader.loadTexture('demo_model/texture2048.png'), 1)


    def modifyTexture4096(self):
        # 4096 x 4096 texture, will take up 48.0 MB of texture memory. (Uncompressed)
        self.modelDemo.findAllMatches('**/ring_top')\
            .setTexture(loader.loadTexture('demo_model/texture4096.png'), 1)


app = driver()
app.run()