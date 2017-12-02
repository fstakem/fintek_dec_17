import requests
import json


url = 'http://api119521live.gateway.akana.com'
full_url = url + '/api/v1/account/details'
request_data = {
    "OperatingCompanyIdentifier" : "815",
    "ProductCode" : "DDA",
    "PrimaryIdentifier" : "00000000000000822943114" }


response = requests.post(full_url, json=request_data)
response_data = response.json()
