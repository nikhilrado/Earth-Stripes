import csv
import globals
import manageJSON

# opens the file from the eia website
# go to link then select options, then select consumption and production for all countries
# https://www.eia.gov/international/data/world/total-energy/total-energy-consumption

# converts a string of 2d array to a 2d array
def string_to_2d_array(string):
    string = string[2:-2].split("],[")
    return_list = []
    for row in string:
        row = row.split(",")
        if len(row) != 0:
            for i in range(len(row)):
                row[i] = int(row[i])
            return_list.append(row)

    return return_list

def str_to_data_type(string):
    if string.isnumeric():
        return int(string)
    try:
        return float(string)
    except:
        return string

def do_states():
    f = open("../Earth Stripes Codebase/data/national-risk-index/NRI_Table_States.csv", encoding='utf-8-sig')
    # opens file and puts data into list
    csv_f = csv.reader(f)

    all_energy_data = []
    for row in csv_f:
        all_energy_data.append(row)

    headers = all_energy_data.pop(0)
    #print(headers)
    for row in all_energy_data:
        state_name = row[2]
        json_template = {}
        for i in range(1,len(headers)):
            label = headers[i]
            value = row[i]

            if label == 'install_size_kw_buckets_json':
                value = string_to_2d_array(value)
            else:
                value = str_to_data_type(value)

            json_template[label] = value
        #print(json_template)
        try:
            manageJSON.updateDataObjet("results/json/US/"+globals.getStateAbrev(state_name)+".json", "national_risk_index", json_template)
            #print("updated: " + state_name)
            pass
        except Exception as e:
            print("Error updating json for state: " + state_name + " (" + str(e) + ")")
            continue

def do_counties():
    f = open("../Earth Stripes Codebase/data/national-risk-index/NRI_Table_Counties.csv", encoding='utf-8-sig')
    # opens file and puts data into list
    csv_f = csv.reader(f)

    all_energy_data = []
    for row in csv_f:
        all_energy_data.append(row)

    headers = all_energy_data.pop(0)
    #print(headers)
    for row in all_energy_data:
        county_name = row[5] + " " + row[6]
        state_name = row[2]
        json_template = {}
        for i in range(1,len(headers)):
            label = headers[i]
            value = row[i]
            try: 
                if label == 'install_size_kw_buckets_json':
                    value = string_to_2d_array(value)
                else:
                    value = str_to_data_type(value)
            except:
                continue

            json_template[label] = value
        #print(json_template)
        try:
            state_abrev = globals.getStateAbrev(state_name)
            manageJSON.updateDataObjet("results/json/US/"+state_abrev+"/"+county_name+" "+state_abrev+".json", "national_risk_index", json_template)
            #print("updated: " + county_name + state_name)
        except Exception as e:
            print("Error updating json for state: " + state_name + " (" + str(e) + ")")
            continue

do_states()
do_counties()