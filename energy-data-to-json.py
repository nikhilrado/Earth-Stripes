import csv
import json
import globals
import manageJSON

#opens the file from the eia website
#go to link then select options, then select consumption and production for all countries
#https://www.eia.gov/international/data/world/total-energy/total-energy-consumption
f = open("data/eia-energy-consumption-proudction-data.csv", encoding='utf-8-sig')

#opens file and puts data into list
csv_f = csv.reader(f)

allEnergyData = []
for row in csv_f:
    allEnergyData.append(row)

#sets the header of the data which is the same for all days (then converts all to int)
years = list(map(int, allEnergyData[1][2:-1])) 

def countryToJSON(list):

    country = list[0][1]
    totalConsumption = list[8][2:-1]
    container = {
        "energy consumption": []
    }
    
    #calculates the percent by dividing the data by the whole
    def getPercent(dataList):
        for i in range(len(dataList)):
            #if there is an error (no data, or "--" in column), null will be placed in the json, which allows the chart to render
            try:
                dataList[i] = round(float(dataList[i])/float(totalConsumption[i])*100,1)
            except:
                dataList[i] = None
            
        return(dataList)

    #this is the template for the json
    z = {
    "years": years,
    "total consumption": totalConsumption,
    "coal": getPercent(list[9][2:-1]),
    "natural gas": getPercent(list[10][2:-1]),
    "petroleum and other liquids": getPercent(list[11][2:-1]),
    "nuclear": getPercent(list[13][2:-1]),
    "renewables and others": getPercent(list[14][2:-1]),
    }
    
    #adds the data to its container then prints it, along with the country
    container["energy consumption"].append(z)
    print(country)
    print(json.dumps(container, indent=2))
    
    #gets the country's country code from the globals file, then adds the data to the country's json file
    countryCode = globals.getCountryCode(country)
    manageJSON.updateDataObjet("results/json/"+countryCode+".json","energy consumption",z)
    #manageJSON.updateDataObjet("JSON stuff/AZtest.json","energy consumption",z) #use for testing


rowsListData = allEnergyData[2:] #chops off last two years because data wasn't reliable
for k in range(len(rowsListData)):
    row = rowsListData[k]

    dataForOneCountryList = []
    #just checks to make sure data is in increments of 15
    if row[0] == "":
        for j in range(15):
            dataForOneCountryList.append(rowsListData[k+j])
        try:
            countryToJSON(dataForOneCountryList)
        except:
            pass
        