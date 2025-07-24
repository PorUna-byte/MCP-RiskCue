import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv()
conn = http.client.HTTPSConnection("api.gpt.ge")
payload = ''
headers = {
   'Authorization': f'Bearer {os.getenv("API_KEY")}',
   'Content-Type': 'application/json'
}
conn.request("GET", "/v1/models", payload, headers)
res = conn.getresponse()
data = res.read()

with open("available_model.json", "w") as f:
    json.dump(json.loads(data.decode("utf-8")), f, indent=4)