import requests
import json


url = 'http://api119525live.gateway.akana.com'
full_url = url + '/user/accounts'
request_data = {
    'LegalParticipantIdentifier': '913996201744144603' }


response = requests.post(full_url, json=request_data)
response_data = response.json()