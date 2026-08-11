from database import save_scan, get_scan_history


def save_scan_result(
    url: str,
    risk_score: int,
    status: str,
    reasons: list
):
    return save_scan(
        url=url,
        risk_score=risk_score,
        status=status,
        reasons=reasons
    )


def get_history():
    return get_scan_history()