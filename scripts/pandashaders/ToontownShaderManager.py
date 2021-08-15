from direct.filter.CommonFilters import CommonFilters
from panda3d.core import WindowProperties
from panda3d.core import NodePath
from panda3d.core import PGTop
from panda3d.core import MouseWatcher
from panda3d.core import MouseAndKeyboard
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText

"""
  ToontownShaderManager
  Demonstrating the use of Panda3D's built-in shaders.
  Author: Loonatic
  Date: 4/30/2021
  https://gist.github.com/loonaticx/7c124790371cf3c5ac0b66c9da7c3765
"""

# https://docs.panda3d.org/1.10/python/_modules/direct/filter/CommonFilters
# is it possible to render a new window & place the gui there instead of the model viewport window?
# alternatively just have hotkeys/something to toggle certain gui since screen real estate is p tight

class ToontownShaderManager(DirectFrame):

    def __init__(self, parent):
        self._parent = parent
        DirectFrame.__init__(self, parent=self._parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.filter = CommonFilters(base.win, base.cam) # Only affects primary window

        # Ambient Occlusion
        self.samples = 0
        self.radius = 0.0
        self.amount = 0.0
        self.strength = 0.0

        # Blur/Sharpen
        self.blur = 1.0 # this is normal value, 0.0 blurs it

        # Cartoon Ink
        self.cartoonSep = 0.0
        self.cartoonR = 0.0
        self.cartoonB = 0.0
        self.cartoonG = 0.0

        # todo: Add bloom

        # Boolean Filters
        self.HDREnabled = False
        self.invertedEnabled = False
        self.sRGBEnabled = False
        self.halfPixelShiftEnabled = False
        self.viewGlowEnabled = False

        # Other Filters
        self.exposure = 0.0

        self.SAMPLES_MAX = 128
        self.RAD_MAX = 1.0
        self.AMT_MAX = 64.0
        self.STR_MAX = 0.01
        self.INCREMENT = 1
        self.numSamples = None
        self.numRadius = None

        self.circleModel = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')
        self.barTexture = loader.loadTexture('phase_3/maps/slider.png')
        self.loadGUI()
        # self.newWindow() # Disabled for now


    def loadGUI(self):
        self.textRowHeight = 0.2
        self.buttonbase_xcoord = 1.4
        self.buttonbase_ycoord = 0.45
        self.loadAmbientOcclusionGUI()
        self.loadBlurGUI()
        self.loadExposureGUI()
        self.loadCartoonInkGUI()
        self.loadHotkeys()


    def loadHotkeys(self):
        # for now instead of gui buttons i'ma just put the bool filters as hotkeys
        self.accept('4', self.__toggleHDR)
        self.accept('5', self.__toggleInverted)
        self.accept('6', self.__toggleSRGB)
        self.accept('7', self.__toggleHalfPixelShift)
        self.accept('8', self.__toggleViewGlow)


    def loadAmbientOcclusionGUI(self):
        self.numSamples = DirectSlider(parent=self, value=self.samples,
                                              pos=(self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.textRowHeight * 3.5),
                                              thumb_relief=None, range=(0, 32), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeAOValue)
                                              #command=self.__changeAOValue(self.samples, self.radius, self.amount, self.strength))
        self.numSamples.setScale(0.5)
        self.numSamples.setTransparency(True)
        self.numSamplesText = OnscreenText(pos=(self.buttonbase_xcoord + 0.1, self.buttonbase_ycoord - self.textRowHeight * 3.2), scale=0.05, text="AO Sample Count = {}".format(self.samples), style=5, mayChange=True)


        self.numRadius = DirectSlider(parent=self, value=self.radius,
                                              pos=(self.buttonbase_xcoord + 0.1, 0.0, (self.buttonbase_ycoord - self.textRowHeight * 4.5)),
                                              thumb_relief=None, range=(0, 1), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeAOValue)

        self.numRadius.setScale(0.5)
        self.numRadius.setTransparency(True)
        self.numRadiusText = OnscreenText(pos=(self.buttonbase_xcoord + 0.1, self.buttonbase_ycoord - self.textRowHeight * 4.2), scale=0.05, text="AO Radius = {}".format(str(self.radius)), style=5, mayChange=True)



        self.numAmount = DirectSlider(parent=self, value=self.amount,
                                              pos=(self.buttonbase_xcoord + 0.1, 0.0, (self.buttonbase_ycoord - self.textRowHeight * 5.5)),
                                              thumb_relief=None, range=(0, 64), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeAOValue)

        self.numAmount.setScale(0.5)
        self.numAmount.setTransparency(True)
        self.numAmountText = OnscreenText(pos=(self.buttonbase_xcoord + 0.1, self.buttonbase_ycoord - self.textRowHeight * 5.2), scale=0.05, text="AO Amount = {}".format(self.amount), style=5, mayChange=True)


        self.numStrength = DirectSlider(parent=self, value=self.strength,
                                              pos=(self.buttonbase_xcoord + 0.1, 0.0, (self.buttonbase_ycoord - self.textRowHeight * 6.5)),
                                              thumb_relief=None, range=(0, 0.1), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeAOValue)

        self.numStrength.setScale(0.5)
        self.numStrength.setTransparency(True)
        self.numStrengthText = OnscreenText(pos=(self.buttonbase_xcoord + 0.1, self.buttonbase_ycoord - self.textRowHeight * 6.2), scale=0.05, text="AO Strength = {}".format(self.strength), style=5, mayChange=True)

    def loadCartoonInkGUI(self):
        self.cSep = DirectSlider(parent=self, value=self.cartoonSep,
                                              pos=(-self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.textRowHeight * 2.5),
                                              thumb_relief=None, range=(0, 32), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeCartoon)
                                              #command=self.__changeAOValue(self.samples, self.radius, self.amount, self.strength))
        self.cSep.setScale(0.5)
        self.cSep.setTransparency(True)

        self.cRed = DirectSlider(parent=self, value=self.cartoonR,
                                              pos=(-self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.textRowHeight * 3.5),
                                              thumb_relief=None, range=(0, 1), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeCartoon)
                                              #command=self.__changeAOValue(self.samples, self.radius, self.amount, self.strength))
        self.cRed.setScale(0.5)
        self.cRed.setTransparency(True)

        self.cBlue = DirectSlider(parent=self, value=self.cartoonB,
                                              pos=(-self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.textRowHeight * 4.5),
                                              thumb_relief=None, range=(0, 1), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeCartoon)
                                              #command=self.__changeAOValue(self.samples, self.radius, self.amount, self.strength))
        self.cBlue.setScale(0.5)
        self.cBlue.setTransparency(True)

        self.cGreen = DirectSlider(parent=self, value=self.cartoonG,
                                              pos=(-self.buttonbase_xcoord + 0.1, 0.0, self.buttonbase_ycoord - self.textRowHeight * 5.5),
                                              thumb_relief=None, range=(0, 1), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeCartoon)
                                              #command=self.__changeAOValue(self.samples, self.radius, self.amount, self.strength))
        self.cGreen.setScale(0.5)
        self.cGreen.setTransparency(True)

    def loadBlurGUI(self):
        self.numBlur = DirectSlider(parent=self, value=self.blur, # pos=(0.0, 0.0, 0.0), # for new window
                                              pos=(self.buttonbase_xcoord + 0.1, 0.0, (self.buttonbase_ycoord - self.textRowHeight * 0.5)),
                                              thumb_relief=None, range=(-10, 10), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeBlur)
        self.numBlur.setScale(0.5)
        self.numBlur.setTransparency(True)
        self.numBlurText = OnscreenText(pos=(self.buttonbase_xcoord + 0.1, self.buttonbase_ycoord - self.textRowHeight * 0.2), scale=0.05, text="Blur Amount = {}".format(self.blur), style=5, mayChange=True)


    def loadExposureGUI(self):
        self.numExposure = DirectSlider(parent=self, value=self.exposure,
                                              pos=(self.buttonbase_xcoord + 0.1, 0.0, (self.buttonbase_ycoord - self.textRowHeight * 2.2)),
                                              thumb_relief=None, range=(0, 5), #self.SAMPLES_MAX
                                              thumb_geom=self.circleModel.find('**/tt_t_gui_mat_namePanelCircle'),
                                              frameTexture=self.barTexture, frameSize=(-0.5, 0.5, -0.08, 0.08),
                                              command=self.__changeExposure)
        self.numExposure.setScale(0.5)
        self.numExposure.setTransparency(True)
        self.numExposureText = OnscreenText(pos=(self.buttonbase_xcoord + 0.1, self.buttonbase_ycoord - self.textRowHeight * 1.9), scale=0.05, text="Exposure Amount = {}".format(self.blur), style=5, mayChange=True)


    def printValue(self):
        print(self.numSamples['value'])

    def __changeCartoon(self):
        self.filter.delCartoonInk()
        s = self.cSep['value']
        self.cartoonSep = s
        r = self.cRed['value']
        self.cartoonR = r
        b = self.cBlue['value']
        self.cartoonB = b
        g = self.cGreen['value']
        self.cartoonG = g
        self.filter.setCartoonInk(s, (r, g, b, 1)) # a doesn't change

    def __changeBlur(self):
        self.filter.delBlurSharpen()
        b = self.numBlur['value']
        self.blur = b
        self.numBlurText.setText("Blur amount = {}".format(b))
        self.filter.setBlurSharpen(b)

    def __changeAOValue(self):
        if self.numSamples is None:
            print("NONE")
            return
        self.filter.delAmbientOcclusion()

        s = self.numSamples['value']
        self.samples = s
        self.numSamplesText.setText("AO Sample Count = {}".format(s))
        if(s == 0):
            return

        r = self.numRadius['value']
        self.radius = r
        self.numRadiusText.setText("AO Radius = {}".format(r))
        if(r == 0):
            return

        a = self.numAmount['value']
        self.amount = a
        self.numAmountText.setText("AO Amount = {}".format(a))
        if(a == 0):
            return

        st = self.numStrength['value']
        self.strength = st
        self.numStrengthText.setText("AO Strength = {}".format(st))
        if(st == 0):
            return

        self.filter.setAmbientOcclusion(numsamples=s, radius=r, amount=a, strength=st)
        print("sample count: {} | radius count: {} | amount count: {} | strength count: {}".format(self.samples, self.radius, self.amount, self.strength))

    # WARNING: Won't work with relatively older Panda versions because this is new
    def __changeExposure(self):
        self.filter.delExposureAdjust()
        e = self.numExposure['value']
        self.exposure = e
        self.numExposureText.setText("Exposure amount = {}".format(e))
        self.filter.setExposureAdjust(e)

    def __toggleInverted(self):
        if not self.invertedEnabled:
            self.filter.setInverted()
            self.invertedEnabled = True
        else:
            self.filter.delInverted()
            self.invertedEnabled = False

    def __toggleHDR(self):
        if not self.HDREnabled:
            self.filter.setHighDynamicRange()
            self.HDREnabled = True
        else:
            self.filter.delHighDynamicRange()
            self.HDREnabled = False

    def __toggleSRGB(self):
        if not self.sRGBEnabled:
            self.filter.setSrgbEncode(True)
            self.sRGBEnabled = True
        else:
            self.filter.delSrgbEncode()
            self.sRGBEnabled = False

    def __toggleHalfPixelShift(self):
        if not self.halfPixelShiftEnabled:
            self.filter.setHalfPixelShift()
            self.halfPixelShiftEnabled = True
        else:
            self.filter.delHalfPixelShift()
            self.halfPixelShiftEnabled = False

    def __toggleViewGlow(self):
        if not self.viewGlowEnabled:
            self.filter.setViewGlow()
            self.viewGlowEnabled = True
        else:
            self.filter.delViewGlow()
            self.viewGlowEnabled = False

    def getValue(self, item, item_MAX):
        return item / item_MAX

    # Not gonna use this feature since it makes it very laggy. I will have to figure out
    # a better way to layout UI some other time.
    # https://discourse.panda3d.org/t/how-to-open-a-new-window/23929/4
    def newWindow(self):
        self.wp = WindowProperties()
        self.wp.setSize(700, 500)
        self.wp.setRawMice(True)
        print(self.wp.getMouseMode())
        win2mouseWatcher = MouseWatcher()
        ar = 1
        self.win2 = base.openWindow(props=self.wp, aspectRatio=ar)
        self.window2render2d = NodePath('window2render2d')
        self.window2render2d.setDepthTest(0)
        self.window2render2d.setDepthWrite(0)

        self.window2camera2d = base.makeCamera2d(self.win2)
        self.window2camera2d.reparentTo(self.window2render2d)

        # Parent gui to this
        self.window2aspect2d = self.window2render2d.attachNewNode(PGTop('window2aspect2d'))
        self.window2aspect2d.setScale(1.0 / ar, 1.0, 1.0)

        name = self.win2.getInputDeviceName(0)
        mk = base.dataRoot.attachNewNode(MouseAndKeyboard(self.win2, 0, name))
        mw = mk.attachNewNode(MouseWatcher(name))
        self.window2aspect2d.node().setMouseWatcher(mw.node())



######

"""
from toontown.shader import ToontownShaderManager
tsm= ToontownShaderManager.ToontownShaderManager()
"""