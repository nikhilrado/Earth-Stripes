def createSVG(colors, width, height,fileName):
    svgHead = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">
    """.format(width,height)

    barWidth = width/len(colors)
    for i in range(len(colors)):
        svgHead += """<rect x="{}" y="0" width="{}" height="{}" fill="{}"><title>{}</title></rect>\n""".format(barWidth*i,barWidth,height,colors[i],colors[i])

    print(svgHead + "</svg>")
    #open a file and write to it
    f = open("test5.svg","w", newline="")
    f.write(svgHead + "</svg>")
    f.close()

createSVG(["#08306b", "#08519c", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef", "#deebf7", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],3780,2126,"test5.svg")