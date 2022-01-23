import json
import sys
sys.path.append('../Earth Stripes Codebase')
import globals

f = open("data/map-data/countries.json")
f = f.read()
f = json.loads(f)

# This replaces the names of countries with the preffered name ex. Myanmar/Burma
def replaceCountryNames(data):
    wordList = ["United Republic of Tanzania","Republic of the Congo","Democratic Republic of the Congo"]
    replaceList = ["Tanzania","Congo","Congo (Democratic Republic of the"]
    for object in data:
            print(object["properties"])
            object["properties"]["NAME"] = object["properties"]["NAME"].replace(wordList[0],replaceList[0])
            
            # adds the ISO alpha 2 (that EarthStripes uses) to the properties with two methods: name lookup and ISO_A3 conversion
            try:
                object["properties"]["countryCode"] = globals.getTerritoryAbrev(object["properties"]["NAME"])
            except:
                try:
                    object["properties"]["countryCode"] = globals.getISOconverted(object["properties"]["ISO_A3"])
                except:
                    print("--------error replace names: " + object["properties"]["NAME"])
            print(object["properties"])


replaceCountryNames(f["features"])

# loops through each item in the geoJSON and gets the color (and other properties) in that place's ES JSON file
for stateData in f["features"]:
    try:
        #print(stateData)
        stateName = stateData["properties"]["NAME"]
        state3ISOcode = stateData["properties"]["ISO_A3"]
        # tries two different ways to get the countryCode, one by getting its name, other by ISO code
        try:
            countryCode = globals.getTerritoryAbrev(stateName)
        except:
            countryCode = globals.getISOconverted(state3ISOcode)

        file = open("results/json/"+countryCode+".json")
        resourceJSON = file.read()
        resourceJSON = json.loads(resourceJSON)
        file.close()

        stateData["properties"]["color"] = resourceJSON["metadata"]["color"]
        print(stateName + stateData["properties"]["color"])
    except:
        print("--------------error: " + stateData["properties"]["NAME"])

# saves file
with open("Site Files/map-page/countries2.js", "w") as myfile:
    myfile.write("var statesData = " + json.dumps(f))  # indent excluded cause data is very large and should be compressed