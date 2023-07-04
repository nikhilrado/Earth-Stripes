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
def get_all_files_in_dir(root):
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            file_list.append(os.path.join(path, name))
    return file_list

# will upload a file to s3 and print a statement stating which file was uploaded
def upload_file(file,upload_file_path=False):
    # lets the user specify if they want to add a custom file path
    if upload_file_path == False:
        upload_file_path = "v3/" + file.replace(RESULTS_DIRECTORY,"")
    else:
        upload_file_path = upload_file_path
    
    content_type = "txt"
    if '.png' in file:
        content_type = 'image/png'
    elif '.jpg' in file:
        content_type = 'image/jpg'
    elif '.json' in file:
        content_type = 'application/json'
    elif '.xml' in file:
        content_type = 'text/xml'
    elif '.csv' in file:
        content_type = 'text/csv'
    elif '.html' in file:
        content_type = 'text/html'
    elif '.js' in file:
        content_type = 'application/javascript'
    elif '.css' in file:
        content_type = 'text/css'
    client.upload_file(file, S3_UPLOAD_BUCKET, upload_file_path,ExtraArgs={'ACL':'public-read', "ContentType":content_type})
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

resource_types = sorting(os.listdir(RESULTS_DIRECTORY))
resource_types.reverse()
#print(resourceTypes)
def get_file_type(file_path):
    for resource_type in resource_types:
        if resource_type in file_path:
            return resource_type

# when run it will upload all files in a directory to s3, if smartUpload is "True", it will only upload files that have been changed since last upload
def upload_new_changes(directory=RESULTS_DIRECTORY,smart_upload=True, exclude=[]):
    # opens the log file
    f = open(LOG_FILE,"r")
    csv_f = csv.reader(f)
    rows_list = []
    for row in csv_f:
        rows_list.append(row)
    # sets variables from log file
    last_upload = rows_list[1][0]
    cost_to_date = float(rows_list[1][-1])
    savings_to_date = float(rows_list[1][-3])
    last_upload = datetime.strptime(last_upload, '%Y-%m-%d %H:%M:%S.%f')
    date_time_start = str(datetime.now())

    # counters, metrics and analytics
    items_processed = 0
    num_uploaded = 0

    # will loop through all of the files
    for file in get_all_files_in_dir(directory):
        # if the file is not in the exclude list
        exclude.append("desktop.ini")
        upload_flag = True
        for ex in exclude:
            if ex in file:
                print("skipping: "+file)
                upload_flag = False
                break
        if not upload_flag:
            continue
        file = file.replace("\\","/")  # fixes annoying formating issue that messes up s3
        items_processed += 1

        # if this is a smart upload then, read the json file, and determine if it needs to be uploaded
        if smart_upload:
            file_type = get_file_type(file)
            json_file = file.replace(file_type,"json").replace(".png",".json").replace(".jpeg",".json")
            f = open(json_file)
            f = f.read()
            f = json.loads(f)
            #print(f)

            # find the date in the json file, if no date is present, skip file 
            try:
                last_updated = f["resources"][file_type]["last updated"]
                last_updated = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S.%f')
                if last_upload < last_updated:
                    upload_file(file)
                    num_uploaded += 1
            except:
                continue
        # when smartUpload isn't true, just upload everything
        else:
            upload_file(file)
            num_uploaded += 1
        

    # open up the log file, and record data from the day's upload
    with open(LOG_FILE, 'w', newline="") as f:
        # using csv.writer method from CSV package
        # ['dateTimeStart', 'dateTimeFinish', 'numUploaded', 'numFailed', 'cost', '', 'smartUpload', 'itemsProcessed', 'itemsSaved', 'initialCost', 'smartCost', 'savings', 'savingsToDate' ,'costToDate']
        cost = S3_PUT_COST*num_uploaded
        savings = S3_PUT_COST*items_processed-S3_PUT_COST*num_uploaded
        upload_log_data = [date_time_start, str(datetime.now()), num_uploaded,"?",cost,"-",smart_upload,items_processed,items_processed-num_uploaded,S3_PUT_COST*items_processed,S3_PUT_COST*num_uploaded,savings,savings_to_date+savings,cost_to_date+cost]
        rows_list.insert(1,upload_log_data)

        write = csv.writer(f)
        write.writerows(rows_list)
        print(upload_log_data)


def test():
    #uploadNewChanges()
    #uploadFile("results/sunny.png")
    upload_new_changes(directory="../Earth Stripes Codebase/results/json/US/",smart_upload=False)
    #uploadNewChanges(directory="results/",smartUpload=False)
    #uploadNewChanges(directory="photos/local-impact-photos/",smartUpload=False)
    # CHART_TYPES = ["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","stripes-svg","light-labeled-bars","large-square-stripes"]
    # CHART_TYPES += ["json"]
    # for chart_type in CHART_TYPES:
    #     upload_new_changes(directory=f"../Earth Stripes Codebase/results/{chart_type}/US/FL/",smart_upload=False) 
    #     #uploadFile(f"../Earth Stripes Codebase/results/{chartType}/US.json")
    #uploadFile("Site Files/map-page/countries2.js", uploadFilePath="map-stuff.js")
    #uploadFile("Map Stuff/mapData.csv",uploadFilePath="mapData2.csv")
    #uploadFile("test5.svg",uploadFilePath="test5.svg")
    #uploadFile("results/json/US.json",uploadFilePath="v3/json/US.json")
    #uploadAll("../Earth Stripes Codebase/results/stripes/US.png")
    #uploadAll("results/stripes/location/earth.png")

    pass

# method to upload all of the image/file types to s3 by inputting the stripes file
def upload_all(file,chart_types=["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","light-labeled-bars","stripes-svg","json"]):
    for chart_type in chart_types:
        if "svg" in chart_type:
            upload_file(file.replace("/stripes/","/"+chart_type+"/").replace(".png",".svg"),upload_file_path="v3/"+file.replace("/stripes/","/"+chart_type+"/").replace("results/","").replace(".png",".svg"))
        elif "json" in chart_type:
            upload_file(file.replace("/stripes/","/"+chart_type+"/").replace(".png",".json"),upload_file_path="v3/"+file.replace("/stripes/","/"+chart_type+"/").replace("results/","").replace(".png",".json"))
        else:
            upload_file(file.replace("/stripes/","/"+chart_type+"/"),upload_file_path="v3/"+file.replace("/stripes/","/"+chart_type+"/").replace("results/",""))

# uploads all files for a foreign (non-US) state/province
def upload_state_provinces(state_provinces = ["AU","CA","BR","CN","IN","RU"]):
    for country in state_provinces:
        for type in ["label","labeled-bars","labeled-stripes","snap-sticker","stripes","twitter-card","light-labeled-bars","stripes-svg","json"]:
            upload_new_changes("../Earth Stripes Codebase/results/{}/{}".format(type,country),smart_upload=False)

# this is the main function that will be called when the script is run
# if the file is imported, it will not run the test function
# test method is created to remove global scope of any variables in test()
if __name__ == "__main__":
    test()