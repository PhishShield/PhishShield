from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from utils.rate_limiter import limiter

from database import save_scan

from services.feature_extractor import extract_features
from services.domain_intelligence import analyze_domain
from services.redirect_analyzer import analyze_redirects
from services.risk_engine import calculate_risk

from utils.helpers import normalize_url
from utils.validators import validate_url
from utils.security import is_private_or_local_url

from api.virustotal import scan_url_with_virustotal
from api.safebrowsing import check_url_with_safebrowsing
from api.urlscan import scan_url_with_urlscan


router = APIRouter(
    prefix="/scan",
    tags=["URL Scanner"]
)


class ScanRequest(BaseModel):
    url: str


@router.post("/")
async def scan_url(request: ScanRequest):

    # =========================================================
    # 1. Normalize URL
    # =========================================================
    url = normalize_url(request.url)

    # =========================================================
    # 2. Validate URL
    # =========================================================
    if not validate_url(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL. Please enter a valid HTTP or HTTPS URL."
        )

    # =========================================================
    # 3. SSRF Protection
    # =========================================================
    if is_private_or_local_url(url):
        raise HTTPException(
            status_code=400,
            detail="Private, local, or internal URLs are not allowed."
        )

    # =========================================================
    # 4. Extract URL Features
    # =========================================================
    features = extract_features(url)

    # =========================================================
    # 5. Domain Intelligence
    # =========================================================
    domain_info = analyze_domain(url)

    # =========================================================
    # 6. Redirect Analysis
    # =========================================================
    redirect_info = analyze_redirects(url)

    # =========================================================
    # 7. VirusTotal
    # =========================================================
    virustotal_result = scan_url_with_virustotal(url)

    # =========================================================
    # 8. Google Safe Browsing
    # =========================================================
    safebrowsing_result = check_url_with_safebrowsing(url)

    # =========================================================
    # 9. URLScan
    # =========================================================
    urlscan_result = scan_url_with_urlscan(url)

    # =========================================================
    # 10. Calculate Final Risk
    # =========================================================
    risk = calculate_risk(
        features,
        {
            "virustotal": virustotal_result,
            "google_safe_browsing": safebrowsing_result,
            "urlscan": urlscan_result,
            "redirect_analysis": redirect_info
        }
    )

    # =========================================================
    # 11. Save Scan To Database
    # =========================================================
    scan_id = save_scan(
        url=url,
        risk_score=risk["risk_score"],
        status=risk["status"],
        reasons=risk["reasons"]
    )

    # =========================================================
    # 12. Return Complete Scan Result
    # =========================================================
    return {
        "scan_id": scan_id,

        "url": url,

        "risk": {
            "score": risk["risk_score"],
            "status": risk["status"],
            "confidence": risk["confidence"],
            "reasons": risk["reasons"],
            "breakdown": risk["breakdown"]
        },

        "features": features,

        "domain": domain_info,

        "redirect_analysis": redirect_info,

        "security_services": {
            "virustotal": virustotal_result,
            "google_safe_browsing": safebrowsing_result,
            "urlscan": urlscan_result
        }
    }
