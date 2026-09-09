import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")
LINKEDIN_VERSION = os.getenv("LINKEDIN_VERSION", "202608")

if not ACCESS_TOKEN:
    raise ValueError("LINKEDIN_ACCESS_TOKEN is missing")

if not PERSON_URN:
    raise ValueError("LINKEDIN_PERSON_URN is missing")


url = "https://api.linkedin.com/rest/posts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "LinkedIn-Version": LINKEDIN_VERSION,
    "X-Restli-Protocol-Version": "2.0.0",
}

payload = {
    "author": PERSON_URN,
    "commentary": (
        "Testing my AI/ML LinkedIn automation agent 🚀\n\n"
        "This is a test post created through the LinkedIn Posts API "
        "using Python."
    ),
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": [],
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False,
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=30,
)

print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 201:
    post_id = response.headers.get("x-restli-id")

    print("\n✅ LinkedIn post published!")
    print("Post ID:", post_id)

else:
    print("\n❌ LinkedIn post failed.")