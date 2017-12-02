import requests
import json


url = 'http://api83944live.gateway.akana.com'
full_url = url + '/GetCurrentDepositRates'
params = {
    'application': 'RIB',
    'output': 'json',
    'branchnumber': '1',
    'CustomerType': 'CONSUMER',
    'Balance': 25000,
    'categoryid': 37,
    'LoanAmount': 25000,
    'Term': 55
}


response = requests.get(full_url, params=params)
response_data = response.json()