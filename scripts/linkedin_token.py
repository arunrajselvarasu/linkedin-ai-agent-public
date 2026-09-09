import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8000/callback"

AUTHORIZATION_CODE = input("Paste your authorization code: ").strip()

url = "https://www.linkedin.com/oauth/v2/accessToken"

data = {
    "grant_type": "authorization_code",
    "code": AUTHORIZATION_CODE,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

response = requests.post(
    url,
    data=data,
    timeout=30,
)

print("\nStatus:", response.status_code)

if response.ok:
    token_data = response.json()

    print("\n✅ Access token received!")
    print("\nAccess Token:")
    print(token_data["access_token"])

    print("\nExpires in:")
    print(token_data.get("expires_in"), "seconds")

else:
    print("\n❌ Token exchange failed:")
    print(response.text)