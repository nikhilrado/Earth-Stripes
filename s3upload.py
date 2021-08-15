from s3keys import access_key, secret_access_key
import boto3
import os
import json
from datetime import datetime
import csv

s3putCost = 0.005/1000
upload_bucket = "ortana-test"
client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

def getAllFilesInDir(root):
    #print(os.listdir("results"))
    fileList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            fileList.append(os.path.join(path, name))
    return fileList

def uploadFile(file):
    upload_file_path = file.replace("results/","")
    client.upload_file(file, upload_bucket, upload_file_path,ExtraArgs={'ACL':'public-read', "ContentType":'image/png'})
    print("Uploaded: "+file)


#allowed us to add a object to all the json files-----------------
'''import createJSON
for file in getAllFilesInDir("results/json"):
    createJSON.updateMetadata(file,"")'''

#find the type of file from the directory (ex. bars, json, stripes)
def getFileType(filePath):
    resourceTypes = os.listdir("results")
    for resourceType in resourceTypes:
        if resourceType in filePath:
            return resourceType

def uploadNewChanges(directory="results",smartUpload=True):
    #opens the log file
    f = open("s3upload-log.csv","r")
    csv_f = csv.reader(f)
    rowsList = []
    for row in csv_f:
        rowsList.append(row)
    lastUpload = rowsList[1][0]
    costToDate = float(rowsList[1][-1])
    savingsToDate = float(rowsList[1][-3])
    lastUpload = datetime.strptime(lastUpload, '%Y-%m-%d %H:%M:%S.%f')
    dateTimeStart = str(datetime.now())

    #counters, metrics and analytics
    itemsProcessed = 0
    numUploaded = 0
    for file in getAllFilesInDir(directory):
        file = file.replace("\\","/")
        itemsProcessed += 1

        if smartUpload:
            fileType = getFileType(file)
            jsonFile = file.replace(fileType,"json").replace(".png",".json").replace(".jpeg",".json")
            f = open(jsonFile)
            f = f.read()
            f = json.loads(f)
            #print(f)
            try:
                lastUpdated = f["resources"][fileType]["last updated"]
                lastUpdated = datetime.strptime(lastUpdated, '%Y-%m-%d %H:%M:%S.%f')
                if lastUpload < lastUpdated:
                    uploadFile(file)
                    numUploaded += 1
            except:
                continue
        else:
            uploadFile(file)
            numUploaded += 1
        

        
    with open('s3upload-log.csv', 'w', newline="") as f:
        # using csv.writer method from CSV package
        #['dateTimeStart', 'dateTimeFinish', 'numUploaded', 'numFailed', 'cost', '', 'smartUpload', 'itemsProcessed', 'itemsSaved', 'initialCost', 'smartCost', 'savings', 'savingsToDate' ,'costToDate']
        cost = s3putCost*numUploaded
        savings = s3putCost*itemsProcessed-s3putCost*numUploaded
        uploadLogData = [dateTimeStart, str(datetime.now()), numUploaded,"?",cost,"-",smartUpload,itemsProcessed,itemsProcessed-numUploaded,s3putCost*itemsProcessed,s3putCost*numUploaded,savings,savingsToDate+savings,costToDate+cost]
        rowsList.insert(1,uploadLogData)

        write = csv.writer(f)
        write.writerows(rowsList)




uploadNewChanges()
