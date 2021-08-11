import gradient
import numpy
import math
import matplotlib
from PIL import Image, ImageDraw, ImageFont
import csv

def createChart(csvName):
    #f = open('30-tavg-12-12-1895-2020.csv')
    #f = open('testdata.csv')
    f = open('AL-003-tavg-1-5-1895-2021 (4).csv')
    #f = open('state-data/'+csvName + '.csv')

    csv_f = csv.reader(f)

    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    rowsList = rowsList[5:] #removes data headers and descriptions
    #print(rowsList)

    #adds the years to a list
    years = []
    for row in rowsList:
        years.append(float(row[0][:-2]))
    #print(years)

    #adds the temperatures to a list
    temps = []
    for row in rowsList:
        temps.append(float(row[1]))
    #print(temps)

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb



    def drawBars():
        mean1971 = numpy.mean(years[76:-21])
        print(len(gradientList))
        barWidth = w/len(temps)
        print("barwidth: %s" % barWidth)
        meanTemp = numpy.mean(temps)
        maxTemp = max(temps)
        minTemp = min(temps)
        maxTemp = meanTemp + 2.6*numpy.std(temps)
        minTemp = meanTemp - 2.6*numpy.std(temps)
        print(minTemp)
        print(maxTemp)
        for i in range(len(years)):
            #--these 4 lines were used to test the stripes
            """if i % 2 == 0:
                img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,h)], fill ="#ffff33")
            else:
            img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,h)], fill ="#ff3333")"""

            #--calculates where on the gradient line the color should be selected from as a decimal from 0-1
            gradientPercent = round(temps[i]-minTemp,3)/(maxTemp-minTemp)

            #--sets the gradint Percent to the min and max of 0 or 1 when the data goes over
            if gradientPercent > 1: 
                gradientPercent = 1
            elif gradientPercent < 0:
                gradientPercent = 0

            gradientListIndex = gradientPercent*(len(gradientList))

            length = len(gradientList)
            for j in range(length):
                thing = j/length, (j+1)/length
                if gradientPercent > (j/length) and gradientPercent <= ((j+1)/length):
                    gradientListIndex = j
                    break
            
            #--use the following line if the gradient is in rgb, such as when it is being generated by gradient.py
            #color = matplotlib.colors.to_hex((float(gradientList[gradientListIndex][0])/256, float(gradientList[gradientListIndex][1])/256, float(gradientList[gradientListIndex][2])/256))
            color = gradientList[gradientListIndex]
            #print(color)
            
            img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,h)], fill =color)

            i += barWidth  
            #print(i)

    def drawInfo():
        #draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        img1.rectangle([(50,h-200),(1000,h-50)], fill ="#ffffff")
        #font = ImageFont.truetype('E:/PythonPillow/Fonts/FreeMono.ttf', 40)
        # draw.text((x, y),"Sample Text",(r,g,b))
        img1.text((50,h-200),"Sample Text",(0,0,0))
    
    w, h = 3780, 2126 
    shape = [(40, 40), (w - 10, h - 10)]
    
    # creating new Image object
    img = Image.new("RGB", (w, h))
    
    # create rectangle image
    img1 = ImageDraw.Draw(img)  
    #img1.rectangle([(0,0),(50,100)], fill ="#ffff33")


    heatmap = [
    [0, (0, 0, 1)],
    [.5, (1.0, 1, 1.0)],
    [1, (1.0, 0, 0)],
    ] 
    #gradientList = gradient.generateGradient(heatmap)
    gradientList = ["#08306bff", "#08519cff", "#2171b5ff", "#4292c6ff", "#6baed6ff", "#9ecae1ff", "#c6dbefff", "#deebf7ff", "#fee0d2ff", "#fcbba1ff", "#fc9272ff", "#fb6a4aff", "#ef3b2cff", "#cb181dff", "#a50f15ff", "#67000dff"]

    drawBars()
    drawInfo()

    img.show()
    #img.save("G:/.shortcut-targets-by-id/1-78WtuBsUrKVKWF1NKxPcsrf1nvacux2/AP CSP VS Code Workspace/states/" + csvName + ".png")



# "HI" was removed from states list cause no data found on NOAA website for it
statesList = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#for state in statesList:
#    createChart(state)
createChart("AK")
