# this program takes the data from the Yale Climate Opinion Survey and places it in the respective JSON files
import csv
import sys
sys.path.insert(0, '../Earth Stripes Codebase')
import globals
import manageJSON

RESULTS_DIR = "../Earth Stripes Codebase/results/json/"
YCOM_DATA_FILE = '../Earth Stripes Codebase/data/yale-climate/YCOM_2021_Data.csv'
YCOM_DATA_YEAR = "2021"

# intercepts function for globals.py to accommodate dif DC naming convention
def get_state_abbrev(state):
    if state == "District of Columbia":
        return "DC"
    if state == "DC":
        return "District of Columbia"
    return globals.getStateAbrev(state)

# gets the resource ID of the file by seeing what location category the yale data belongs to
def get_resource_id_from_yale(row):
    if row[0] == "County":
        county = row[2].split(",")[0]
        state_code = get_state_abbrev(row[2].split(",")[1].strip())
        return "US/"+state_code+"/"+county+" "+state_code
    if row[0] == "State":
        return "US/" + get_state_abbrev(row[2])
    if row[0] == "National":
        return row[2]
    return None

with open(YCOM_DATA_FILE, "r") as file:
    rows_list = list(csv.reader(file))
data_headers = rows_list.pop(0)  # sets first row as headers and removes it

# loops through csv to translate the data
for i, row in enumerate(rows_list):
    if len(data_headers) != len(row):  # just a check to make sure the row has all data
        raise Exception("Potentially missing data: row length does not match header length for row "+str(i+1))

    # template JSON/python dict
    json_data = {
        "YaleClimateOpinionData": {
            "metadata": {
                "source": 'Howe, Peter D., Matto Mildenberger, Jennifer R. Marlon, and Anthony Leiserowitz (2015). "Geographic variation in opinions on climate change at state and local scales in the USA." Nature Climate Change, doi:10.1038/nclimate2583',
                "disclaimer": "The YPCCC bears no responsibility for the analyses or interpretations of the data presented here.",
                "year": YCOM_DATA_YEAR
            },
            # translates YCOM csv data structure to our json via dictionary comprehension
            "data": {key_name: value for key_name, value in zip(data_headers, row)}
        }
    }
    
    json_file = RESULTS_DIR + get_resource_id_from_yale(row) + ".json"
    try:
        manageJSON.updateDataObjet(json_file, "YaleClimateOpinionData", json_data["YaleClimateOpinionData"])
        print(f"updated YCOM data for: {json_file}")
    except Exception as e:
        print(str(e) + f" - ({json_file})")