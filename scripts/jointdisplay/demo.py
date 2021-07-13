from pandac.PandaModules import *
loadPrcFileData("interpolate-frames", "#t")
import direct.directbase.DirectStart
from direct.actor.Actor import Actor
from random import random

actor = Actor("joint_demo.egg", {"test" : "anim_test.egg"})
actor.reparentTo(render)
actor.setBin('background', 1)

# Credit to rdb for original joint visualization script
# https://discourse.panda3d.org/t/visualise-actor-bones-joints/9976


def walkJointHierarchy(actor, part, parentNode = None, indent = ""):
    if isinstance(part, CharacterJoint):
        np = actor.exposeJoint(None, 'modelRoot', part.getName())
        print(np)

        if parentNode and parentNode.getName() != "root":
            print("!!!!!!!!! {}".format(parentNode.getName()))
            lines = LineSegs()
            lines.setThickness(3.0)
            lines.setColor(random(), random(), random())
            lines.moveTo(0, 0, 0)
            lines.drawTo(np.getPos(parentNode))
            lnp = parentNode.attachNewNode(lines.create())

            lnp.setBin("fixed", 40)
            lnp.setDepthWrite(False)
            lnp.setDepthTest(False)
            lnp.setTwoSided(True)

        parentNode = np

    for child in part.getChildren():
        walkJointHierarchy(actor, child, parentNode, indent + "  ")

walkJointHierarchy(actor, actor.getPartBundle('modelRoot'), None)
actor.loop("test")
actor.setTwoSided(True)
base.cam.setY(-50)

base.run()