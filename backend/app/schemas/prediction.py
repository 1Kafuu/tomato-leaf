from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class PredictionFeatures(BaseModel):
    spot_area: float
    yellow_ratio: float
    brown_ratio: float
    dark_ratio: float
    color_change: float

class PredictionData(BaseModel):
    disease_name: str
    fuzzy_score: float
    severity_level: str
    plant_status: str
    features: PredictionFeatures

class PredictionResponse(BaseModel):
    success: bool = True
    message: str = "Prediksi berhasil"
    data: PredictionData

class PredictionHistoryResponse(BaseModel):
    id: UUID
    image_url: str
    disease_name: str
    fuzzy_score: float
    severity_level: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PredictionHistoryDetailResponse(PredictionHistoryResponse):
    spot_area: float
    yellow_ratio: float
    brown_ratio: float
    dark_ratio: float
    color_change: float

class FeatureData(BaseModel):
    spot_area: float
    yellow_ratio: float
    brown_ratio: float
    dark_ratio: float
    color_change: float

class Pagination(BaseModel):
    page: int
    size: int
    total_items: int
    total_pages: int
