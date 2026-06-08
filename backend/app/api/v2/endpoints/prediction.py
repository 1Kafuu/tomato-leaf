from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import tempfile
import os

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionRecordResponse, PredictionFeatures
from app.crud.prediction import create_prediction_record
from app.core.model.pipeline import predict as model_predict
from app.services.supabase_service import upload_image_to_storage

router = APIRouter()

@router.post("/predict", response_model=PredictionRecordResponse)
async def predict_disease_v2(
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    image_bytes = await image.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 10MB")
    
    file_ext = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_ext}"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name
    
    try:
        result = model_predict(tmp_path)
    except Exception as e:
        os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    image_url = await upload_image_to_storage(image_bytes, filename)
    
    features = {
        "spot_area": result["features"]["spot_area"],
        "yellow_ratio": result["features"]["yellow_ratio"],
        "brown_ratio": result["features"]["brown_ratio"],
        "dark_ratio": result["features"]["dark_ratio"],
        "color_change": result["features"]["color_change"],
    }
    
    prediction_record = await create_prediction_record(
        db=db,
        user_id=current_user.id,
        image_url=image_url,
        features=features,
        fuzzy_score=result["fuzzy_score"],
        severity_score=result["severity_score"],
        severity_level=result["severity_level"],
        plant_status=result["plant_status"],
    )
    
    return PredictionRecordResponse(
        id=prediction_record.id,
        image_url=prediction_record.image_url,
        severity_level=prediction_record.severity_level,
        plant_status=prediction_record.plant_status,
        fuzzy_score=prediction_record.fuzzy_score,
        severity_score=prediction_record.severity_score,
        features=PredictionFeatures(
            spot_area=features["spot_area"],
            color_change=features["color_change"],
            yellow_ratio=features["yellow_ratio"],
            brown_ratio=features["brown_ratio"],
            dark_ratio=features["dark_ratio"],
            spot_count=result.get("spot_count", 0),
            texture_var=result.get("texture_var", 0.0),
        ),
        created_at=prediction_record.created_at,
    )