from urllib.parse import urlparse
import ipaddress
import re


def validate_url(url: str) -> bool:
    """
    Validate that the URL has:
    - HTTP or HTTPS scheme
    - A valid hostname
    - A realistic domain/IP format
    """

    try:
        parsed = urlparse(url)

        # Only HTTP/HTTPS
        if parsed.scheme.lower() not in {"http", "https"}:
            return False

        hostname = parsed.hostname

        if not hostname:
            return False

        hostname = hostname.lower().strip()

        # Reject whitespace
        if any(char.isspace() for char in hostname):
            return False

        # Accept valid IP addresses
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            pass

        # Domain must contain a dot
        if "." not in hostname:
            return False

        # Domain cannot start/end with a dot
        if hostname.startswith(".") or hostname.endswith("."):
            return False

        # Basic domain validation
        domain_pattern = re.compile(
            r"^(?=.{1,253}$)"
            r"(?:[a-zA-Z0-9]"
            r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
            r"\.)+"
            r"[a-zA-Z]{2,63}$"
        )

        return bool(domain_pattern.match(hostname))

    except Exception:
        return False