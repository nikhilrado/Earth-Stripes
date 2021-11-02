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
import statistics

counter = 0

def createChart(csvPath,imagePath,chartType="bars",save=True,width=3780,height=2126,transparency=False): 
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

    if "NOAA" in csvPath:
        dataSource = "NOAA"
        dataSourceLink = "https://www.noaa.gov/"
    if "berkley-earth" in csvPath:
        dataSource = "Berkeley Earth"
        dataSourceLink = "http://berkeleyearth.org/"
    else:
        dataSource = "unknown"
        dataSourceLink = None

    manageJSON.updateMetadata(imagePath,chartType,width=width,height=height,startYear=firstYear,endYear=lastYear,dataSource=dataSource, dataSourceLink=dataSourceLink, name=location)

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

        #returns temperatures between two dates inclusive with date1 being lower than date2
        def getDatesBetween(listOfTemperatures,date1,date2):
            tempsBetweenDates = []
            if len(years) != len(listOfTemperatures): #just a check
                print("----------ERROR: temps and years don't have same length")
            for i in range(len(listOfTemperatures)):
                if years[i] >= date1 and  years[i] <= date2:
                    tempsBetweenDates.append(listOfTemperatures[i])
            return tempsBetweenDates
            
                    
        #runs a bunch of stats on the data
        mean1971_2000 = numpy.mean(removeNAN(getDatesBetween(temps,1971,2000))) #QualityControlDone #mean temperature from 1971-2000
        temps1901_2000 = removeNAN(getDatesBetween(temps,1901,2000)) #QualityControlDone #all temps from 1901-2000 without NaN
        mean1901_2000 = numpy.mean(temps1901_2000) #mean temperature from 1971-2000
        maxstd1901_2000 = mean1901_2000 + 2.6*numpy.std(temps1901_2000)
        minstd1901_2000 = mean1901_2000 - 2.6*numpy.std(temps1901_2000)
        meanTemp = numpy.mean(cleanTemps) #mean of all temperatures
        maxTemp = max(cleanTemps) #max of all temps
        minTemp = min(cleanTemps) #min of all temps
        upperBoundTemp = maxstd1901_2000#numpy.average(temps1901_2000) + 2.6*statistics.stdev(temps1901_2000)#meanTemp + 2.6*numpy.std(cleanTemps) #if any temp is higher than this it will be pushed down to highest bar color
        lowerBoundTemp = minstd1901_2000 #numpy.average(temps1901_2000) - 2.6*statistics.stdev(temps1901_2000) #meanTemp - 2.6*numpy.std(cleanTemps) #if any temp is lower than this it will be pushed up to lowest bar color
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
            #anomalyList.append(round(anomaly,3))
            anomalyList.append(round(anomaly,1))
            #print(anomaly)
            #anomaly = round(anomaly,1)
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
            unboundedGradientPercent = gradientPercent #this keeps the original gradient percent so it can be used as height in the bars, but allows the gradientPercent to continue so colors will fall in their consistant categories
            if gradientPercent > 1: 
                gradientPercent = 1       
            elif gradientPercent < 0:
                gradientPercent = 0


            gradientListIndex = gradientPercent*(len(gradientList))

            #this segment breaks the colors up into buckets instead of rounding
            #for m in range(len(gradientList)):
            #    gradientListIndex = gradientPercent*(len(gradientList))
            #    if gradientListIndex > m and gradientListIndex <= m+1:
            #        gradientListIndex = m +1
            #        break
            
            
            #--use the following line if the gradient is in rgb, such as when it is being generated by gradient.py
            #color = matplotlib.colors.to_hex((float(gradientList[gradientListIndex][0])/256, float(gradientList[gradientListIndex][1])/256, float(gradientList[gradientListIndex][2])/256))
            if gradientListIndex < 1:
                gradientListIndex = 1
            try:
                color = gradientList[round(gradientListIndex-1)]
                #print(round(gradientListIndex)-1)
                #print(color)
            except:
                pass

            if gradientPercent > 1: 
                color = "#67000dff"
            elif gradientPercent < 0:
                color = "#08306bff"
            fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 30) #for testing only

            if "stripes" in chartType:
                barWidth = width/len(temps) #how wide each bar should be
                img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,height)], fill=color)

            if "twitter-card" in chartType:
                width = 600*2
                height = 314*2
                barWidth = width/len(temps) #how wide each bar should be
                img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,height)], fill=color)
                
            if "snap-sticker" in chartType:
                width = 4000
                height = 4000
                barWidth = (width*.8)/len(temps)

                if i == 0:
                    text = location + " Temp. %i-%i" %(firstYear,lastYear)
                    bottomText = "#globalwarming"
                    
                    img1.rounded_rectangle([(width*.09,height*.39),(width*.91,height*.61)], fill="white", radius=30) #draws big box

                    #draws the top text box
                    fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 200)
                    textLength = img1.textlength(text,font=fnt)
                    img1.rounded_rectangle([(width/2-textLength/2-.01*width,height*.32),(width/2+textLength/2+.01*width,height*.5)], fill="white", radius=30)
                    img1.text((width/2-textLength/2,height*.325),text,(0,0,0),font=fnt)
                    
                    #draws the bottom text box
                    fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 120)
                    textLength = img1.textlength(bottomText,font=fnt)
                    img1.rounded_rectangle([(width/2-textLength/2-.01*width,height*.5),(width/2+textLength/2+.01*width,height*.65)], fill="white", radius=30)
                    img1.text((width/2-textLength/2,height*.61),bottomText,(0,0,0),font=fnt)

                if i == 0 or i == len(temps)-1:
                    radius = 50
                    if i == 0:
                        img1.rectangle([(i*barWidth+width*.1+barWidth/2,height*.4),(i*barWidth+width*.1+barWidth,height*.6)], fill=color)
                    if i == len(temps)-1:
                        img1.rectangle([(i*barWidth+width*.1,height*.4),(i*barWidth+width*.1+barWidth-barWidth/2,height*.6)], fill=color)
                else:
                    radius = 0
                img1.rounded_rectangle([(i*barWidth+width*.1,height*.4),(i*barWidth+width*.1+barWidth,height*.6)], fill=color, radius=radius)

                #img1.ellipse([(20,100),(width-20,300)],fill="red")
                #barWidth = width/len(temps) #how wide each bar should be
                #img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,height)], fill=color)
            
            elif "bars" in chartType:
                #barHeight = height/2-(gradientPercent-.5)*2000
                #for some reason bars under zero have an issue with them being halved, working on a better solution rn
                if anomaly < 0:
                    unboundedGradientPercent = (unboundedGradientPercent -.5)*2 + .5
                barHeight = height/2-(unboundedGradientPercent-.5)*900
                
                sideBorder = 100
                barWidth = (width-2*sideBorder)/len(temps)
                img1.rectangle([(round(i*barWidth+sideBorder),height/2),(i*barWidth+sideBorder+barWidth,barHeight)], fill=color)  
                #img1.text((i*barWidth+sideBorder,barHeight),str(round(anomaly,2)),(255,255,255),font=fnt)
            
        #attempts to get a color for the last 20 years, to show rate of warming
        jsonPath = imagePath.replace(chartType,"json")+".json"
        last20YrsAnomaly = numpy.mean(anomalyList[-20:])
        if last20YrsAnomaly < 0:
            #gradientPercent = anomaly/(min1901_2000-mean1971_2000)
            last20YrsAnomaly = 0.5-(last20YrsAnomaly/(lowerBoundTemp-mean1971_2000))/2
        if last20YrsAnomaly >= 0:
            #gradientPercent = anomaly/(max1901_2000-mean1971_2000)
            last20YrsAnomaly = 0.5+(last20YrsAnomaly/(upperBoundTemp-mean1971_2000))/2
        if last20YrsAnomaly > 1:
            last20YrsAnomaly = 1
        AveColor = gradientList[round(last20YrsAnomaly*len(gradientList)-1)]
        manageJSON.updateDataObjet(jsonPath,"metadata",AveColor,"color")
        #(fileName,name,data)

            #print(i)
        #print(anomalyList)

    def drawInfo(text="New York, NY", infoType=chartType):
        #draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 130)
        
        if "twitter-card" in infoType:
            fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 60)
            width = 600*2
            height = 314*2
            text = text + " Temp %i-%i" %(firstYear,lastYear)
            textLength = img1.textlength(text,font=fnt) #gets the width in px of the text so we know where to end background
            img1.rectangle([(50,height-120),(textLength+50+10,height-50)], fill ="#ffffff")
            img1.text((45+10,height-120),text,(0,0,0),font=fnt)
        if "stripes" in infoType:
            #font = ImageFont.truetype('E:/PythonPillow/Fonts/FreeMono.ttf', 40)
            # draw.text((x, y),"Sample Text",(r,g,b))
            height=2126
            textLength = img1.textlength(text,font=fnt) #gets the width in px of the text so we know where to end background
            img1.rectangle([(50,height-200),(textLength+50+30,height-50)], fill ="#ffffff")
            img1.text((50+10,height-200),text,(0,0,0),font=fnt)
        if "label" in infoType:
            #font = ImageFont.truetype('E:/PythonPillow/Fonts/FreeMono.ttf', 40)
            # draw.text((x, y),"Sample Text",(r,g,b))
            height=150
            text = "earthstripes.org"
            textLength = img1.textlength(text,font=fnt) #gets the width in px of the text so we know where to end background
            img1.rectangle([(0,0),(textLength+20,height)], fill ="#ffffff")
            img1.text((10,0),text,(0,0,0),font=fnt)
        elif "bars" in infoType:
            img1.text((100+10,120),text + " Temperature %i-%i" %(firstYear,lastYear),(255,255,255),font=fnt)
    
    
    shape = [(40, 40), (width - 10, height - 10)]
    
    # creating new Image object
    if chartType == "snap-sticker":
        img = Image.new("RGBA", (4000, 4000))
    elif chartType == "twitter-card":
        img = Image.new("RGBA", (600*2, 314*2))
    elif chartType == "label":
        img = Image.new("RGBA", (2126, 150))
    else:
        img = Image.new("RGB", (width, height))
    
    # create rectangle image
    #newsize = (300, 300)
    #im1 = im1.resize(newsize)
    img1 = ImageDraw.Draw(img)  
    #img1.rectangle([(0,0),(50,100)], fill ="#ffff33")


    heatmap = [
    [0, (0, 0, 1)],
    [.5, (1.0, 1, 1.0)],
    [1, (1.0, 0, 0)],
    ] 
    #gradientList = gradient.generateGradient(heatmap)
    gradientList = ["#08306bff", "#08519cff", "#2171b5ff", "#4292c6ff", "#6baed6ff", "#9ecae1ff", "#c6dbefff", "#deebf7ff", "#fee0d2ff", "#fcbba1ff", "#fc9272ff", "#fb6a4aff", "#ef3b2cff", "#cb181dff", "#a50f15ff", "#67000dff"]
    #gradientList = ["#08519cff", "#2171b5ff", "#4292c6ff", "#6baed6ff", "#9ecae1ff", "#c6dbefff", "#deebf7ff", "#fee0d2ff", "#fcbba1ff", "#fc9272ff", "#fb6a4aff", "#ef3b2cff", "#cb181dff", "#a50f15ff"]


    drawBars(chartType)
    #only draws info on the thing if the file name says labeled in it
    if "labeled" in chartType or "twitter-card" in chartType or chartType == "label":
        drawInfo(location,chartType)
    #TODO figure out how to add the info
    #TODO test the algorithim
    #TODO investiate why alaska won't work

    #img.show() #will display the image in popup
    #actually saves the image unless save is false
    if save:
        if not(os.path.isdir(os.path.dirname(imagePath))):
            os.makedirs(os.path.dirname(imagePath))
        img.save(imagePath + ".png")
        
    
    img.save("C:/Users/radon/Downloads/test201" + ".png")
    print("Done: Image %s: %s" % (str(counter),imagePath))




# "HI" was removed from states list cause no data found on NOAA website for it
statesList = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#for state in statesList:
#    createChart(state)
#createChart("data/us-state-data-NOAA/AL.csv","results/labeled-stripes/US/AL",chartType="labeled-stripes")
#createChart("World Data Stuff/global-land - AnnTemp 1901-2020.csv","results/label/US",chartType="labeled-bars")
createChart("data/USA.csv","results/twitter-card/US",chartType="twitter-card")
#createChart("state-data\AK.csv","test7.png")
#createChart("state-province data stuff/Acre - AnnTemp 1901-2020.csv","results/stripes/EG",chartType="stripes",save=False)
#createChart("data/us-state-data-NOAA/CA.csv","results/stripes/US/CA",chartType="stripes",save=False)
#createChart("data/us-state-data-NOAA/CA.csv","results/labeled-bars/US/CA",chartType="labeled-bars",save=False)

