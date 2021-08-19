import os.path
import csv
import test6

#convert between long or short name of the state
stateFullName = ["County","Washington D.C.","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
stateShortName = ["ty","DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
def getStateAbrev(state):
    if len(state) == 2:
        return stateFullName[stateShortName.index(state)]
    return stateShortName[stateFullName.index(state)]

def main(chartType="bars"):
    f = open('data/list of US counties.csv', "r")
    csv_f = csv.reader(f)

    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    #print(rowsList)

    for row in rowsList:
        #if row[0] == "County" or row[1]!="complete2":
        #    continue
        dataFileName = "data/us-county-data-NOAA/" + getStateAbrev(row[0][-2:]) + "/"+row[0]+" - AnnTemp 1895-2020.csv"
        
        #https://stackoverflow.com/questions/1274405/how-to-create-new-folder #https://stackoverflow.com/a/1274465
        newpath = 'results/'+chartType+'/US/'+row[0][-2:] 
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        imagePath = 'results/'+chartType+'/US/'+row[0][-2:]+"/"+row[0]
        try:
            test6.createChart(dataFileName,imagePath,chartType)
        except:
            print("----------error: "+dataFileName)
            continue
        #test6.createChart(fileName,imagePath,chartType)


main("stripes")

