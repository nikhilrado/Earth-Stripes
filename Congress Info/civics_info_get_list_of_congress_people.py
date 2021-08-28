from civicsInfoApiKey import googleCivicsAPIkey
import requests
import json


listOfStates = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
listOfS = ["AL"]

listOfSenators = []
for state in listOfStates:
    try:
        requestURL = 'https://www.googleapis.com/civicinfo/v2/representatives?key='+googleCivicsAPIkey+'&levels=country&roles=legislatorUpperBody&address='+state+",USA"
        resp = requests.get(requestURL)
        JSONresponse = json.loads(resp.text)
        
        senator1 = JSONresponse["officials"][0]["name"]
        senator2 = JSONresponse["officials"][1]["name"]

        listOfSenators.append(senator1)
        listOfSenators.append(senator2)
        #print(listOfSenators)
        print(senator1 +","+ state)
        print(senator2 +","+ state)
    except:
        print("----------------error: "+state)

