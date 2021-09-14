import requests
from globals import stateShortName, getStateAbrev
import manageJSON

#this is a quick program that downloads data from Climate Central's "States at Risk Report"
#used with permission

#removes any html tags like <p> from a string
def removeHTMLTags(code):
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

#main method that downloads and cleans the data
def getStatesAtRiskData(state):

    #gets the full state name and formats it for url
    state = getStateAbrev(state)
    state = state.replace(" ","-")

    URL = "http://reportcard.statesatrisk.org/report-card/" + state
    print(URL)
    page = requests.get(URL, verify=False) #no SSL required cause content was on unsecure origin when program written

    #cleans up the page's html and puts it in a list
    pageText = page.text.split('\n')
    pageText2 = []
    for line in pageText:
        pageText2.append(line.strip())

    #will extract the tags <p> where the paragraphs are
    #will extract the <span> tags that contain the scores
    paragraphList = []
    scoreList = []
    passed = False
    for line in pageText2:
        if line == "<!--page title-->" or passed == True:
            if "<p>" in line:
                paragraphList.append(removeHTMLTags(line))
            if "<span>" in line:
                if removeHTMLTags(line) == "NA":
                    line = "N/A"
                scoreList.append(removeHTMLTags(line))
            passed = True
    
    print(scoreList)
    print(paragraphList)
    if len(scoreList) == 11: #some states have extra infographic data which we remove
        scoreList.pop(3)

    if (len(paragraphList) != 6):
        print("--------error: more or less than 6 <p> tags found")
        raise Exception("--------error: more or less than 6 <p> tags found")
    if (len(scoreList) != 10):
        print("--------error: more or less than 10 span tags found")
        raise Exception("--------error: more or less than 10 <span> tags found")

    #removes excess information
    scoreList.pop(0)
    scoreList.pop(1)
    scoreList.pop(-2)
    scoreList.pop(-1)
    stateOverallRating = removeHTMLTags(scoreList[0])


    #print(stateOverallRating)
    return(scoreList,paragraphList)

def createStatesAtRiskJSON(scoreList,paragraphList,state):
    y = {
        "statesAtRisk": {
            "Overall": {
                "score": scoreList[0],
                "paragraph": paragraphList[0]
            },
            "Extreme Heat": {
                "score": scoreList[1],
                "paragraph": paragraphList[1]
            },
            "Drought": {
                "score": scoreList[2],
                "paragraph": paragraphList[2]
            },
            "Wildfires": {
                "score": scoreList[3],
                "paragraph": paragraphList[3]
            },
            "Inland Flooding": {
                "score": scoreList[4],
                "paragraph": paragraphList[4]
            },
            "Costal Flooding": {
                "score": scoreList[5],
                "paragraph": paragraphList[5]
            }

        }
    }
    manageJSON.updateDataObjet("results/json/US/%s.json" % state,"statesAtRisk",y["statesAtRisk"])


#getStatesAtRiskData("WA")
errorList = []
for state in stateShortName:
    try:
        data = getStatesAtRiskData(state)
        createStatesAtRiskJSON(data[0],data[1],state)
    except:
        print("-----------Error: "+state)
        errorList.append("-----------Error: "+state)

for error in errorList:
    print(error)
    
