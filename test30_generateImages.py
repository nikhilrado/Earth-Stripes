import test13_create_county_images
import test25_create_state_images
import test18_create_country_images
import test42_create_province_state_images
import test6
from datetime import datetime

now = datetime.now()

test13_create_county_images.main("stripes")
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


test6.createChart("data/USA.csv","results/label/US",chartType="label")
test6.createChart("data/USA.csv","results/labeled-bars/US",chartType="labeled-bars")
test6.createChart("data/USA.csv","results/labeled-stripes/US",chartType="labeled-stripes")
test6.createChart("data/USA.csv","results/snap-sticker/US",chartType="snap-sticker")
test6.createChart("data/USA.csv","results/stripes/US",chartType="stripes")
test6.createChart("data/USA.csv","results/twitter-card/US",chartType="twitter-card")

current_time = now.strftime("%H:%M:%S")
print("Time Finished =", current_time)