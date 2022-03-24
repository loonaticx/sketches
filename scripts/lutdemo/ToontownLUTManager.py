"""
ToontownLUTManager.py
Author: Loonatic
Date: 8/15/2021

To make custom LUTs for Toontown, open "def_lut.png" in Photoshop, go to Adjustments>Color Lookup...
Either pick one of the default presets or import a cube file, then export the result as a new png file.

Note: Filters won't work properly if textures-power-2 is enabled or set to True
"""
from direct.filter.FilterManager import FilterManager


class ToontownLUTManager():
    def __init__(self):
        self.manager = FilterManager(base.win, base.cam)

        # Gonna use a Tuple for now
        # This list should be stored somewhere else ultimately, probably like in a globals file
        # [Friendly LUT Name, LUT Filepath]
        self.LUTList = (
            ["Default", "phase_3/luts/def_lut.png"],
            ["LSD", "phase_3/luts/lsd_lut.png"],
            ["Sunset", "phase_3/luts/sunset_lut.png"],
            ["Natural Pop", "phase_3/luts/pop_lut.png"],
            ["Red+Black", "phase_3/luts/2_lut.png"]
        )
        self.vertexShader = "phase_3/shaders/lut-vert.glsl"
        self.fragmentShader = "phase_3/shaders/lut-frag.glsl"
        self.setupLUT(self.LUTList[0][1])

    def setupLUT(self, lut_file):
        colortex = Texture()
        self.quad = self.manager.renderSceneInto(colortex = colortex)
        self.quad.setShader(Shader.load(Shader.SLGLSL, self.vertexShader, self.fragmentShader))
        self.quad.setShaderInput("colortex", colortex)
        lut = loader.loadTexture(lut_file)
        lut.setFormat(Texture.F_rgb16)
        lut.setWrapU(Texture.WMClamp)
        lut.setWrapV(Texture.WMClamp)
        self.quad.setShaderInput("lut", lut)

    def loadTUL(self, lut_file, format = Texture.F_rgb):
        lut = loader.loadTexture(lut_file)
        lut.setFormat(Texture.F_rgb16)
        lut.setWrapU(Texture.WMClamp)
        lut.setWrapV(Texture.WMClamp)
        self.quad.setShaderInput("lut", lut)

    def getLUTS(self):
        return self.LUTList

    def cleanup(self):
        self.manager.cleanup()


"""
from toontown.shader import ToontownLUTManager
lutman = ToontownLUTManager.ToontownLUTManager()
luts = lutman.getLUTS()
lutman.loadTUL(luts[4][1])

"""
