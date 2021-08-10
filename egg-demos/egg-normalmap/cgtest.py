
# old https://discourse.panda3d.org/t/per-pixel-lighting/474/9

from direct.interval.IntervalGlobal import*
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import os


class testShaders(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.addGeom()
        self.addLighting()
        self.TextureStage = TextureStage("ts")
        self.TextureStage.setMode(TextureStage.MNormal)
        base.accept('tab', base.bufferViewer.toggleEnable)
        base.accept('1', self.changeNormal)
        self.inv = False

    def addGeom(self):
        scene = render.attach_new_node("scene")
        self.cube = loader.loadModel("untitled.egg")
        self.cube.reparentTo(scene)
        self.cube.set_p(90)


    def addLighting(self):
        self.lightpivot = render.attachNewNode("lightpivot")
        self.lightpivot.setPos(0, 0, 4)
        self.lightpivot.hprInterval(10, LPoint3(360, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor((1, 1, 1, 1))
        plight.setAttenuation(LVector3(0.7, 0.05, 0)) # todo: make slider
        plnp = self.lightpivot.attachNewNode(plight)
        plnp.setPos(2, 0, 0)
        render.setLight(plnp)

        plight.show_frustum()

        # Also add an ambient light and set sky color.
        skycol = VBase3(135 / 255.0, 206 / 255.0, 235 / 255.0)
        base.set_background_color(skycol)

        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

        # Enable per-pixel lighting
        render.setShaderAuto()

    def changeNormal(self):
        if not self.inv:
            self.cube.setTexture(self.TextureStage, loader.loadTexture('normalmap3.png'), 1)
            self.inv = True
        else:
            self.cube.setTexture(self.TextureStage, loader.loadTexture('normalmap2.png'), 1)
            self.inv = False




app = testShaders()
app.run()