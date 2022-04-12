import os
from PIL import Image
import globals

def cropAndResizeSenatorImages(filepath,savepath,crop_dimensions=False):
    # Opens a image in RGB mode
    im = Image.open(filepath)
    ogSizeKB = os.path.getsize(filepath)/1000
    
    # Size of the image in pixels (size of original image)
    width, height = im.size
    
    #resizes the image to be square positioned at the top, and crops it
    #mimics the original css croping, so we don't have to have the cropped part in the image file
    if crop_dimensions:
        left,top,right,bottom = crop_dimensions
    else:
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


import boto3
import base64
from es_secrets import s3

def detect_faces(photo):

    client=boto3.client('rekognition', region_name='us-east-2', aws_access_key_id=s3.access_key, aws_secret_access_key=s3.secret_access_key)

    with open(photo, 'rb') as image:
        base64_image=base64.b64encode(image.read())
        base_64_binary = base64.decodebytes(base64_image)

        response = client.detect_faces(Image={'Bytes': base_64_binary}, Attributes=['ALL'])

    #print(response)

    return response['FaceDetails']


if __name__ == "__main__":
    #main()
    pass

def crop_to_center(photo,savePath,border=.12):
    im = Image.open(photo)
    data = detect_faces(photo)[0]['BoundingBox']
    width, height = im.size

    print("yeet")

    left = (data['Left'] - border) * width
    print(left)
    top = (data['Top'] - border) * height
    print(top)
    right = (data['Left'] + data['Width'] + border) * width
    print(right)
    bottom = (data['Top'] + data['Height'] + border) * height


    box_height = bottom - top
    box_width = right - left

    if box_height > box_width:
        left = left - (box_height - box_width) / 2
        right = right + (box_height - box_width) / 2
    else:
        top = top - (box_width - box_height) / 2
        bottom = bottom + (box_width - box_height) / 2
    
    cropAndResizeSenatorImages(photo,savePath,crop_dimensions=(left,top,right,bottom))


for photo in globals.getAllFilesInDir("photos/senators"):
    savePath = photo.replace("/","/compressed/")
    #cropAndResizeSenatorImages(photo,savePath)
    errors = []
    try:
        crop_to_center(photo,savePath)
    except:
        print("Error cropping: %s" % photo)
        errors.append(photo)
print(errors)