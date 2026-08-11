from urllib.parse import urlparse
import ipaddress
import re


def extract_features(url: str) -> dict:
    """
    Extract security-related features from a URL.

    These features are used by the PhishShield risk engine.
    """

    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    hostname_lower = hostname.lower()
    url_lower = url.lower()

    features = {
        # -------------------------------------------------
        # Basic URL information
        # -------------------------------------------------
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),

        # -------------------------------------------------
        # Existing security indicators
        # -------------------------------------------------
        "has_https": parsed.scheme.lower() == "https",

        "has_ip_address": _looks_like_ip(hostname),

        "has_at_symbol": "@" in url,

        "has_dash": "-" in hostname,

        "has_many_subdomains": _has_many_subdomains(hostname),

        "has_suspicious_words": _has_suspicious_words(url),

        # -------------------------------------------------
        # New security indicators
        # -------------------------------------------------
        "has_suspicious_port": _has_suspicious_port(parsed),

        "has_encoded_characters": _has_encoded_characters(url),

        "has_punycode": hostname_lower.startswith("xn--")
        or ".xn--" in hostname_lower,

        "has_double_slash_path": _has_double_slash_path(path),

        "has_suspicious_extension": _has_suspicious_extension(path),

        "has_long_hostname": len(hostname) > 50,

        "has_many_digits": _has_many_digits(hostname),

        "has_query_parameters": bool(query),

        "subdomain_count": _count_subdomains(hostname),

        # -------------------------------------------------
        # Additional useful indicators
        # -------------------------------------------------
        "has_fragment": bool(parsed.fragment),

        "has_username": parsed.username is not None,

        "has_password": parsed.password is not None,

        "domain_parts": len(
            [part for part in hostname.split(".") if part]
        ),
    }

    return features


# =========================================================
# IP ADDRESS DETECTION
# =========================================================

def _looks_like_ip(hostname: str) -> bool:
    """
    Detect IPv4 and IPv6 addresses.
    """

    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


# =========================================================
# SUBDOMAIN DETECTION
# =========================================================

def _count_subdomains(hostname: str) -> int:
    """
    Count approximate subdomains.

    Example:
        login.example.com
        -> 1

        login.secure.example.com
        -> 2
    """

    parts = [
        part for part in hostname.split(".")
        if part
    ]

    if len(parts) <= 2:
        return 0

    return len(parts) - 2


def _has_many_subdomains(hostname: str) -> bool:
    """
    Detect unusually large numbers of subdomains.
    """

    return _count_subdomains(hostname) >= 3


# =========================================================
# SUSPICIOUS KEYWORD DETECTION
# =========================================================

def _has_suspicious_words(url: str) -> bool:
    """
    Detect common phishing-related keywords.
    """

    suspicious_words = [
        "login",
        "log-in",
        "signin",
        "sign-in",
        "verify",
        "verification",
        "password",
        "account",
        "secure",
        "security",
        "update",
        "confirm",
        "confirmation",
        "bank",
        "banking",
        "payment",
        "wallet",
        "billing",
        "credential",
        "unlock",
        "recover",
        "suspend",
        "suspended",
        "alert",
        "support",
        "webmail",
    ]

    url_lower = url.lower()

    return any(
        word in url_lower
        for word in suspicious_words
    )


# =========================================================
# PORT DETECTION
# =========================================================

def _has_suspicious_port(parsed) -> bool:
    """
    Detect uncommon HTTP/HTTPS ports.

    Standard:
        HTTP  -> 80
        HTTPS -> 443
    """

    try:
        port = parsed.port
    except ValueError:
        return True

    if port is None:
        return False

    return port not in [80, 443]


# =========================================================
# URL ENCODING DETECTION
# =========================================================

def _has_encoded_characters(url: str) -> bool:
    """
    Detect percent-encoded characters.

    Example:
        %20
        %2F
        %40
    """

    return bool(
        re.search(r"%[0-9a-fA-F]{2}", url)
    )


# =========================================================
# DOUBLE SLASH DETECTION
# =========================================================

def _has_double_slash_path(path: str) -> bool:
    """
    Detect // inside the URL path.

    The normal https:// is not checked because
    only the parsed path is inspected.
    """

    return "//" in path


# =========================================================
# SUSPICIOUS FILE EXTENSION
# =========================================================

def _has_suspicious_extension(path: str) -> bool:
    """
    Detect potentially suspicious executable/script
    extensions frequently seen in malicious URLs.

    This is only an indicator, not proof of malware.
    """

    suspicious_extensions = [
        ".exe",
        ".scr",
        ".bat",
        ".cmd",
        ".msi",
        ".dll",
        ".ps1",
        ".vbs",
        ".js",
        ".jar",
    ]

    path_lower = path.lower()

    return any(
        path_lower.endswith(extension)
        for extension in suspicious_extensions
    )


# =========================================================
# DIGIT DETECTION
# =========================================================

def _has_many_digits(hostname: str) -> bool:
    """
    Detect hostnames containing an unusually high
    number of numeric characters.
    """

    if not hostname:
        return False

    digit_count = sum(
        character.isdigit()
        for character in hostname
    )

    return digit_count >= 5