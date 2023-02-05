import manageJSON
import globals
import csv
import s3upload

def extract_county_adjacency_data():
    # gets county adjacency data from https://www2.census.gov/geo/docs/reference/county_adjacency.txt
    f = open("data/adjacent-location-data/county_adjacency.txt", "r")
    f = f.readlines()

    countyList = []
    adjacentCounties = [""]

    for line in f:
        line = line.replace('"', "")  # removes quotes
        line = line.split("\t")  # splits the line into a list
        line[-1] = line[-1].strip()  # removes newline character

        # converts it into a list of lists, where the first item is the county, and the rest are adjacent counties
        if line[0] != '':  # if new county block exists then
            try:
                temp = adjacentCounties[1:]
                # removes the current county name from the list of adjacent counties (but it is still the first county)
                temp.remove(adjacentCounties[0])
                adjacentCounties = [adjacentCounties[0]] + temp
            except:
                print("--------error next line:")
                print(adjacentCounties[0])

            countyList.append(adjacentCounties)
            adjacentCounties = []
            adjacentCounties.append(line[0:2])
            adjacentCounties.append(line[2:4])
        # if the counties are adjacent to the first county (not the first one), just add it to the list
        else:
            adjacentCounties.append(line[2:])

        # print(line)

    # removes the first county block from the list because it is empty
    countyList.pop(0)
    print(countyList)

    # will loop throught each block of counties, generate links for them, and add those links to the JSON file
    for countyBlock in countyList:
        countyName = countyBlock[0][0].split(",")[0]
        stateCode = countyBlock[0][0].split(",")[1].strip()
        countyGeoID = countyBlock[0][1]
        print(countyName, stateCode, countyGeoID)

        counties = []
        links = []

        # loops through each county, adds the name to one list, and link to another. Removes the state if state is same as current county.
        for county in countyBlock:
            adjacentCountyStateCode = county[0].split(",")[1].strip()
            url = "/result/?country=US&state="+adjacentCountyStateCode + \
                "&county="+county[0].split(",")[0].replace(" ", "%20")

            # Removes the state if state is same as current county.
            if countyName + ", " + stateCode != county[0]:
                if county[0][-2:] == stateCode:
                    shortCounty = county[0][:-4]
                    counties.insert(0, shortCounty)
                    links.insert(0, url)
                else:
                    counties.append(county[0])
                    links.append(url)

        hierarchy_locations = [globals.getStateAbrev(stateCode), "United States","Earth"]
        hierarchy_links = ["/result/?country=US&state="+stateCode, "/result/?country=US","/result/?location=earth"]

        # JSON template
        adjacencyJSON = {
            "adjacent":{
                "locations": counties[:1],
                "links": links[:1],
            },
            "hierarchy": {
                "locations": hierarchy_locations,
                "links": hierarchy_links
            }
        }

        # adds the JSON to the JSON file, will print error if error occurs
        try:
            manageJSON.updateDataObjet("results/json/US/"+stateCode+"/"+countyName +
                                    " "+stateCode+".json", "metadata", adjacencyJSON, "recommended locations")
            pass
        except:
            print("--------error next line:")
            print(countyName, stateCode, countyGeoID)

def extract_country_adjacency_data():
    # gets country adjacency data from https://github.com/geodatasource/country-borders/blob/master/GEODATASOURCE-COUNTRY-BORDERS.CSV
    f = open("data/adjacent-location-data/GEODATASOURCE-COUNTRY-BORDERS.CSV", "r")
    # turn csv to python array
    f = list(csv.reader(f, delimiter=','))
    print(f)

    compressed_data = {}

    for line in f[1:]:
        country_code = line[0]
        adjacent_country_code = line[2]

        # if country does not exist in our system pass
        # TODO: make a better solution of this
        try:
            x = globals.getCountryCode(country_code) + globals.getCountryCode(adjacent_country_code)
        except:
            print("--------error")
            print(country_code, adjacent_country_code)
            continue

        if country_code not in compressed_data:
            compressed_data[country_code] = [adjacent_country_code]
        else:
            compressed_data[country_code].append(adjacent_country_code)

    for country_code in compressed_data:
        if compressed_data[country_code] == ['']:
            continue
        print(country_code, compressed_data[country_code])
        country_names = [globals.getCountryCode(c) for c in compressed_data[country_code]]
        links = ["/result/?country="+c for c in compressed_data[country_code]]

        # JSON template
        adjacencyJSON = {
            "adjacent": {
                "locations": country_names,
                "links": links,
            },
            "hierarchy": {
                "locations": ["Earth"],
                "links": ["/result/?location=earth"]
            }
        }
        print(adjacencyJSON)

        # adds the JSON to the JSON file, will print error if error occurs
        try:
            manageJSON.updateDataObjet("results/json/"+country_code+".json", "metadata", adjacencyJSON, "recommended locations")
            #s3upload.uploadFile("results/json/"+country_code+".json",uploadFilePath="v3/json/"+country_code+".json")
            pass
        except:
            print("--------error next line:")
            print(country_code)

extract_country_adjacency_data()
extract_county_adjacency_data()