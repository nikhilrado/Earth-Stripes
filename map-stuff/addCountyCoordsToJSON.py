import os
import json
import csv

#this code was written very slopily because deadline was approaching very quickly
#and I was waiting on contacting mapbox sales about bulk geocoder

#returns a list of all files in a directory
def getAllFilesInDir(root):
    fileList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            fileList.append(os.path.join(path, name))    
    return fileList

files = getAllFilesInDir("results/json")

#static file of county information
f = open("Map Stuff/countyCoordinates.csv")

csv_f = csv.reader(f)

rowsList = []
for row in csv_f:
    rowsList.append(row)

#returns a filtered list of counties, in case counties in multiple states have the same name
def getCountiesOfState(stateCode):
    list = []
    for row in rowsList:
        if row[1] == stateCode:
            list.append(row)
    return list

#returns the coordinates of the county
def getCoordsOfCounty(county,countiesList):
    for row in countiesList:
        if  county == row[3] + " County":
            Latitude = float(row[12][1:-2]) #only works for lat coords in northern hemisphere
            Longitude = float("-"+row[13][3:-2]) #only works for long coords in western hemisphere
            return Latitude,Longitude

#taken from the sitemap generator
for filePath in files:
    filePath = filePath.replace("\\","/") #fixes annoying formating issue that messes up stuff


    
    f = open(filePath)
    f = f.read()
    f = json.loads(f)

    def getPageURL ():
        splitPath = filePath.split("/")
        splitPath[-1] = splitPath[-1].replace(".json","") #removes .json
        splitPath.remove('results') #removes irrelevant info
        splitPath.remove('json') #removes irrelevant info
        url = "https://www.earthstripes.org/result/"
        for i in range(len(splitPath)):
            if i == 0:
                url = url + '?country=' + splitPath[0]
                fullLocName = f["metadata"]["name"]
            listOfCountriesWithStates = ['US','RU','CN','IN','CA','BR','AU']
            if i == 1 and splitPath[0] in listOfCountriesWithStates:
                url = url + '&state=' + splitPath[1]
                fullLocName = f["metadata"]["name"] + ", " +splitPath[1] + ", " +splitPath[0]
            if i == 2 and splitPath[0] == 'US':
                url = url + '&county=' + splitPath[2][:-3].replace(" ","%20")

                stateList = getCountiesOfState(splitPath[1])
                print()

                y = {
                    "coords":getCoordsOfCounty(splitPath[2][:-3],stateList)
                }

                f["metadata"].update(y)
                    
                print(json.dumps(f, indent=2))
                with open(filePath, "w") as myfile:
                    myfile.write(json.dumps(f, indent=2))

    getPageURL()