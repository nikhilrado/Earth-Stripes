#This Program was created to download temperature data from berkley earth
#It is a modified version of the program to download country data which is a modified version of the program to download NOAA data
#
#

import csv
from lib2to3.pgen2.token import NEWLINE
import requests
import json
import manageJSON
import globals

countryErrorList = [] #contains list of any countries who couldn't be accessed

def saveResource(resourceURL,country_code):
    #use this to individually download a certain URL to fix error or test program
    #resourceURL = 'http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/japan-TAVG-Trend.txt'

    with requests.Session() as s:
        #resourceURL = "http://berkeleyearth.org/wp-content/themes/client-theme/temperature-data/Albania-projection.txt"
        download = s.get(resourceURL)
        #print(resourceURL)
        decoded_content = download.content.decode('Windows-1252')
        #print(decoded_content)
        cr = csv.reader(decoded_content.splitlines(), delimiter=' ')
        my_list = list(cr)
        for row in my_list:
            #removes all whitespace
            while("" in row) :
                row.remove("")
        #write to file
        with open("../Earth Stripes Codebase/data/temperature-predictions-berkeley-earth/{}.txt".format(country_code), "w") as f:
            for row in my_list:
                f.write(" ".join(row))
                f.write("\n")
        

    #extract metadata from csv
    #this ends up not being used, but may be helpful in the future
    metaDataList = []
    for row in my_list:

        #print(row[0])
        if len(row) > 0 and row[0] == "%%":
            metaDataList.append(row)

        #print(row)
    
    #skip this country if can't access expected file format of berkley data (url gives us 404 or other error)
    if my_list[0][0] != "%":
        countryErrorList.append(resourceURL)
        return "done"

    #extracts country name
    country = " "
    country_code = metaDataList[2][2]
    
    #country = re.match("ISO_Code:(.*?)", metaDataList[2]).group(0)
    #print(country_code)

    data_2 = []
    for row in my_list:
        #print(row)

        if len(row) == 1 and "\t" in row[0]:
            data = row[0].split("\t")
            #print(data)
            data_2.append(data)
            #print(data)
        if len(row) > 1 and row[1] == "year,":
            headers = row

    template = {}
    for col in range(len(data_2[0])):
        list_template = []
        label = headers[1:][col].replace(",","").lower()
        for row in range(len(data_2)):
            data_point = data_2[row][col]
            if data_point == "NaN":
                data_point = None
                list_template.append(data_point)
            elif label == "Year":
                list_template.append(int(data_point))
            else:
                list_template.append(float(data_point))
            
        #print(list_template)
        template[label] = list_template
    
    #print(template)
    #print(json.dumps(template, indent=4, separators=(",",":")))
    manageJSON.updateDataObjet("results/json/{}.json".format(globals.getISOconverted(country_code)), "temperature_projections", template)


#saveResource("http://berkeleyearth.org/wp-content/themes/client-theme/temperature-data/Albania-projection.txt")


for country in globals.allTerritories:
    request_url = "http://berkeleyearth.org/wp-content/themes/client-theme/temperature-data/" + country + "-projection.txt"
    
    try:
        saveResource(request_url,globals.getCountryCode(country))
        print("{}: {}".format(country,request_url))
    except Exception as e:
        print("Error: {} {}".format(country,request_url))
        print(e)