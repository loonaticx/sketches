# https://docs.panda3d.org/1.10/python/programming/directgui/directscrollbar
from direct.gui.DirectGui import *
#from direct.gui.DirectGui import DirectScrollBar

mybar = DirectScrollBar(range=(0, 100), value=50, pageSize=3, orientation= DGG.VERTICAL)
mybar.setPos(-1, 0, -0.5)