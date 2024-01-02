import csv
import requests
import os
import datetime

# convert between long or short name of the state
stateFullName = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
stateShortName = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

def saveResource(resourceURL):
    with requests.Session() as s:
        download = s.get(resourceURL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    # extracts metadata from csv
    try:
        county = my_list[0][0]
    except:
        return "done"
    state = " ".join(my_list[0][1].split(" ")[:-3]).strip()
    basePeriod = my_list[2][0][-9:]
    startYear = my_list[5][0][:4]
    endYear = my_list[-1][0][:4]

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
    #TODO: restore previous data folder
    #TODO: make year date reflect end year (dynamic)
    file_path = 'data/us-county-data-NOAA/2023/%s/%s %s - AnnTemp %s-%s.csv' % (state,county,getStateAbrev(state),startYear,endYear)

    # create folder if it doesn't exist
    folder_path = file_path[:file_path.rfind("/")]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(my_list)

newData = ""
counter = 0
for state in stateShortName:
    for i in range(250):
        counter += 1
        # TODO: Miami-Dade FIPS is 086, need to make new system
        noaa_data_url = "https://www.ncdc.noaa.gov/cag/county/time-series/%s-%s-tavg-12-12-1895-2022.csv?base_prd=true&begbaseyear=1901&endbaseyear=2000" % (state,f"{i*2+1:03d}")
        noaa_data_url = f"https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/county/time-series/{state}-{f'{i*2+1:03d}'}-tavg-12-12-1895-2022.csv?base_prd=true&begbaseyear=1901&endbaseyear=2000"

        print("County: " + str(counter)  +  ' ' + noaa_data_url)

        newData = newData + noaa_data_url + "\n"
        try:
            if saveResource(noaa_data_url) == "done":
                continue
        except Exception as e:
            print("Error: " + str(e))
