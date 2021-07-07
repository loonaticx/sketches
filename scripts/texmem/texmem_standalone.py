from direct.tkwidgets.MemoryExplorer import MemoryExplorer
from direct.showbase.ShowBase import ShowBase

class driver(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.base = ShowBase
        m = loader.loadModel('models/panda.egg.pz')
        m.reparentTo(render)
        base.setSceneGraphAnalyzerMeter(True)
        self.base.toggleTexMem(self)
        render.analyze()


app = driver()
app.run()