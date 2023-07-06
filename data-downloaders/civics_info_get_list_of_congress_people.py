import sys
sys.path.append("../Earth Stripes Codebase")
from es_secrets import googleCivicsAPI
import requests
import json


list_of_states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
list_of_states2 = ["AL"]

list_of_senators = []
for state in list_of_states:
    try:
        request_url = 'https://www.googleapis.com/civicinfo/v2/representatives?key='+googleCivicsAPI.key+'&levels=country&roles=legislatorUpperBody&address='+state+",USA"
        resp = requests.get(request_url)
        JSON_response = json.loads(resp.text)
        
        senator_1 = JSON_response["officials"][0]["name"]
        senator_2 = JSON_response["officials"][1]["name"]

        list_of_senators.append(senator_1)
        list_of_senators.append(senator_2)
        print(list_of_senators)
        print(senator_1 +","+ state)
        print(senator_2 +","+ state)
    except:
        print("----------------error: "+state)

