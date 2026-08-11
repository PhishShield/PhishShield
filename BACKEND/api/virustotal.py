import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/urls"
VIRUSTOTAL_ANALYSIS_URL = "https://www.virustotal.com/api/v3/analyses"

MAX_ATTEMPTS = 5
WAIT_SECONDS = 2
REQUEST_TIMEOUT = 15


def scan_url_with_virustotal(url: str) -> dict:
    """
    Submit a URL to VirusTotal and retrieve its analysis result.

    The function waits briefly for VirusTotal to finish processing
    the submitted URL so that detection statistics are more likely
    to be complete.
    """

    if not VIRUSTOTAL_API_KEY:
        return {
            "available": False,
            "analysis_ready": False,
            "error": "VirusTotal API key is not configured"
        }

    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY,
        "Accept": "application/json"
    }

    try:
        # ---------------------------------------------------------
        # 1. Submit URL
        # ---------------------------------------------------------
        response = requests.post(
            VIRUSTOTAL_URL,
            headers=headers,
            data={"url": url},
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code not in (200, 201):
            return {
                "available": False,
                "analysis_ready": False,
                "error": (
                    f"VirusTotal returned HTTP "
                    f"{response.status_code}"
                )
            }

        data = response.json()

        analysis_id = (
            data.get("data", {}).get("id")
        )

        if not analysis_id:
            return {
                "available": False,
                "analysis_ready": False,
                "error": "VirusTotal did not return an analysis ID"
            }

        # ---------------------------------------------------------
        # 2. Poll analysis result
        # ---------------------------------------------------------
        analysis_url = f"{VIRUSTOTAL_ANALYSIS_URL}/{analysis_id}"

        last_status = "unknown"

        for attempt in range(MAX_ATTEMPTS):

            analysis_response = requests.get(
                analysis_url,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

            if analysis_response.status_code != 200:
                return {
                    "available": True,
                    "analysis_id": analysis_id,
                    "analysis_ready": False,
                    "error": (
                        "Unable to retrieve VirusTotal "
                        f"analysis. HTTP "
                        f"{analysis_response.status_code}"
                    )
                }

            analysis_data = analysis_response.json()

            attributes = (
                analysis_data
                .get("data", {})
                .get("attributes", {})
            )

            status = attributes.get("status", "unknown")
            last_status = status

            # VirusTotal analysis is finished
            if status == "completed":

                stats = attributes.get("stats", {})

                malicious = int(
                    stats.get("malicious", 0) or 0
                )

                suspicious = int(
                    stats.get("suspicious", 0) or 0
                )

                harmless = int(
                    stats.get("harmless", 0) or 0
                )

                undetected = int(
                    stats.get("undetected", 0) or 0
                )

                return {
                    "available": True,
                    "analysis_id": analysis_id,
                    "analysis_ready": True,
                    "status": "completed",

                    "malicious": malicious > 0,
                    "malicious_detections": malicious,
                    "suspicious_detections": suspicious,
                    "harmless_detections": harmless,
                    "undetected": undetected,

                    "total_engines": (
                        malicious
                        + suspicious
                        + harmless
                        + undetected
                    )
                }

            # Still processing
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(WAIT_SECONDS)

        # ---------------------------------------------------------
        # 3. Analysis did not finish within our polling window
        # ---------------------------------------------------------
        return {
            "available": True,
            "analysis_id": analysis_id,
            "analysis_ready": False,
            "status": last_status,
            "message": (
                "VirusTotal analysis is still processing. "
                "Try the scan again later."
            )
        }

    except requests.Timeout:
        return {
            "available": False,
            "analysis_ready": False,
            "error": "VirusTotal request timed out"
        }

    except requests.RequestException as e:
        return {
            "available": False,
            "analysis_ready": False,
            "error": f"VirusTotal request failed: {str(e)}"
        }

    except (ValueError, TypeError) as e:
        return {
            "available": False,
            "analysis_ready": False,
            "error": f"Invalid VirusTotal response: {str(e)}"
        }

    except Exception as e:
        return {
            "available": False,
            "analysis_ready": False,
            "error": f"Unexpected VirusTotal error: {str(e)}"
        }

