from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Clean and normalize a URL before scanning.
    """

    url = url.strip()

    if not url:
        return url

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def get_domain(url: str) -> str:
    """
    Extract the domain name from a URL.
    """

    parsed = urlparse(url)

    return parsed.hostname or ""


def is_https(url: str) -> bool:
    """
    Check whether a URL uses HTTPS.
    """

    parsed = urlparse(url)

    return parsed.scheme.lower() == "https"