from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.prediction import (
    PredictionRecordResponse,
    PredictionRecordDetailResponse,
    build_record_response,
    build_record_detail_response,
)
from app.crud.prediction import (
    get_user_prediction_records,
    get_prediction_record_by_id,
)

router = APIRouter()


@router.get("/", response_model=List[PredictionRecordResponse])
async def get_history(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = await get_user_prediction_records(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return [build_record_response(r) for r in records]


@router.get("/{prediction_id}", response_model=PredictionRecordDetailResponse)
async def get_history_detail(
    prediction_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction = await get_prediction_record_by_id(db=db, prediction_id=prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    if prediction.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this prediction"
        )

    return build_record_detail_response(prediction)
