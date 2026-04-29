from pydantic import BaseModel
from typing import List, Optional


class DiseaseAnalysisRequest(BaseModel):
    image_base64: str


class DiseaseAnalysisResponse(BaseModel):
    crop_name: str
    disease_name: str
    confidence: float
    description: str
    remedy: str
    is_healthy: bool
