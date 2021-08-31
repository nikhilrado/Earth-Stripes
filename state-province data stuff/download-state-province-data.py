#This Program was created to download temperature data from berkley earth
#It is a modified version of the program to download country data which is a modified version of the program to download NOAA data
#
#

import csv
import requests
import os
from requests.utils import quote

countryErrorList = [] #contains list of any countries who couldn't be accessed

#list of territories to download
provincesToDownload = ["Acre", "Adygey", "Aga Buryat", "Alagoas", "Alberta", "Altay", "Amapá", "Amazonas", "Amur", "Andaman and Nicobar", "Andhra Pradesh", "Anhui", "Arkhangel'sk", "Arunachal Pradesh", "Assam", "Astrakhan'", "Australian Capital Territory", "Bahia", "Bashkortostan", "Beijing", "Belgorod", "Bihar", "British Columbia", "Bryansk", "Buryat", "Ceará", "Chandigarh", "Chechnya", "Chelyabinsk", "Chhattisgarh", "Chita", "Chongqing", "Chukot", "Chuvash", "City of St. Petersburg", "Dadra and Nagar Haveli", "Dagestan", "Daman and Diu", "Delhi", "Distrito Federal", "Espírito Santo", "Evenk", "Fujian", "Gansu", "Goa", "Goiás", "Gorno-Altay", "Guangdong", "Guangxi", "Guizhou", "Gujarat", "Hainan", "Haryana", "Hebei", "Heilongjiang", "Henan", "Himachal Pradesh", "Hubei", "Hunan", "Ingush", "Irkutsk", "Ivanovo", "Jammu and Kashmir", "Jharkhand", "Jiangsu", "Jiangxi", "Jilin", "Kabardin-Balkar", "Kaliningrad", "Kalmyk", "Kaluga", "Kamchatka", "Karachay-Cherkess", "Karelia", "Karnataka", "Kemerovo", "Kerala", "Khabarovsk", "Khakass", "Khanty-Mansiy", "Kirov", "Komi", "Komi-Permyak", "Koryak", "Kostroma", "Krasnodar", "Krasnoyarsk", "Kurgan", "Kursk", "Leningrad", "Liaoning", "Lipetsk", "Madhya Pradesh", "Maga Buryatdan", "Maharashtra", "Manipur", "Manitoba", "Maranhão", "Mariy-El", "Mato Grosso", "Mato Grosso do Sul", "Meghalaya", "Minas Gerais", "Mizoram", "Mordovia", "Moscow City", "Moskva", "Murmansk", "Nagaland", "Nei Mongol", "Nenets", "New Brunswick", "New South Wales", "Newfoundland and Labrador", "Ningxia Hui", "Nizhegorod", "North Ossetia", "Northern Territory", "Northwest Territories", "Nova Scotia", "Novgorod", "Novosibirsk", "Nunavut", "Omsk", "Ontario", "Orel", "Orenburg", "Orissa", "Pará", "Paraíba", "Paraná", "Penza", "Perm'", "Pernambuco", "Piauí", "Primor'ye", "Prince Edward Island", "Pskov", "Puducherry", "Punjab", "Qinghai", "Québec", "Queensland", "Rajasthan", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Rostov", "Ryazan'", "Sakha", "Sakhalin", "Samara", "Santa Catarina", "São Paulo", "Saratov", "Saskatchewan", "Sergipe", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan", "Sikkim", "Smolensk", "South Australia", "Stavropol'", "Sverdlovsk", "Tambov", "Tamil Nadu", "Tasmania", "Tatarstan", "Taymyr", "Tianjin", "Tocantins", "Tomsk", "Tripura", "Tula", "Tuva", "Tver'", "Tyumen'", "Udmurt", "Ul'yanovsk", "Ust-Orda Buryat", "Uttar Pradesh", "Uttaranchal", "Victoria", "Vladimir", "Volgograd", "Vologda", "Voronezh", "West Bengal", "Western Australia", "Xinjiang Uygur", "Xizang", "Yamal-Nenets", "Yaroslavl'", "Yevrey", "Yukon", "Yunnan", "Zhejiang"]
countriesThatStatesAreIn = ["Brazil","Russia","Russia","Brazil","Canada","Russia","Brazil","Brazil","Russia","India","India","China","Russia","India","India","Russia","Australia","Brazil","Russia","China","Russia","India","Canada","Russia","Russia","Brazil","India","Russia","Russia","India","Russia","China","Russia","Russia","Russia","India","Russia","India","India","Brazil","Brazil","Russia","China","China","India","Brazil","Russia","China","China","China","India","China","India","China","China","China","India","China","China","Russia","Russia","Russia","India","India","China","China","China","Russia","Russia","Russia","Russia","Russia","Russia","Russia","India","Russia","India","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","China","Russia","India","Russia","India","India","Canada","Brazil","Russia","Brazil","Brazil","India","Brazil","India","Russia","Russia","Russia","Russia","India","China","Russia","Canada","Australia","Canada","China","Russia","Russia","Australia","Canada","Canada","Russia","Russia","Canada","Russia","Canada","Russia","Russia","India","Brazil","Brazil","Brazil","Russia","Russia","Brazil","Brazil","Russia","Canada","Russia","India","India","China","Canada","Australia","India","Brazil","Brazil","Brazil","Brazil","Brazil","Russia","Russia","Russia","Russia","Russia","Brazil","Brazil","Russia","Canada","Brazil","China","China","China","China","China","India","Russia","Australia","Russia","Russia","Russia","India","Australia","Russia","Russia","China","Brazil","Russia","India","Russia","Russia","Russia","Russia","Russia","Russia","Russia","India","India","Australia","Russia","Russia","Russia","Russia","India","Australia","China","China","Russia","Russia","Russia","Canada","China","China"]

#list of all countries for reference: 
allTerritories = ["Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua And Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia And Herzegovina","Botswana","Bouvet Island","Brazil","British Indian Ocean Territory","Brunei Darussalam","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Cocos (keeling) Islands","Colombia","Comoros","Congo","Congo, The Democratic Republic Of The","Cook Islands","Costa Rica","Cote D'ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands (malvinas)","Faroe Islands","Fiji","Finland","France","French Guiana","French Polynesia","French Southern Territories","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guinea","Guinea-bissau","Guyana","Haiti","Heard Island And Mcdonald Islands","Holy See (vatican City State)","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran, Islamic Republic Of","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakstan","Kenya","Kiribati","Korea, Democratic People's Republic Of","Korea, Republic Of","Kosovo","Kuwait","Kyrgyzstan","Lao People's Democratic Republic","Latvia","Lebanon","Lesotho","Liberia","Libyan Arab Jamahiriya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia, The Former Yugoslav Republic Of","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia, Federated States Of","Moldova, Republic Of","Monaco","Mongolia","Montserrat","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Palestinian Territory, Occupied","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russian Federation","Rwanda","Saint Helena","Saint Kitts And Nevis","Saint Lucia","Saint Pierre And Miquelon","Saint Vincent And The Grenadines","Samoa","San Marino","Sao Tome And Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Georgia And The South Sandwich Islands","Spain","Sri Lanka","Sudan","Suriname","Svalbard And Jan Mayen","Swaziland","Sweden","Switzerland","Syrian Arab Republic","Taiwan, Province Of China","Tajikistan","Tanzania, United Republic Of","Thailand","Togo","Tokelau","Tonga","Trinidad And Tobago","Tunisia","Turkey","Turkmenistan","Turks And Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","United States Minor Outlying Islands","Uruguay","Uzbekistan","Vanuatu","Venezuela","Viet Nam","Virgin Islands, British","Virgin Islands, U.s.","Wallis And Futuna","Western Sahara","Yemen","Zambia","Zimbabwe"]
allTerritoriesAbbreviations = ["AF","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BM","BT","BO","BA","BW","BV","BR","IO","BN","BG","BF","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CC","CO","KM","CG","CD","CK","CR","CI","HR","CU","CY","CZ","DK","DJ","DM","DO","TP","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GN","GW","GY","HT","HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IL","IT","JM","JP","JO","KZ","KE","KI","KP","KR","KV","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX","FM","MD","MC","MN","MS","ME","MA","MZ","MM","NA","NR","NP","NL","AN","NC","NZ","NI","NE","NG","NU","NF","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA","RE","RO","RU","RW","SH","KN","LC","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SK","SI","SB","SO","ZA","GS","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TG","TK","TO","TT","TN","TR","TM","TC","TV","UG","UA","AE","GB","US","UM","UY","UZ","VU","VE","VN","VG","VI","WF","EH","YE","ZM","ZW"]

berklyTerritories = ["Afghanistan","Åland","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bonaire, Saint Eustatius and Saba","Bosnia and Herzegovina","Botswana","Brazil","British Virgin Islands","Bulgaria","Burkina Faso","Burma","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Colombia","Comoros","Congo","Congo (Democratic Republic of the)","Costa Rica","Côte d'Ivoire","Croatia","Cuba","Curaçao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands (Islas Malvinas)","Faroe Islands","Fiji","Finland","France (Europe)","French Guiana","French Polynesia","French Southern and Antarctic Lands","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti","Heard Island and McDonald Islands","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands (Europe)","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","North Korea","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Palestina","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Barthélemy","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Sint Maarten","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Georgia and the South Sandwich Isla","South Korea","Spain","Sri Lanka","Sudan","Suriname","Svalbard and Jan Mayen","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicas Islands","Uganda","Ukraine","United Arab Emirates","United Kingdom (Europe)","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands","Western Sahara","Yemen","Zambia","Zimbabwe"]
berklyTerritoriesAbbreviations = ["AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BT","BO","BQ","BA","BW","BR","IO","BG","BF","MM","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CO","KM","CG","CD","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT","HM","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ","KE","KI","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","ML","MT","MQ","MR","MU","YT","MX","MD","MC","MN","ME","MS","MA","MZ","NA","NP","NL","NC","NZ","NI","NE","NG","NU","KP","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PL","PT","PR","QA","RE","RO","RU","RW","BL","KN","LC","MF","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","GS","KR","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TO","TT","TN","TR","TM","TC","UG","UA","AE","GB","US","UY","UZ","VE","VN","VG","EH","YE","ZM","ZW"]

windowsChars = ["À","Á","Â","Ã","Ä","Å","Æ","Ç","È","É","Ê","Ë","Ì","Í","Î","Ï","Ð","Ñ","Ò","Ó","Ô","Õ","Ö","×","Ø","Ù","Ú","Û","Ü","Ý","Þ","ß","à","á","â","ã","ä","å","æ","ç","è","é","ê","ë","ì","í","î","ï","ð","ñ","ò","ó","ô","õ","ö","÷","ø","ù","ú","û","ü","ý","þ","ÿ"]
windowsCharsEncodedSymbol = []

def getTerritoryAbrev(state):
    if len(state) == 2:
        return berklyTerritories[berklyTerritoriesAbbreviations.index(state)]
    return berklyTerritoriesAbbreviations[berklyTerritories.index(state)]

def getStateCountry(state):
    return countriesThatStatesAreIn[provincesToDownload.index(state)]

def saveResource(resourceURL):
    #use this to indivicually download a certain URL to fix error or test program
    #resourceURL = 'http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/japan-TAVG-Trend.txt'

    with requests.Session() as s:
        #resourceURL = "http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/amap%a0-TAVG-Trend.txt"
        download = s.get(resourceURL)
        #print(resourceURL)
        decoded_content = download.content.decode('Windows-1252')
        #print(decoded_content)
        cr = csv.reader(decoded_content.splitlines(), delimiter=' ')
        my_list = list(cr)
        for row in my_list:
            #removes all whitespace
            while("" in row) :
                row.remove("")
        

    #extract metadata from csv
    #this ends up not being used, but may be helpful in the future
    metaDataList = []
    for row in my_list:
        try:
            #print(row[0])
            if row[0] == "%%":
                metaDataList.append(row)
        except:
            for row in metaDataList:
                print(row)
            break
    
    #skip this country if can't access expected file format of berkley data (url gives us 404 or other error)
    if my_list[0][0] != "%":
        countryErrorList.append(resourceURL)
        return "done"

    #extracts country name
    country = " "
    country = country.join(my_list[4][1:])

    #extracts information about the base period of anomaly data
    basePeriod = " "
    basePeriod = basePeriod.join(my_list[15])

    #searches the raw file for the first and last year that data is provided
    startYear = "0000"
    endYear = my_list[-1][0][:4]
    for i in range(len(my_list)):
        try:
            if my_list[i][1] == "Year,":
                startYear = my_list[i+2][0]
                break
        except:
            continue

    processedData = []
    processedDataStartYear = 1901 #EDITABLE change this to start all of the processed data at a new year
    tempData = 0 #variable used to count average temperature throughout loop
    for row in my_list:
        if row == [] or "%" in row[0] or int(row[0]) < processedDataStartYear:
            continue
        #row[0] is year, row[1] is month, row[2] is temp data
        if int(row[1]) == 1:
            tempData = 0
        tempData += float(row[2])
        if int(row[1]) == 12:
            processedData.append([row[0],round(tempData/12,3)]) #saves clean data to list

    processedDataEndYear = processedData[-1][0] #gets the last year in the processed data list
    
    #formats the processed data just like the US NOAA data so we can create a chart (this is mostly filler data)
    firstFewLines = [[country, getStateCountry(country), "Average Temperature", "Annual Average of Months"],["Units: Degrees C"],["Base Period: "+ basePeriod[2:]],["Data: "+str(processedDataStartYear)+"-"+str(processedDataEndYear)],["Date","Value","Anomaly"]]
    processedData = firstFewLines + processedData

    #Creates a new OS path if we ever want to change file path structure
    #https://stackoverflow.com/questions/1274405/how-to-create-new-folder #https://stackoverflow.com/a/1274465
    #newpath = 'World Data Stuff/data/'+state 
    #if not os.path.exists(newpath):
    #    os.makedirs(newpath)

    #saves raw file with country name
    with open('data/state-province-data/raw/%s %s RAW - AnnTemp %s-%s.txt' % (country,country,startYear,endYear), "w") as myfile:
        myfile.write(decoded_content)

    #saves processed file with country name
    with open('data/state-province-data/processed/%s - AnnTemp %s-%s.csv' % (country,processedDataStartYear,processedDataEndYear), 'w', newline="") as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerows(processedData)


#creates the URLS needed to access the berkley data
newData = ""
counter = 0
for territory in provincesToDownload:
    
        counter += 1
        resourceURL = "http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/%s-TAVG-Trend.txt" % (territory.lower().replace(" ","-"))
        #use for custom URL request
        #resourceURL = """http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/c%F4te-d%27ivoire-TAVG-Trend.txt"""
        print("County: " + str(counter)  +  ' ' + resourceURL)

        newData = newData + resourceURL + "\n"
        if saveResource(resourceURL) == "done":
            continue
    #print(newData)

    #with open('County Data Stuff/test11.txt', "w") as myfile:
    #    myfile.write(newData)

#prints a list of countries where data could not be retrieved for manual retrieval
print("Could not access the following data files:")
for url in countryErrorList:
    print(url)

errorURLList = ["http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/amap%a0-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/cear%a0-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/esp%a1rito-santo-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/goi%a0s-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/maranhao-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/par%a0-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/para%a1ba-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/paran%a0-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/piau%a1-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/qu%82bec-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/rond%93nia-TAVG-Trend.txt","http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/sao-paulo-TAVG-Trend.txt"]
for errorURL in errorURLList:
    saveResource(errorURL)

