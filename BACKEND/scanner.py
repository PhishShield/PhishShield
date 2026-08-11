from urllib.parse import urlparse
import re


def scan_url(url: str):
    score = 0
    reasons = []

    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    # Check HTTPS
    if parsed.scheme != "https":
        score += 20
        reasons.append("Website is not using HTTPS")

    # Check if IP address is used
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        score += 30
        reasons.append("Uses an IP address instead of a domain")

    # Check URL length
    if len(url) > 100:
        score += 10
        reasons.append("URL is unusually long")

    # Check suspicious keywords
    keywords = [
        "login",
        "verify",
        "update",
        "password",
        "bank",
        "secure",
        "signin"
    ]

    found = [word for word in keywords if word in url.lower()]

    if found:
        score += min(len(found) * 5, 20)
        reasons.append("Contains suspicious keywords")

    # Check @ symbol
    if "@" in url:
        score += 20
        reasons.append("Contains '@' symbol")

    # Final status
    score = min(score, 100)

    if score >= 70:
        status = "Phishing"
    elif score >= 40:
        status = "Suspicious"
    else:
        status = "Safe"

    if not reasons:
        reasons.append("No obvious suspicious patterns found.")

    return {
        "risk_score": score,
        "status": status,
        "reasons": reasons
    }