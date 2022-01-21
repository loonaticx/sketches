# https://docs.panda3d.org/1.10/python/programming/directgui/directentry

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *


class QuizzyGUI(DirectFrame):
    def __init__(self):
        DirectFrame.__init__(
            self,
            relief = None,
            image_color = (1, 0, 0, 1),
            sortOrder = DGG.BACKGROUND_SORT_INDEX,
        )

        self.Ring4Data = None
        self.Ring3DData = None
        self.Ring1Data = None
        self.RingDatas = []

        self.BuildRings()
        self.loadGUI()

    def setText(self, val, index, ringLevel=0):
        """
        :param val: Character input
        :param index: Dictionary Key entry
        :param ringLevel: 0 is outermost ring (Ring4)
        """
        target = self.RingDatas[ringLevel]
        target[index] = val

    # clear the text
    def clearText(self, keyId):
        self.Ring4[keyId].enterText('')

    def BuildRings(self):
        defaultChar = 'A'
        self.Ring4 = {
            1: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, extraArgs = [1], numLines = 1, focus = 1,
                pos = (-1, 0, 0.75),
                initialText = defaultChar, width = 1,
            ),
            2: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.75, 0, 0.75), numLines = 1,
                initialText = defaultChar, focus = 1,
                width = 1, extraArgs = [2],
            ),
            3: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.5, 0, 0.75),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [3],
            ),
            4: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.25, 0, 0.75),
                numLines = 1, initialText = defaultChar, focus = 1,  width = 1, extraArgs = [4],
            ),
            5: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, numLines = 1, focus = 1,
                pos = (-0.25, 0, 0.50), extraArgs = [5], initialText = defaultChar,  width = 1,
            ),
            6: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.25, 0, 0.25), numLines = 1,
                initialText = defaultChar, focus = 1, width = 1, extraArgs = [6],
            ),
            7: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.25, 0, 0),
                numLines = 1, initialText = defaultChar, focus = 1,  width = 1, extraArgs = [7],
            ),
            8: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.5, 0, 0),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [8],
            ),
            9: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.75, 0, 0),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [9],
            ),
            10: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-1, 0, 0),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [10],
            ),
            11: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-1, 0, 0.25),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [11],
            ),
            12: DirectEntry(
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-1, 0, 0.5),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [12],
            ),
        }
        self.Ring4Data = {
            1: defaultChar,
            2: defaultChar,
            3: defaultChar,
            4: defaultChar,
            5: defaultChar,
            6: defaultChar,
            7: defaultChar,
            8: defaultChar,
            9: defaultChar,
            10: defaultChar,
            11: defaultChar,
            12: defaultChar
        }

        Ring3Color = (0.8, 0, 0.8, 1)
        self.Ring3 = {
            1: DirectEntry(
                color = Ring3Color,
                #color = (0, 1, 0, 1),
                text = "", parent = self, scale = 0.1, command = self.setText, extraArgs = [1, 1], numLines = 1, focus = 1,
                pos = (-0.80, 0, 0.55),
                initialText = defaultChar, width = 1,
            ),
            2: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.60, 0, 0.55), numLines = 1,
                initialText = defaultChar, focus = 1,
                width = 1, extraArgs = [2, 1],
            ),
            3: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.40, 0, 0.55),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [3, 1],
            ),
            4: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.40, 0, 0.35),
                numLines = 1, initialText = defaultChar, focus = 1,  width = 1, extraArgs = [4, 1],
            ),
            5: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, numLines = 1, focus = 1,
                pos = (-0.40, 0, 0.15), extraArgs = [5, 1], initialText = defaultChar,  width = 1,
            ),
            6: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.60, 0, 0.15), numLines = 1,
                initialText = defaultChar, focus = 1, width = 1, extraArgs = [6, 1],
            ),
            7: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.80, 0, 0.15),
                numLines = 1, initialText = defaultChar, focus = 1,  width = 1, extraArgs = [7, 1],
            ),
            8: DirectEntry(
                color = Ring3Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.80, 0, 0.35),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [8, 1],
            ),
        }
        self.Ring3Data = {
            1: defaultChar,
            2: defaultChar,
            3: defaultChar,
            4: defaultChar,
            5: defaultChar,
            6: defaultChar,
            7: defaultChar,
            8: defaultChar,
        }

        Ring1Color = (0.8, 0.8, 0, 1)
        self.Ring1 = {
            1: DirectEntry(
                color = Ring1Color,
                text = "", parent = self, scale = 0.1, command = self.setText, pos = (-0.60, 0, 0.35),
                numLines = 1, initialText = defaultChar, focus = 1, width = 1, extraArgs = [1, 2],
            ),
        }
        self.Ring1Data = {
            1: defaultChar
        }

        self.RingDatas = [self.Ring4Data, self.Ring3Data, self.Ring1Data]

    def extractText(self):
        for ringDict in self.RingDatas:
            if ringDict is None:
                print("none")
                return
            charList = []
            for index in ringDict:
                charList.append(ringDict[index][0].upper())  # Just in case a typo is made, ONLY get the first char
            print(charList)
            # return charList

    def loadGUI(self):
        self.extractButton = DirectButton(
            parent = self,
            pos = (0.8, 0, 0),
            text = "Extract Text",
            scale = 0.1,
            command = self.extractText,
        )



QuizzyGUI = QuizzyGUI()
base.run()
