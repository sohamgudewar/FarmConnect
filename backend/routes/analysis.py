from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.services.analysis_service import analyze_crop_image
from backend.services.advisory_service import generate_market_advisory
from backend.schemas.analysis import DiseaseAnalysisRequest, DiseaseAnalysisResponse
from backend.schemas.advisory import MarketAdvisoryRequest, MarketAdvisoryResponse
import base64

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze-disease", response_model=DiseaseAnalysisResponse)
def analyze_disease(request: DiseaseAnalysisRequest):
# ... (existing code remains)
    """
    Analyze a crop image (base64) for diseases using Google Gemini AI.
    """
    result = analyze_crop_image(request.image_base64)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result

@router.post("/analyze-disease-file", response_model=DiseaseAnalysisResponse)
async def analyze_disease_file(file: UploadFile = File(...)):
    """
    Analyze a crop image (file upload) for diseases using Google Gemini AI.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        contents = await file.read()
        # Convert to base64 to reuse the existing service logic
        image_base64 = base64.b64encode(contents).decode("utf-8")
        result = analyze_crop_image(image_base64)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/market-advisory", response_model=MarketAdvisoryResponse)
def get_market_advisory(request: MarketAdvisoryRequest, db: Session = Depends(get_db)):
    """
    Get personalized market advisory based on crop and location.
    Combines market prices and weather forecasts.
    """
    return generate_market_advisory(db, request.commodity, request.city, request.district)
