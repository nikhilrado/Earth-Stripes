import requests
from globals import state_short_name, getStateAbrev
import manageJSON

# this is a quick program that downloads data from Climate Central's "States at Risk Report"
# used with permission

# removes any html tags like <p> from a string
def remove_html_tags(code):
    remove = False
    code2 = ""
    for char in code:
        if char == "<":
            remove = True
        if not(remove):
            code2 = code2 + char
        if char == ">":
            remove = False
    return code2

# main method that downloads and cleans the data


def get_states_at_risk_data(state):

    # gets the full state name and formats it for url
    state = getStateAbrev(state)
    state = state.replace(" ", "-")

    URL = "http://reportcard.statesatrisk.org/report-card/" + state
    print(URL)
    # no SSL required cause content was on unsecure origin when program written
    page = requests.get(URL, verify=False)

    # cleans up the page's html and puts it in a list
    page_text = page.text.split('\n')
    page_text2 = []
    for line in page_text:
        page_text2.append(line.strip())

    # will extract the tags <p> where the paragraphs are
    # will extract the <span> tags that contain the scores
    paragraph_list = []
    score_list = []
    passed = False
    for line in page_text2:
        if line == "<!--page title-->" or passed == True:
            if "<p>" in line:
                paragraph_list.append(remove_html_tags(line))
            if "<span>" in line:
                if remove_html_tags(line) == "NA":
                    line = "N/A"
                score_list.append(remove_html_tags(line))
            passed = True

    print(score_list)
    print(paragraph_list)
    if len(score_list) == 11:  # some states have extra infographic data which we remove
        score_list.pop(3)

    if (len(paragraph_list) != 6):
        print("--------error: more or less than 6 <p> tags found")
        raise Exception("--------error: more or less than 6 <p> tags found")
    if (len(score_list) != 10):
        print("--------error: more or less than 10 span tags found")
        raise Exception(
            "--------error: more or less than 10 <span> tags found")

    # removes excess information
    score_list.pop(0)
    score_list.pop(1)
    score_list.pop(-2)
    score_list.pop(-1)
    stateOverallRating = remove_html_tags(score_list[0])

    # print(stateOverallRating)
    return(score_list, paragraph_list)


def create_states_at_risk_json(score_list, paragraph_list, state):
    y = {
        "statesAtRisk": {
            "Overall": {
                "score": score_list[0],
                "paragraph": paragraph_list[0]
            },
            "Extreme Heat": {
                "score": score_list[1],
                "paragraph": paragraph_list[1]
            },
            "Drought": {
                "score": score_list[2],
                "paragraph": paragraph_list[2]
            },
            "Wildfires": {
                "score": score_list[3],
                "paragraph": paragraph_list[3]
            },
            "Inland Flooding": {
                "score": score_list[4],
                "paragraph": paragraph_list[4]
            },
            "Costal Flooding": {
                "score": score_list[5],
                "paragraph": paragraph_list[5]
            }

        }
    }
    manageJSON.updateDataObjet("results/json/US/%s.json" %
                               state, "statesAtRisk", y["statesAtRisk"])


# getStatesAtRiskData("WA")
error_list = []
for state in state_short_name:
    try:
        data = get_states_at_risk_data(state)
        create_states_at_risk_json(data[0], data[1], state)
    except:
        print("-----------Error: "+state)
        error_list.append("-----------Error: "+state)

for error in error_list:
    print(error)