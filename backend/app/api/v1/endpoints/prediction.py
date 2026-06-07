from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionResponse, PredictionData, PredictionFeatures
from app.crud.prediction import create_prediction
from app.services.image_processor import extract_features
from app.services.fuzzy_engine import evaluate_fuzzy
from app.services.supabase_service import upload_image_to_storage

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
        
    image_bytes = await image.read()
    
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 10MB")
        
    # Process image
    try:
        features = extract_features(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # Evaluate fuzzy logic
    fuzzy_score, disease_name, severity = evaluate_fuzzy(
        spot_area=features["spot_area"],
        color_change=features["color_change"]
    )
    
    # Generate unique filename for storage
    file_ext = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_ext}"
    
    # Upload to storage
    image_url = await upload_image_to_storage(image_bytes, filename)
    
    plant_status = "Sehat" if disease_name in ["Sehat", "Sangat Sehat"] else "Terinfeksi"
    
    # Save to database
    prediction_record = await create_prediction(
        db=db,
        user_id=current_user.id,
        image_url=image_url,
        features=features,
        fuzzy_score=fuzzy_score,
        disease_name=disease_name,
        severity_level=severity
    )
    
    prediction_data = PredictionData(
        disease_name=disease_name,
        fuzzy_score=fuzzy_score,
        severity_level=severity,
        plant_status=plant_status,
        features=PredictionFeatures(**features)
    )
    
    return PredictionResponse(data=prediction_data)
