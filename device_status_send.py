import requests
import json

url = "https://my-home-automation-api.herokuapp.com/device/status"

payload = json.dumps({
  "device": "611e35ada7eb2f23a5a86999",
  "statusValue": "99",
  "statusType": "new test"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
