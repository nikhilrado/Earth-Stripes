from venv import create
import test13_create_county_images
#import test25_create_state_images
import test18_create_country_images
import test42_create_province_state_images
import test6
from datetime import datetime
import os.path
import csv

class test25_create_state_images:

    def main(chartType="bars"):
        #TODO get Alaska and Hawaii to work
        states = ["DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
        
        for state in states:
            dataFileName = "data/us-state-data-NOAA/2021/" + state + " - AnnTemp 1895-2021.csv"
            
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

    #main("stripes")

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

test25_create_state_images.main("stripes")
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

def createChartsFromData(dataFile,locationID,chartTypes=["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg"]):
    for chartType in chartTypes:
        test6.createChart(dataFile,"results/"+chartType+"/"+locationID,chartType=chartType,save=True)

def create_charts_for_image_type(image_type: str):
    test13_create_county_images.main(image_type)
    test25_create_state_images.main(image_type)
    test18_create_country_images.main(image_type)
    test42_create_province_state_images.main(image_type)

#create_charts_for_image_type("stripes-svg")

#createChartsFromData("data/USA2021.csv","US")
current_time = now.strftime("%H:%M:%S")
print("Time Finished =", current_time)