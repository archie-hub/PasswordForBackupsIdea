import requests
import sys
import json

"""
By the time you see this this will all be invalid and I dont hardcode stuff... putting here for example
Copy and paste the output from terraform below to do a basic test.
Then run 

(.venv) archie@archie passwordendpoints % python python_tests.py test this
"""

api_gateway_url = "https://gz77c0r82h.execute-api.us-east-1.amazonaws.com/dev/execute"
api_key_value = "REbi4I5tBpUOh9fZ8Xrv8M2AcO2fmeXYwvem3250"

string1 = sys.argv[1]
string2 = sys.argv[2]

payload = {"string1": string1, "string2": string2}
headers = {"Content-Type": "application/json", "x-api-key": api_key_value}

response = requests.post(api_gateway_url, json=payload, headers=headers)
formatted_json = json.dumps(response.json(), indent=4)
print(formatted_json)
