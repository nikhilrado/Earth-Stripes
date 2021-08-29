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

def getHumanReadableTerm(termNum):
    if termNum == 1:
        return "1st"
    if termNum == 2:
        return "2nd"
    if termNum == 3:
        return "3rd"
    return str(termNum) + "th"

bothSenatorsList = []
for row in rowsList:
    #print(row)


    
    bothSenatorsList.append(row)
    if row[7] == "":
        row[7] = 0

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
        senator1 = bothSenatorsList[0]
        senator2 = bothSenatorsList[1]

        y = {
            "SenatorInfo":{
                senator1[0]:{
                    "stateCode": senator1[1],
                    "stateName": senator1[8],
                    "image": senator1[2],
                    "current term": int(senator1[7]) + 1,
                    "current term readable": getHumanReadableTerm(int(senator1[7]) + 1),
                    "party": senator1[10],
                    "position": senator1[11],
                    "leadership": senator1[12],
                    "positionScore": senator1[13],
                    "voteScore": senator1[14],
                    "leadershipScore": senator1[15],
                    "carbonFree": senator1[16],
                    "carbonFreeScore": senator1[17],
                    "overallScore": senator1[18]
                },
                senator2[0]:{
                    "stateCode": senator2[1],
                    "stateName": senator2[8],
                    "image": senator2[2],
                    "current term": int(senator2[7]) + 1,
                    "current term readable": getHumanReadableTerm(int(senator2[7]) + 1),
                    "party": senator2[10],
                    "position": senator2[11],
                    "leadership": senator2[12],
                    "positionScore": senator2[13],
                    "voteScore": senator2[14],
                    "leadershipScore": senator2[15],
                    "carbonFree": senator2[16],
                    "carbonFreeScore": senator2[17],
                    "overallScore": senator2[18]
                }
            }
        }
    
        print(json.dumps(y, indent=2))
        bothSenatorsList = [] #resets the list

        file.update(y)
        print(json.dumps(file, indent=2))
        
        #sets name and saves file
        with open('results/json/US/'+state+'.json', "w") as myfile:
            myfile.write(json.dumps(file, indent=2))