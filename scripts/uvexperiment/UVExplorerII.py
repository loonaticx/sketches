import copy
from eggtools.EggMan import EggMan
import os
from panda3d.core import *
from panda3d.egg import *
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

import math

# avoid true zero values
padding = 0.001

# https://www.albany.edu/faculty/jmower/geog/gog530Python/src/NormalizingCoordinatesManual.html
class UVExplorer:
    def __init__(self, eggman):
        # self.egg = EggData()
        # self.egg.read(filename)

        # print(str(self.egg))
        self.eggman = eggman

        # Sanitize the eggs first
        self.eggman.rename_all_trefs()

        for egg in self.eggman.egg_datas.keys():
            uvList, binormalList = self.get_uvs(egg)
            plt.grid(True)
            plt.title(egg.egg_filename.getBasenameWoExtension())
            self.eggman.write_egg_manually(egg, custom_suffix = "test1233.egg")
            # with open("egg_text_export.egg", "w") as egg_file:
            #     egg_file.write(str(self.egg))

        ax = plt.gca()
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        plt.show()

    def bounding_box(self, points):
        """returns a list containing the bottom left and the top right
        points in the sequence
        Here, we use min and max four times over the collection of points
        """
        # print(f"points- {points}")
        # if not points:
        #     return [(0, 0), (0,0)]
        # [ [x1, x2], [y1, y2] ]
        x, y = points
        bot_left_x = min(point for point in x)
        bot_left_y = min(point for point in y)
        top_right_x = max(point for point in x)
        top_right_y = max(point for point in y)
        # print("BBox")
        # print(points)
        # print(bot_left_x)
        # print([point for point in x])

        return [(bot_left_x, bot_left_y), (top_right_x, top_right_y)]

    def get_uvs(self, eggFile):
        uvList = []
        binormalList = []

        random.seed("absdddc")

        global textureNames
        textureNames = {}

        global tex2UV
        tex2UV = {}

        global found
        found = False

        global name2Color
        name2Color = {}

        global testarrX, testarrY
        testarrX = []
        testarrY = []

        global identification
        identification = {
            # child.getParent(): { "vertexId": [ U, V ] }
        }

        # global color
        # color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        def traverse_egg(egg):
            global tex2UV
            global found
            global name2Color
            global testarrX, testarrY
            global identification
            global textureNames

            # global color

            # if found:
            #     return

            for child in egg.getChildren():
                if isinstance(child, EggGroupNode):
                    traverse_egg(child)

                # Random color for tri differentiation
                # color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                cstrips = {}

                if isinstance(child, EggPolygon):
                    """
                    <Polygon> {
                      <TRef> { cc_t_fx_shadow_circle_2 }
                      <VertexRef> { 0 1 2 <Ref> { tt_r_ara_ttc_hydrant.egg } }
                    }
                    """

                    # { EggGroupName { { Polygon_TREFNAME : { "vertexID" : [ U, V ] } } }
                    # For now can we only use one tref for Polygon entries, even though having more is possible
                    polyTexture = child.getTexture()
                    if not polyTexture:
                        continue

                    texName = polyTexture.getName()
                    if texName not in textureNames.keys():
                        textureNames[texName] = polyTexture

                    # Random color for node differentiation
                    if not name2Color.get(child.getParent().getName()):
                        name2Color[child.getParent().getName()] = (
                        random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
                        )

                    color = name2Color[child.getParent().getName()]

                    # Check to see if parent group name exists first...
                    if not identification.get(child.getParent().getName()):
                        identification[child.getParent().getName()] = {}

                    nodeIdentification = identification[child.getParent().getName()]
                    if not nodeIdentification.get(polyTexture.getName()):
                        nodeIdentification[polyTexture.getName()] = {}
                    nodeIdentification = nodeIdentification[polyTexture.getName()]



                    if not cstrips.get(hash(str(color))):
                        cstrips[hash(str(color))] = []

                    # Ideally, we need to get vertex ids 0, 1, 2 from the group tt_r..blah
                    uvList = []
                    # or getPool...
                    for egg_vertex in child.getVertices():
                        if egg_vertex.hasUv():
                            """
                            "vertexid" : [u, v]
                            """
                            v_uv = egg_vertex.getUv()
                            """
                            <Vertex> 0 {
                              1.6 1.59227 0.025
                              <UV> { 1 0 }
                              <RGBA> { 1 1 1 0.5 }
                              // def_shadow:1
                            }
                            """
                            # print(egg_vertex)
                            nodeIdentification[egg_vertex] = egg_vertex.getUv()

                            x, y = egg_vertex.getUv()
                            uvList.append(egg_vertex.getUv())
                            # -k, mfc='C1', mec='C1',
                            cstrips[hash(str(color))].append([x, y])
                            # plt.plot(x, y, '-o', c=color, linestyle="--")

                    xlist = []
                    ylist = []

                    colLists = cstrips[hash(str(color))]  # [ [1,2] [3,4] ]
                    for coords in colLists:
                        x, y = coords
                        xlist.append(x)
                        ylist.append(y)

                    # hack to add a line for first and last point to finish the triangle
                    if colLists:
                        xlist.append(colLists[0][0])
                        ylist.append(colLists[0][1])

                    found = True
                    for x, y in uvList:
                        pass
                        # xlist.append(x)
                        # ylist.append(y)

                    # if the count is an odd number we need to add one more to make it balance
                    if len(xlist) % 2:
                        xlist.append(xlist[-1])
                        ylist.append(ylist[-1])

                    testarrX.extend(xlist)
                    xlist = np.array(xlist)
                    testarrY.extend(ylist)
                    ylist = np.array(ylist)

                    xx = np.vstack([xlist[0::2], xlist[1::2]])
                    yy = np.vstack([ylist[0::2], ylist[1::2]])

                    plt.plot(xx, yy, '-o', c = color)
                    pass

        traverse_egg(eggFile)
        i = 0

        for nodeGroup in identification.keys():
            nodeTextures = identification[nodeGroup]  # Contains EggTextures
            print(f"Ddd - {nodeTextures}")
            print(f"nodeGroup - {nodeGroup}")
            # Eggman ends up generating new textures so we need to create a snapshot
            # nodeTexSnapshot = copy.deepcopy(nodeTextures)
            nodeTexNames = list(nodeTextures.keys())
            # print(f"nodeTexSnapshot - {nodeTexSnapshot}")

            for nodeTexName in nodeTexNames:
                nodeID = nodeTextures[nodeTexName]  # Contains [ EggVertex: [U, V] ]
                nodeTex = textureNames[nodeTexName]  # note: not connected to our working egg
                # nodeTex = self.eggman.get_texture_by_name(eggFile, nodeTexName)
                # nodeTex = eggFile.getTexture(nodeTexName)
                # We need to get the bounding box
                # This is not the best way to do this but whatever
                allX = []
                allY = []
                # allX = allY = []
                for u, v in nodeID.values():
                    allX.append(u)
                    allY.append(v)

                # this bounding box is for the original uv layout -- consider this when cropping images
                bbox = self.bounding_box(np.array([allX, allY]))
                xMin, yMin = bbox[0]
                xMax, yMax = bbox[1]

                plt.plot(xMin, yMin, '-o', color = "red")
                plt.plot(xMax, yMax, '-o', color = "black")

                textureImage = Image.open(nodeTex.getFullpath())
                width, height = textureImage.size
                # Cropped out area, we should keep note of this new image size.
                boundsLocation = (
                    width * xMin, abs(height - (height * yMax)), width * xMax, abs(height - (height * yMin))
                )
                img2 = textureImage.crop(boundsLocation)
                croppedImagePath = os.path.join(
                    eggFile.egg_filename.getDirname(),
                    nodeTex.getFilename().getBasenameWoExtension() + f"_cropped_{i}.png"
                )
                img2.save(Filename.toOsSpecific(Filename.fromOsSpecific(croppedImagePath)), quality=100)
                i += 1

                # TODO:
                # Some meshes will need new EggTextures generated and assigned instead of being swapped
                # ( See bathtub bed )
                xMin += padding
                yMin -= padding
                xMax -= padding
                yMax += padding
                scale = max(xMax - xMin, yMax - yMin)
                # print(f"x - {xMax - xMin} | y - {yMax - yMin} --> {scale}")
                for vertex, uvCoords in nodeID.items():
                    xVal, yVal = uvCoords
                    newX = xVal - ((xMax + xMin) / 2)
                    newX /= xMax - xMin
                    # newX /= scale
                    newX += 0.5
                    newY = yVal - ((yMax + yMin) / 2)
                    # newY /= scale
                    newY /= yMax - yMin
                    newY += 0.5
                    vertex.set_uv(LPoint2d(newX, newY))

                nodeTex = self.eggman.get_texture_by_name(eggFile, nodeTexName)
                self.eggman.repath_egg_texture(eggFile, nodeTex, Filename.fromOsSpecific(croppedImagePath))
                # self.eggman.fix_broken_texpaths(eggFile)
                # We will clamp the edges, sometimes the values are ever so slightly out of the 0:1 area
                nodeTex.setWrapU(EggTexture.WM_clamp)
                nodeTex.setWrapV(EggTexture.WM_clamp)

        return uvList, binormalList
        # https://stackoverflow.com/questions/2450035/scale-2d-coordinates-and-keep-their-relative-euclidean-distances-intact

        twoArr = np.array([testarrX, testarrY])
        print(testarrX)


        # this bounding box is for the original uv layout -- consider this when cropping images
        bbox = self.bounding_box(twoArr)
        xMin, yMin = bbox[0]
        xMin += padding
        yMin -= padding
        xMax, yMax = bbox[1]
        xMax -= padding
        yMax += padding
        plt.plot(xMin, yMin, '-o', color = "black")
        plt.plot(xMax, yMax, '-o', color = "black")

        # using nodeIdentification for now since there is only one entry in identification (focusing on 1 poly grp rn)
        nodeID = identification[[*identification.keys()][0]]
        print(f"NODEID = {nodeID}")

        scale = max(xMax - xMin, yMax - yMin)
        for vertex, uvCoords in nodeID.items():
            xVal, yVal = uvCoords
            newX = xVal - ((xMax + xMin) / 2)
            newX /= scale
            newX += 0.5
            newY = yVal - ((yMax + yMin) / 2)
            newY /= scale
            newY += 0.5
            vertex.set_uv(LPoint2d(newX, newY))


        scaledXArr = []
        scaledYArr = []

        for xVal in testarrX:
            centerVal = xVal - ((xMax + xMin) / 2)
            # Scale down such that the larger of the two ranges becomes (-0.5, 0.5)
            scale = max(xMax - xMin, yMax - yMin)
            centerVal /= scale
            centerVal += 0.5

            # centerVal =(xVal - xMin) / (xMax - xMin)
            scaledXArr.append(centerVal)


        for yVal in testarrY:
            centerVal = yVal - ((yMax + yMin) / 2)
            # Scale down such that the larger of the two ranges becomes (-0.5, 0.5)
            scale = max(xMax - xMin, yMax - yMin)
            centerVal /= scale
            centerVal += 0.5

            # centerVal = (yVal - yMin)/(yMax - yMin)
            scaledYArr.append(centerVal)

        # [(bot_left_x, bot_left_y), (top_right_x, top_right_y)]
        bbox = self.bounding_box(twoArr)
        xMin, yMin = bbox[0]
        xMax, yMax = bbox[1]
        print(f"{xMin} - {yMin} - {xMax} - {yMax}")


        twoArr = np.array([scaledXArr, scaledYArr])
        # twoArr *= 0.98
        bbox = self.bounding_box(twoArr)
        xMin, yMin = bbox[0]
        xMax, yMax = bbox[1]

        normalized_array = twoArr

        # print(normalized_array)
        normX = normalized_array[0]
        normY = normalized_array[1]
        xx = np.vstack([normX[0::2], normX[1::2]])
        yy = np.vstack([normY[0::2], normY[1::2]])
        plt.plot(xx, yy, '-o')

        return uvList, binormalList

    def get_vertexes(self, eggFile):
        vertList_X = []
        vertList_Y = []
        vertList_Z = []

        def traverse_egg(egg):
            for child in egg.getChildren():
                if isinstance(child, EggGroupNode):
                    traverse_egg(child)

                if isinstance(child, EggVertexPool):
                    for egg_vertex in child:
                        x, y, z = egg_vertex.get_pos3()
                        vertList_X.append(x)
                        vertList_Y.append(y)
                        vertList_Z.append(z)

        traverse_egg(eggFile)
        return vertList_X, vertList_Y, vertList_Z

    def getUVList(self, eggFile):
        uvList = []
        # Some models don't get pass through the vertexPool check
        # so the UVs for smaller models don't get picked up
        for vertexPool in eggFile.getChildren():
            if not isinstance(vertexPool, EggVertexPool):
                continue
            for vertex in vertexPool:
                if not vertex.hasUv():
                    continue
                uvList.append(vertex.getUv())  # matplotlib lol
        return uvList


target_path = os.getcwd()
# tt_r_ara_ttc_hydrant
from eggtools.EggMan import EggMan
eggman = EggMan(
    [Filename.fromOsSpecific(os.path.join(target_path, "sample2/toon_cannon.egg"))]
    # [os.path.join(target_path, "testeggs")]
)
uve = UVExplorer(eggman)
