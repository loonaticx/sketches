from direct.showbase.ShowBase import ShowBase
import makeBillboard
class demo(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.model = loader.loadModel("model/banana.egg")
        self.model.reparentTo(render)
        self.model.setPos(0.5, 5, -0.1)
        billboard = makeBillboard
        billboard.billboardOf(self.model, 512)

app = demo()
app.run()