import urllib.request
import os

#create a function to request an image from the web and save it to a file
#the function takes two arguments, the url and the filename
def saveWebImage(url, filename):
    #open a connection to the web server
    connection = urllib.request.urlopen(url)
    #read the data from the connection
    data = connection.read()
    #write the data to a file
    with open(filename, "wb") as file:
        file.write(data)


saveWebImage("https://earthstripes.s3.us-east-2.amazonaws.com/v3/stripes/PK.png", "promotion/python.png")

"https://rlv.zazzle.com/svc/view?pid=168540946485519042&max_dim=600&at=238391408801122257&t_stripes_url=https://earthstripes.s3.us-east-2.amazonaws.com/v3/stripes/PK.png?request=zazzle&t_labeledstripes_url=https://earthstripes.s3.us-east-2.amazonaws.com/v3/labeled-stripes/PK.png?request=zazzle"

"https://rlv.zcache.com/svc/view?realview=113236100541059671&design=f40c5ae9-d905-4a11-80ca-a0b58c68ccbe&rlvnet=1&style=combo_mug&color=navyblue&size=11oz&addon=none&max_dim=2000"

def saveMugImages(designID, locationName):
    maxDim = 500
    mugColors = ["navyblue", "red", "green", "yellow", "orange", "pink", "black", "maroon", "lightblue", "lime"]
    mugSizes = ["11oz", "15oz"]
    #create directory if it doesn't exist
    if not os.path.exists("promotion/"+locationName + "/mugs"):
        os.makedirs("promotion/"+locationName + "/mugs")

    for color in mugColors:
        saveWebImage("https://rlv.zcache.com/svc/view?realview=113236100541059671&design=" + designID + "&rlvnet=1&style=combo_mug&color=" + color + "&size=11oz&addon=none&max_dim=" + str(maxDim), "promotion/"+locationName+"/mugs/" + locationName + "_mug_" + color + ".png")

def saveTieImages(designID, locationName):
    images = ["113054760991432759","113344814997928302","113445645434204735", "113374635533120632", "113358413879803726"]
    imageName = ["front", "back", "rolled", "tied", "in-situ"]

    #create directory if it doesn't exist
    if not os.path.exists("promotion/"+locationName + "/ties"):
        os.makedirs("promotion/"+locationName + "/ties")

    for i in range(len(images)):
        print("https://rlv.zcache.com/svc/view?realview=" + images[i] + "&design=" + designID + "&rlvnet=1&style=standard_tie&max_dim=500")
        saveWebImage("https://rlv.zcache.com/svc/view?realview=" + images[i] + "&design=" + designID + "&rlvnet=1&style=standard_tie&max_dim=500&t_stripes_iid=a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8", "promotion/"+locationName+"/ties/" + locationName + "_tie_" + imageName[i] + ".png")

#https://rlv.zcache.com/svc/view?realview=113358413879803726&design=a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8&rlvnet=1&style=standard_tie&max_dim=704&t_stripes_iid=a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8
#https://rlv.zcache.com/svc/view?realview=113054760991432759&design=a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8&rlvnet=1&style=standard_tie&max_dim=500
saveTieImages("f40c5ae9-d905-4a11-80ca-a0b58c68ccbe", "Phillipines")
"a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8"
"a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8"
"a1e7ef9c-e7e9-4d20-9631-6e518d0f1ac8"