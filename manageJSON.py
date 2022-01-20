import json
from datetime import datetime
import s3upload
import os
berklyTerritoriesAbbreviations = ["AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BT","BO","BQ","BA","BW","BR","IO","BG","BF","MM","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CO","KM","CG","CD","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT","HM","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ","KE","KI","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","ML","MT","MQ","MR","MU","YT","MX","MD","MC","MN","ME","MS","MA","MZ","NA","NP","NL","NC","NZ","NI","NE","NG","NU","KP","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PL","PT","PR","QA","RE","RO","RU","RW","BL","KN","LC","MF","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","GS","KR","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TO","TT","TN","TR","TM","TC","UG","UA","AE","GB","US","UY","UZ","VE","VN","VG","EH","YE","ZM","ZW"]
berklyTerritories = ["Afghanistan","Åland","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bonaire, Saint Eustatius and Saba","Bosnia and Herzegovina","Botswana","Brazil","British Virgin Islands","Bulgaria","Burkina Faso","Burma","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Colombia","Comoros","Congo","Congo (Democratic Republic of the)","Costa Rica","Côte d'Ivoire","Croatia","Cuba","Curaçao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands (Islas Malvinas)","Faroe Islands","Fiji","Finland","France (Europe)","French Guiana","French Polynesia","French Southern and Antarctic Lands","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti","Heard Island and McDonald Islands","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands (Europe)","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","North Korea","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Palestina","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Barthélemy","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Sint Maarten","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Georgia and the South Sandwich Isla","South Korea","Spain","Sri Lanka","Sudan","Suriname","Svalbard and Jan Mayen","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicas Islands","Uganda","Ukraine","United Arab Emirates","United Kingdom (Europe)","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands","Western Sahara","Yemen","Zambia","Zimbabwe"]

#creates json files
def main(fileLocation,name):
    f = open("JSON stuff/template2.json")
    f = f.read()
    f = json.loads(f)

    f["metadata"]["name"] = (name)

    #creates directory is not present, need to use stripes cause I'm lazy
    if not os.path.exists(fileLocation.replace("stripes","json").replace(name,"")):
        os.makedirs(fileLocation.replace("stripes","json").replace(name,""))

    #sets name
    with open(fileLocation.replace("stripes","json")+'.json', "w") as myfile:
        myfile.write(json.dumps(f, indent=2))

#updates a property in the metadata
def updateDataObjet(fileName,name,data,subobject=False):
    f = open(fileName)
    f = f.read()
    f = json.loads(f)

    #if subobject exists, add it there, if not don't
    if not subobject:
        f[name] = data
    else:
        f[name][subobject] = data

    #creates directory is not present, need to use stripes cause I'm lazy
    if not os.path.exists(fileName):
        os.makedirs(fileName)

    #sets name
    with open(fileName, "w") as myfile:
        myfile.write(json.dumps(f, indent=2))

#deletes stuff from the files
def deleteObject(directoryOfJSONFiles,object,subobject=False):
    for file in s3upload.getAllFilesInDir(directoryOfJSONFiles):
        f = open(file.replace("\\","/"),"r")
        f = f.read()
        f = json.loads(f)
        #print(f)
        
        if subobject:
            try:
                del f[object][subobject]
            except:
                continue
        else:
            try:
                del f[object]
            except:
                continue
        with open(file, "w") as myfile:
            myfile.write(json.dumps(f, indent=2))
#deleteObject("results/json","resources","bars")

def updateMetadata(resourceID,resourceType,width=None,height=None,startYear=None,endYear=None,dataSource=None,dataSourceLink=None,name=None):
    #f = open('results/json/'+resourceID+'.json')
    jsonFile = resourceID.replace(resourceType,"json")+".json"
    try:
        f = open(jsonFile)
        f = f.read()
        f = json.loads(f)
    except:
        main(resourceID,name)
        f = open(jsonFile)
        f = f.read()
        f = json.loads(f)
        print("created new json file: " +jsonFile)

    y = {
        resourceType:{
            "resourceID":resourceID.replace("results/",""),
            "width":width,
            "height":height,
            "last updated": str(datetime.now()),
            "startYear": startYear,
            "endYear": endYear,
            "dataSource": dataSource,
            "dataSourceLink": dataSourceLink,
        }
    }
    f["resources"].update(y)

    #sets name
    #with open('results/json/'+resourceID+'.json', "w") as myfile:
    with open(jsonFile, "w") as myfile:
        myfile.write(json.dumps(f, indent=2))

#updateMetadata("US/AL","png")