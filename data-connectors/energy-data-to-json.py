import csv, sys
sys.path.insert(0, './')
import globals
import manageJSON

# # opens the file from the eia website
# # go to link then select options, then select consumption and production for all countries
# # https://www.eia.gov/international/data/world/total-energy/total-energy-consumption
# f = open("../Earth Stripes Codebase/data/eia-energy-consumption-production-data.csv", encoding='utf-8-sig')

# # opens file and puts data into list
# csv_f = csv.reader(f)

# all_energy_data = []
# for row in csv_f:
#     all_energy_data.append(row)

# # sets the header of the data which is the same for all days (then converts all to int)
# years = list(map(int, all_energy_data[1][2:-1]))

# count = 0
# failed = 0
# list_of_failed = []

# def country_to_json(list):
#     global count

#     country = list[0][1]
#     total_consumption = list[8][2:-1]
#     container = {
#         "energy consumption": []
#     }

#     # calculates the percent by dividing the data by the whole
#     def get_percent(data_list):
#         for i in range(len(data_list)):
#             # if there is an error (no data, or "--" in column), null will be placed in the json, which allows the chart to render
#             try:
#                 data_list[i] = round(float(data_list[i]) /
#                                     float(total_consumption[i])*100, 1)
#             except:
#                 data_list[i] = None

#         return(data_list)

#     # this is the template for the json
#     z = {
#         "years": years,
#         "total consumption": total_consumption,
#         "coal": get_percent(list[9][2:-1]),
#         "natural gas": get_percent(list[10][2:-1]),
#         "petroleum and other liquids": get_percent(list[11][2:-1]),
#         "nuclear": get_percent(list[13][2:-1]),
#         "renewables and others": get_percent(list[14][2:-1]),
#     }

#     # adds the data to its container then prints it, along with the country
#     container["energy consumption"].append(z)
#     count += 1
#     print(country + " " + str(count))
#     #print(json.dumps(container, indent=2))

#     # gets the country's country code from the globals file, then adds the data to the country's json file
#     try:
#         countryCode = globals.getCountryCode(country)
#     except:
#         three_letter_country_code = list[1][0].split("-")[2]
#         print(three_letter_country_code)
#         countryCode = globals.getISOconverted(three_letter_country_code)
#     manageJSON.updateDataObjet("results/json/"+countryCode+".json", "energy consumption", z)
#     # manageJSON.updateDataObjet("JSON stuff/AZtest.json","energy consumption",z) #use for testing


# # chops off last two years because data wasn't reliable
# rows_list_data = all_energy_data[2:]
# for k in range(len(rows_list_data)):
#     row = rows_list_data[k]

#     data_for_one_country_list = []
#     # just checks to make sure data is in increments of 15
#     if row[0] == "":
#         for j in range(15):
#             data_for_one_country_list.append(rows_list_data[k+j])
#         try:
#             country_to_json(data_for_one_country_list)
#         except:
#             failed += 1
#             list_of_failed.append(data_for_one_country_list[0][1])
#             pass

# print("success: " + str(count-failed)+"/"+str(count))
# print("failed: " + str(failed)+"/"+str(count))
# print(list_of_failed)

class country_electricity_consumption:
    # opens the file from the eia website
    # go to link then select options, then select consumption and production for all countries
    # https://www.eia.gov/international/data/world/total-energy/total-energy-consumption
    f = open("../Earth Stripes Codebase/data/eia/eia-electricity-consumption-2022.csv", encoding='utf-8-sig')

    # opens file and puts data into list
    csv_f = csv.reader(f)

    all_energy_data = []
    for row in csv_f:
        all_energy_data.append(row)

    # sets the header of the data which is the same for all days (then converts all to int)
    years = list(map(int, all_energy_data[1][2:]))

    count = 0
    failed = 0
    list_of_failed = []

    def csv_to_json(csv):
        temp = {}
        for row in csv:
            temp[row[1]] = row[2]
        return temp



    def country_json_to_json(data):
        # calculates the percent by dividing the data by the whole
        def get_percent(data_list, total_consumption_list):
            for i in range(len(data_list)):
                # if there is an error (no data, or "--" in column), null will be placed in the json, which allows the chart to render
                try:
                    data_list[i] = round(float(data_list[i]) /
                                        float(total_consumption_list[i])*100, 1)
                except:
                    data_list[i] = None

            return(data_list)

        global count
        container = {
            "energy consumption": []
        }

        # this is the template for the json
        z = {
            "years": country_electricity_consumption.years,
            "total consumption": data["    Generation (billion kWh)"],
            "nuclear": get_percent(data["Nuclear"], data["    Generation (billion kWh)"]),
            "coal": get_percent(data),
            "natural gas": get_percent(data[10][2:-1]),
            "petroleum and other liquids": get_percent(data[11][2:-1]),
            "nuclear": get_percent(data[13][2:-1]),
            "renewables and others": get_percent(data[14][2:-1]),
        }

    def country_to_json(list):

        country = list[0][1]
        total_consumption = list[8][2:-1]
        container = {
            "energy consumption": []
        }



        # this is the template for the json
        z = {
            "years": years,
            "total consumption": total_consumption,
            "coal": get_percent(list[9][2:-1]),
            "natural gas": get_percent(list[10][2:-1]),
            "petroleum and other liquids": get_percent(list[11][2:-1]),
            "nuclear": get_percent(list[13][2:-1]),
            "renewables and others": get_percent(list[14][2:-1]),
        }

        # adds the data to its container then prints it, along with the country
        container["energy consumption"].append(z)
        count += 1
        print(country + " " + str(count))
        #print(json.dumps(container, indent=2))

        # gets the country's country code from the globals file, then adds the data to the country's json file
        try:
            countryCode = globals.getCountryCode(country)
        except:
            three_letter_country_code = list[1][0].split("-")[2]
            print(three_letter_country_code)
            countryCode = globals.getISOconverted(three_letter_country_code)
        # manageJSON.updateDataObjet("results/json/"+countryCode+".json", "energy consumption", z)
        # manageJSON.updateDataObjet("JSON stuff/AZtest.json","energy consumption",z) #use for testing


    # chops off last two years because data wasn't reliable
    rows_list_data = all_energy_data #[2:]
    for k in range(len(rows_list_data)):
        row = rows_list_data[k]

        data_for_one_country_list = []
        # just checks to make sure data is in increments of 15
        if row[0] == "":
            for j in range(15):
                data_for_one_country_list.append(rows_list_data[k+j])
            try:
                print(csv_to_json(data_for_one_country_list))
            except:
                failed += 1
                list_of_failed.append(data_for_one_country_list[0][1])
                pass

    print("success: " + str(count-failed)+"/"+str(count))
    print("failed: " + str(failed)+"/"+str(count))
    print(list_of_failed)