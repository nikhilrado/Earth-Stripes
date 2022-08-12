import manageJSON
import globals

#gets county adjacency data from https://www2.census.gov/geo/docs/reference/county_adjacency.txt

f = open("data/county_adjacency.txt", "r")
f = f.readlines()

countyList = []
adjacentCounties = [""]

for line in f:
    line = line.replace('"', "") #removes quotes
    line = line.split("\t") #splits the line into a list
    line[-1] = line[-1].strip() #removes newline character
    
    #converts it into a list of lists, where the first item is the county, and the rest are adjacent counties
    if line[0] != '': #if new county block exists then
        try:
            temp = adjacentCounties[1:]
            temp.remove(adjacentCounties[0]) #removes the current county name from the list of adjacent counties (but it is still the first county)
            adjacentCounties = [adjacentCounties[0]] + temp
        except:
            print("--------error next line:")
            print(adjacentCounties[0])

        countyList.append(adjacentCounties)
        adjacentCounties = []
        adjacentCounties.append(line[0:2])
        adjacentCounties.append(line[2:4])
    else: #if the counties are adjacent to the first county (not the first one), just add it to the list
        adjacentCounties.append(line[2:])
    
    #print(line)

#removes the first county block from the list because it is empty
countyList.pop(0)
print(countyList)

#will loop throught each block of counties, generate links for them, and add those links to the JSON file
for countyBlock in countyList:
    countyName = countyBlock[0][0].split(",")[0]
    stateCode = countyBlock[0][0].split(",")[1].strip()
    countyGeoID = countyBlock[0][1]
    print(countyName, stateCode, countyGeoID)

    counties = []
    links = []

    #loops through each county, adds the name to one list, and link to another. Removes the state if state is same as current county.
    for county in countyBlock:
        adjacentCountyStateCode = county[0].split(",")[1].strip()
        url = "/result/?country=US&state="+adjacentCountyStateCode+"&county="+county[0].split(",")[0].replace(" ", "%20")

        #Removes the state if state is same as current county.
        if countyName + ", " + stateCode != county[0]:
            if county[0][-2:] == stateCode:
                shortCounty = county[0][:-4]
                counties.insert(0,shortCounty)
                links.insert(0,url)
            else:
                counties.append(county[0])
                links.append(url)

    counties.append(globals.getStateAbrev(stateCode)) #adds state
    counties.append("United States") #adds US

    links.append("/result/?country=US&state="+stateCode) #adds state link
    links.append("/result/?country=US") #adds US link

    #JSON template
    adjacencyJSON = {
        "locations": counties[1:],
        "links": links[1:]
    }

    #adds the JSON to the JSON file, will print error if error occurs
    try:
        manageJSON.updateDataObjet("results/json/US/"+stateCode+"/"+countyName+" "+stateCode+".json","metadata", adjacencyJSON, "recommended locations")
        pass
    except:
        print("--------error next line:")
        print(countyName, stateCode, countyGeoID)

