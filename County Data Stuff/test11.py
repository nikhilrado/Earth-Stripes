import csv
import requests
import os

#convert between long or short name of the state
stateFullName = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
stateShortName = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
stateShortName2 = ["GA"]
def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

def saveResource(resourceURL):
    CSV_URL = 'https://www.ncdc.noaa.gov/cag/county/time-series/NY-001-tavg-1-6-1895-2021.csv'

    with requests.Session() as s:
        download = s.get(resourceURL)
        #print(resourceURL)
        decoded_content = download.content.decode('utf-8')
        #print(decoded_content)
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        #for row in my_list:
            #print(row)
        

    #extract metadata from csv
    try:
        county = my_list[0][0]
    except:
        return "done"
    state = my_list[0][1].strip()
    basePeriod = my_list[2][0][-9:]
    startYear = my_list[5][0][:4]
    endYear = my_list[-1][0][:4]

    #https://stackoverflow.com/questions/1274405/how-to-create-new-folder #https://stackoverflow.com/a/1274465
    newpath = 'data2/us-county-data-NOAA/'+state 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    import datetime

    metaDataList = [["County:", county],
                    ["State:", state],
                    ["Base Period:", basePeriod],
                    ["Start Year:", startYear],
                    ["End Year:", endYear],
                    [],
                    ["Data Source:", "NOAA"],
                    ["Data Source URL:", "https://www.noaa.gov/"],
                    ["Data File URL:", resourceURL],
                    ["Access Date (UTC):",  datetime.datetime.now()]]
    my_list = metaDataList + my_list
    # for row in my_list:
    #    print(row)
    #saves file with county name
    with open('data/us-county-data-NOAA/2021/%s/%s %s - AnnTemp %s-%s.csv' % (state,county,getStateAbrev(state),startYear,endYear), 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(my_list)
    #with open('data2/us-county-data-NOAA/%s/%s %s - AnnTemp %s-%s.csv' % (state,county,getStateAbrev(state),startYear,endYear), "w") as myfile:
    #    myfile.write(str(my_list))

with open('County Data Stuff/test11.txt', "r") as myfile:
    data = myfile.read()

newData = ""
counter = 0
for state in stateShortName:
    for i in range(250):
        counter += 1
        #resourceURL = "https://www.ncdc.noaa.gov/cag/county/time-series/FL-086-tavg-12-12-1895-2021.csv?base_prd=true&begbaseyear=1901&endbaseyear=2000"
        resourceURL = "https://www.ncdc.noaa.gov/cag/county/time-series/%s-%s-tavg-12-12-1895-2021.csv?base_prd=true&begbaseyear=1901&endbaseyear=2000" % (state,f"{i*2+1:03d}")
        #use for custom URL request
        #resourceURL = "https://www.ncdc.noaa.gov/cag/county/time-series/FL-086-tavg-12-12-1895-2021.csv"
        #"/cag/statewide/time-series/1-tavg-12-12-1895-2021.json?base_prd=true&begbaseyear=1901&endbaseyear=2000"
        print("County: " + str(counter)  +  ' ' + resourceURL)

        newData = newData + resourceURL + "\n"
        try:
            if saveResource(resourceURL) == "done":
                continue
        except:
            continue
    #print(newData)

    #with open('County Data Stuff/test11.txt', "w") as myfile:
    #    myfile.write(newData)


