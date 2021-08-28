import csv
import json

#This program takes the data from the Yale Climate Opinion Survey and places it in the respective JSON files
#Note: changed the name of DC state from "District of Columbia" to "Washington D.C." then deleted the DC county line in the data file

#convert between long or short name of the state
stateFullName = ["County","Washington D.C.","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
stateShortName = ["ty","DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

f = open('Yale Climate\YCOM_2020_Data.csv', "r")
csv_f = csv.reader(f)

rowsList = []
for row in csv_f:
    rowsList.append(row)

dataHeader = rowsList[0] #sets first row as headers
rowsList.pop(0) #removes first row

#gets the resource ID of the file by seeing what location category the yale data belongs to
def getYaleResourceID(row):
    resourceID = None
    if row[0] == "County":
        county = row[2].split(",")[0]
        state = getStateAbrev(row[2].split(",")[1].strip())
        resourceID = "US/"+state+"/"+county+" "+state
    elif row[0] == "State":
        state = row[2]
        resourceID = "US/" + getStateAbrev(state)
    elif row[0] == "National":
        resourceID = row[2]
    return resourceID

for row in rowsList:
    #print(row)
    resourceID = getYaleResourceID(row)
    try:
        f = open('results/json/'+resourceID+'.json')
    except:
        continue
    f = f.read()
    f = json.loads(f)

    #template JSON/python dict
    y = {
        "YaleClimateOpinionData2020":{
            "metadata":{
                "source":'Howe, Peter D., Matto Mildenberger, Jennifer R. Marlon, and Anthony Leiserowitz (2015). “Geographic variation in opinions on climate change at state and local scales in the USA.” Nature Climate Change, doi:10.1038/nclimate2583',
                "disclaimer":"The YPCCC bears no responsibility for the analyses or interpretations of the data presented here."
            },
            "data":{}
        }
    }
    
    print(y)
    if len(dataHeader) != len(row): #just a check
        print("---------Error: potentially missing data")
    for i in range(len(dataHeader)):
        y["YaleClimateOpinionData2020"]["data"][dataHeader[i]]=row[i]
    f.update(y)
    print(y)
    
    #sets name and saves file
    with open('results/json/'+resourceID+'.json', "w") as myfile:
        myfile.write(json.dumps(f, indent=2))