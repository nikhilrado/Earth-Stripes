import os.path
import csv

# this checks to see how many counties we have data for by comparing it to the list of counties
# found at /data/us-county-data-NOAA/list of US counties.csv where data is outputted

LIST_OF_COUNTIES_FILE = 'data/us-county-data-NOAA/list of US counties.csv'

# convert between long or short name of the state
stateFullName = ["County", "District of Columbia", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
                 "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
stateShortName = ["ty", "DC", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
                  "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

f = open(LIST_OF_COUNTIES_FILE, "r")
csv_f = csv.reader(f)

rows_list = []
for row in csv_f:
    rows_list.append(row)
print(rows_list)

counter = 0
for row in rows_list:
    file_name = f"data/us-county-data-NOAA/2022/{getStateAbrev(row[0][-2:])}/{row[0]} - AnnTemp 1895-2022.csv"
    print(file_name)
    if os.path.isfile(file_name) == True:
        row[1] = "complete"
        counter += 1
    else:
        row[1] = ""
print(f"{counter}/{len(rows_list)} {round(counter/len(rows_list)*100,1)}% counties have data")

with open(LIST_OF_COUNTIES_FILE, 'w', newline="") as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(rows_list)