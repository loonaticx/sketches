from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import Geom, GeomPoints, GeomNode, NodePath
from panda3d.core import TextureStage, TexGenAttrib, TransparencyAttrib
from panda3d.core import AmbientLight, DirectionalLight, Vec4
from random import uniform

# try uncommenting these 2 lines if the sprites have opaque gray background
#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData('', 'gl-force-pixfmt 6')

app = ShowBase()
app.setBackgroundColor(0.6, 0.65, 1.0)

# render-to-texture stuff
altBuffer=app.win.makeTextureBuffer("spritebuf", 256, 256)
#altBuffer.setInverted(True)
altRender=NodePath("alt render")
altCam=app.makeCamera(altBuffer)
altCam.reparentTo(altRender)
#altCam.setPos(0.25, -12, 0)
teapot=loader.loadModel('model/banana.egg')
teapot.reparentTo(altRender)
teapot.setPos(0, 5, -0.1)
teapot.setH(270) # lazy way to compensate for the inverted buffer
teapot.setP(180)
app.accept("v", app.bufferViewer.toggleEnable)
app.bufferViewer.setPosition("llcorner")
app.bufferViewer.setCardSize(1.0, 0.0)

# lighting
dlight = DirectionalLight('dlight')
alight = AmbientLight('alight')
dlnp = altRender.attachNewNode(dlight)
alnp = altRender.attachNewNode(alight)
dlight.setColor(Vec4(0.8, 0.8, 0.5, 1))
alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
dlnp.setHpr(0, -60, 0)
#altRender.setLight(dlnp)
#altRender.setLight(alnp)

# vertex writer
vdata = GeomVertexData('points', GeomVertexFormat.getV3(), Geom.UHDynamic)
vwriter = GeomVertexWriter(vdata, 'vertex')

# 100 randomly generated vertex coordinates
for i in range(100):
    vwriter.addData3f(uniform(-100,100), uniform(-100,100), uniform(-100,100))

# create geom
points = GeomPoints(Geom.UHDynamic)
points.addNextVertices(100)
points.closePrimitive()
geo = Geom(vdata)
geo.addPrimitive(points)
gnode = GeomNode('points')
gnode.addGeom(geo)
np = render.attachNewNode(gnode)

# point sprite effect
np.setTransparency(TransparencyAttrib.MDual)
np.setTexGen(TextureStage.getDefault(), TexGenAttrib.MPointSprite)
np.setTexture(altBuffer.getTexture())
np.setRenderModePerspective(True)
np.setRenderModeThickness(8)

# additional controls
def toggle_perspective():
    np.setRenderModePerspective(not np.getRenderModePerspective())

app.accept('p', toggle_perspective)

for i in range(1,10):
    app.accept(str(i), np.setRenderModeThickness, [i])

app.run()