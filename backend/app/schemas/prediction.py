from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class PredictionFeatures(BaseModel):
    spot_area: float
    color_change: float
    yellow_ratio: float
    brown_ratio: float
    dark_ratio: float
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

# PredictionRecord schemas
class PredictionRecordResponse(BaseModel):
    id: UUID
    success: bool = True
    message: str = "Prediksi berhasil"
    image_url: str
    plant_status: str
    severity_level: str
    fuzzy_score: float
    severity_score: float
    features: PredictionFeatures
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionRecordDetailResponse(PredictionRecordResponse):
    spot_area: float
    color_change: float
    yellow_ratio: float
    brown_ratio: float
    dark_ratio: float
    spot_count: int
    texture_var: float


# ===== Helper: compose features nested dari field flat SQLAlchemy =====
def build_features_from_record(record) -> PredictionFeatures:
    """Bangun PredictionFeatures dari objek SQLAlchemy PredictionRecord."""
    return PredictionFeatures(
        spot_area=float(record.spot_area),
        color_change=float(record.color_change),
        yellow_ratio=float(record.yellow_ratio),
        brown_ratio=float(record.brown_ratio),
        dark_ratio=float(record.dark_ratio),
        spot_count=int(record.spot_count) if record.spot_count is not None else 0,
        texture_var=float(record.texture_var) if record.texture_var is not None else 0.0,
    )


def build_record_response(record) -> PredictionRecordResponse:
    """Bangun PredictionRecordResponse dari objek SQLAlchemy PredictionRecord."""
    return PredictionRecordResponse(
        id=record.id,
        image_url=record.image_url,
        plant_status=record.plant_status,
        severity_level=record.severity_level,
        fuzzy_score=float(record.fuzzy_score),
        severity_score=float(record.severity_score),
        features=build_features_from_record(record),
        created_at=record.created_at,
    )


def build_record_detail_response(record) -> PredictionRecordDetailResponse:
    """Bangun PredictionRecordDetailResponse dari objek SQLAlchemy PredictionRecord."""
    return PredictionRecordDetailResponse(
        id=record.id,
        image_url=record.image_url,
        plant_status=record.plant_status,
        severity_level=record.severity_level,
        fuzzy_score=float(record.fuzzy_score),
        severity_score=float(record.severity_score),
        features=build_features_from_record(record),
        spot_area=float(record.spot_area),
        color_change=float(record.color_change),
        yellow_ratio=float(record.yellow_ratio),
        brown_ratio=float(record.brown_ratio),
        dark_ratio=float(record.dark_ratio),
        spot_count=int(getattr(record, "spot_count", None) or 0),
        texture_var=float(getattr(record, "texture_var", None) or 0.0),
        created_at=record.created_at,
    )
