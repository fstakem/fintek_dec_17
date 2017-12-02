import json

from api.visa.visa_api_client import VisaAPIClient

client = VisaAPIClient()

data = json.loads('''{
                 "header": {
                     "messageDateTime": "'''+ date  +'''",
                     "requestMessageId": "CDISI_GMR_001",
                     "startIndex": "1"
                 },
              "searchAttrList": {
                 "visaMerchantId":"11687107",
                 "visaStoreId":"125861096",
                 "merchantName":"ALOHA CAFE",
                 "merchantCountryCode":"840",
                 "merchantCity": "LOS ANGELES",
                 "merchantState": "CA",
                 "merchantPostalCode": "90012",
                 "merchantStreetAddress": "410 E 2ND ST", 
                 "businessRegistrationId":"196007747",
                 "acquirerCardAcceptorId":"191642760469222", 
                 "acquiringBin":"486168"
              },
              "responseAttrList": [
                 "GNSTANDARD"
              ],
              "searchOptions": {
                 "maxRecords": "2",
                 "matchIndicators": "true",
                 "matchScore": "true"
              }
            }''')

base_uri = 'merchantsearch/'
resource_path = 'v1/search'
path = base_uri + resource_path
body = {}
test_info = 'Merchant Search Test'
method_type = 'post'


client.do_mutual_auth_request(path, body, test_info, method_type)
