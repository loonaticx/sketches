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


#GeomNodes are typically under PandaNodes
# https://docs.panda3d.org/1.10/python/reference/panda3d.core.GeomNode?highlight=geomnode#panda3d.core.GeomNode.unify
loader = Loader.getGlobalPtr()
node1 = loader.loadSync("testmodel.egg")
node1 = NodePath(node1)

#node1.writeBamFile("testmodel.bam")
alsonp = node1.__copy__()
alsonp.flattenStrong()
#alsonp.writeBamFile("testmodel-f.bam")
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
        for nodes in node.getChildren():
            if not isinstance(nodes, GeomNode):
                walkgeom(nodes)
            else:
                #print("stashing {}".format(nodes))
                #node.stashChild(nodes)
                #collPandaNode.stealChildren(nodes)
                geomPandaNode.addChild(nodes)
                node.removeChild(nodes)
                continue

    walkgeom(model)

    geomNode = NodePath("geom")
    geomPandaNode = geomNode.attachNewNode(geomPandaNode)
    for c in geomNode.getChildren():
        for d in c.getChildren():
            #print(d)
            d.flattenStrong()

def method4():
    for m in model.getChildren():
        p = m.getNode(0) # p is a PandaNode
        #print(len(p.getChildren()))
        if len(p.getChildren()) > 0:
            #print(p.getChild(0))
            pp = p.getChild(0)
            print(pp.getChildren())
        #for geom in m.findAllMatches("**/GeomNode"):
        #    geom.flattenStrong()

def method5():
    np = NodePath("geom")
    for m in model.getChildren(): # gives us NodePaths
        print(m.getName())
        if m.getName() == "geom":
            m.flattenStrong()
        for npc in m.getChildren():
            print(type(npc))


#method1() does not work
#method2() does not work
#method3() does not work
#method4()
method5()

def printstuff():
    print("node1")
    print(node1.ls())
    print()
    print("alsonp")
    print(alsonp.ls())
    print()
    print("model")
    print(model.ls())
printstuff()


