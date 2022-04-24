import csv
from datetime import datetime
import globals
import test6

class create_state_images:
    states = ["DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

    def main(chartType="stripes"):
        #TODO get Alaska and Hawaii to work
        for state in create_state_images.states:
            dataFileName = "data/us-state-data-NOAA/2021/" + state + " - AnnTemp 1895-2021.csv"
            imagePath = 'results/'+chartType+'/US/'+state

            try:
                test6.createChart(dataFileName,imagePath,chartType)
            except:
                print("Error creating chart for " + dataFileName)

class create_country_images:
    def main(chartType="stripes"):
        for country in globals.allTerritoriesAbbreviations:
            dataFileName = "data/country-data-berkley-earth/processed/" + country + " - AnnTemp 1901-2020.csv"

            imagePath = 'results/'+chartType+'/'+country
            try:
                test6.createChart(dataFileName,imagePath,chartType)
            except:
                try:
                    dataFileName = "data/country-data-berkley-earth/processed/" + country + " - AnnTemp 1901-2015.csv"
                    test6.createChart(dataFileName,imagePath,chartType)
                except:
                    print("----------error: "+dataFileName)

class create_county_images:
    def main(chartType="stripes"):
        f = open('data/list of US counties.csv', "r")
        csv_f = csv.reader(f)

        rowsList = []
        for row in csv_f:
            rowsList.append(row)

        for row in rowsList:
            dataFileName = "data/us-county-data-NOAA/2021/" + globals.getStateAbrev(row[0][-2:]) + "/"+row[0]+" - AnnTemp 1895-2021.csv"

            imagePath = 'results/'+chartType+'/US/'+row[0][-2:]+"/"+row[0]
            try:
                test6.createChart(dataFileName,imagePath,chartType)
            except:
                print("----------error: "+dataFileName)
            #test6.createChart(fileName,imagePath,chartType)
        createChartsFromData("data/USA2021.csv","US")

class create_province_state_images:
    provincesToDownload = ["Acre", "Adygey", "Aga Buryat", "Alagoas", "Alberta", "Altay", "Amapá", "Amazonas", "Amur", "Andaman and Nicobar", "Andhra Pradesh", "Anhui", "Arkhangel'sk", "Arunachal Pradesh", "Assam", "Astrakhan'", "Australian Capital Territory", "Bahia", "Bashkortostan", "Beijing", "Belgorod", "Bihar", "British Columbia", "Bryansk", "Buryat", "Ceará", "Chandigarh", "Chechnya", "Chelyabinsk", "Chhattisgarh", "Chita", "Chongqing", "Chukot", "Chuvash", "City of St. Petersburg", "Dadra and Nagar Haveli", "Dagestan", "Daman and Diu", "Delhi", "Distrito Federal", "Espírito Santo", "Evenk", "Fujian", "Gansu", "Goa", "Goiás", "Gorno-Altay", "Guangdong", "Guangxi", "Guizhou", "Gujarat", "Hainan", "Haryana", "Hebei", "Heilongjiang", "Henan", "Himachal Pradesh", "Hubei", "Hunan", "Ingush", "Irkutsk", "Ivanovo", "Jammu and Kashmir", "Jharkhand", "Jiangsu", "Jiangxi", "Jilin", "Kabardin-Balkar", "Kaliningrad", "Kalmyk", "Kaluga", "Kamchatka", "Karachay-Cherkess", "Karelia", "Karnataka", "Kemerovo", "Kerala", "Khabarovsk", "Khakass", "Khanty-Mansiy", "Kirov", "Komi", "Komi-Permyak", "Koryak", "Kostroma", "Krasnodar", "Krasnoyarsk", "Kurgan", "Kursk", "Leningrad", "Liaoning", "Lipetsk", "Madhya Pradesh", "Maga Buryatdan", "Maharashtra", "Manipur", "Manitoba", "Maranhão", "Mariy-El", "Mato Grosso", "Mato Grosso do Sul", "Meghalaya", "Minas Gerais", "Mizoram", "Mordovia", "Moscow City", "Moskva", "Murmansk", "Nagaland", "Nei Mongol", "Nenets", "New Brunswick", "New South Wales", "Newfoundland and Labrador", "Ningxia Hui", "Nizhegorod", "North Ossetia", "Northern Territory", "Northwest Territories", "Nova Scotia", "Novgorod", "Novosibirsk", "Nunavut", "Omsk", "Ontario", "Orel", "Orenburg", "Orissa", "Pará", "Paraíba", "Paraná", "Penza", "Perm'", "Pernambuco", "Piauí", "Primor'ye", "Prince Edward Island", "Pskov", "Puducherry", "Punjab", "Qinghai", "Québec", "Queensland", "Rajasthan", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Rostov", "Ryazan'", "Sakha", "Sakhalin", "Samara", "Santa Catarina", "São Paulo", "Saratov", "Saskatchewan", "Sergipe", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan", "Sikkim", "Smolensk", "South Australia", "Stavropol'", "Sverdlovsk", "Tambov", "Tamil Nadu", "Tasmania", "Tatarstan", "Taymyr", "Tianjin", "Tocantins", "Tomsk", "Tripura", "Tula", "Tuva", "Tver'", "Tyumen'", "Udmurt", "Ul'yanovsk", "Ust-Orda Buryat", "Uttar Pradesh", "Uttaranchal", "Victoria", "Vladimir", "Volgograd", "Vologda", "Voronezh", "West Bengal", "Western Australia", "Xinjiang Uygur", "Xizang", "Yamal-Nenets", "Yaroslavl'", "Yevrey", "Yukon", "Yunnan", "Zhejiang"]
    countriesThatStatesAreIn = ["Brazil","Russia","Russia","Brazil","Canada","Russia","Brazil","Brazil","Russia","India","India","China","Russia","India","India","Russia","Australia","Brazil","Russia","China","Russia","India","Canada","Russia","Russia","Brazil","India","Russia","Russia","India","Russia","China","Russia","Russia","Russia","India","Russia","India","India","Brazil","Brazil","Russia","China","China","India","Brazil","Russia","China","China","China","India","China","India","China","China","China","India","China","China","Russia","Russia","Russia","India","India","China","China","China","Russia","Russia","Russia","Russia","Russia","Russia","Russia","India","Russia","India","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","China","Russia","India","Russia","India","India","Canada","Brazil","Russia","Brazil","Brazil","India","Brazil","India","Russia","Russia","Russia","Russia","India","China","Russia","Canada","Australia","Canada","China","Russia","Russia","Australia","Canada","Canada","Russia","Russia","Canada","Russia","Canada","Russia","Russia","India","Brazil","Brazil","Brazil","Russia","Russia","Brazil","Brazil","Russia","Canada","Russia","India","India","China","Canada","Australia","India","Brazil","Brazil","Brazil","Brazil","Brazil","Russia","Russia","Russia","Russia","Russia","Brazil","Brazil","Russia","Canada","Brazil","China","China","China","China","China","India","Russia","Australia","Russia","Russia","Russia","India","Australia","Russia","Russia","China","Brazil","Russia","India","Russia","Russia","Russia","Russia","Russia","Russia","Russia","India","India","Australia","Russia","Russia","Russia","Russia","India","Australia","China","China","Russia","Russia","Russia","Canada","China","China"]

    def getStateCountry(state):
        return create_province_state_images.countriesThatStatesAreIn[create_province_state_images.provincesToDownload.index(state)]

    def main(chartType="stripes"):
        for province in create_province_state_images.provincesToDownload:
            dataFileName = "data/state-province-data/processed/" + province + " - AnnTemp 1901-2020.csv"

            countryCode = globals.getCountryCode(create_province_state_images.getStateCountry(province))
            countriesWithProvinceAbbrv = ['AU','BR','CA','IN'] #countries that google maps and mapbox return province code with
            if globals.getCountryCode(create_province_state_images.getStateCountry(province)) in countriesWithProvinceAbbrv:
                province = globals.getProvinceAbrev(province)

            imagePath = 'results/'+chartType+'/'+countryCode+'/'+province
            try:
                test6.createChart(dataFileName,imagePath,chartType)
            except:
                try:
                   dataFileName = "data/state-province-data/processed/" + province + " - AnnTemp 1901-2015.csv"
                   test6.createChart(dataFileName,imagePath,chartType)
                except:
                    print("----------error: "+dataFileName)

            #TODO: figure out what to do with countries that have data only to 2015

class create_earth_images:

    def main(chartType="light-labeled-bars"):
        try:
            test6.createChart("data/hadcrut_dataset.csv","results/" + chartType + "/location/earth",chartType,globe=True)
        except:
            print("----------error: data/hadcrut_dataset.csv")

now = datetime.now()
#test25_create_state_images.main("labeled-stripes")
#test25_create_state_images.main("stripes-svg")
#test13_create_county_images.main("stripes")
#test13_create_county_images.main("labeled-stripes")
#test13_create_county_images.main("stripes-svg")
#test18_create_country_images.main("labeled-bars")
# test18_create_country_images.main("stripes")
#test18_create_country_images.main("stripes-svg")
# test42_create_province_state_images.main("labeled-bars")
# test42_create_province_state_images.main("stripes")
# test42_create_province_state_images.main("stripes-svg")

#create_province_state_images.main("snap-sticker")
"""
test18_create_country_images.main("stripes")
test42_create_province_state_images.main("stripes")

test13_create_county_images.main("labeled-bars")
test25_create_state_images.main("labeled-bars")
test18_create_country_images.main("labeled-bars")
test42_create_province_state_images.main("labeled-bars")

test13_create_county_images.main("labeled-stripes")
test25_create_state_images.main("labeled-stripes")
test18_create_country_images.main("labeled-stripes")
test42_create_province_state_images.main("labeled-stripes")

test13_create_county_images.main("snap-sticker")
test25_create_state_images.main("snap-sticker")
test18_create_country_images.main("snap-sticker")
test42_create_province_state_images.main("snap-sticker")

test13_create_county_images.main("twitter-card")
test25_create_state_images.main("twitter-card")
test18_create_country_images.main("twitter-card")
test42_create_province_state_images.main("twitter-card")

test13_create_county_images.main("label")
test25_create_state_images.main("label")
test18_create_country_images.main("label")
test42_create_province_state_images.main("label")

"""
# test6.createChart("data/USA2021.csv","results/label/US",chartType="label")
# test6.createChart("data/USA2021.csv","results/labeled-bars/US",chartType="labeled-bars")
# test6.createChart("data/USA2021.csv","results/labeled-stripes/US",chartType="labeled-stripes")
# test6.createChart("data/USA2021.csv","results/snap-sticker/US",chartType="snap-sticker")
# test6.createChart("data/USA2021.csv","results/stripes/US",chartType="stripes")
# test6.createChart("data/USA2021.csv","results/twitter-card/US",chartType="twitter-card")

# def createChartsFromData(dataFile,chartTypes=["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card"]):
#     for chartType in chartTypes:
#         test6.createChart(dataFile,"results/"+chartType+"/US",chartType=chartType)

def createChartsFromData(dataFile,locationID,chartTypes=["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg","light-labeled-bars"]):
    for chartType in chartTypes:
        test6.createChart(dataFile,"results/"+chartType+"/"+locationID,chartType=chartType,save=True)

def create_charts_for_image_type(image_type: str):
    create_state_images.main(image_type)
    create_country_images.main(image_type)
    create_province_state_images.main(image_type)
    create_county_images.main(image_type)
    create_earth_images.main(image_type)

for chart in ["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg","light-labeled-bars"]:
    create_province_state_images.main(chart)


#create_charts_for_image_type("light-labeled-bars")
#createChartsFromData("data/hadcrut_dataset.csv","location/earth")
current_time = now.strftime("%H:%M:%S")
print("Time Finished =", current_time)
