"""
from panda3d.core import Fog
render.clearFog()
myFog = Fog("Fog Nasme")
myFog.setColor(0.05, 0.05, 0.05)
myFog.setExpDensity(0.01)
render.setFog(myFog)

https://docs.panda3d.org/1.10/python/programming/render-attributes/fog
https://docs.panda3d.org/1.10/python/reference/panda3d.core.Fog#panda3d.core.Fog


In linear mode, the onset and opaque distances of the fog are defined as offsets along the local forward (+Y) axis of the fog node.
The onset distance is the distance from the fog node at which the fog will begin to have effect,
and the opaque distance is the distance from the fog node at which the fog will be completely opaque.
From reading the API page for the Fog class, it sounds as if beyond this opaque point there is no fog
(rather than continuing opaque fog up to the location of the fog node as you might expect):
"the fog will be rendered as if it extended along the vector from the onset point to the opaque point."

"""

from panda3d.core import Fog
class ToontownFogManager():
    def __init__(self):
        self.fog = None
        self.fogMode = None
        print("Initialized Fog Manager")

        self.fog = Fog("ActiveFog")
        self.fog.setColor(1, 1, 1)

        self.fogTypes = {
            0: Fog.MExponential,
            1: Fog.MExponentialSquared,
            2: Fog.MLinear
        }


    def setFog(self, np):
        np.setFog(self.fog)

    def setColor(self, r, g, b):
        self.fog.setColor(r, g, b)

    def clearFog(self):
        return render.clearFog()

    def getFogMode(self):
        self.fogMode = self.fog.getMode()

    def setFogMode(self, id):
        mode = self.fog.setMode(self.fogTypes[id])
        self.fogMode = mode

    ## For Exponential Fog

    """
    Determines the density value used for exponential fog calculations.
    """
    def setDensity(self, density): # 0 to 1
        self.fog.setExpDensity(density)


    ## For Linear Fog

    """
    Specifies the effects of the fog in linear distance units. This is only used if the mode is M_linear.
    This specifies a fog that begins at distance onset units from the origin,
    and becomes totally opaque at distance opaque unitsfrom the origin, along the forward axis (usually Y).
    This function also implicitly sets the mode the M_linear, if it is not already set.

    """
    def setLinearRange(self, range, opacity):
        self.fog.setLinearRange(range, opacity)

    """
    The Fog method setLinearFallback(float angle, float onset, float opaque) defines how the fog should be rendered when the fog effect
    is diminished in this way. angle is the minimum viewing angle
    (angle between the camera direction and fog direction) at which the fallback effect will be employed.
    onset and opaque specify camera-relative onset and opaque distances that will be fallen back on,
    overriding the Fog node's own onset and opaque distances.

    The linear fallback workaround will only look good in certain situations, for example when the fog is deep inside a dark cave.
    So in general, exponential mode fog is more useful than the default linear mode fog.
    """
    def setLinearFallback(angle, onset, opaque):
        self.fog.setLinearFallback(angle, onset, opaque)

    ## Extra
