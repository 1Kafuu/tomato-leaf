from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import tempfile
import os

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionResponse, PredictionData, PredictionFeatures
from app.crud.prediction import create_prediction
from app.core.model.pipeline import predict as model_predict
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
    
    # Save uploaded image to temp file for model pipeline
    file_ext = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_ext}"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name
    
    try:
        # Run model pipeline (core/model)
        result = model_predict(tmp_path)
    except Exception as e:
        os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Upload to storage
    image_url = await upload_image_to_storage(image_bytes, filename)
    
    # Build features dict from pipeline result
    features = {
        "spot_area": result["spot_area"],
        "yellow_ratio": result["yellow_ratio"],
        "brown_ratio": result["brown_ratio"],
        "dark_ratio": result["dark_ratio"],
        "color_change": result["color_change"],
    }
    
    # Save to database
    prediction_record = await create_prediction(
        db=db,
        user_id=current_user.id,
        image_url=image_url,
        features=features,
        fuzzy_score=result["fuzzy_score"],
        disease_name=result["disease_name"],
        severity_level=result["severity_level"]
    )
    
    prediction_data = PredictionData(
        disease_name=result["disease_name"],
        fuzzy_score=result["fuzzy_score"],
        severity_level=result["severity_level"],
        plant_status=result["plant_status"],
        features=PredictionFeatures(**features)
    )
    
    return PredictionResponse(data=prediction_data)
