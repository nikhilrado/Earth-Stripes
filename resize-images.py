import os
from PIL import Image
import globals

def cropAndResizeSenatorImages(filepath,savepath):
    # Opens a image in RGB mode
    im = Image.open(filepath)
    ogSizeKB = os.path.getsize(filepath)/1000
    
    # Size of the image in pixels (size of original image)
    width, height = im.size
    
    #resizes the image to be square positioned at the top, and crops it
    #mimics the original css croping, so we don't have to have the cropped part in the image file
    left,top,right,bottom = 0,0,width,width

    im1 = im.crop((left, top, right, bottom))
    im1 = im1.resize((200, 200))

    #saves image and creates directory if it doesn't exist
    if not(os.path.isdir(os.path.dirname(savepath))):
        os.makedirs(os.path.dirname(savepath))
    im1.save(savepath,quality=95)
    
    #collects and prints image stats
    newSizeKB = os.path.getsize(savepath)/1000
    percentSavings = round(((ogSizeKB-newSizeKB)/ogSizeKB)*100)
    print("Resized: %s Size: %iKB to %iKB -- %i%% savings" % (filepath,ogSizeKB,newSizeKB,percentSavings))

    #im1.show()


for photo in globals.getAllFilesInDir("photos/senators"):
    savePath = photo.replace("/","/compressed/")
    cropAndResizeSenatorImages(photo,savePath)