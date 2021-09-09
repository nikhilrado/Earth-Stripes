import os
import json
import xml.dom.minidom



#returns a list of all files in a directory
def getAllFilesInDir(root):
    fileList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            fileList.append(os.path.join(path, name))    
    return fileList

files = getAllFilesInDir("results/json")

xmlFileList = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for filePath in files:
    filePath = filePath.replace("\\","/") #fixes annoying formating issue that messes up stuff

    #f = open(file)
    #f = f.read()
    #f = json.loads(f)

    def getPageURL ():
        splitPath = filePath.split("/")
        splitPath[-1] = splitPath[-1].replace(".json","") #removes .json
        splitPath.remove('results') #removes irrelevant info
        splitPath.remove('json') #removes irrelevant info
        url = "https://www.earthstripes.org/result/"
        for i in range(len(splitPath)):
            if i == 0:
                url = url + '?country=' + splitPath[0]
            listOfCountriesWithStates = ['US','RU','CN','IN','CA','BR','AU']
            if i == 1 and splitPath[0] in listOfCountriesWithStates:
                url = url + '&state=' + splitPath[1]
            if i == 2 and splitPath[0] == 'US':
                url = url + '&county=' + splitPath[2][:-3].replace(" ","%20")

        url = url.replace("&","&amp;")

        #print(url)
        #print(splitPath)
        return url

    def addImage (imageURL,imageCaption,imageLocation,imageTitle,imageLicense):
        imageXML = []
        imageXML.append('<image:image>')
        imageXML.append('<image:loc>' + imageURL + '</image:loc>')
        imageXML.append('<image:caption>' + imageCaption + '</image:caption>')
        imageXML.append('<image:geo_location>' + imageLocation + '</image:geo_location>')
        imageXML.append('<image:title>' + imageTitle + '</image:title>')
        imageXML.append('<image:license>' + imageLicense + '</image:license>')
        imageXML.append('</image:image>')
        return imageXML

    

    xmlFileList.append('<url>')
    xmlFileList.append('<loc>' + getPageURL() + '</loc>')
    xmlFileList = xmlFileList + addImage()
    xmlFileList.append('</url>')

xmlFileList.append('</urlset>')
xmlFile = ""
for line in xmlFileList:
    xmlFile = xmlFile + line #+ "\n"
    print(line)



dom = xml.dom.minidom.parseString(xmlFile) #xml.dom.minidom.parse(xml_fname)
pretty_xml_as_string = dom.toprettyxml()

with open('SEO/result-sitemap.xml', 'w') as f:
    f.write(pretty_xml_as_string)



