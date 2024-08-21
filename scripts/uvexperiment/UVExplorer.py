from eggtools.EggMan import EggMan
import os
from panda3d.core import *
from panda3d.egg import *
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import math

# https://www.albany.edu/faculty/jmower/geog/gog530Python/src/NormalizingCoordinatesManual.html
class UVExplorer:
    def __init__(self, filename):
        self.egg = EggData()
        self.egg.read(filename)
        uvList, binormalList = self.get_uvs(self.egg)
        plt.grid(True)
        plt.title(self.egg.egg_filename.getBasenameWoExtension())

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
        print("BBox")
        print(points)
        print(bot_left_x)
        print([point for point in x])

        return [(bot_left_x, bot_left_y), (top_right_x, top_right_y)]

    def get_uvs(self, eggFile):
        uvList = []
        binormalList = []

        random.seed("absdddc")

        global tex2UV
        tex2UV = {}

        global found
        found = False

        global name2Color
        name2Color = {}

        global testarrX, testarrY
        testarrX = []
        testarrY = []

        # global color
        # color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        def traverse_egg(egg):
            global tex2UV
            global found
            global name2Color
            global testarrX, testarrY

            # global color

            if found:
                return

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

                    # Random color for node differentiation
                    if not name2Color.get(child.getParent().getName()):
                        name2Color[child.getParent().getName()] = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

                    color = name2Color[child.getParent().getName()]

                    # print(child.getParent().getName())
                    if not cstrips.get(hash(str(color))):
                        cstrips[hash(str(color))] = []
                    #print(f"Guh - {isinstance(child, EggVertexPool)}")
                    # Ideally, we need to get vertex ids 0, 1, 2 from the group tt_r..blah
                    #print(child.getPool())
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
                            #print(egg_vertex)
                            # print(f"dimensions = {egg_vertex.getNumDimensions()}")

                            # uv_normalized = v_uv.normalized()

                            # egg_vertex.set_uv(uv_normalized.project(v_uv))

                            # egg_vertex.set_uv(v_uv.project(uv_normalized))
                            uv_obj = egg_vertex.get_uv_obj("")
                            if uv_obj.has_binormal():
                                binormalList.append(uv_obj.get_binormal())
                                print(uv_obj.get_binormal())
                            if egg_vertex.getUv()[0] == 1 or egg_vertex.getUv()[0] == 0 or egg_vertex.getUv()[1] == 1 or \
                                    egg_vertex.getUv()[1] == 0:
                                continue
                            x, y = egg_vertex.getUv()
                            # x *= 100
                            # y *= 100
                            uvList.append(egg_vertex.getUv())
                            # -k, mfc='C1', mec='C1',
                            cstrips[hash(str(color))].append([x, y])
                            # plt.plot(x, y, '-o', c=color, linestyle="--")


                    xlist = []
                    ylist = []
                    # bbox = self.bounding_box(uvList)

                    # print(f"bbox = {bbox}")
                    # print(child.getTextures())
                    # print(child.getVertices())

                    colLists = cstrips[hash(str(color))] # [ [1,2] [3,4] ]
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
                    # print(f"XX - {xx} | YY - {yy}")
                    # bx, by = bbox
                    # bxlist = np.array(bx)
                    # bylist = np.array(by)
                    # bxx = np.vstack([bxlist[0::2], bxlist[1::2]])
                    # byy = np.vstack([bylist[0::2], bylist[1::2]])
                    # rect = patches.Rectangle(bbox[0], bbox[1][0], bbox[1][1], linewidth=1, edgecolor='r', fc=(1,0,0,0.5))
                    # Create figure and axes
                    # fig, ax = plt.subplots(1)
                    # ax.add_patch(rect)
                    plt.plot(xx, yy, '-o',  c=color)
                    pass

        traverse_egg(eggFile)

        # https://stackoverflow.com/questions/2450035/scale-2d-coordinates-and-keep-their-relative-euclidean-distances-intact

        twoArr = np.array([testarrX, testarrY])
        print(testarrX)
        bbox = self.bounding_box(twoArr)
        xMin, yMin = bbox[0]
        xMax, yMax = bbox[1]
        # plt.plot(xMin, yMin, '-o', color="blue")
        # plt.plot(xMax, yMax, '-o', color="blue")

        norm = np.linalg.norm(twoArr, 1,  keepdims = True)

        twoArr /= norm

        # [(bot_left_x, bot_left_y), (top_right_x, top_right_y)]
        bbox = self.bounding_box(twoArr)
        xMin, yMin = bbox[0]
        xMax, yMax = bbox[1]
        print(f"{xMin} - {yMin} - {xMax} - {yMax}")
        # plt.plot(bbox, '-o', c = "red")
        # plt.plot(xMin, yMin, '-o', color="black")
        # plt.plot(xMax, yMax, '-o', color="black")

        scaledXArr = []
        scaledYArr = []
        print(f"(xMax + xMin)  = {(xMax + xMin) }")
        offsetX = 1 - (xMax + xMin)
        # offsetX = 1
        offsetY = 1 - (yMax + yMin)
        # offsetY = 1

        for xVal in testarrX:
            # xVal /= norm
            centerVal = xVal - (xMax + xMin) / 2
            centerVal += (xMax - xMin)


            centerVal = (centerVal - xMin) / (xMin - xMax)

            # centerVal += 2

            # does the fun scaling
            # centerVal /= max(xMax - xMin, yMax - yMin)

            # centerVal = abs(centerVal - math.ceil(centerVal))

            # centerVal /= 0.2

            # centerVal -= round(xMax)
            # centerVal += 0.5
            scaledXArr.append(centerVal)

        newXMax = xMax + (xMax - xMin)

        for yVal in testarrY:
            # yVal /= norm
            centerVal = yVal - (yMax + yMin) / 2
            centerVal += (yMax - yMin)

            print(f"CV = {centerVal}")
            print(f"C = {centerVal / max(xMax - xMin, yMax - yMin)}")
            print(f"Ceil - {math.ceil(max(xMax - xMin, yMax - yMin))}")
            # centerVal /= max(xMax - xMin, yMax - yMin)

            # centerVal = abs(centerVal - math.ceil(centerVal))

            centerVal = (centerVal - yMin) / (yMin - yMax)
            # centerVal += 2

            # does the fun scaling
            # centerVal /= max(xMax - xMin, yMax - yMin)
            # centerVal /= 0.2

            # centerVal += 0.5
            # centerVal -= round(yMax)

            scaledYArr.append(centerVal)

        twoArr = np.array([scaledXArr, scaledYArr])
        bbox = self.bounding_box(twoArr)
        xMin, yMin = bbox[0]
        xMax, yMax = bbox[1]
        # plt.plot(xMin, yMin, '-o', color="black")
        # plt.plot(xMax, yMax, '-o', color="black")
        #
        # newXArr = []
        # newYArr = []
        # for xVal in scaledXArr:
        #     centerVal = xVal
        #     centerVal /= max(xMax - xMin, yMax - yMin)
        #     newXArr.append(centerVal)
        #
        # for yVal in scaledYArr:
        #     centerVal = yVal
        #     centerVal /= max(xMax - xMin, yMax - yMin)
        #     newYArr.append(centerVal)
        #
        # twoArr = np.array([newXArr, newYArr])



        # twoArr /= max(xMax - xMin, yMax - yMin)
        twoArr /= 2
        twoArr *= -1

        # twoArr += 1


        print(f"norm - {norm}")

        # norm = np.linalg.norm(twoArr, 1, (0, 1))
        # twoArr /= norm

        # norm = np.linalg.norm([[xMin, yMin], [xMax, yMax]], 1, (0, 1))
        # twoArr /= norm


        # print(bbox)
        # plt.plot(bbox[0][0], bbox[0][1], '-ok', mfc = 'C1')
        # plt.plot(bbox[1][0], bbox[1][1], '-ok', mfc = 'C1')
        # 186.73092127
        # 186.73092127
        # np.append(twoArr, bbox[0])
        # np.append(twoArr, bbox[1])


        # np.append(twoArr, bbox[0][0], 0)
        # np.append(twoArr, bbox[1][0], 0)
        # np.append(twoArr, bbox[0][1], 1)
        # np.append(twoArr, bbox[1][1], 1)
        # twoArr[0].append(bbox[0][0])
        # twoArr[0].append(bbox[1][0])
        # twoArr[1].append(bbox[0][1])
        # twoArr[1].append(bbox[1][1])

        # twoArr.concatenate(bbox[0])
        # twoArr.concatenate(bbox[1])


        # x, y = np.where(twoArr)
        # print(x)

        # rows = np.any(twoArr, axis = 1)
        # cols = np.any(twoArr, axis = 0)
        # rmin, rmax = np.where(rows)[0][[0, -1]]
        # cmin, cmax = np.where(cols)[0][[0, -1]]

        # xMin, xMax = np.where(testarrX)[0][[0, -1]]
        # yMin, yMax = np.where(testarrY)[0][[0, -1]]
        # print(twoArr)
        # print(f"rmin - {rmin} | rmax - {rmax} | cmin - {cmin} | cmax - {cmax}")
        # plt.plot(xMin, xMax, '-o', mfc='C1')
        # plt.plot(yMin, yMax, '-o', mfc='C1')


        norm = np.linalg.norm(twoArr, 1)
        print(f"Norm = {norm}")
        # normalized_array = twoArr / norm
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
uve = UVExplorer(Filename.fromOsSpecific(os.path.join(target_path, "testeggs/target.egg")))
