"""
  BlendAnimTest
  Utility to cycle through a dictionary of animations to check if blending visually works as intended.
  Author: Loonatic
  Date: 8/15/2021

  There is a common bug in Toontown where some animations played in some locations (such as in the Match Minnie minigame) will flicker at the end of the animation.
  This is caused by frame blending interfering with the pingpong loop that's used to balance out the duration of the animations being played.
  Frame blending may cause some issues with certain animations using pingpong, so this tool can be used to ensure that certain animations
  don't act wonky when blending is applied.

  The default animation being called is the "up" animation used in the Match Minnie trolley minigame and the dancefloor party minigame.
"""

from direct.actor import Actor
from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData
loadPrcFileData('BlendAnimTest.py', 'model-path $RESOURCE_DIR')

class BlendAnimTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.animBlend = False
        self.frameBlend = False # It's better practice to have frame blending enabled by default on modern Toontown clients.

        # Load up a dog Toon
        self.Toon = Actor.Actor({"head":"phase_3/models/char/tt_a_chr_dgm_shorts_head_1000.bam",
                              "torso":"phase_3/models/char/tt_a_chr_dgm_shorts_torso_1000.bam",
                              "legs":"phase_3/models/char/tt_a_chr_dgm_shorts_legs_1000.bam"},
                        {"head":{"walk":"phase_3/models/char/tt_a_chr_dgm_shorts_head_neutral.bam", \
                                 "run":"phase_3/models/char/tt_a_chr_dgm_shorts_head_walk.bam"}, \
                         "torso":{"walk":"phase_3/models/char/tt_a_chr_dgm_shorts_torso_neutral.bam", \
                                  "run":"phase_3/models/char/tt_a_chr_dgm_shorts_torso_walk.bam",
                                  "up":"phase_3.5/models/char/tt_a_chr_dgm_shorts_torso_up.bam"}, \
                         "legs":{"walk":"phase_3/models/char/tt_a_chr_dgm_shorts_legs_neutral.bam", \
                                 "run":"phase_3/models/char/tt_a_chr_dgm_shorts_legs_walk.bam",
                                 "up":"phase_3.5/models/char/tt_a_chr_dgm_shorts_legs_up.bam"}})
        self.Toon.reparentTo(render)
        self.Toon.attach("head", "torso", "def_head")
        self.Toon.attach("torso", "legs", "joint_hips")
        self.Toon.find('**/shoes').removeNode()
        self.Toon.find('**/boots_short').removeNode()
        self.Toon.find('**/boots_long').removeNode()

        # It would probably be more efficient & useful if I were to load up a bigger dictionary of all the Toon animations and have
        # some gui to toggle through each one, but for now, I am keeping it simple with only loading one.
        # I can probably aim to do that later in the future though.
        # todo: make some text that displays what animation, what mode (pingpong, loop, stopped), if animBlend/frameBlend is True/False, num frames of current anim...
        self.accept('1', self.Toon.play, ["up"])
        self.accept('2', self.Toon.loop, ["up"])
        self.accept('3', self.Toon.pingpong, ["up"])
        self.accept('4', self.Toon.stop)
        self.accept('5', self.changeAnimBlend)
        self.accept('6', self.changeFrameBlend)

        #print(self.Toon.pprint())
        print("numFrames of up: {}".format(self.Toon.getNumFrames("up")))

    """
    https://docs.panda3d.org/1.10/python/reference/direct.actor.Actor#direct.actor.Actor.Actor.setBlend

    When animBlend is True, multiple different animations may simultaneously be playing on the Actor.
    This means you may call play(), loop(), or pose() on multiple animations and have all of them contribute
    to the final pose each frame.

    The frameBlend flag is unrelated to playing multiple animations.
    It controls whether the Actor smoothly interpolates between consecutive frames of its animation
    (when the flag is True) or holds each frame until the next one is ready (when the flag is False).
    The default value of frameBlend is controlled by the interpolate-frames Config.prc variable.
    """
    def updateBlend(self):
        self.Toon.setBlend(self.animBlend, self.frameBlend)
        print("animBlend is {}, frameBlend is {}".format(self.animBlend, self.frameBlend))

    def changeAnimBlend(self):
        self.animBlend = not self.animBlend
        self.updateBlend()

    def changeFrameBlend(self):
        self.frameBlend = not self.frameBlend
        self.updateBlend()


app = BlendAnimTest()
app.run()