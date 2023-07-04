#list of global data that needs to be accessed multiple times
import os

#convert between long or short name of the state
stateFullName = ["County","Washington D.C.","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
state_short_name = ["ty","DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[state_short_name.index(state)]
    return state_short_name[stateFullName.index(state)]

#list of all countries for reference: 
allTerritories = ["Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua And Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia And Herzegovina","Botswana","Bouvet Island","Brazil","British Indian Ocean Territory","Brunei Darussalam","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Cocos (keeling) Islands","Colombia","Comoros","Congo","Congo, The Democratic Republic Of The","Cook Islands","Costa Rica","Cote D'ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands (malvinas)","Faroe Islands","Fiji","Finland","France","French Guiana","French Polynesia","French Southern Territories","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guinea","Guinea-bissau","Guyana","Haiti","Heard Island And Mcdonald Islands","Holy See (vatican City State)","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran, Islamic Republic Of","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakstan","Kenya","Kiribati","Korea, Democratic People's Republic Of","Korea, Republic Of","Kosovo","Kuwait","Kyrgyzstan","Lao People's Democratic Republic","Latvia","Lebanon","Lesotho","Liberia","Libyan Arab Jamahiriya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia, The Former Yugoslav Republic Of","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia, Federated States Of","Moldova, Republic Of","Monaco","Mongolia","Montserrat","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Palestinian Territory, Occupied","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Helena","Saint Kitts And Nevis","Saint Lucia","Saint Pierre And Miquelon","Saint Vincent And The Grenadines","Samoa","San Marino","Sao Tome And Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","South Georgia And The South Sandwich Islands","Spain","Sri Lanka","Sudan","Suriname","Svalbard And Jan Mayen","Swaziland","Sweden","Switzerland","Syrian Arab Republic","Taiwan, Province Of China","Tajikistan","Tanzania, United Republic Of","Thailand","Togo","Tokelau","Tonga","Trinidad And Tobago","Tunisia","Turkey","Turkmenistan","Turks And Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","United States Minor Outlying Islands","Uruguay","Uzbekistan","Vanuatu","Venezuela","Viet Nam","Virgin Islands, British","Virgin Islands, U.s.","Wallis And Futuna","Western Sahara","Yemen","Zambia","Zimbabwe"]
allTerritoriesAbbreviations = ["AF","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BM","BT","BO","BA","BW","BV","BR","IO","BN","BG","BF","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CC","CO","KM","CG","CD","CK","CR","CI","HR","CU","CY","CZ","DK","DJ","DM","DO","TP","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GN","GW","GY","HT","HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IL","IT","JM","JP","JO","KZ","KE","KI","KP","KR","KV","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX","FM","MD","MC","MN","MS","ME","MA","MZ","MM","NA","NR","NP","NL","AN","NC","NZ","NI","NE","NG","NU","NF","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA","RE","RO","RU","RW","SH","KN","LC","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SK","SI","SB","SO","ZA","SS","GS","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TG","TK","TO","TT","TN","TR","TM","TC","TV","UG","UA","AE","GB","US","UM","UY","UZ","VU","VE","VN","VG","VI","WF","EH","YE","ZM","ZW"]
def getCountryCode(country):
    if len(country) == 2:
        return allTerritories[allTerritoriesAbbreviations.index(country)]
    return allTerritoriesAbbreviations[allTerritories.index(country)]

provinces = ["Australian Capital Territory","New South Wales","Northern Territory","Queensland","South Australia","Tasmania","Victoria","Western Australia","Acre","Alagoas","Amapá","Amazonas","Bahia","Ceará","Distrito Federal","Espírito Santo","Goiás","Maranhão","Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará","Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro","Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima","Santa Catarina","São Paulo","Sergipe","Tocantins","Alberta","British Columbia","Manitoba","New Brunswick","Newfoundland and Labrador","Northwest Territories","Nova Scotia","Nunavut","Ontario","Prince Edward Island","Québec","Saskatchewan","Yukon","Andaman and Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli","Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Orissa","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttaranchal","West Bengal"]
provinceAbrev = ["ACT","NSW","NT","QLD","SA","TAS","VIC","WA","AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO","AB","BC","MB","NB","NL","NT","NS","NU","ON","PE","QC","SK","YT","AN","AP","AR","AS","BR","CH","CT","DN","DD","DL","GA","GJ","HR","HP","JK","JH","KA","KL","MP","MH","MN","ML","MZ","NL","OR","PY","PB","RJ","SK","TN","TR","UP","UT","WB"]

def getProvinceAbrev(province): 
    #if len(province) <= 3:
    #    return provinces[provinceAbrev.index(province)]
    return provinceAbrev[provinces.index(province)]

#convert between long or short name of the state
ISO_CODE_3 = ["AND","ARE","AFG","ATG","AIA","ALB","ARM","AGO","ATA","ARG","ASM","AUT","AUS","ABW","ALA","AZE","BIH","BRB","BGD","BEL","BFA","BGR","BHR","BDI","BEN","BLM","BMU","BRN","BOL","BES","BRA","BHS","BTN","BVT","BWA","BLR","BLZ","CAN","CCK","COD","CAF","COG","CHE","CIV","COK","CHL","CMR","CHN","COL","CRI","CUB","CPV","CUW","CXR","CYP","CZE","DEU","DJI","DNK","DMA","DOM","DZA","ECU","EST","EGY","ESH","ERI","ESP","ETH","FIN","FJI","FLK","FSM","FRO","FRA","GAB","GBR","GRD","GEO","GUF","GGY","GHA","GIB","GRL","GMB","GIN","GLP","GNQ","GRC","SGS","GTM","GUM","GNB","GUY","HKG","HMD","HND","HRV","HTI","HUN","IDN","IRL","ISR","IMN","IND","IOT","IRQ","IRN","ISL","ITA","JEY","JAM","JOR","JPN","KEN","KGZ","KHM","KIR","COM","KNA","PRK","KOR","KWT","CYM","KAZ","LAO","LBN","LCA","LIE","LKA","LBR","LSO","LTU","LUX","LVA","LBY","MAR","MCO","MDA","MNE","MAF","MDG","MHL","MKD","MLI","MMR","MNG","MAC","MNP","MTQ","MRT","MSR","MLT","MUS","MDV","MWI","MEX","MYS","MOZ","NAM","NCL","NER","NFK","NGA","NIC","NLD","NOR","NPL","NRU","NIU","NZL","OMN","PAN","PER","PYF","PNG","PHL","PAK","POL","SPM","PCN","PRI","PSE","PRT","PLW","PRY","QAT","REU","ROU","SRB","RUS","RWA","SAU","SLB","SYC","SDN","SWE","SGP","SHN","SVN","SJM","SVK","SLE","SMR","SEN","SOM","SUR","SSD","STP","SLV","SXM","SYR","SWZ","TCA","TCD","ATF","TGO","THA","TJK","TKL","TLS","TKM","TUN","TON","TUR","TTO","TUV","TWN","TZA","UKR","UGA","UMI","USA","URY","UZB","VAT","VCT","VEN","VGB","VIR","VNM","VUT","WLF","WSM","YEM","MYT","ZAF","ZMB","ZWE"]
ISO_CODE_2 = ["AD" ,"AE" ,"AF" ,"AG" ,"AI" ,"AL" ,"AM" ,"AO" ,"AQ" ,"AR" ,"AS" ,"AT" ,"AU" ,"AW" ,"AX" ,"AZ" ,"BA" ,"BB" ,"BD" ,"BE" ,"BF" ,"BG" ,"BH" ,"BI" ,"BJ" ,"BL" ,"BM" ,"BN" ,"BO" ,"BQ" ,"BR" ,"BS" ,"BT" ,"BV" ,"BW" ,"BY" ,"BZ" ,"CA" ,"CC" ,"CD" ,"CF" ,"CG" ,"CH" ,"CI" ,"CK" ,"CL" ,"CM" ,"CN" ,"CO" ,"CR" ,"CU" ,"CV" ,"CW" ,"CX" ,"CY" ,"CZ" ,"DE" ,"DJ" ,"DK" ,"DM" ,"DO" ,"DZ" ,"EC" ,"EE" ,"EG" ,"EH" ,"ER" ,"ES" ,"ET" ,"FI" ,"FJ" ,"FK" ,"FM" ,"FO" ,"FR" ,"GA" ,"GB" ,"GD" ,"GE" ,"GF" ,"GG" ,"GH" ,"GI" ,"GL" ,"GM" ,"GN" ,"GP" ,"GQ" ,"GR" ,"GS" ,"GT" ,"GU" ,"GW" ,"GY" ,"HK" ,"HM" ,"HN" ,"HR" ,"HT" ,"HU" ,"ID" ,"IE" ,"IL" ,"IM" ,"IN" ,"IO" ,"IQ" ,"IR" ,"IS" ,"IT" ,"JE" ,"JM" ,"JO" ,"JP" ,"KE" ,"KG" ,"KH" ,"KI" ,"KM" ,"KN" ,"KP" ,"KR" ,"KW" ,"KY" ,"KZ" ,"LA" ,"LB" ,"LC" ,"LI" ,"LK" ,"LR" ,"LS" ,"LT" ,"LU" ,"LV" ,"LY" ,"MA" ,"MC" ,"MD" ,"ME" ,"MF" ,"MG" ,"MH" ,"MK" ,"ML" ,"MM" ,"MN" ,"MO" ,"MP" ,"MQ" ,"MR" ,"MS" ,"MT" ,"MU" ,"MV" ,"MW" ,"MX" ,"MY" ,"MZ" ,"NA" ,"NC" ,"NE" ,"NF" ,"NG" ,"NI" ,"NL" ,"NO" ,"NP" ,"NR" ,"NU" ,"NZ" ,"OM" ,"PA" ,"PE" ,"PF" ,"PG" ,"PH" ,"PK" ,"PL" ,"PM" ,"PN" ,"PR" ,"PS" ,"PT" ,"PW" ,"PY" ,"QA" ,"RE" ,"RO" ,"RS" ,"RU" ,"RW" ,"SA" ,"SB" ,"SC" ,"SD" ,"SE" ,"SG" ,"SH" ,"SI" ,"SJ" ,"SK" ,"SL" ,"SM" ,"SN" ,"SO" ,"SR" ,"SS" ,"ST" ,"SV" ,"SX" ,"SY" ,"SZ" ,"TC" ,"TD" ,"TF" ,"TG" ,"TH" ,"TJ" ,"TK" ,"TL" ,"TM" ,"TN" ,"TO" ,"TR" ,"TT" ,"TV" ,"TW" ,"TZ" ,"UA" ,"UG" ,"UM" ,"US" ,"UY" ,"UZ" ,"VA" ,"VC" ,"VE" ,"VG" ,"VI" ,"VN" ,"VU" ,"WF" ,"WS" ,"YE" ,"YT" ,"ZA" ,"ZM" ,"ZW" ]
def getISOconverted(code):
    if len(code) == 2:
        return ISO_CODE_3[ISO_CODE_2.index(code)]
    return ISO_CODE_2[ISO_CODE_3.index(code)]

#returns a list of all files in a directory
def getAllFilesInDir(root):
    fileList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            fileList.append(os.path.join(path, name))
    return fileList

# returns url path of result page from location id
def get_result_page(location_id):
    location_id = location_id.split("/")
    print(location_id)

    url = "/result/"
    if "location/" in location_id:
        return url + "?location=" + location_id[1]
    url += "?country=" + location_id[0] if location_id[0] else ""
    url += "&state=" + location_id[1] if location_id[1] else ""
    url += "&county=" + location_id[2] if location_id[2] else ""

    return url