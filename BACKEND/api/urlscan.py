import os
import requests
from dotenv import load_dotenv

load_dotenv()

URLSCAN_API_KEY = os.getenv("URLSCAN_API_KEY")

URLSCAN_SUBMIT_URL = "https://urlscan.io/api/v1/scan/"


def scan_url_with_urlscan(url: str) -> dict:
    """
    Submit a URL to urlscan.io for analysis.
    """

    if not URLSCAN_API_KEY:
        return {
            "available": False,
            "message": "URLScan API key is not configured"
        }

    headers = {
        "API-Key": URLSCAN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "url": url,
        "visibility": "unlisted"
    }

    try:
        response = requests.post(
            URLSCAN_SUBMIT_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Successful submission
        if response.status_code in (200, 201):
            data = response.json()

            return {
                "available": True,
                "uuid": data.get("uuid"),
                "result_url": data.get("result"),
                "submitted": True
            }

        # Try to get URLScan's actual error
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        return {
            "available": False,
            "submitted": False,
            "status_code": response.status_code,
            "error": "URLScan rejected the request",
            "details": error_data
        }

    except requests.RequestException as e:
        return {
            "available": False,
            "submitted": False,
            "error": f"URLScan request failed: {str(e)}"
        }
