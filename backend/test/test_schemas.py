"""
Unit tests for prediction.py - Pydantic Schemas
"""

import pytest
from pydantic import ValidationError
from app.schemas.prediction import (
    PredictionFeatures,
    PredictionData,
    PredictionResponse,
    PredictionHistoryResponse,
    PredictionHistoryDetailResponse,
    FeatureData,
    Pagination,
)


class TestPredictionFeatures:
    """Test PredictionFeatures schema."""

    def test_valid_features(self):
        """Should accept valid 6 features."""
        features = PredictionFeatures(
            spot_area=12.5,
            color_change=25.0,
            yellow_ratio=10.0,
            brown_ratio=2.0,
            spot_count=50,
            texture_var=28.5,
        )
        assert features.spot_area == 12.5
        assert features.spot_count == 50

    def test_no_disease_name(self):
        """Should NOT have disease_name field."""
        with pytest.raises(ValidationError):
            PredictionFeatures(disease_name="EarlyBlight")

    def test_no_dark_ratio(self):
        """Should NOT have dark_ratio field."""
        with pytest.raises(ValidationError):
            PredictionFeatures(dark_ratio=5.0)

    def test_spot_count_is_int(self):
        """spot_count should be integer."""
        features = PredictionFeatures(
            spot_area=10.0, color_change=20.0, yellow_ratio=5.0,
            brown_ratio=1.0, spot_count=50, texture_var=25.0,
        )
        assert isinstance(features.spot_count, int)


class TestPredictionData:
    """Test PredictionData schema."""

    def test_valid_prediction_data(self):
        """Should accept valid prediction data."""
        data = PredictionData(
            plant_status="Terinfeksi",
            severity_level="Ringan",
            fuzzy_score=75.0,
            severity_score=35.0,
            features=PredictionFeatures(
                spot_area=12.5, color_change=25.0, yellow_ratio=10.0,
                brown_ratio=2.0, spot_count=50, texture_var=28.5,
            ),
        )
        assert data.plant_status == "Terinfeksi"
        assert data.severity_score == 35.0

    def test_no_disease_name(self):
        """Should NOT have disease_name field."""
        with pytest.raises(ValidationError):
            PredictionData(
                disease_name="EarlyBlight",
                plant_status="Terinfeksi",
                severity_level="Ringan",
                fuzzy_score=75.0,
                severity_score=35.0,
                features=PredictionFeatures(
                    spot_area=12.5, color_change=25.0, yellow_ratio=10.0,
                    brown_ratio=2.0, spot_count=50, texture_var=28.5,
                ),
            )

    def test_has_severity_score(self):
        """Should have severity_score field."""
        data = PredictionData(
            plant_status="Sehat",
            severity_level="Sehat",
            fuzzy_score=90.0,
            severity_score=15.0,
            features=PredictionFeatures(
                spot_area=2.0, color_change=5.0, yellow_ratio=1.0,
                brown_ratio=0.5, spot_count=5, texture_var=18.0,
            ),
        )
        assert hasattr(data, "severity_score")


class TestPredictionResponse:
    """Test PredictionResponse schema."""

    def test_valid_response(self):
        """Should accept valid API response."""
        response = PredictionResponse(
            success=True,
            message="Prediksi berhasil",
            data=PredictionData(
                plant_status="Terinfeksi",
                severity_level="Ringan",
                fuzzy_score=75.0,
                severity_score=35.0,
                features=PredictionFeatures(
                    spot_area=12.5, color_change=25.0, yellow_ratio=10.0,
                    brown_ratio=2.0, spot_count=50, texture_var=28.5,
                ),
            ),
        )
        assert response.success is True
        assert response.data.severity_level == "Ringan"

    def test_default_values(self):
        """Should have correct default values."""
        response = PredictionResponse(
            data=PredictionData(
                plant_status="Sehat",
                severity_level="Sehat",
                fuzzy_score=90.0,
                severity_score=10.0,
                features=PredictionFeatures(
                    spot_area=2.0, color_change=5.0, yellow_ratio=1.0,
                    brown_ratio=0.5, spot_count=5, texture_var=18.0,
                ),
            ),
        )
        assert response.success is True
        assert response.message == "Prediksi berhasil"


class TestPredictionHistoryResponse:
    """Test PredictionHistoryResponse schema."""

    def test_valid_history_response(self):
        """Should accept valid history response."""
        from uuid import uuid4
        from datetime import datetime

        history = PredictionHistoryResponse(
            id=uuid4(),
            image_url="http://example.com/image.jpg",
            severity_level="Ringan",
            plant_status="Terinfeksi",
            fuzzy_score=75.0,
            severity_score=35.0,
            created_at=datetime.now(),
        )
        assert history.severity_level == "Ringan"
        assert history.severity_score == 35.0

    def test_no_disease_name(self):
        """Should NOT have disease_name field."""
        from uuid import uuid4
        from datetime import datetime

        with pytest.raises(ValidationError):
            PredictionHistoryResponse(
                id=uuid4(),
                image_url="http://example.com/image.jpg",
                disease_name="EarlyBlight",
                severity_level="Ringan",
                plant_status="Terinfeksi",
                fuzzy_score=75.0,
                severity_score=35.0,
                created_at=datetime.now(),
            )


class TestPredictionHistoryDetailResponse:
    """Test PredictionHistoryDetailResponse schema."""

    def test_valid_detail_response(self):
        """Should accept valid detail response with features."""
        from uuid import uuid4
        from datetime import datetime

        detail = PredictionHistoryDetailResponse(
            id=uuid4(),
            image_url="http://example.com/image.jpg",
            severity_level="Ringan",
            plant_status="Terinfeksi",
            fuzzy_score=75.0,
            severity_score=35.0,
            created_at=datetime.now(),
            spot_area=12.5,
            color_change=25.0,
            yellow_ratio=10.0,
            brown_ratio=2.0,
            spot_count=50,
            texture_var=28.5,
        )
        assert detail.spot_area == 12.5
        assert detail.spot_count == 50

    def test_has_all_6_features(self):
        """Should have all 6 features."""
        from uuid import uuid4
        from datetime import datetime

        detail = PredictionHistoryDetailResponse(
            id=uuid4(),
            image_url="http://example.com/image.jpg",
            severity_level="Ringan",
            plant_status="Terinfeksi",
            fuzzy_score=75.0,
            severity_score=35.0,
            created_at=datetime.now(),
            spot_area=12.5,
            color_change=25.0,
            yellow_ratio=10.0,
            brown_ratio=2.0,
            spot_count=50,
            texture_var=28.5,
        )

        expected = ["spot_area", "color_change", "yellow_ratio",
                   "brown_ratio", "spot_count", "texture_var"]
        for key in expected:
            assert hasattr(detail, key)


class TestFeatureData:
    """Test FeatureData schema."""

    def test_valid_feature_data(self):
        """Should accept valid feature data."""
        data = FeatureData(
            spot_area=12.5,
            color_change=25.0,
            yellow_ratio=10.0,
            brown_ratio=2.0,
            spot_count=50,
            texture_var=28.5,
        )
        assert data.spot_area == 12.5

    def test_no_dark_ratio(self):
        """Should NOT have dark_ratio field."""
        with pytest.raises(ValidationError):
            FeatureData(
                spot_area=12.5, color_change=25.0, yellow_ratio=10.0,
                brown_ratio=2.0, spot_count=50, texture_var=28.5, dark_ratio=5.0,
            )


class TestPagination:
    """Test Pagination schema."""

    def test_valid_pagination(self):
        """Should accept valid pagination."""
        pagination = Pagination(
            page=1,
            size=10,
            total_items=100,
            total_pages=10,
        )
        assert pagination.page == 1
        assert pagination.total_pages == 10