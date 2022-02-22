# creates svg file from a list of colors and years
def createSVG(colors, years, fileName, width=3780, height=2126):
    if len(colors) != len(years):
        print("Error: colors and years must be the same length " + fileName)
        return
    svgHead = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg  viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg">\n""".format(width,height)

    barWidth = width/len(colors)
    for i in range(len(colors)):
        svgHead += """<rect x="{}" y="0" width="{}" height="{}" fill="{}"><title>{}</title></rect>\n""".format(round(barWidth*i,2),round(barWidth+1.5),height,colors[i][:-2],int(years[i]))

    #open a file and write to it
    f = open(fileName+".svg","w", newline="")
    f.write(svgHead + "</svg>")
    f.close()
    print("SVG created: " + fileName)

#createSVG(["#08306b", "#08519c", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef", "#deebf7", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],3780,2126,"test5.svg")