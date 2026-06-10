from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.prediction import PredictionHistory, PredictionRecord
from typing import List
from uuid import UUID

async def create_prediction(
    db: AsyncSession, 
    user_id: UUID, 
    image_url: str, 
    features: dict, 
    fuzzy_score: float, 
    disease_name: str, 
    severity_level: str
) -> PredictionHistory:
    db_prediction = PredictionHistory(
        user_id=user_id,
        image_url=image_url,
        spot_area=features["spot_area"],
        yellow_ratio=features["yellow_ratio"],
        brown_ratio=features["brown_ratio"],
        dark_ratio=features["dark_ratio"],
        color_change=features["color_change"],
        fuzzy_score=fuzzy_score,
        disease_name=disease_name,
        severity_level=severity_level
    )
    db.add(db_prediction)
    await db.commit()
    await db.refresh(db_prediction)
    return db_prediction

async def get_user_predictions(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 10) -> List[PredictionHistory]:
    result = await db.execute(
        select(PredictionHistory)
        .filter(PredictionHistory.user_id == user_id)
        .order_by(PredictionHistory.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())

async def get_prediction_by_id(db: AsyncSession, prediction_id: UUID) -> PredictionHistory | None:
    result = await db.execute(
        select(PredictionHistory).filter(PredictionHistory.id == prediction_id)
    )
    return result.scalars().first()


# PredictionRecord CRUD functions
async def create_prediction_record(
    db: AsyncSession,
    user_id: UUID,
    image_url: str,
    features: dict,
    fuzzy_score: float,
    severity_score: float,
    severity_level: str,
    plant_status: str,
) -> PredictionRecord:
    db_pred = PredictionRecord(
        user_id=user_id,
        image_url=image_url,
        spot_area=features["spot_area"],
        yellow_ratio=features["yellow_ratio"],
        brown_ratio=features["brown_ratio"],
        dark_ratio=features["dark_ratio"],
        color_change=features["color_change"],
        fuzzy_score=fuzzy_score,
        severity_score=severity_score,
        spot_count=features.get("spot_count"),
        texture_var=features.get("texture_var"),
        severity_level=severity_level,
        plant_status=plant_status,
    )
    db.add(db_pred)
    await db.commit()
    await db.refresh(db_pred)
    return db_pred


async def get_user_prediction_records(
    db: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
) -> List[PredictionRecord]:
    result = await db.execute(
        select(PredictionRecord)
        .filter(PredictionRecord.user_id == user_id)
        .order_by(PredictionRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_prediction_record_by_id(
    db: AsyncSession,
    prediction_id: UUID,
) -> PredictionRecord | None:
    result = await db.execute(
        select(PredictionRecord).filter(PredictionRecord.id == prediction_id)
    )
    return result.scalars().first()
