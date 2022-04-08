from es_secrets import s3
import boto3
import os
import json
from datetime import datetime
import csv
import sys

# This file handles uploading of all files to s3

# declaration of basic variables
RESULTS_DIRECTORY = "../Earth Stripes Codebase/results/"
LOG_FILE = "../Earth Stripes Codebase/s3upload-log.csv"
S3_PUT_COST = 0.005/1000
S3_UPLOAD_BUCKET = "earthstripes"
client = boto3.client('s3', aws_access_key_id=s3.access_key, aws_secret_access_key=s3.secret_access_key)

# returns a list of all files in a directory
def getAllFilesInDir(root):
    fileList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            fileList.append(os.path.join(path, name))
    return fileList

# will upload a file to s3 and print a statement stating which file was uploaded
def uploadFile(file,uploadFilePath=False):
    # lets the user specify if they want to add a custom file path
    if uploadFilePath == False:
        upload_file_path = "v3/" + file.replace(RESULTS_DIRECTORY,"")
    else:
        upload_file_path = uploadFilePath
    
    contentType = "txt"
    if '.png' in file:
        contentType = 'image/png'
    if '.jpg' in file:
        contentType = 'image/jpg'
    if '.json' in file:
        contentType = 'application/json'
    if '.xml' in file:
        contentType = 'text/xml'
    if '.csv' in file:
        contentType = 'text/csv'
    if '.html' in file:
        contentType = 'text/html'
    if '.js' in file:
        contentType = 'application/javascript'
    if '.css' in file:
        contentType = 'text/css'
    client.upload_file(file, S3_UPLOAD_BUCKET, upload_file_path,ExtraArgs={'ACL':'public-read', "ContentType":contentType})
    print("Uploaded: "+ file +" --to-- "+S3_UPLOAD_BUCKET+"/"+upload_file_path)


# allowed us to add a object to all the json files-----------------
'''import createJSON
for file in getAllFilesInDir("results/json"):
    createJSON.updateMetadata(file,"")'''

# find the type of file from the directory (ex. bars, json, stripes)
# sorts list by length, so it will recognize labeled versions
# https://www.geeksforgeeks.org/python-sort-list-according-length-elements/
def sorting(lst):
    lst2 = sorted(lst, key=len)
    return lst2

resourceTypes = sorting(os.listdir(RESULTS_DIRECTORY))
resourceTypes.reverse()
#print(resourceTypes)
def getFileType(filePath):
    for resourceType in resourceTypes:
        if resourceType in filePath:
            return resourceType

# when run it will upload all files in a directory to s3, if smartUpload is "True", it will only upload files that have been changed since last upload
def uploadNewChanges(directory=RESULTS_DIRECTORY,smartUpload=True, exclude=[]):
    # opens the log file
    f = open(LOG_FILE,"r")
    csv_f = csv.reader(f)
    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    # sets variables from log file
    lastUpload = rowsList[1][0]
    costToDate = float(rowsList[1][-1])
    savingsToDate = float(rowsList[1][-3])
    lastUpload = datetime.strptime(lastUpload, '%Y-%m-%d %H:%M:%S.%f')
    dateTimeStart = str(datetime.now())

    # counters, metrics and analytics
    itemsProcessed = 0
    numUploaded = 0

    # will loop through all of the files
    for file in getAllFilesInDir(directory):
        #if the file is not in the exclude list
        exclude.append("desktop.ini")
        uploadFlag = True
        for ex in exclude:
            if ex in file:
                print("skipping: "+file)
                uploadFlag = False
                break
        if not uploadFlag:
            continue
        file = file.replace("\\","/")  # fixes annoying formating issue that messes up s3
        itemsProcessed += 1

        # if this is a smart upload then, read the json file, and determine if it needs to be uploaded
        if smartUpload:
            fileType = getFileType(file)
            jsonFile = file.replace(fileType,"json").replace(".png",".json").replace(".jpeg",".json")
            f = open(jsonFile)
            f = f.read()
            f = json.loads(f)
            #print(f)

            # find the date in the json file, if no date is present, skip file 
            try:
                lastUpdated = f["resources"][fileType]["last updated"]
                lastUpdated = datetime.strptime(lastUpdated, '%Y-%m-%d %H:%M:%S.%f')
                if lastUpload < lastUpdated:
                    uploadFile(file)
                    numUploaded += 1
            except:
                continue
        # when smartUpload isn't true, just upload everything
        else:
            uploadFile(file)
            numUploaded += 1
        

    # open up the log file, and record data from the day's upload
    with open(LOG_FILE, 'w', newline="") as f:
        # using csv.writer method from CSV package
        # ['dateTimeStart', 'dateTimeFinish', 'numUploaded', 'numFailed', 'cost', '', 'smartUpload', 'itemsProcessed', 'itemsSaved', 'initialCost', 'smartCost', 'savings', 'savingsToDate' ,'costToDate']
        cost = S3_PUT_COST*numUploaded
        savings = S3_PUT_COST*itemsProcessed-S3_PUT_COST*numUploaded
        uploadLogData = [dateTimeStart, str(datetime.now()), numUploaded,"?",cost,"-",smartUpload,itemsProcessed,itemsProcessed-numUploaded,S3_PUT_COST*itemsProcessed,S3_PUT_COST*numUploaded,savings,savingsToDate+savings,costToDate+cost]
        rowsList.insert(1,uploadLogData)

        write = csv.writer(f)
        write.writerows(rowsList)
        print(uploadLogData)


def test():
    #uploadNewChanges()
    #uploadFile("results/sunny.png")
    #uploadNewChanges(directory="results/json/US/",smartUpload=False)
    #uploadNewChanges(directory="results/",smartUpload=False)
    #uploadNewChanges(directory="photos/local-impact-photos/",smartUpload=False)
    uploadNewChanges(directory="results/stripes-svg/",smartUpload=False)
    #uploadFile("Site Files/map-page/countries2.js", uploadFilePath="map-stuff.js")
    #uploadFile("Map Stuff/mapData.csv",uploadFilePath="mapData2.csv")
    #uploadFile("test5.svg",uploadFilePath="test5.svg")
    #uploadFile("results/json/US.json",uploadFilePath="v3/json/US.json")
    uploadAll("../Earth Stripes Codebase/results/stripes/US.png")
    pass

# method to upload all of the image/file types to s3 by inputting the stripes file
def uploadAll(file,chartTypes=["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg"]):
    for chartType in chartTypes:
        if not "svg" in chartType:
            uploadFile(file.replace("/stripes/","/"+chartType+"/"),uploadFilePath="v3/"+file.replace("/stripes/","/"+chartType+"/").replace("results/",""))
        else:
            uploadFile("results/"+chartType+".svg",uploadFilePath=chartType+".svg")

# this is the main function that will be called when the script is run
# if the file is imported, it will not run the test function
# test method is created to remove global scope of any variables in test()
if __name__ == "__main__":
    test()