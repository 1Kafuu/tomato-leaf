from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from .base import Base

class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    spot_area = Column(Numeric(5, 2), nullable=False)
    yellow_ratio = Column(Numeric(5, 2), nullable=False)
    brown_ratio = Column(Numeric(5, 2), nullable=False)
    dark_ratio = Column(Numeric(5, 2), nullable=False)
    color_change = Column(Numeric(5, 2), nullable=False)
    fuzzy_score = Column(Numeric(5, 2), nullable=False)
    disease_name = Column(String(100), nullable=False)
    severity_level = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PredictionRecord(Base):
    __tablename__ = "prediction_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    spot_area = Column(Numeric(5, 2), nullable=False)
    yellow_ratio = Column(Numeric(5, 2), nullable=False)
    brown_ratio = Column(Numeric(5, 2), nullable=False)
    dark_ratio = Column(Numeric(5, 2), nullable=False)
    color_change = Column(Numeric(5, 2), nullable=False)
    fuzzy_score = Column(Numeric(5, 2), nullable=False)
    severity_score = Column(Numeric(5, 2), nullable=False)
    severity_level = Column(String(50), nullable=False)
    plant_status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
