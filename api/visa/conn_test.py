import requests

headers = ''
body = ''

r = requests.post(url,
  cert = ('./keys/cert.pem','./keys/key_b9bdf401-9c99-4259-9a75-1b831e6a5eff.pem'),
  headers = headers,
  auth = ('4OYJU3E5I5XSGFYMNK0621lrQ-MAwZrgnok3pgL8tyH5Pux8k', '6789jFZus60vfPDE85omuJ1QD8GnzQ3x'),
  data = body)