import requests

my_headers = {'token' : 'vuqgjmWUyGoUzZHEhWswbwzdOMyvnbFk'}
response = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datacategories/ANNTEMP', headers=my_headers)
print(response.json())