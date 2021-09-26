from panda3d.core import InputDevice
from direct.showbase.ShowBase import ShowBase



class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        print(base.devices.getDevices())
        gamepad = base.devices.getDevices()[0]
        print(gamepad.buttons)
        ##messenger.toggleVerbose()
        left_x = gamepad.findAxis(InputDevice.Axis.left_x)
        #if right_stick.pressed:
        #    print("Right stick detected")

app = MyApp()
app.run()