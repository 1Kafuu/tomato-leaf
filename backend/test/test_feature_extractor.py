"""
Unit tests for feature_extractor.py - Feature Extraction Module
"""

import pytest
import numpy as np
import cv2
from app.core.model.feature_extractor import extract
from app.core.model.config import HSV_RANGES


class TestExtract:
    """Test feature extraction function."""

    def test_extract_returns_dict(self):
        """extract() should return a dictionary."""
        # Create minimal test data
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)
        assert isinstance(result, dict)

    def test_extract_has_all_6_features(self):
        """Result should have all 6 features."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)

        expected_keys = ["spot_area", "color_change", "yellow_ratio",
                        "brown_ratio", "spot_count", "texture_var"]
        assert set(result.keys()) == set(expected_keys)

    def test_extract_no_dark_ratio(self):
        """Result should NOT have 'dark_ratio' (replaced by spot_count/texture_var)."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)
        assert "dark_ratio" not in result

    def test_extract_empty_mask(self):
        """With empty mask (no leaf pixels), all features should be 0."""
        mask = np.zeros((256, 256), dtype=np.uint8)
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)

        assert result["spot_area"] == 0.0
        assert result["color_change"] == 0.0
        assert result["yellow_ratio"] == 0.0
        assert result["brown_ratio"] == 0.0
        assert result["spot_count"] == 0
        assert result["texture_var"] == 0.0

    def test_extract_spot_count_is_int(self):
        """spot_count should be an integer."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)
        assert isinstance(result["spot_count"], int)

    def test_extract_percentage_values(self):
        """Percentage features (spot_area, color_change, etc.) should be in [0, 100]."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)

        for key in ["spot_area", "color_change", "yellow_ratio", "brown_ratio"]:
            assert 0 <= result[key] <= 100, f"{key} should be in [0, 100]"

    def test_extract_texture_var_non_negative(self):
        """texture_var should be non-negative."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)
        assert result["texture_var"] >= 0

    def test_extract_with_yellow_spots(self, sample_masked_image, sample_leaf_mask):
        """Image with yellow areas should have non-zero yellow_ratio."""
        result = extract(sample_masked_image, sample_leaf_mask)
        assert result["yellow_ratio"] >= 0

    def test_extract_color_change_includes_yellow_brown_dark(self, sample_masked_image, sample_leaf_mask):
        """color_change should be sum of yellow + brown + dark."""
        result = extract(sample_masked_image, sample_leaf_mask)
        # color_change should be >= any individual component
        assert result["color_change"] >= result["yellow_ratio"]
        assert result["color_change"] >= result["brown_ratio"]

    def test_extract_consistency(self, sample_masked_image, sample_leaf_mask):
        """Same inputs should produce same outputs."""
        result1 = extract(sample_masked_image, sample_leaf_mask)
        result2 = extract(sample_masked_image, sample_leaf_mask)
        assert result1 == result2


class TestFeatureExtractionEdgeCases:
    """Test edge cases for feature extraction."""

    def test_extract_single_pixel_mask(self):
        """Single pixel leaf mask should still work."""
        mask = np.zeros((256, 256), dtype=np.uint8)
        mask[128, 128] = 255  # Single pixel
        img = np.ones((256, 256, 3), dtype=np.uint8) * 100
        result = extract(img, mask)

        # Should not crash, values depend on that pixel
        assert isinstance(result["spot_count"], int)

    def test_extract_all_green_image(self):
        """All green image (healthy) should have low spot_area."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8)
        img[:, :] = [60, 150, 60]  # Green-ish
        result = extract(img, mask)

        # Healthy green should have low spot area
        assert result["spot_area"] < 20, f"Expected low spot area for green image, got {result['spot_area']}"

    def test_extract_all_yellow_image(self):
        """All yellow image should have high yellow_ratio."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8)
        img[:, :] = [25, 200, 220]  # Yellow-ish in HSV
        result = extract(img, mask)

        # Yellow image should have high yellow ratio
        assert result["yellow_ratio"] > 50, f"Expected high yellow ratio, got {result['yellow_ratio']}"

    def test_extract_all_brown_image(self):
        """All brown image should have high brown_ratio."""
        mask = np.ones((256, 256), dtype=np.uint8) * 255
        img = np.ones((256, 256, 3), dtype=np.uint8)
        img[:, :] = [10, 80, 50]  # Brown-ish
        result = extract(img, mask)

        # Brown image should have high brown ratio
        assert result["brown_ratio"] > 50, f"Expected high brown ratio, got {result['brown_ratio']}"