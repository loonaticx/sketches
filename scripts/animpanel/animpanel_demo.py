"""
This is a script intended to demonstrate an obsolete Panda3D utility for viewing animations
Program is very unstable right now and will not function properly
Works a little bit better on older versions of panda/python but still unstable
"""

from direct.actor import Actor
from direct.tkpanels import AnimPanel
from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData
# Older import
#from pandac.PandaModules import loadPrcFileData

loadPrcFileData('animpanel_demo.py', 'model-path $RESOURCE_DIR')

class animPanelApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        a = Actor.Actor({"head":"phase_3/models/char/tt_a_chr_dgm_shorts_head_1000.egg",
                              "torso":"phase_3/models/char/tt_a_chr_dgm_shorts_torso_1000.egg",
                              "legs":"phase_3/models/char/tt_a_chr_dgm_shorts_legs_1000.egg"},
                        {"head":{"walk":"phase_3/models/char/tt_a_chr_dgm_shorts_head_neutral.egg", \
                                 "run":"phase_3/models/char/tt_a_chr_dgm_shorts_head_walk.egg"}, \
                         "torso":{"walk":"phase_3/models/char/tt_a_chr_dgm_shorts_torso_neutral.egg", \
                                  "run":"phase_3/models/char/tt_a_chr_dgm_shorts_torso_walk.egg"}, \
                         "legs":{"walk":"phase_3/models/char/tt_a_chr_dgm_shorts_legs_neutral.egg", \
                                 "run":"phase_3/models/char/tt_a_chr_dgm_shorts_legs_walk.egg"}})
        a.attach("head", "torso", "def_head")
        a.attach("torso", "legs", "joint_hips")
        a.drawInFront("joint-pupil?", "eyes*", -1)
        a.fixBounds()
        #a.ls()
        a.reparentTo(render)

        """
        a2 = Actor.Actor({250:{"head":"phase_3/models/char/dogMM_Shorts-head-250.bam",
                              "torso":"phase_3/models/char/dogMM_Shorts-torso-250.bam",
                              "legs":"phase_3/models/char/dogMM_Shorts-legs-250.bam"},
                         500:{"head":"phase_3/models/char/dogMM_Shorts-head-500.bam",
                              "torso":"phase_3/models/char/dogMM_Shorts-torso-500.bam",
                              "legs":"phase_3/models/char/dogMM_Shorts-legs-500.bam"},
                         1000:{"head":"phase_3/models/char/dogMM_Shorts-head-1000.bam",
                              "torso":"phase_3/models/char/dogMM_Shorts-torso-1000.bam",
                              "legs":"phase_3/models/char/dogMM_Shorts-legs-1000.bam"}},
                        {"head":{"walk":"phase_3/models/char/dogMM_Shorts-head-walk.bam", \
                                 "run":"phase_3/models/char/dogMM_Shorts-head-run.bam"}, \
                         "torso":{"walk":"phase_3/models/char/dogMM_Shorts-torso-walk.bam", \
                                  "run":"phase_3/models/char/dogMM_Shorts-torso-run.bam"}, \
                         "legs":{"walk":"phase_3/models/char/dogMM_Shorts-legs-walk.bam", \
                                 "run":"phase_3/models/char/dogMM_Shorts-legs-run.bam"}})
        a2.attach("head", "torso", "joint-head", 250)
        a2.attach("torso", "legs", "joint-hips", 250)
        a2.attach("head", "torso", "joint-head", 500)
        a2.attach("torso", "legs", "joint-hips", 500)
        a2.attach("head", "torso", "joint-head", 1000)
        a2.attach("torso", "legs", "joint-hips", 1000)
        a2.drawInFront("joint-pupil?", "eyes*", -1, lodName=250)
        a2.drawInFront("joint-pupil?", "eyes*", -1, lodName=500)
        a2.drawInFront("joint-pupil?", "eyes*", -1, lodName=1000)
        a2.setLOD(250, 250, 75)
        a2.setLOD(500, 75, 15)
        a2.setLOD(1000, 15, 1)
        a2.fixBounds()
        a2.reparentTo(render)
        """


        #ap = AnimPanel.AnimPanel([a, a2])

        # Alternately
        ap = a.animPanel()
        #ap2 = a2.animPanel()

app = animPanelApp()
app.run()