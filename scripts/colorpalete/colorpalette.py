from panda3d.core import Vec3, Vec4

import math
import sys
from PIL import Image, ImageDraw
import extcolors


# https://kylermintah.medium.com/coding-a-color-palette-generator-in-python-inspired-by-procreate-5x-b10df37834ae

def normalToDecimal(colors):
    print(colors)
    if type(colors) == list:
        for colorVec in colors:
            for colorValue in range(len(tuple(colorVec))):
                colorVec[colorValue] *= 255
                # colorVec[colorValue] = int(colorVec[colorValue])
            colorVec = ((tuple(colorVec)), 0)
        return colors
    for colorVec in range(colors):
        colors[colorVec] *= 255
    return tuple(colors)


def render_color_platte(colors):
    colors = normalToDecimal(colors)
    print(colors)
    size = 100
    columns = 6
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill = color[0])
    return result


TrophyStarColors = [
    Vec4(0.9, 0.6, 0.2, 1),
    Vec4(0.9, 0.6, 0.2, 1),
    Vec4(0.8, 0.8, 0.8, 1),
    Vec4(0.8, 0.8, 0.8, 1),
    Vec4(1, 1, 0, 1),
    Vec4(1, 1, 0, 1)
]

colorList = [
    ((255, 255, 255), 0)
]
print(render_color_platte(TrophyStarColors))
