from urllib.parse import urlparse
import ipaddress

import requests


MAX_REDIRECTS = 5
REQUEST_TIMEOUT = 5


def _is_unsafe_hostname(hostname: str) -> bool:
    """
    Prevent the backend from requesting localhost,
    private IPs, loopback addresses, or reserved IPs.
    """

    if not hostname:
        return True

    hostname = hostname.lower().strip()

    blocked_names = {
        "localhost",
        "localhost.localdomain",
        "0.0.0.0",
        "::1",
    }

    if hostname in blocked_names:
        return True

    try:
        ip = ipaddress.ip_address(hostname)

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_reserved
            or ip.is_link_local
        ):
            return True

    except ValueError:
        # Normal domain name
        pass

    return False


def analyze_redirects(url: str) -> dict:
    """
    Safely analyze URL redirects.

    Returns:
    - redirect count
    - redirect chain
    - final URL
    - whether redirect limit was exceeded
    """

    parsed = urlparse(url)

    if parsed.scheme.lower() not in {"http", "https"}:
        return {
            "available": False,
            "redirect_count": 0,
            "has_redirects": False,
            "final_url": None,
            "redirect_chain": [],
            "exceeded_limit": False,
            "error": "Only HTTP and HTTPS URLs are supported."
        }

    hostname = parsed.hostname

    if _is_unsafe_hostname(hostname):
        return {
            "available": False,
            "redirect_count": 0,
            "has_redirects": False,
            "final_url": None,
            "redirect_chain": [],
            "exceeded_limit": False,
            "blocked": True,
            "error": "Redirect analysis blocked for local or private destination."
        }

    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=REQUEST_TIMEOUT,
            stream=True,
            headers={
                "User-Agent": "PhishShield-Security-Scanner/1.0"
            }
        )

        history = response.history

        redirect_chain = []

        for item in history:
            redirect_chain.append({
                "status_code": item.status_code,
                "url": item.url,
                "location": item.headers.get("Location")
            })

        final_url = response.url

        # Close response without downloading the page body
        response.close()

        redirect_count = len(history)

        return {
            "available": True,
            "redirect_count": redirect_count,
            "has_redirects": redirect_count > 0,
            "final_url": final_url,
            "redirect_chain": redirect_chain,
            "exceeded_limit": redirect_count > MAX_REDIRECTS
        }

    except requests.TooManyRedirects:
        return {
            "available": True,
            "redirect_count": MAX_REDIRECTS,
            "has_redirects": True,
            "final_url": None,
            "redirect_chain": [],
            "exceeded_limit": True,
            "error": "Maximum redirect limit exceeded."
        }

    except requests.Timeout:
        return {
            "available": False,
            "redirect_count": 0,
            "has_redirects": False,
            "final_url": None,
            "redirect_chain": [],
            "exceeded_limit": False,
            "error": "Redirect analysis timed out."
        }

    except requests.RequestException as e:
        return {
            "available": False,
            "redirect_count": 0,
            "has_redirects": False,
            "final_url": None,
            "redirect_chain": [],
            "exceeded_limit": False,
            "error": f"Redirect analysis failed: {str(e)}"
        }