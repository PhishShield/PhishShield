import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SAFE_BROWSING_API_KEY = os.getenv(
    "GOOGLE_SAFE_BROWSING_API_KEY"
)

SAFE_BROWSING_URL = (
    "https://safebrowsing.googleapis.com/v4/"
    "threatMatches:find"
)


def check_url_with_safebrowsing(url: str) -> dict:
    """
    Check a URL against Google Safe Browsing.
    """

    if not GOOGLE_SAFE_BROWSING_API_KEY:
        return {
            "available": False,
            "message": "Google Safe Browsing API key is not configured"
        }

    params = {
        "key": GOOGLE_SAFE_BROWSING_API_KEY
    }

    payload = {
        "client": {
            "clientId": "phishshield",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": [
                "ANY_PLATFORM"
            ],
            "threatEntryTypes": [
                "URL"
            ],
            "threatEntries": [
                {
                    "url": url
                }
            ]
        }
    }

    try:
        response = requests.post(
            SAFE_BROWSING_URL,
            params=params,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            return {
                "available": False,
                "error": (
                    f"Google Safe Browsing returned "
                    f"HTTP {response.status_code}"
                )
            }

        data = response.json()

        matches = data.get("matches", [])

        return {
            "available": True,
            "is_threat": len(matches) > 0,
            "matches": matches
        }

    except requests.RequestException as e:
        return {
            "available": False,
            "error": str(e)
        }

