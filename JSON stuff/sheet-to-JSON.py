import csv
import json

#convert between long or short name of the state
stateFullName = ["County","Washington D.C.","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
stateShortName = ["ty","DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
def getStateAbrev(state):
    state = state.strip()
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

f = open("JSON stuff\State Data Information - CleanData12.csv", encoding='utf-8-sig')

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
transposedSheet.pop(0) #removes first line

#print(headings)
#for line in transposedSheet:
#    print(line)
def sanitizeText(text):
    text.replace("\n", " ") #removes newlines, although they should already be removed
    text.replace("’", "'")
    text.replace("â€™","HHHH")
    #print(text)
    return text

def columnToJSON(column):
    #print(column)
    state = column[0]
    container = {
        "local impacts": []
    }


    contentNum = 1
    for i in range(len(column)):
        z = {
        #"category": None,
        "headline": None,
        "content": [],
        }
        if column[i] == "END":
            break
        if column[i] == "CONTENT " + str(contentNum):
            #z["category"] = column[i+1]
            z["headline"] = column[i+3]

            
            #gets the content, could make this code more compact, but want it to be modular for the future
            if column[i+4] != "":
                z["content"].append(sanitizeText(column[i+4]))
            if column[i+5] != "":
                z["content"].append(sanitizeText(column[i+5]))
            if column[i+6] != "":
                z["content"].append(sanitizeText(column[i+6]))
            if column[i+7] != "":
                z["content"].append(sanitizeText(column[i+7]))
            if column[i+8] != "":
                z["content"].append(sanitizeText(column[i+8]))
            
            if z["headline"] != "":
                container["local impacts"].append(z)
            
            
            contentNum += 1

    #filePath = 'JSON stuff/'+getStateAbrev(state)+"test.json" #test folder
    filePath = 'results/json/US/'+getStateAbrev(state)+".json" #real folder
    try:
        f2 = open(filePath)
        f2 = f2.read()
        f2 = json.loads(f2)
        f2["local impacts"] = container["local impacts"]

        print(json.dumps(container, indent=2))

        
        with open(filePath, "w") as myfile: #real folder
            myfile.write(json.dumps(f2, indent=2))
    except:
        print("---------Error: " + filePath)

for row in transposedSheet:
    columnToJSON(row)
#columnToJSON(transposedSheet[0])

"""
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
    """