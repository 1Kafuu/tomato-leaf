from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import os
import tempfile

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.prediction import PredictionResponse, PredictionData, PredictionFeatures
from app.crud.prediction import create_prediction
from app.core.model.pipeline import predict
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

    file_ext = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=f".{file_ext}", delete=False) as tmp:
            tmp.write(image_bytes)
            tmp.flush()
            temp_file_path = tmp.name

        result = predict(temp_file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run prediction model: {e}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass

    file_ext = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_ext}"

    image_url = await upload_image_to_storage(image_bytes, filename)
    if not image_url:
        raise HTTPException(status_code=500, detail="Failed to upload image to storage")

    prediction_record = await create_prediction(
        db=db,
        user_id=current_user.id,
        image_url=image_url,
        features={
            "spot_area": result["spot_area"],
            "yellow_ratio": result["yellow_ratio"],
            "brown_ratio": result["brown_ratio"],
            "dark_ratio": result["dark_ratio"],
            "color_change": result["color_change"],
        },
        fuzzy_score=result["fuzzy_score"],
        disease_name=result["disease_name"],
        severity_level=result["severity_level"]
    )
    
    prediction_data = PredictionData(
        disease_name=result["disease_name"],
        fuzzy_score=result["fuzzy_score"],
        severity_level=result["severity_level"],
        plant_status=result["plant_status"],
        features=PredictionFeatures(
            spot_area=result["spot_area"],
            yellow_ratio=result["yellow_ratio"],
            brown_ratio=result["brown_ratio"],
            dark_ratio=result["dark_ratio"],
            color_change=result["color_change"]
        )
    )

    return PredictionResponse(data=prediction_data)
