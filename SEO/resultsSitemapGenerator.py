import os, json, sys
import xml.dom.minidom
sys.path.append('.')
import SSHupload

#returns a list of all files in a directory
def get_all_files_in_dir(root):
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            file_list.append(os.path.join(path, name))    
    return file_list

files = get_all_files_in_dir("results/json/US")

xml_file_list = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
print(files)
for file_path in files:
    if "desktop.ini" in file_path or len(file_path) > 23:  # removes desktop.ini and county files for now
        continue
    file_path = file_path.replace("\\","/") #fixes annoying formatting issue that messes up stuff
    #f = open(file)
    #f = f.read()
    #f = json.loads(f)

    def getPageURL ():
        split_path = file_path.split("/")
        split_path[-1] = split_path[-1].replace(".json","") #removes .json
        split_path.remove('results') #removes irrelevant info
        split_path.remove('json') #removes irrelevant info
        url = "https://www.earthstripes.org/result/"
        for i in range(len(split_path)):
            if i == 0:
                url = url + '?country=' + split_path[0]
            list_of_countries_with_states = ['US','RU','CN','IN','CA','BR','AU']
            if i == 1 and split_path[0] in list_of_countries_with_states:
                url = url + '&state=' + split_path[1]
            if i == 2 and split_path[0] == 'US':
                url = url + '&county=' + split_path[2][:-3].replace(" ","%20")

        url = url.replace("&","&amp;")

        #print(url)
        #print(splitPath)
        return url

    def addImage (image_url,image_caption,image_location,image_title,image_license):
        image_xml = []
        image_xml.append('<image:image>')
        image_xml.append('<image:loc>' + image_url + '</image:loc>')
        image_xml.append('<image:caption>' + image_caption + '</image:caption>')
        image_xml.append('<image:geo_location>' + image_location + '</image:geo_location>')
        image_xml.append('<image:title>' + image_title + '</image:title>')
        image_xml.append('<image:license>' + image_license + '</image:license>')
        image_xml.append('</image:image>')
        return image_xml

    

    xml_file_list.append('<url>')
    xml_file_list.append('<loc>' + getPageURL() + '</loc>')
    #xmlFileList = xmlFileList + addImage()
    xml_file_list.append('</url>')

xml_file_list.append('</urlset>')
xml_file = ""
for line in xml_file_list:
    xml_file = xml_file + line #+ "\n"
    print(line)



dom = xml.dom.minidom.parseString(xml_file) #xml.dom.minidom.parse(xml_fname)
pretty_xml_as_string = dom.toprettyxml()

with open('SEO/result-sitemap.xml', 'w') as f:
    f.write(pretty_xml_as_string)

SSHupload.upload("/public_html/result-sitemap.xml","SEO/result-sitemap.xml")

