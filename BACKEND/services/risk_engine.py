def calculate_risk(features: dict, security_services: dict) -> dict:
    """
    Calculate the final PhishShield risk score.

    Risk sources:
    - Local URL analysis
    - Google Safe Browsing
    - VirusTotal
    - URLScan

    Final score is always between 0 and 100.
    """

    # =========================================================
    # 1. LOCAL URL ANALYSIS
    # =========================================================

    local_score = 0
    local_reasons = []

    # IP address
    if features.get("has_ip_address"):
        local_score += 25
        local_reasons.append(
            "URL uses an IP address instead of a domain name."
        )

    # HTTPS
    if not features.get("has_https"):
        local_score += 10
        local_reasons.append(
            "URL does not use HTTPS."
        )

    # Suspicious keywords
    if features.get("has_suspicious_words"):
        local_score += 20
        local_reasons.append(
            "URL contains phishing-related keywords."
        )

    # @ symbol
    if features.get("has_at_symbol"):
        local_score += 15
        local_reasons.append(
            "URL contains an @ symbol that can obscure the destination."
        )

    # Many subdomains
    if features.get("has_many_subdomains"):
        local_score += 10
        local_reasons.append(
            "URL contains an unusually high number of subdomains."
        )

    # Suspicious port
    if features.get("has_suspicious_port"):
        local_score += 10
        local_reasons.append(
            "URL uses a potentially suspicious port."
        )

    # Encoded characters
    if features.get("has_encoded_characters"):
        local_score += 5
        local_reasons.append(
            "URL contains encoded characters."
        )

    # Punycode
    if features.get("has_punycode"):
        local_score += 15
        local_reasons.append(
            "URL contains punycode, which can be used in lookalike domains."
        )

    # Double slash in path
    if features.get("has_double_slash_path"):
        local_score += 5
        local_reasons.append(
            "URL contains a suspicious double-slash path pattern."
        )

    # Suspicious extension
    if features.get("has_suspicious_extension"):
        local_score += 10
        local_reasons.append(
            "URL contains a potentially suspicious file extension."
        )

    # Long hostname
    if features.get("has_long_hostname"):
        local_score += 5
        local_reasons.append(
            "Hostname is unusually long."
        )

    # Many digits
    if features.get("has_many_digits"):
        local_score += 5
        local_reasons.append(
            "Hostname contains an unusually high number of digits."
        )

    # Query parameters
    if features.get("has_query_parameters"):
        local_score += 3
        local_reasons.append(
            "URL contains query parameters."
        )

    # Username
    if features.get("has_username"):
        local_score += 10
        local_reasons.append(
            "URL contains a username component."
        )

    # Password
    if features.get("has_password"):
        local_score += 15
        local_reasons.append(
            "URL contains a password component."
        )

    # Cap local analysis
    local_score = min(local_score, 100)

    # =========================================================
    # 2. GOOGLE SAFE BROWSING
    # =========================================================

    google_score = 0
    google_reasons = []

    google = security_services.get(
        "google_safe_browsing", {}
    )

    if google.get("available"):

        if google.get("is_threat"):
            google_score = 100

            google_reasons.append(
                "Google Safe Browsing identified this URL as a threat."
            )

            matches = google.get("matches", [])

            if matches:
                for match in matches[:3]:
                    threat_type = match.get(
                        "threatType"
                    )

                    if threat_type:
                        google_reasons.append(
                            f"Google Safe Browsing threat type: {threat_type}."
                        )

    # =========================================================
    # 3. VIRUSTOTAL
    # =========================================================

    virustotal_score = 0
    virustotal_reasons = []

    vt = security_services.get(
        "virustotal", {}
    )

    if vt.get("available") and vt.get("analysis_ready"):

        malicious = int(
            vt.get("malicious_detections", 0) or 0
        )

        suspicious = int(
            vt.get("suspicious_detections", 0) or 0
        )

        # Strong malicious evidence
        if malicious > 0:

            virustotal_score = min(
                100,
                malicious * 10
            )

            virustotal_reasons.append(
                f"VirusTotal detected {malicious} malicious security engine result(s)."
            )

        # Suspicious detections
        elif suspicious > 0:

            virustotal_score = min(
                70,
                suspicious * 5
            )

            virustotal_reasons.append(
                f"VirusTotal reported {suspicious} suspicious security engine result(s)."
            )

    # =========================================================
    # 4. URLSCAN
    # =========================================================

    urlscan_score = 0
    urlscan_reasons = []

    urlscan = security_services.get(
        "urlscan", {}
    )

    if urlscan.get("available"):

        # Submission itself is not proof of maliciousness.
        # Therefore we don't add risk just because a scan
        # was submitted.
        urlscan_score = 0

    # =========================================================
    # 5. FINAL SCORE
    # =========================================================

    # Start with local analysis.
    final_score = local_score

    # External intelligence should be strong evidence.
    if google_score > 0:
        final_score = max(
            final_score,
            google_score
        )

    if virustotal_score > 0:
        final_score = max(
            final_score,
            virustotal_score
        )

    # URLScan submission alone does not increase score.
    final_score = min(
        100,
        max(0, final_score)
    )

    # =========================================================
    # 6. COMBINE REASONS
    # =========================================================

    reasons = (
        local_reasons
        + google_reasons
        + virustotal_reasons
        + urlscan_reasons
    )

    # Remove duplicate reasons while keeping order
    reasons = list(dict.fromkeys(reasons))

    # =========================================================
    # 7. STATUS
    # =========================================================

    if final_score >= 70:
        status = "High Risk"

    elif final_score >= 40:
        status = "Medium Risk"

    else:
        status = "Low Risk"

    # =========================================================
    # 8. CONFIDENCE
    # =========================================================

    available_services = 0

    for service_name in (
        "virustotal",
        "google_safe_browsing",
        "urlscan"
    ):
        service = security_services.get(
            service_name,
            {}
        )

        if service.get("available"):
            available_services += 1

    # Base confidence from local analysis
    confidence = 60

    # External services increase confidence
    confidence += available_services * 10

    # Strong evidence increases confidence
    if google_score > 0:
        confidence += 10

    if virustotal_score > 0:
        confidence += 10

    confidence = min(
        100,
        confidence
    )

    # =========================================================
    # 9. RETURN
    # =========================================================

    return {
        "risk_score": final_score,
        "status": status,
        "confidence": confidence,

        "reasons": reasons,

        "breakdown": {
            "local_url_analysis": local_score,
            "google_safe_browsing": google_score,
            "virustotal": virustotal_score,
            "urlscan": urlscan_score
        }
    }
