# https://docs.panda3d.org/1.10/python/programming/directgui/directoptionmenu
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *

# Add some text
bk_text = "DirectOptionMenu Demo"
textObject = OnscreenText(text=bk_text, pos=(0.85, 0.85), scale=0.07,
                          fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                          mayChange=1)

# Add some text
output = ""
textObject = OnscreenText(text=output, pos=(0.95, -0.95), scale=0.07,
                          fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                          mayChange=1)

# Callback function to set  text
def itemSel(arg):
    output = "Item Selected is: " + arg
    textObject.setText(output)

# Create a frame
menu = DirectOptionMenu(text="options", scale=0.1, command=itemSel,
                        items=["item1", "item2", "item3"], initialitem=2,
                        highlightColor=(0.65, 0.65, 0.65, 1))

# Run the tutorial
base.run()