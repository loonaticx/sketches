from panda3d.core import *

"""
My goal here is to be able to flattenStrong GeomNodes in models WITHOUT touching any sensitive
parts, like collisions (which should be FlattenLight i believe?), dcs points, ModelNodes(i think?)

I can't just do render.flattenStrong() since that'll flatten ALL of the nodes -- we don't want that.

I've tried out different ideas such as migrating ("stealing") the child GeomNodes off the PandaNodes, putting them
into their own nodepath to flattenStrong, then aggregating back to the original NP.

My problem here is that these sensitive nodes (and collisions) can be scattered. It would be a good day
if all of the collisions were placed in their own group instead of being with the GeomNodes, but it ain't like that.

"""

# GeomNodes are typically under PandaNodes
# https://docs.panda3d.org/1.10/python/reference/panda3d.core.GeomNode?highlight=geomnode#panda3d.core.GeomNode.unify
loader = Loader.getGlobalPtr()
node1 = loader.loadSync("testmodel.egg")
node1 = NodePath(node1)
print("node1")
print(node1.ls())
# node1.writeBamFile("testmodel.bam")
alsonp = node1.__copy__()
alsonp.flattenStrong()
# alsonp.writeBamFile("testmodel-f.bam")
model = node1.__copy__()


def method1():
    for geomnode in model.findAllMatches("**/+GeomNode"):
        gname = model.find(geomnode.getName())
        if str(gname) != "**not found**":
            gname.flattenStrong()


def method2():
    geom = model.findAllMatches("**/+GeomNode")
    for g in geom:
        g.flattenStrong()


def method3():
    geomPandaNode = PandaNode("geom")

    # this is what we want to focus our flattening on...
    def walkgeom(node):
        for nodes in node.getChildren():  # nodepaths in collection i think
            # print(nodes.getNodes())
            for nodetype in nodes.getNodes():
                if not isinstance(nodetype, GeomNode):  # none are GeomNode instances rn
                    walkgeom(nodes)
                else:
                    # print(".")
                    # print("stashing {}".format(nodes))
                    # node.stashChild(nodes)
                    # collPandaNode.stealChildren(nodes)
                    if isinstance(nodetype, PandaNode):
                        geomPandaNode.addChild(nodetype)
                        # node.removeChild(nodetype)
                    continue

    walkgeom(model)
    # print(geomPandaNode.getChildren())
    geomNode = NodePath("geom")
    geomPandaNode = geomNode.attachNewNode(geomPandaNode)
    print(geomNode.ls())
    for c in geomNode.getChildren():
        # print(c) # prints geom/geom
        for d in c.getChildren():
            print(d.node())  # doesn't print anything
            d.node().setPreserved(False)  # geomnodes is d.node()
            d.node().unify(10, True)
    print(geomNode.ls())


def method4():
    for m in model.getChildren():
        p = m.getNode(0)  # p is a PandaNode
        # print(len(p.getChildren()))
        if len(p.getChildren()) > 0:
            # print(p.getChild(0))
            pp = p.getChild(0)
            print(pp.getChildren())
        # for geom in m.findAllMatches("**/GeomNode"):
        #    geom.flattenStrong()


def method5():
    np = NodePath("geom")
    for m in model.getChildren():  # gives us NodePaths
        print(m.getName())
        if m.getName() == "geom":
            m.flattenStrong()
        for npc in m.getChildren():
            print(type(npc))


# use this method to look into flattening not the entire nodepath butsome child nodes
def method6():
    geomNode = NodePath("geom")
    collNode = NodePath("coll")
    for m in model.getChildren():
        for n in m.getChildren():
            if isinstance(n.node(), GeomNode):
                geomNode.attachNewNode(n.node())
            if isinstance(n.node(), CollisionNode):
                collNode.attachNewNode(n.node())
            if isinstance(n.node(), PandaNode):
                for pn in n.getChildren():
                    if pn.node().isGeomNode():
                        geomNode.attachNewNode(pn.node())
                    elif pn.node().isCollisionNode():
                        collNode.attachNewNode(pn.node())
            # They can be hiding in here too, though idk if i should associate tem with the same group bcause these may be delicate nodes
            elif isinstance(n.node(), ModelNode):
                for pn in n.getChildren():
                    if pn.node().isGeomNode():
                        geomNode.attachNewNode(pn.node())
                    elif pn.node().isCollisionNode():
                        collNode.attachNewNode(pn.node())

    # print(geomNode.ls())
    # geomNode.flattenStrong()
    # print(geomNode.ls()) # it flattened it!!! yahooo

    for node in geomNode.getChildren():
        for item in model.findAllMatches("**/{}".format(node.getName())):
            print(item.node())
            item.removeNode()
        # if not check.isEmpty(): ## um i dont think any of this did anything helpful
        #   check.removePath(model)


# method6 but actually this time dammit
def method7():
    for m in model.getChildren():
        if m.getName() == "geom":
            m.flattenStrong()  # ok i wish it was thaaat easy? :/


# method1() does not work
# method2() does not work
# method3() # does not work but cool
# method4()
# method5()
# method6() maybe
method7()


def printstuff():
    print()
    print("alsonp")
    print(alsonp.ls())
    print()
    print("model")
    print(model.ls())


printstuff()
