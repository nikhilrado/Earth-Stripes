#!/usr/bin/env python
#This code was taken and modified from https://stackoverflow.com/a/31125282

width, height = 1000, 200

import math
from PIL import Image
im = Image.new('RGB', (width, height))
ld = im.load()



def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b)**2 / (2 * c**2)) + d

def pixel(x, width=100, map=[], spread=1.7):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
    g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
    b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
    return min(1.0, r), min(1.0, g), min(1.0, b)

# A map of rgb points in your distribution
# [distance, (r, g, b)]
# distance is percentage from left edge
defaultHeatmap = [ #not called rn
[0, (0, 0, 1)],
[1, (1.0, 1.0, 1.0)],
[1, (1.0, 0, 0)],
] 
def generateGradient(heatmap):
    gradientList = []
    for x in range(im.size[0]):
        r, g, b = pixel(x, width=im.size[0], map=heatmap)
        r, g, b = [int(256*v) for v in (r, g, b)]
        gradientList.append([r,g,b])
        #print("(%d,%d,%d)" % (r, g, b))
        for y in range(im.size[1]):
            ld[x, y] = r, g, b
    
    im.save('grad.png')
    return gradientList

["#08306bff", "#08519cff", "#2171b5ff", "#4292c6ff", "#6baed6ff", "#9ecae1ff", "#c6dbefff", "#deebf7ff", "#fee0d2ff", "#fcbba1ff", "#fc9272ff", "#fb6a4aff", "#ef3b2cff", "#cb181dff", "#a50f15ff", "#67000dff"]