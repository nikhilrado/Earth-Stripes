import test13_create_county_images
import test25_create_state_images
import test18_create_country_images
import test42_create_province_state_images
import test6
from datetime import datetime

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
#test42_create_province_state_images.main("stripes-svg")
"""
test25_create_state_images.main("stripes")
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

createChartsFromData("data/USA2021.csv","US")
current_time = now.strftime("%H:%M:%S")
print("Time Finished =", current_time)