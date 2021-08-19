#from numpy.core.numeric import NaN
#from numpy.lib.type_check import nan_to_num
import gradient
import numpy
import math
import matplotlib
from PIL import Image, ImageDraw, ImageFont
import csv
from datetime import datetime
import os
import manageJSON

counter = 0

def createChart(csvPath,imagePath,chartType="bars",save=False,width=3780,height=2126): 
    global counter
    counter += 1
    #f = open('testdata.csv')
    #f = open('state-data/'+csvName + '.csv')
    f = open(csvPath)

    csv_f = csv.reader(f)

    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    location = rowsList[0][0]
    if len(location) == 2:
        location = rowsList[0][1]
    rowsList = rowsList[5:] #removes data headers and descriptions
    #print(rowsList)
    #manageJSON.main(imagePath,location)
    
    #adds the years to a list
    years = []
    for row in rowsList:
        if len(row[0]) == 6:
            years.append(float(row[0][:-2]))
        else:
            years.append(float(row[0]))
    #print(years)

    firstYear = years[0]
    lastYear = years[-1]

    manageJSON.updateMetadata(imagePath,chartType,width=width,height=height,startYear=firstYear,endYear=lastYear)

    #adds the temperatures to a list
    temps = []
    for row in rowsList:
        temps.append(float(row[1]))
    #print(temps)

    #supposed to convert rbg to hexadecimal for gradient, not sure if it works well
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    def drawBars(chartType=chartType,width=width, height=height):
        #creates a new list without any "nan" values so statistics can be calculated
        def removeNAN(list):
            newList = []
            for item in list:
                if not(math.isnan(item)):
                    newList.append(item)
            return newList
        cleanTemps = removeNAN(temps)

        #runs a bunch of stats on the data
        mean1971_2000 = numpy.mean(removeNAN(temps[76:-21])) #mean temperature from 1971-2000
        temps1901_2000 = removeNAN(temps[6:-21]) #all temps from 1901-2000 without NaN
        max1901_2000 = max(temps1901_2000) + 2.6*numpy.std(temps1901_2000)
        min1901_2000 = min(temps1901_2000) - 2.6*numpy.std(temps1901_2000)
        meanTemp = numpy.mean(cleanTemps) #mean of all temperatures
        maxTemp = max(cleanTemps) #max of all temps
        minTemp = min(cleanTemps) #min of all temps
        upperBoundTemp = meanTemp + 2.6*numpy.std(cleanTemps) #if any temp is higher than this it will be pushed down to highest bar color
        lowerBoundTemp = meanTemp - 2.6*numpy.std(cleanTemps) #if any temp is lower than this it will be pushed up to lowest bar color
        #gradientPercent = round(mean1971_2000-lowerBoundTemp,3)/(upperBoundTemp-lowerBoundTemp)

        #print("Gradient List Length: %s" % len(gradientList))
        #print("barwidth: %s" % barWidth)
        #print("lowerBoundTemp: %s" % lowerBoundTemp)
        #print("upperBoundTemp: %s" % upperBoundTemp)
        #print("gradientPercent: %s" % gradientPercent)
        #print("diff:"+str(max1901_2000-mean1971_2000))

        anomalyList = []

        for i in range(len(years)):
            #--these 4 lines were used to test the stripes
            """if i % 2 == 0:
                img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,h)], fill ="#ffff33")
            else:
            img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,h)], fill ="#ff3333")"""

            #if the data is not reliable this will not draw a box for "nan" value
            if numpy.isnan(temps[i]):
                #print("yeeeeeeet")
                continue
            
            anomaly = temps[i]-mean1971_2000
            anomalyList.append(round(anomaly,3))
            #print(anomaly)
            if anomaly < 0:
                #gradientPercent = anomaly/(min1901_2000-mean1971_2000)
                gradientPercent = 0.5-(anomaly/(lowerBoundTemp-mean1971_2000))/2
                
            if anomaly >= 0:
                #gradientPercent = anomaly/(max1901_2000-mean1971_2000)
                gradientPercent = 0.5+(anomaly/(upperBoundTemp-mean1971_2000))/2
            #print(gradientPercent)

            #--calculates where on the gradient line the color should be selected from as a decimal from 0-1
            #gradientPercent = round(temps[i]-minTemp,3)/(maxTemp-minTemp)

            #--sets the gradint Percent to the min and max of 0 or 1 when the data goes over
            if gradientPercent > 1: 
                gradientPercent = 1
            elif gradientPercent < 0:
                gradientPercent = 0


            gradientListIndex = gradientPercent*(len(gradientList))

            """lenOfGradientList = len(gradientList)
            for j in range(lenOfGradientList):
                
                if gradientPercent > (j/lenOfGradientList) and gradientPercent <= ((j+1)/lenOfGradientList):
                    gradientListIndex = j
                    break"""
            
            #--use the following line if the gradient is in rgb, such as when it is being generated by gradient.py
            #color = matplotlib.colors.to_hex((float(gradientList[gradientListIndex][0])/256, float(gradientList[gradientListIndex][1])/256, float(gradientList[gradientListIndex][2])/256))
            if gradientListIndex < 1:
                gradientListIndex = 1
            color = gradientList[round(gradientListIndex)-1]
            #print(round(gradientListIndex)-1)
            #print(color)

            if "stripes" in chartType:
                barWidth = width/len(temps) #how wide each bar should be
                img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,height)], fill=color)
            elif "bars" in chartType:
                barHeight = height/2-(gradientPercent-.5)*2000
                sideBorder = 100
                barWidth = (width-2*sideBorder)/len(temps)
                img1.rectangle([(round(i*barWidth+sideBorder),height/2),(i*barWidth+sideBorder+barWidth,barHeight)], fill=color)            

            #print(i)
        #print(anomalyList)

    def drawInfo(text="New York, NY", infoType=chartType):
        #draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("Roboto/Roboto-Regular.ttf", 130)
        
        if "stripes" in infoType:
            #font = ImageFont.truetype('E:/PythonPillow/Fonts/FreeMono.ttf', 40)
            # draw.text((x, y),"Sample Text",(r,g,b))
            textLength = img1.textlength(text,font=fnt) #gets the width in px of the text so we know where to end background
            img1.rectangle([(50,height-200),(textLength+50+30,height-50)], fill ="#ffffff")
            img1.text((50+10,height-200),text,(0,0,0),font=fnt)
        elif "bars" in infoType:
            img1.text((100+10,120),text + " Temperature %i-%i" %(firstYear,lastYear),(255,255,255),font=fnt)
    
    
    shape = [(40, 40), (width - 10, height - 10)]
    
    # creating new Image object
    img = Image.new("RGB", (width, height))
    
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

    drawBars(chartType)
    #only draws info on the thing if the file name says labeled in it
    if "labeled" in chartType:
        drawInfo(location,chartType)
    #TODO figure out how to add the info
    #TODO test the algorithim
    #TODO investiate why alaska won't work

    #img.show() #will display the image in popup
    #actually saves the image unless save is false
    if save:
        if not(os.path.isdir(os.path.dirname(imagePath))):
            os.mkdir(os.path.dirname(imagePath))
        img.save(imagePath + ".png")

    print("Done: Image %s: %s" % (str(counter),imagePath))




# "HI" was removed from states list cause no data found on NOAA website for it
statesList = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#for state in statesList:
#    createChart(state)
#createChart("World Data Stuff\data\processed\Japan COUNTRY - AnnTemp 1901-2020.csv","World Data Stuff\data\processed\Japan COUNTRY - AnnTemp 1901-2020.png")
#createChart("G:/.shortcut-targets-by-id/1-78WtuBsUrKVKWF1NKxPcsrf1nvacux2/AP CSP VS Code Workspace/USA.csv","test12.jpg")
#createChart("state-data\AK.csv","test7.png")
createChart("data\country-data-berkley-earth\processed\TZ - AnnTemp 1901-2015.csv","results/bars/TZ")
