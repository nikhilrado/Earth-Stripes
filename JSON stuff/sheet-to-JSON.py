import csv
import json

#convert between long or short name of the state
stateFullName = ["County","Washington D.C.","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
stateShortName = ["ty","DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

f = open("JSON stuff\states.csv")

csv_f = csv.reader(f)

rowsList = []
for row in csv_f:
    rowsList.append(row)
    #print(row)

#transponse rows and columns; seperates headers
#assumes first column is the longest
transposedSheet = []
for i in range(len(rowsList[0])):
    temp = []
    for row in rowsList:
        temp.append(row[i])
    transposedSheet.append(temp)
    
headings = transposedSheet[0]
transposedSheet.pop(0)

#print(headings)
#print(transposedSheet)

def columnToJSON(column):
    localImpactData = []
    location = transposedSheet[column][0]
    #Loops through each coloumn in the spreadsheet (transposed column in the transposedSheet)
    for i in range(2):
        #TODO: figure out why setting local Impact equal to local impact template makes them both equal
        localImpact = {
        "category": None,
        "headline": None,
        "content": None,}
        
        localImpact["category"] = transposedSheet[column][4*(i)+1]
        localImpact["headline"] = transposedSheet[column][4*(i)+2]
        localImpact["content"] = transposedSheet[column][4*(i)+3]
        #localImpact["testList"].append("yeey")

        localImpactData.append(localImpact)
        print(json.dumps(localImpact))
        print("ttt")

    print(json.dumps(localImpactData))

    #loads data from current file
    try:
        f = open('results/json/US/'+getStateAbrev(location)+'.json')
    except:
        #will create the JSON file if not found, cause this program was the first program to create/access the JSON files
        f = open("JSON stuff/template.json")
        
    f = f.read()
    f = json.loads(f)
    if f["metadata"]["name"] == "Template State":
        f["metadata"]["name"] = location
    f["local impacts"] = localImpactData
    #print("")
    #print(f)

    #saves file with county name
    with open('results/json/US/'+getStateAbrev(location)+'.json', "w") as myfile:
        myfile.write(json.dumps(f, indent=2))

for k in range(len(transposedSheet)):
    if transposedSheet[k][1] == "":
        continue
    columnToJSON(k)