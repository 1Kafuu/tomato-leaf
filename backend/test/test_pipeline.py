"""
Unit tests for pipeline.py - Pipeline Orchestrator
"""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np

from app.core.model.pipeline import predict


class TestPredict:
    """Test the main predict function."""

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_returns_correct_format(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """predict() should return the new format with severity_score."""
        # Setup mocks
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        mock_extract.return_value = {
            "spot_area": 10.0,
            "color_change": 20.0,
            "yellow_ratio": 5.0,
            "brown_ratio": 1.0,
            "spot_count": 15,
            "texture_var": 25.0,
        }
        mock_infer.return_value = 75.0
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 35.0

        result = predict("dummy_path.jpg")

        # Check top-level keys
        assert "plant_status" in result
        assert "severity_level" in result
        assert "fuzzy_score" in result
        assert "severity_score" in result
        assert "features" in result

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_no_disease_name(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """predict() should NOT return 'disease_name' (new format)."""
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        mock_extract.return_value = {
            "spot_area": 10.0, "color_change": 20.0, "yellow_ratio": 5.0,
            "brown_ratio": 1.0, "spot_count": 15, "texture_var": 25.0,
        }
        mock_infer.return_value = 75.0
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 35.0

        result = predict("dummy_path.jpg")

        assert "disease_name" not in result

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_features_nested(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """Features should be nested under 'features' key."""
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        mock_extract.return_value = {
            "spot_area": 10.0, "color_change": 20.0, "yellow_ratio": 5.0,
            "brown_ratio": 1.0, "spot_count": 15, "texture_var": 25.0,
        }
        mock_infer.return_value = 75.0
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 35.0

        result = predict("dummy_path.jpg")

        assert isinstance(result["features"], dict)
        expected_features = ["spot_area", "color_change", "yellow_ratio",
                            "brown_ratio", "spot_count", "texture_var"]
        assert set(result["features"].keys()) == set(expected_features)

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_calls_calculate_severity_score(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """predict() should call calculate_severity_score."""
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        mock_extract.return_value = {
            "spot_area": 10.0, "color_change": 20.0, "yellow_ratio": 5.0,
            "brown_ratio": 1.0, "spot_count": 15, "texture_var": 25.0,
        }
        mock_infer.return_value = 75.0
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 35.0

        predict("dummy_path.jpg")

        mock_severity.assert_called_once()

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_severity_score_in_result(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """Result should include severity_score."""
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        mock_extract.return_value = {
            "spot_area": 10.0, "color_change": 20.0, "yellow_ratio": 5.0,
            "brown_ratio": 1.0, "spot_count": 15, "texture_var": 25.0,
        }
        mock_infer.return_value = 75.0
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 42.5

        result = predict("dummy_path.jpg")

        assert result["severity_score"] == 42.5

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_fuzzy_score_in_result(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """Result should include fuzzy_score."""
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        mock_extract.return_value = {
            "spot_area": 10.0, "color_change": 20.0, "yellow_ratio": 5.0,
            "brown_ratio": 1.0, "spot_count": 15, "texture_var": 25.0,
        }
        mock_infer.return_value = 82.5
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 35.0

        result = predict("dummy_path.jpg")

        assert result["fuzzy_score"] == 82.5

    @patch('app.core.model.pipeline.segment')
    @patch('app.core.model.pipeline.extract')
    @patch('app.core.model.pipeline.infer')
    @patch('app.core.model.pipeline.classify')
    @patch('app.core.model.pipeline.calculate_severity_score')
    def test_predict_passes_features_to_severity(
        self, mock_severity, mock_classify, mock_infer, mock_extract, mock_segment
    ):
        """predict() should pass extracted features to calculate_severity_score."""
        mock_segment.return_value = (np.ones((256, 256), dtype=np.uint8) * 255,
                                     np.ones((256, 256, 3), dtype=np.uint8) * 100)
        expected_features = {
            "spot_area": 12.5, "color_change": 22.0, "yellow_ratio": 6.0,
            "brown_ratio": 1.5, "spot_count": 20, "texture_var": 28.0,
        }
        mock_extract.return_value = expected_features
        mock_infer.return_value = 70.0
        mock_classify.return_value = {"severity_level": "Ringan", "plant_status": "Terinfeksi"}
        mock_severity.return_value = 40.0

        predict("dummy_path.jpg")

        # Verify the features dict was passed correctly
        call_args = mock_severity.call_args[0][0]
        assert call_args == expected_features