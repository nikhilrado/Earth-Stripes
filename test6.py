import gradient
import numpy
import math
from PIL import Image, ImageDraw, ImageFont
import csv
from datetime import datetime
import os
import manageJSON
import createSVG

counter = 0
color2020 = []
color2021 = []
temp2020 = []
temp2021 = []

# main function that takes in a data file and creates a chart.
# parameter globe sets the color scale to the +0.75C to -0.75C scale when true
def createChart(csvPath,imagePath,chartType="bars",save=True,width=3780,height=2126,globe=False): 
    global counter, color2020, color2021, temp2020, temp2021
    colors = []

    counter += 1

    # reads data in file, converts to list, extracts relevant metadata
    f = open(csvPath)
    csv_f = csv.reader(f)
    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    location = rowsList[0][1]
    metadataList = rowsList[:15] # creates list containing file metadata
    rowsList = rowsList[15:] # removes data headers and descriptions
    #print(rowsList)
    
    # adds the years to a list, and trims excess chars from the year to make it 4 digits
    years = []
    for row in rowsList:
        if len(row[0]) == 6:
            years.append(float(row[0][:-2]))
        else:
            years.append(float(row[0]))
    firstYear = years[0]
    lastYear = years[-1]
    #print("years: ", years)

    # adds the temperatures to a list
    temps = []
    for row in rowsList:
        temps.append(float(row[1]))
    #print("temps: ", temps)

    # sets dataSource and dataSourceLink properties to be added to the JSON file, updates the JSON image metadata file
    dataSource = metadataList[6][1] if metadataList[6][0] == "Data Source:" else None
    dataSourceLink = metadataList[7][1] if metadataList[7][0] == "Data Source URL:" else None
    manageJSON.updateMetadata(imagePath,chartType,width=width,height=height,startYear=firstYear,endYear=lastYear,dataSource=dataSource, dataSourceLink=dataSourceLink, name=location)


    def drawBars(chartType=chartType,width=width, height=height):

        #creates a new list without any "nan" values so statistics can be calculated
        def removeNAN(list):
            newList = []
            for item in list:
                if not(math.isnan(item)):
                    newList.append(item)
            return newList

        #returns temperatures between two dates inclusive with date1 being lower than date2, returns one value if both dates are equal
        def getTempsBetweenDates(listOfTemperatures,date1,date2):
            tempsBetweenDates = []
            if len(years) != len(listOfTemperatures): #just a check
                print("----------ERROR: temps and years don't have same length")
            for i in range(len(listOfTemperatures)):
                if years[i] >= date1 and  years[i] <= date2:
                    tempsBetweenDates.append(listOfTemperatures[i])
            return tempsBetweenDates
        
        # runs a bunch of statistics on the data
        cleanTemps = removeNAN(temps)  # should only be used to calculate stats because it removes NAN values, shortening the length
        mean1971_2000 = numpy.mean(removeNAN(getTempsBetweenDates(temps,1971,2000)))
        temps1901_2000 = removeNAN(getTempsBetweenDates(temps,1901,2000))
        mean1901_2000 = numpy.mean(temps1901_2000)
        maxstd1901_2000 = mean1901_2000 + 2.6*numpy.std(temps1901_2000)
        minstd1901_2000 = mean1901_2000 - 2.6*numpy.std(temps1901_2000)
        range2 = 2.6*numpy.std(temps1901_2000)
        meanTemp = numpy.mean(cleanTemps)
        maxTemp = max(cleanTemps)
        minTemp = min(cleanTemps)
        # sets upper and lower bound temperatures to 2.6 standard deviations above and below the mean, or 0.75C to -0.75C if globe is true
        upperBoundTemp = maxstd1901_2000 if not globe else 0.75
        lowerBoundTemp = minstd1901_2000 if not globe else -0.75

        anomalyList = []  # will be list of anomalies from 1971-2000 mean
        for i in range(len(years)):

            # if the data is not reliable this will not draw a box for "nan" value
            if numpy.isnan(temps[i]):
                continue

            anomaly = temps[i]-mean1971_2000
            anomalyList.append(anomaly)

            if anomaly < 0:
                gradientPercent = 0.5-(-1*anomaly/(range2))/2
                if globe:  # overwrite gradient percent if is entire globe
                    gradientPercent = 0.5-(anomaly/(lowerBoundTemp))/2
            if anomaly >= 0:
                gradientPercent = 0.5+(anomaly/(range2))/2
                if globe:  # overwrite gradient percent if is entire globe
                    gradientPercent = 0.5+(anomaly/(-1*lowerBoundTemp))/2
            #print(gradientPercent)
            
            # sets the gradient Percent to the min and max of 0 or 1 when the data goes over the upper or lower bound
            # this keeps the original gradient percent so it can be used as height in the bars
            unboundedGradientPercent = gradientPercent
            # restricts gradient between 0 and 1
            if gradientPercent > 1:
                gradientPercent = 1
            elif gradientPercent < 0:
                gradientPercent = 0

            #gradientListIndex = gradientPercent*(len(gradientList))  # this is the old code that didn't use buckets, and just rounded
            # this segment breaks the colors up into buckets instead of rounding. there is one bucket for each color.
            for m in range(len(gradientList)):
                gradientListIndex = gradientPercent*(len(gradientList))
                if gradientListIndex > m and gradientListIndex <= m + 1:
                    gradientListIndex = m + 1
                    break

            color = gradientList[round(gradientListIndex-1)]
            if unboundedGradientPercent > 1:  # sets stripe color to max color if data is above upper bound
                color = "#67000dff"
            elif unboundedGradientPercent < 0: # sets stripe color to min color if data is below lower bound
                color = "#08306bff"
            fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 30) #for testing only

            #remove stats stuff
            colors.append(color)

            if "stripes" in chartType and chartType != "stripes-svg":
                barWidth = width/len(temps)  # how wide each bar should be
                img1.rectangle([(i*barWidth, 0), (i*barWidth+barWidth, height)], fill=color)

            if "twitter-card" in chartType:
                width = 600*2
                height = 314*2
                barWidth = width/len(temps)  # how wide each bar should be
                img1.rectangle([(i*barWidth, 0), (i*barWidth+barWidth, height)], fill=color)
                
            if "snap-sticker" in chartType:
                width = 4000
                height = 4000
                barWidth = (width*.8)/len(temps)

                if i == 0:  # draw before first bar
                    text = location + " Temp. %i-%i" % (firstYear, lastYear)
                    bottomText = "#globalwarming"

                    #draws the top text box
                    fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 200)
                    textLength = img1.textlength(text, font=fnt)
                    img1.rounded_rectangle([(width/2-textLength/2-.01*width, height*.32), (width/2+textLength/2+.01*width, height*.5)], fill="white", radius=30)
                    img1.text((width/2-textLength/2, height*.325), text, (0, 0, 0), font=fnt)

                    #draws the bottom text box
                    fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 120)
                    textLength = img1.textlength(bottomText, font=fnt)
                    img1.rounded_rectangle([(width/2-textLength/2-.01*width, height*.5), (width/2+textLength/2+.01*width, height*.65)], fill="white", radius=30)
                    img1.text((width/2-textLength/2, height*.61), bottomText, (0, 0, 0), font=fnt)

                if i == 0 or i == len(temps)-1:  # if first or last bar
                    radius = 50
                    if i == 0:
                        img1.rectangle([(i*barWidth+width*.1+barWidth/2, height*.4), (i*barWidth+width*.1+barWidth, height*.6)], fill=color)
                    if i == len(temps)-1:
                        img1.rectangle([(i*barWidth+width*.1, height*.4), (i*barWidth + width*.1+barWidth-barWidth/2, height*.6)], fill=color)
                else:
                    radius = 0
                img1.rounded_rectangle([(i*barWidth+width*.1, height*.4), (i*barWidth+width*.1+barWidth, height*.6)], fill=color, radius=radius)

                #img1.ellipse([(20,100),(width-20,300)],fill="red")
                #barWidth = width/len(temps) #how wide each bar should be
                #img1.rectangle([(i*barWidth,0),(i*barWidth+barWidth,height)], fill=color)
            
            elif "bars" in chartType:
                STRETCH = 900  # how tall/short the bars should be
                if anomaly < 0:
                    unboundedGradientPercent = (unboundedGradientPercent - .5) + .5
                barHeight = height/2-(unboundedGradientPercent-.5)*STRETCH

                sideBorder = 100
                barWidth = (width-2*sideBorder)/len(temps)
                img1.rectangle([(round(i*barWidth+sideBorder), height/2), (i*barWidth+sideBorder+barWidth, barHeight)], fill=color)
                if "debug" in chartType:  # adds debug info to image
                    img1.rectangle([(0, height/2-(1-.5)*STRETCH), (width, height/2-(1-.5)*STRETCH)], fill="#ffffff")
                    img1.rectangle([(0, height/2-(0-.5)*STRETCH), (width, height/2-(0-.5)*STRETCH)], fill="#ffffff")
                    for p in range(0, 16):
                        bobby = (p/16)
                        img1.rectangle([(0, height/2-(bobby-.5)*STRETCH), (width, height/2-(bobby-.5)*STRETCH)], fill="#ffffff")
                    img1.text((i*barWidth+sideBorder, barHeight),str(round(anomaly, 2)), (255, 255, 255), font=fnt)

        # attempts to get a color for the last 20 years, to show rate of warming
        jsonPath = imagePath.replace(chartType, "json")+".json"
        last20YrsAnomaly = numpy.mean(anomalyList[-20:])
        if last20YrsAnomaly < 0:
            last20YrsAnomaly = 0.5-(-1*last20YrsAnomaly/(range2))/2
        if last20YrsAnomaly >= 0:
            last20YrsAnomaly = 0.5+(last20YrsAnomaly/(range2))/2
        if last20YrsAnomaly > 1:
            last20YrsAnomaly = 1
        AveColor = gradientList[round(last20YrsAnomaly*len(gradientList)-1)]
        manageJSON.updateDataObjet(jsonPath, "metadata", AveColor, "color")

    def drawInfo(text="New York, NY", infoType=chartType,height2=height,width=width):
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
            height=2126
            textLength = img1.textlength(text,font=fnt) #gets the width in px of the text so we know where to end background
            img1.rectangle([(50,height-200),(textLength+50+30,height-50)], fill ="#ffffff")
            img1.text((50+10,height-200),text,(0,0,0),font=fnt)
        if "label" in infoType:
            height=150

            textLength = img1.textlength(text,font=fnt) #gets the width in px of the text so we know where to end background
            #img1.rectangle([(0,0),(textLength+20,height)], fill ="#ffffff")
            #img1.text((10,0),text,(0,0,0),font=fnt)
        if "bars" in infoType:
            if "light" in infoType:
                textColor = "#000000"
            else:
                textColor = "#ffffff"
            img1.text((100+10,120),text + " Temperature %i-%i" %(firstYear,lastYear),textColor,font=fnt)
            fnt = ImageFont.truetype("data/Roboto/Roboto-Regular.ttf", 60)
            footerText = "CC BY 4.0 EARTHSTRIPES.ORG"
            footerTextLength = img1.textlength(footerText,font=fnt) #gets the width in px
            img1.text((width-footerTextLength-100,height2-120),footerText,(150,150,150),font=fnt)
    
    
    # creating new Image object, RGBA allows for transparency
    if chartType == "snap-sticker":
        img = Image.new("RGBA", (4000, 4000))
    elif chartType == "twitter-card":
        img = Image.new("RGBA", (600*2, 314*2))
    elif chartType == "label":
        img = Image.new("RGBA", (2126, 150))
    elif chartType == "stripes-svg":
        pass
    elif chartType == "light-labeled-bars":
        img = Image.new("RGBA", (width, height), "white")
    else:
        img = Image.new("RGB", (width, height))
    
    # create rectangle image
    #newsize = (300, 300)
    #im1 = im1.resize(newsize)
 
    #img1.rectangle([(0,0),(50,100)], fill ="#ffff33")


    heatmap = [
    [0, (0, 0, 1)],
    [.5, (1.0, 1, 1.0)],
    [1, (1.0, 0, 0)],
    ] 
    #gradientList = gradient.generateGradient(heatmap)
    gradientList = ["#08306bff", "#08519cff", "#2171b5ff", "#4292c6ff", "#6baed6ff", "#9ecae1ff", "#c6dbefff", "#deebf7ff", "#fee0d2ff", "#fcbba1ff", "#fc9272ff", "#fb6a4aff", "#ef3b2cff", "#cb181dff", "#a50f15ff", "#67000dff"]

    if chartType != "stripes-svg":
        img1 = ImageDraw.Draw(img) 
    drawBars(chartType)
    #only draws info on the thing if the file name says labeled in it
    if "labeled" in chartType or "twitter-card" in chartType or chartType == "label":
        drawInfo(location,chartType)
    #TODO figure out how to add the info
    #TODO investigate why alaska won't work

    #img.show()  # will display the image in popup
    # actually saves the image unless save is false
    if save:
        # creates folders if they don't exist
        if not(os.path.isdir(os.path.dirname(imagePath))):
            os.makedirs(os.path.dirname(imagePath))
        
        if chartType == "stripes-svg":
            createSVG.createSVG(colors,years,imagePath)
        else:
            img.save(imagePath + ".png")
    
    #img.save("C:/Users/radon/Downloads/test201" + ".png")
    print("Done: Image %s: %s" % (str(counter),imagePath))

    #color2020.append(colors[len(colors-2)])
    #color2021.append(colors[len(colors-1)])
    # with open('countyStats.csv', 'a', newline='') as f_object:  
    #     # Pass the CSV  file object to the writer() function
    #     writer_object = csv.writer(f_object)
    #     # Result - a writer object
    #     # Pass the data in the list as an argument into the writerow() function
    #     writer_object.writerow([location,colors[len(colors)-2],temps[len(temps)-2],colors[len(colors)-1],temps[len(temps)-1]])  
    #     # Close the file object
    #     f_object.close()




# "HI" was removed from states list cause no data found on NOAA website for it
statesList = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#for state in statesList:
#    createChart(state)
#createChart("data/us-state-data-NOAA/AL.csv","results/labeled-stripes/US/AL",chartType="labeled-stripes")
#createChart("World Data Stuff/global-land - AnnTemp 1901-2020.csv","results/label/US",chartType="labeled-bars")
#createChart("data/country-data-berkley-earth/processed/ES - AnnTemp 1901-2020.csv","results/stripes/US/MI/Wayne County MI",chartType="labeled-bars",save=False)
#createChart("C:/Users/radon/Downloads/world2021.csv","test7.png",chartType="labeled-bars-debug",save=False,globe=True)
#createChart("state-province data stuff/Acre - AnnTemp 1901-2020.csv","results/stripes/EG",chartType="stripes",save=False)
#createChart("data/us-state-data-NOAA/CA.csv","results/stripes/US/CA",chartType="stripes",save=False)
createChart("data/us-county-data-NOAA/2021/Florida/Miami-Dade County FL - AnnTemp 1895-2021.csv","results/stripes-svg/US/FL/Miami-Dade County FL",chartType="stripes-svg",save=True)
#createChart("C:/Users/radon/Downloads/azt2.csv","test7.png",chartType="stripes-svg",save=True,globe=False)
#createChart("data/country-data-berkley-earth/processed/AO - AnnTemp 1901-2020.csv","test7.png",chartType="labeled-bars-debug",save=False,globe=False)

