import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_POSTS_URL = "https://api.linkedin.com/rest/posts"


def get_linkedin_config():
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN")
    linkedin_version = os.getenv("LINKEDIN_VERSION", "202608")

    if not access_token:
        raise ValueError("LINKEDIN_ACCESS_TOKEN is not set.")

    if not person_urn:
        raise ValueError("LINKEDIN_PERSON_URN is not set.")

    return access_token, person_urn, linkedin_version


def publish_to_linkedin(content: str) -> str:

    access_token, person_urn, linkedin_version = get_linkedin_config()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": linkedin_version,
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": person_urn,
        "commentary": content,
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
        LINKEDIN_POSTS_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"LinkedIn API request failed: "
            f"{response.status_code} - {response.text}"
        )

    post_id = response.headers.get("x-restli-id")

    if not post_id:
        raise RuntimeError(
            "LinkedIn API succeeded but did not return x-restli-id."
        )

    return post_id