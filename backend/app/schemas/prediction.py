from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class PredictionFeatures(BaseModel):
    spot_area: float
    color_change: float
    yellow_ratio: float
    brown_ratio: float
    spot_count: int
    texture_var: float

class PredictionData(BaseModel):
    plant_status: str
    severity_level: str
    fuzzy_score: float
    severity_score: float
    features: PredictionFeatures

class PredictionResponse(BaseModel):
    success: bool = True
    message: str = "Prediksi berhasil"
    data: PredictionData

class PredictionHistoryResponse(BaseModel):
    id: UUID
    image_url: str
    severity_level: str
    plant_status: str
    fuzzy_score: float
    severity_score: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PredictionHistoryDetailResponse(PredictionHistoryResponse):
    spot_area: float
    color_change: float
    yellow_ratio: float
    brown_ratio: float
    spot_count: int
    texture_var: float

class FeatureData(BaseModel):
    spot_area: float
    color_change: float
    yellow_ratio: float
    brown_ratio: float
    spot_count: int
    texture_var: float

class Pagination(BaseModel):
    page: int
    size: int
    total_items: int
    total_pages: int