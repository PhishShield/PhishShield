from pydantic import BaseModel, HttpUrl
from typing import List


class ScanRequest(BaseModel):
    url: HttpUrl


class ScanResponse(BaseModel):
    url: str
    risk_score: int
    status: str
    reasons: List[str]