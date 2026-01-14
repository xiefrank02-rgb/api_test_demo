import requests
import json
import pprint
url = "http://fat-varx.creocreditapi.mx/calc/run"
# url = "http://localhost:8080/calc/run"

payload = json.dumps({
   "appid": "",
   "userid": 39176,
   "listingid": 0,
   "bizid": 5505,
   "flowid": "uuid64",
   "flowCount": 0,
   "debtid": 0,
   "vars": [
      "vl_listing_loan_dept_days"
   ]
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.json())
