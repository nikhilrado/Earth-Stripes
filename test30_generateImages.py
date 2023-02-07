import csv
from datetime import datetime
import globals
import test6

class us_state_images:
    states = ["DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

    def generate(chart_type="stripes"):
        #TODO: get Alaska and Hawaii to work
        for state in us_state_images.states:
            data_file_name = "data/us-state-data-NOAA/2022/" + state + " - AnnTemp 1895-2022.csv"
            image_path = 'results/'+chart_type+'/US/'+state

            try:
                test6.createChart(data_file_name,image_path,chart_type,data_start=15)
            except Exception as e:
                print("Error creating chart for " + data_file_name)
                print(e)

class country_images:
    def generate(chart_type="stripes"):
        for country in globals.allTerritoriesAbbreviations:
            data_file_name = "data/country-data-berkley-earth/processed/" + country + " - AnnTemp 1901-2020.csv"

            image_path = 'results/'+chart_type+'/'+country
            try:
                test6.createChart(data_file_name,image_path,chart_type,data_start=5)
            except:
                try:
                    data_file_name = "data/country-data-berkley-earth/processed/" + country + " - AnnTemp 1901-2015.csv"
                    test6.createChart(data_file_name,image_path,chart_type,data_start=5)
                except:
                    print("----------error: "+data_file_name)
        test6.createChart("data/USA 2022.csv","US",chart_type)

class county_images:
    def generate(chart_type="stripes"):
        f = open('data/list of US counties.csv', "r")
        csv_f = csv.reader(f)

        list_of_counties = []
        for row in csv_f:
            list_of_counties.append(row)

        for row in list_of_counties:
            data_file_name = "data/us-county-data-NOAA/2022/" + globals.getStateAbrev(row[0][-2:]) + "/"+row[0]+" - AnnTemp 1895-2022.csv"

            image_path = 'results/'+chart_type+'/US/'+row[0][-2:]+"/"+row[0]
            try:
                test6.createChart(data_file_name,image_path,chart_type,data_start=15)
            except Exception as e:
                print("----------error:",data_file_name,e)

class foreign_province_images:
    provinces_to_download = ["Acre", "Adygey", "Aga Buryat", "Alagoas", "Alberta", "Altay", "Amapá", "Amazonas", "Amur", "Andaman and Nicobar", "Andhra Pradesh", "Anhui", "Arkhangel'sk", "Arunachal Pradesh", "Assam", "Astrakhan'", "Australian Capital Territory", "Bahia", "Bashkortostan", "Beijing", "Belgorod", "Bihar", "British Columbia", "Bryansk", "Buryat", "Ceará", "Chandigarh", "Chechnya", "Chelyabinsk", "Chhattisgarh", "Chita", "Chongqing", "Chukot", "Chuvash", "City of St. Petersburg", "Dadra and Nagar Haveli", "Dagestan", "Daman and Diu", "Delhi", "Distrito Federal", "Espírito Santo", "Evenk", "Fujian", "Gansu", "Goa", "Goiás", "Gorno-Altay", "Guangdong", "Guangxi", "Guizhou", "Gujarat", "Hainan", "Haryana", "Hebei", "Heilongjiang", "Henan", "Himachal Pradesh", "Hubei", "Hunan", "Ingush", "Irkutsk", "Ivanovo", "Jammu and Kashmir", "Jharkhand", "Jiangsu", "Jiangxi", "Jilin", "Kabardin-Balkar", "Kaliningrad", "Kalmyk", "Kaluga", "Kamchatka", "Karachay-Cherkess", "Karelia", "Karnataka", "Kemerovo", "Kerala", "Khabarovsk", "Khakass", "Khanty-Mansiy", "Kirov", "Komi", "Komi-Permyak", "Koryak", "Kostroma", "Krasnodar", "Krasnoyarsk", "Kurgan", "Kursk", "Leningrad", "Liaoning", "Lipetsk", "Madhya Pradesh", "Maga Buryatdan", "Maharashtra", "Manipur", "Manitoba", "Maranhão", "Mariy-El", "Mato Grosso", "Mato Grosso do Sul", "Meghalaya", "Minas Gerais", "Mizoram", "Mordovia", "Moscow City", "Moskva", "Murmansk", "Nagaland", "Nei Mongol", "Nenets", "New Brunswick", "New South Wales", "Newfoundland and Labrador", "Ningxia Hui", "Nizhegorod", "North Ossetia", "Northern Territory", "Northwest Territories", "Nova Scotia", "Novgorod", "Novosibirsk", "Nunavut", "Omsk", "Ontario", "Orel", "Orenburg", "Orissa", "Pará", "Paraíba", "Paraná", "Penza", "Perm'", "Pernambuco", "Piauí", "Primor'ye", "Prince Edward Island", "Pskov", "Puducherry", "Punjab", "Qinghai", "Québec", "Queensland", "Rajasthan", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Rostov", "Ryazan'", "Sakha", "Sakhalin", "Samara", "Santa Catarina", "São Paulo", "Saratov", "Saskatchewan", "Sergipe", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan", "Sikkim", "Smolensk", "South Australia", "Stavropol'", "Sverdlovsk", "Tambov", "Tamil Nadu", "Tasmania", "Tatarstan", "Taymyr", "Tianjin", "Tocantins", "Tomsk", "Tripura", "Tula", "Tuva", "Tver'", "Tyumen'", "Udmurt", "Ul'yanovsk", "Ust-Orda Buryat", "Uttar Pradesh", "Uttaranchal", "Victoria", "Vladimir", "Volgograd", "Vologda", "Voronezh", "West Bengal", "Western Australia", "Xinjiang Uygur", "Xizang", "Yamal-Nenets", "Yaroslavl'", "Yevrey", "Yukon", "Yunnan", "Zhejiang"]
    countries_that_provinces_are_in = ["Brazil","Russia","Russia","Brazil","Canada","Russia","Brazil","Brazil","Russia","India","India","China","Russia","India","India","Russia","Australia","Brazil","Russia","China","Russia","India","Canada","Russia","Russia","Brazil","India","Russia","Russia","India","Russia","China","Russia","Russia","Russia","India","Russia","India","India","Brazil","Brazil","Russia","China","China","India","Brazil","Russia","China","China","China","India","China","India","China","China","China","India","China","China","Russia","Russia","Russia","India","India","China","China","China","Russia","Russia","Russia","Russia","Russia","Russia","Russia","India","Russia","India","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","Russia","China","Russia","India","Russia","India","India","Canada","Brazil","Russia","Brazil","Brazil","India","Brazil","India","Russia","Russia","Russia","Russia","India","China","Russia","Canada","Australia","Canada","China","Russia","Russia","Australia","Canada","Canada","Russia","Russia","Canada","Russia","Canada","Russia","Russia","India","Brazil","Brazil","Brazil","Russia","Russia","Brazil","Brazil","Russia","Canada","Russia","India","India","China","Canada","Australia","India","Brazil","Brazil","Brazil","Brazil","Brazil","Russia","Russia","Russia","Russia","Russia","Brazil","Brazil","Russia","Canada","Brazil","China","China","China","China","China","India","Russia","Australia","Russia","Russia","Russia","India","Australia","Russia","Russia","China","Brazil","Russia","India","Russia","Russia","Russia","Russia","Russia","Russia","Russia","India","India","Australia","Russia","Russia","Russia","Russia","India","Australia","China","China","Russia","Russia","Russia","Canada","China","China"]

    def getStateCountry(state):
        return foreign_province_images.countries_that_provinces_are_in[foreign_province_images.provinces_to_download.index(state)]

    def generate(chart_type="stripes"):
        for province in foreign_province_images.provinces_to_download:
            data_file_name = "data/state-province-data/processed/" + province + " - AnnTemp 1901-2020.csv"

            country_code = globals.getCountryCode(foreign_province_images.getStateCountry(province))
            countries_with_province_abbrev = ['AU','BR','CA','IN'] #countries that google maps and mapbox return province code with
            if globals.getCountryCode(foreign_province_images.getStateCountry(province)) in countries_with_province_abbrev:
                province = globals.getProvinceAbrev(province)

            image_path = 'results/'+chart_type+'/'+country_code+'/'+province
            try:
                test6.createChart(data_file_name,image_path,chart_type,data_start=5)
            except:
                try:
                   data_file_name = "data/state-province-data/processed/" + province + " - AnnTemp 1901-2015.csv"
                   test6.createChart(data_file_name,image_path,chart_type,data_start=5)
                except:
                    print("----------error: "+data_file_name)

            #TODO: figure out what to do with countries that have data only to 2015

class earth_images:
    def generate(chart_type="light-labeled-bars"):
        try:
            test6.createChart("data/hadcrut_dataset.csv","results/" + chart_type + "/location/earth",chart_type,globe=True,data_start=15)
        except:
            print("----------error: data/hadcrut_dataset.csv")

# creates chart of location for all image types
CHART_TYPES = ["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg","light-labeled-bars","large-square-stripes"]
def create_charts_from_data(data_file,location_id,data_start=15,chart_types=CHART_TYPES):
    for chart_type in chart_types:
        test6.createChart(data_file,"results/"+chart_type+"/"+location_id,chartType=chart_type,save=True,data_start=data_start)

# creates chart of image type for all locations
def create_charts_for_image_type(image_type: str):
    us_state_images.generate(image_type)
    country_images.generate(image_type)
    foreign_province_images.generate(image_type)
    county_images.generate(image_type)
    earth_images.generate(image_type)
    print("----------finished creating charts for image type: "+image_type)

def create_all_images():
    for chart in CHART_TYPES:
        create_charts_for_image_type(chart)

if __name__ == "__main__":
    start_time = datetime.now()

    create_all_images()

    #for chart in ["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg","light-labeled-bars"]:
    #    create_province_state_images.main(chart)
    #create_charts_for_image_type("light-labeled-bars")
    #createChartsFromData("data/hadcrut_dataset.csv","location/earth")
    #createChartsFromData("data/country-data-berkley-earth/processed/IT - AnnTemp 1901-2020.csv","IT",5)
    #createChartsFromData("data/USA 2022.csv","US")
    #create_charts_for_image_type("svg")
    #create_charts_for_image_type("large-square-stripes")

    end_time = datetime.now()
    time_delta = end_time - start_time
    print("Start Time: ", start_time.strftime("%H:%M:%S"))
    print("End Time: ", end_time.strftime("%H:%M:%S"))
    print("Time Delta: ", time_delta)