import os.path
import csv
import test6


#TODO get Alaska and Hawaii to work

states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

def main(chartType="bars"):
    for state in states:
        dataFileName = "data/us-state-data-NOAA/" + state + ".csv"
        
        #https://stackoverflow.com/questions/1274405/how-to-create-new-folder #https://stackoverflow.com/a/1274465
        #newpath = 'G:\.shortcut-targets-by-id/1-78WtuBsUrKVKWF1NKxPcsrf1nvacux2/AP CSP VS Code Workspace/World Data Stuff/images/'+country
        #if not os.path.exists(newpath):
        #    os.makedirs(newpath)

        

        imagePath = 'results/'+chartType+'/US/'+state
        try:
            test6.createChart(dataFileName,imagePath,chartType)
        except:
            print("----------error: "+dataFileName)
            continue


main("bars")