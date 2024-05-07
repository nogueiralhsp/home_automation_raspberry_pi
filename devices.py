import requests



apiurl = 'http://192.168.0.9:9000/devicesall'

payload = {}
headers = {}

response = requests.request("GET", apiurl, headers=headers, data=payload)

mydevices = response.json()

for i in range(len(mydevices)):
    print(mydevices[i]['device'])
    