import json
from api.visa.visa_api_client import VisaAPIClient

client = VisaAPIClient()

url = 'https://sandbox.api.visa.com/merchantmeasurement/v1/merchantbenchmark'
body = {
  "requestData": {
        "naicsCodes": [
            ""
        ],
        "merchantCategoryCodes": [
            "Fast Food Restaurants"
        ],
        "merchantCategoryGroupsCodes": [
            ""
        ],
        "merchantCountry": "840",
        "postalCodeList": [
            ""
        ],
        "msaList": [
            "7362"
        ],
        "countrySubdivisionList": [
            ""
        ],
        "monthList": [
            "201706"
        ],
        "cardPresentIndicator": "CARDPRESENT",
        "accountFundingSource": [
            "All"
        ],
        "eciIndicator": [
            "All"
        ],
        "platformID": [
            "All"
        ],
        "posEntryMode": [
            "All"
        ],
        "groupList": [
            "standard",
            "cardholder",
            "cbreasoncode"
        ]
    }
}
test_info = 'Merchant Search Test'
method_type = 'post'
response = client.do_mutual_auth_request(url, body, test_info, method_type)