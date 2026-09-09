import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("LINKEDIN_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {token}"
}

url = "https://api.linkedin.com/v2/userinfo"

res = requests.get(url, headers=headers)

print(res.status_code)
print(res.json())