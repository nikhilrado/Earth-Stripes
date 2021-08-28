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

f = open('data/Congress Data/Senator Data - main.csv', "r", encoding = 'utf8')
csv_f = csv.reader(f)

rowsList = []
for row in csv_f:
    rowsList.append(row)
    print(row)

dataHeader = rowsList[0] #sets first row as headers
rowsList.pop(0) #removes first row

bothSenatorsList = []
for row in rowsList:
    #print(row)


    
    bothSenatorsList.append(row)

    #checks that there are two in the list and that the state code matches up:
    if len(bothSenatorsList) == 2 and bothSenatorsList[0][1] == bothSenatorsList[0][1]:
        state = row[1]
        try:
            file = open('results/json/US/'+state+'.json')
        except:
            continue
        file = file.read()
        file = json.loads(file)

        #template JSON/python dict
        y = {
            "SenatorInfo":{
                bothSenatorsList[0][0]:{
                    "state": bothSenatorsList[0][1],
                    "image": bothSenatorsList[0][2]
                },
                bothSenatorsList[1][0]:{
                    "state": bothSenatorsList[1][1],
                    "image": bothSenatorsList[1][2]
                }
            }
        }
    
        print(json.dumps(y, indent=2))
        bothSenatorsList = []

    """
    if len(dataHeader) != len(row): #just a check
        print("---------Error: potentially missing data")
    for i in range(len(dataHeader)):
        y["YaleClimateOpinionData2020"]["data"][dataHeader[i]]=row[i]
    f.update(y)
    print(y)
    
    #sets name and saves file
    with open('results/json/'+resourceID+'.json', "w") as myfile:
        myfile.write(json.dumps(f, indent=2))"""