'''
Created on 12.12.2010

@author: Praios
'''
from panda3d.core import NodePath, Vec4, Vec3, OrthographicLens, Point3, TransparencyAttrib

def texOf(np, size=256):
    altBuffer= makeBufferRelCent(np, size)[0]
    tex = altBuffer.getTexture()
    def dml(task):
        altBuffer.getEngine().removeWindow(altBuffer)
    base.taskMgr.doMethodLater(1, dml, "removeBuffer")
    return tex

def makePosRelCent(np):
    minv = Point3()
    maxv = Point3()
    np.calcTightBounds(minv, maxv)


    cent = (minv + maxv) / 2
    pos = Vec3(cent)
    pos.setY(minv.getY() - 1)

    rel = (abs(minv.getX()) + abs(maxv.getX()), abs(minv.getZ()) + abs(maxv.getZ()))
    return pos, rel, cent


def makeBufferRelCent(np, size=256):
    #we get a handle to the default window
    mainWindow = base.win

    #we now get buffer thats going to hold the texture of our new scene
    altBuffer = mainWindow.makeTextureBuffer("hello", size, size)
    altBuffer.setClearColor(Vec4(0.5, 0.5, 0.5, 0))
    #now we have to setup a new scene graph to make this scene
    altRender = NodePath("new render")

    #this takes care of setting up ther camera properly
    altCam = base.makeCamera(altBuffer)
    altCam.reparentTo(altRender)


    #get the teapot and rotates it for a simple animation
    teapot = NodePath("dummy")
    np.instanceTo(teapot)
    pos, rel, cent = makePosRelCent(teapot)
    lens = OrthographicLens()
    lens.setFilmSize(*rel)
    altCam.setPos(pos)
    altCam.node().setLens(lens)

    teapot.reparentTo(altRender)
    altBuffer.setOneShot(True)
    return altBuffer, rel, cent

def cardOf(np, size=256):
    altBuffer= makeBufferRelCent(np, size)[0]
    card = altBuffer.getTextureCard()
    def dml(task):
        altBuffer.getEngine().removeWindow(altBuffer)
    base.taskMgr.doMethodLater(1, dml, "removeBuffer")
    return card

def billboardOf(np, size=256):
    altBuffer, rel, cent = makeBufferRelCent(np, size)
    card = altBuffer.getTextureCard()
    card.setSx(rel[0] / 2)
    card.setSz(rel[1] / 2)
    dummy = NodePath("dummy")
    card.reparentTo(dummy)
    card.setPos(cent)
    dummy.setTransparency(TransparencyAttrib.MAlpha)
    dummy.setBillboardAxis()
    def dml(task):
        altBuffer.getEngine().removeWindow(altBuffer)
    base.taskMgr.doMethodLater(1, dml, "removeBuffer")
    return dummy
