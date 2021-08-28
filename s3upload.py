from s3keys import access_key, secret_access_key
import boto3
import os
import json
from datetime import datetime
import csv

#declaration of basic variables
resultsDirectory = "results/"
logFile = "s3upload-log.csv"
s3putCost = 0.005/1000
upload_bucket = "ortana-test"
client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

#returns a list of all files in a directory
def getAllFilesInDir(root):
    fileList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            fileList.append(os.path.join(path, name))
    return fileList

#will upload a file to s3 and print a statement stating which file was uploaded
def uploadFile(file):
    upload_file_path = file.replace(resultsDirectory,"")
    if '.png' in upload_file_path:
        contentType = 'image/png'
    if '.json' in upload_file_path:
        contentType = 'application/json'
    client.upload_file(file, upload_bucket, upload_file_path,ExtraArgs={'ACL':'public-read', "ContentType":contentType})
    print("Uploaded: "+ file +" --to-- "+upload_bucket+"/"+upload_file_path)


#allowed us to add a object to all the json files-----------------
'''import createJSON
for file in getAllFilesInDir("results/json"):
    createJSON.updateMetadata(file,"")'''

#find the type of file from the directory (ex. bars, json, stripes)
#sorts list by length, so it will recognize labeled versions
#https://www.geeksforgeeks.org/python-sort-list-according-length-elements/
def sorting(lst):
    lst2 = sorted(lst, key=len)
    return lst2

resourceTypes = sorting(os.listdir(resultsDirectory))
resourceTypes.reverse()
#print(resourceTypes)
def getFileType(filePath):
    for resourceType in resourceTypes:
        if resourceType in filePath:
            return resourceType

#when run it will upload all files in a directory to s3, if smartUpload is "True", it will only upload files that have been changed since last upload
def uploadNewChanges(directory=resultsDirectory,smartUpload=True):
    #opens the log file
    f = open(logFile,"r")
    csv_f = csv.reader(f)
    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    #sets variables from log file
    lastUpload = rowsList[1][0]
    costToDate = float(rowsList[1][-1])
    savingsToDate = float(rowsList[1][-3])
    lastUpload = datetime.strptime(lastUpload, '%Y-%m-%d %H:%M:%S.%f')
    dateTimeStart = str(datetime.now())

    #counters, metrics and analytics
    itemsProcessed = 0
    numUploaded = 0

    #will loop through all of the files
    for file in getAllFilesInDir(directory):
        file = file.replace("\\","/") #fixes annoying formating issue that messes up s3
        itemsProcessed += 1

        #if this is a smart upload then, read the json file, and determine if it needs to be uploaded
        if smartUpload:
            fileType = getFileType(file)
            jsonFile = file.replace(fileType,"json").replace(".png",".json").replace(".jpeg",".json")
            f = open(jsonFile)
            f = f.read()
            f = json.loads(f)
            #print(f)

            #todo make it upload everything if no last updated object present
            #find the date in the json file, if no date is present, skip file 
            try:
                lastUpdated = f["resources"][fileType]["last updated"]
                lastUpdated = datetime.strptime(lastUpdated, '%Y-%m-%d %H:%M:%S.%f')
                if lastUpload < lastUpdated:
                    uploadFile(file)
                    numUploaded += 1
            except:
                continue
        #when smartUpload isn't true, just upload everything
        else:
            uploadFile(file)
            numUploaded += 1
        

    #open up the log file, and record data from the day's upload
    with open(logFile, 'w', newline="") as f:
        # using csv.writer method from CSV package
        #['dateTimeStart', 'dateTimeFinish', 'numUploaded', 'numFailed', 'cost', '', 'smartUpload', 'itemsProcessed', 'itemsSaved', 'initialCost', 'smartCost', 'savings', 'savingsToDate' ,'costToDate']
        cost = s3putCost*numUploaded
        savings = s3putCost*itemsProcessed-s3putCost*numUploaded
        uploadLogData = [dateTimeStart, str(datetime.now()), numUploaded,"?",cost,"-",smartUpload,itemsProcessed,itemsProcessed-numUploaded,s3putCost*itemsProcessed,s3putCost*numUploaded,savings,savingsToDate+savings,costToDate+cost]
        rowsList.insert(1,uploadLogData)

        write = csv.writer(f)
        write.writerows(rowsList)
        print(uploadLogData)


#uploadNewChanges()
uploadFile("results/labeled-stripes/US/MT/Gallatin County MT.png")
#uploadNewChanges(directory="results/json/US/",smartUpload=False)
