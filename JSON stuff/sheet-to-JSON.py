import csv
import json

f = open("Earth Stripes\JSON stuff\states.csv")

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
        f = open('Earth Stripes/JSON stuff/'+location+'.json')
    except:
        #will create the JSON file if not found, cause this program was the first program to create/access the JSON files
        f = open("Earth Stripes/JSON stuff/template.json")
        
    f = f.read()
    f = json.loads(f)
    if f["Metadata"]["Name"] == "Template State":
        f["Metadata"]["Name"] = location
    f["Local Impacts"] = localImpactData
    #print("")
    #print(f)

    #saves file with county name
    with open('Earth Stripes/JSON stuff/'+location+'.json', "w") as myfile:
        myfile.write(json.dumps(f, indent=2))

for k in range(len(transposedSheet)):
    if transposedSheet[k][1] == "":
        continue
    columnToJSON(k)