from urllib.parse import urlparse
import ipaddress


def analyze_domain(url: str) -> dict:
    """
    Analyze the domain/hostname of a URL.

    IP addresses are handled separately from normal domains.
    """

    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower().strip()

    if not hostname:
        return {
            "available": False,
            "error": "Hostname could not be extracted"
        }

    # ---------------------------------------------------------
    # 1. Check whether hostname is an IP address
    # ---------------------------------------------------------
    try:
        ip = ipaddress.ip_address(hostname)

        return {
            "available": True,
            "hostname": hostname,
            "domain": None,
            "tld": None,
            "hostname_length": len(hostname),
            "subdomain_count": 0,
            "is_ip_address": True,
            "ip_version": ip.version,
            "is_private_ip": ip.is_private,
            "is_loopback_ip": ip.is_loopback,
            "is_reserved_ip": ip.is_reserved,
            "is_punycode": False,
            "has_https": parsed.scheme.lower() == "https",
            "domain_parts": 0
        }

    except ValueError:
        pass

    # ---------------------------------------------------------
    # 2. Normal domain analysis
    # ---------------------------------------------------------
    parts = hostname.split(".")

    domain_parts = len(parts)

    if domain_parts >= 2:
        domain = ".".join(parts[-2:])
        tld = parts[-1]
        subdomain_count = max(domain_parts - 2, 0)
    else:
        domain = hostname
        tld = None
        subdomain_count = 0

    # ---------------------------------------------------------
    # 3. Punycode detection
    # ---------------------------------------------------------
    is_punycode = any(
        part.startswith("xn--")
        for part in parts
    )

    # ---------------------------------------------------------
    # 4. Additional indicators
    # ---------------------------------------------------------
    digit_count = sum(
        character.isdigit()
        for character in hostname
    )

    hyphen_count = hostname.count("-")

    return {
        "available": True,

        "hostname": hostname,
        "domain": domain,
        "tld": tld,

        "hostname_length": len(hostname),
        "domain_parts": domain_parts,
        "subdomain_count": subdomain_count,

        "is_ip_address": False,
        "is_punycode": is_punycode,

        "has_https": parsed.scheme.lower() == "https",

        "digit_count": digit_count,
        "hyphen_count": hyphen_count,

        "has_many_digits": digit_count >= 5,
        "has_many_hyphens": hyphen_count >= 3,

        "has_www": hostname.startswith("www."),

        "is_private_ip": False,
        "is_loopback_ip": False,
        "is_reserved_ip": False
    }
