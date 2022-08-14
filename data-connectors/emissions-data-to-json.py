import csv, sys
sys.path.insert(0, './')
import globals
import manageJSON

# opens the file from the World Bank website
# https://data.worldbank.org/indicator/EN.ATM.CO2E.PC
f = open("../Earth Stripes Codebase/data/emissions/API_EN.ATM.CO2E.PC_DS2_en_csv_v2_4353266.csv", encoding='utf-8-sig')

# opens file and puts data into list
csv_f = csv.reader(f)

all_energy_data = []
for row in csv_f:
    all_energy_data.append(row)

# sets the header of the data which is the same for all days (then converts all to int)
years = all_energy_data[4][4:-1]
print(years)

count = 0
failed = 0
list_of_failed = []

for row in all_energy_data[5:]:
    country = row[1]
    try:
        country_code = globals.getISOconverted(country)
    except:
        failed += 1
        list_of_failed.append(country)
        continue
    data = row[4:-1]
    years_data = []
    emissions_data = []

    for i in range(len(data)):
        if data[i] == "":
            continue
        try:
            data[i] = float(data[i])
        except:
            data[i] = None

        years_data.append(years[i])
        emissions_data.append(data[i])

    container = {
        "years": years_data,
        "metric tons of co2 per capita": emissions_data
    }
    print(country_code)
    try:
        manageJSON.updateDataObjet("results/json/"+country_code+".json", "emissions", container)
    except Exception as e:
        print("Error updating json for country: " + country + " (" + str(e) + ")")
        failed += 1
        list_of_failed.append(country)

    count += 1
    print(country_code)
    print(years_data)
    print(emissions_data)


print("success: " + str(count-failed)+"/"+str(count))
print("failed: " + str(failed)+"/"+str(count))
print(list_of_failed)