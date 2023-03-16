import requests

r = requests.session()
r.cert = ("../z5361056.crt", "../z5361056.key")

response = r.post("https://haas.quoccabank.com", data={"requestBox": "http request here"})
print(response.text)