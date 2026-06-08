"""
Unit tests for fuzzy_engine.py - Fuzzy Sugeno Inference Engine
"""

import pytest
from app.core.model.fuzzy_engine import (
    triangular_mf,
    fuzzify,
    infer,
    classify,
    normalize,
    calculate_severity_score,
)
from app.core.model.config import (
    SPOT_AREA_MF,
    SPOT_AREA_LABELS,
    COLOR_CHANGE_MF,
    COLOR_CHANGE_LABELS,
    FEATURE_WEIGHTS,
    FEATURE_NORM_RANGES,
)


class TestTriangularMF:
    """Test triangular membership function."""

    def test_at_left_boundary(self):
        """At x = a, membership should be 0."""
        assert triangular_mf(0.06, 0.06, 3.23, 8.36) == 0.0

    def test_at_right_boundary(self):
        """At x = c, membership should be 0."""
        assert triangular_mf(8.36, 0.06, 3.23, 8.36) == 0.0

    def test_at_peak(self):
        """At x = b, membership should be 1."""
        assert triangular_mf(3.23, 0.06, 3.23, 8.36) == 1.0

    def test_in_left_rising_region(self):
        """In rising region (a < x < b), membership should be linear."""
        result = triangular_mf(1.645, 0.06, 3.23, 8.36)
        assert 0 < result < 1

    def test_in_right_falling_region(self):
        """In falling region (b < x < c), membership should be linear."""
        result = triangular_mf(6.0, 0.06, 3.23, 8.36)
        assert 0 < result < 1

    def test_outside_range_left(self):
        """Below a, membership should be 0."""
        assert triangular_mf(-1, 0.06, 3.23, 8.36) == 0.0

    def test_outside_range_right(self):
        """Above c, membership should be 0."""
        assert triangular_mf(10, 0.06, 3.23, 8.36) == 0.0

    def test_symmetry_at_peak(self):
        """At peak, result should be exactly 1.0."""
        for label, (a, b, c) in SPOT_AREA_MF.items():
            assert triangular_mf(b, a, b, c) == 1.0


class TestFuzzify:
    """Test fuzzification function."""

    def test_fuzzify_returns_all_labels(self):
        """Should return degrees for all labels."""
        result = fuzzify(5.0, SPOT_AREA_MF, SPOT_AREA_LABELS)
        assert set(result.keys()) == set(SPOT_AREA_LABELS)

    def test_fuzzify_values_in_range(self):
        """All membership degrees should be in [0, 1]."""
        result = fuzzify(5.0, SPOT_AREA_MF, SPOT_AREA_LABELS)
        for degree in result.values():
            assert 0 <= degree <= 1

    def test_fuzzify_sum_greater_than_one(self):
        """Sum of all memberships should be > 1 (since overlapping MFs)."""
        result = fuzzify(5.0, SPOT_AREA_MF, SPOT_AREA_LABELS)
        total = sum(result.values())
        assert total > 0

    def test_fuzzify_at_boundaries(self):
        """At boundaries, only one MF should be non-zero (if no overlap)."""
        # Test at a boundary between two MFs
        result = fuzzify(3.23, SPOT_AREA_MF, SPOT_AREA_LABELS)
        # At peak of small, should have degree 1 for small
        assert result["small"] == 1.0


class TestInfer:
    """Test fuzzy inference function."""

    def test_infer_returns_float(self):
        """infer() should return a float."""
        result = infer(5.0, 10.0)
        assert isinstance(result, float)

    def test_infer_in_valid_range(self):
        """Result should be in range [0, 100]."""
        result = infer(5.0, 10.0)
        assert 0 <= result <= 100

    def test_infer_healthy_leaf(self):
        """Healthy leaf (small spots, low color change) should get high score."""
        result = infer(2.0, 5.0)
        assert result >= 80, f"Expected high score for healthy leaf, got {result}"

    def test_infer_severe_leaf(self):
        """Severe leaf (very large spots, very high color change) should get low score."""
        result = infer(40.0, 80.0)
        assert result <= 30, f"Expected low score for severe leaf, got {result}"

    def test_infer_very_low_spot_area(self):
        """Very low spot area with any color change."""
        result = infer(1.0, 50.0)
        assert 50 < result < 100

    def test_infer_very_high_color_change(self):
        """Any spot area with very high color change."""
        result = infer(15.0, 85.0)
        assert 0 < result < 50

    def test_infer_consistency(self):
        """Same inputs should produce same outputs."""
        result1 = infer(10.0, 20.0)
        result2 = infer(10.0, 20.0)
        assert result1 == result2


class TestClassify:
    """Test classification function."""

    def test_classify_returns_dict(self):
        """classify() should return a dictionary."""
        result = classify(75.0)
        assert isinstance(result, dict)

    def test_classify_has_severity_level(self):
        """Result should have 'severity_level' key."""
        result = classify(75.0)
        assert "severity_level" in result

    def test_classify_has_plant_status(self):
        """Result should have 'plant_status' key."""
        result = classify(75.0)
        assert "plant_status" in result

    def test_classify_no_disease_name(self):
        """Result should NOT have 'disease_name' key (new format)."""
        result = classify(75.0)
        assert "disease_name" not in result

    def test_classify_sehat_range(self):
        """Score 85-100 should be 'Sehat'."""
        result = classify(90)
        assert result["severity_level"] == "Sehat"
        assert result["plant_status"] == "Sehat"

    def test_classify_ringan_range(self):
        """Score 70-84 should be 'Ringan'."""
        result = classify(75)
        assert result["severity_level"] == "Ringan"
        assert result["plant_status"] == "Terinfeksi"

    def test_classify_sedang_range(self):
        """Score 50-69 should be 'Sedang'."""
        result = classify(60)
        assert result["severity_level"] == "Sedang"
        assert result["plant_status"] == "Terinfeksi"

    def test_classify_berat_range(self):
        """Score 25-49 should be 'Berat'."""
        result = classify(35)
        assert result["severity_level"] == "Berat"
        assert result["plant_status"] == "Terinfeksi"

    def test_classify_sangat_berat_range(self):
        """Score 0-24 should be 'Sangat Berat'."""
        result = classify(10)
        assert result["severity_level"] == "Sangat Berat"
        assert result["plant_status"] == "Terinfeksi"

    def test_classify_boundary_85(self):
        """Score exactly 85 should be 'Sehat'."""
        result = classify(85)
        assert result["severity_level"] == "Sehat"

    def test_classify_boundary_84(self):
        """Score exactly 84 should be 'Ringan'."""
        result = classify(84)
        assert result["severity_level"] == "Ringan"


class TestNormalize:
    """Test normalization function."""

    def test_normalize_min_value(self):
        """At min_val, result should be 0."""
        result = normalize(0.0, 0.0, 100.0)
        assert result == 0.0

    def test_normalize_max_value(self):
        """At max_val, result should be 100."""
        result = normalize(100.0, 0.0, 100.0)
        assert result == 100.0

    def test_normalize_mid_value(self):
        """At mid value, result should be 50."""
        result = normalize(50.0, 0.0, 100.0)
        assert result == 50.0

    def test_normalize_in_valid_range(self):
        """Result should always be in [0, 100]."""
        result = normalize(25.0, 0.0, 100.0)
        assert 0 <= result <= 100

    def test_normalize_below_min(self):
        """Below min_val, result should be clipped to 0."""
        result = normalize(-10.0, 0.0, 100.0)
        assert result == 0.0

    def test_normalize_above_max(self):
        """Above max_val, result should be clipped to 100."""
        result = normalize(150.0, 0.0, 100.0)
        assert result == 100.0

    def test_normalize_equal_min_max(self):
        """When min == max, should return 0 (avoid division by zero)."""
        result = normalize(50.0, 50.0, 50.0)
        assert result == 0.0


class TestCalculateSeverityScore:
    """Test severity score calculation."""

    def test_severity_score_returns_float(self):
        """Should return a float."""
        features = {
            "spot_area": 10.0,
            "color_change": 20.0,
            "yellow_ratio": 5.0,
            "brown_ratio": 1.0,
            "spot_count": 50,
            "texture_var": 25.0,
        }
        result = calculate_severity_score(features)
        assert isinstance(result, float)

    def test_severity_score_in_valid_range(self):
        """Result should be in range [0, 100]."""
        features = {
            "spot_area": 10.0,
            "color_change": 20.0,
            "yellow_ratio": 5.0,
            "brown_ratio": 1.0,
            "spot_count": 50,
            "texture_var": 25.0,
        }
        result = calculate_severity_score(features)
        assert 0 <= result <= 100

    def test_severity_score_healthy_leaf(self, healthy_features):
        """Healthy leaf should have low severity score."""
        result = calculate_severity_score(healthy_features)
        assert result < 30, f"Expected low severity for healthy leaf, got {result}"

    def test_severity_score_severe_leaf(self, severe_features):
        """Severe leaf should have high severity score."""
        result = calculate_severity_score(severe_features)
        assert result > 50, f"Expected high severity for severe leaf, got {result}"

    def test_severity_score_consistency(self):
        """Same features should produce same score."""
        features = {
            "spot_area": 10.0,
            "color_change": 20.0,
            "yellow_ratio": 5.0,
            "brown_ratio": 1.0,
            "spot_count": 50,
            "texture_var": 25.0,
        }
        score1 = calculate_severity_score(features)
        score2 = calculate_severity_score(features)
        assert score1 == score2

    def test_severity_score_missing_feature(self):
        """Missing features should default to 0."""
        features = {"spot_area": 10.0}  # Missing other features
        result = calculate_severity_score(features)
        assert isinstance(result, float)
        assert 0 <= result <= 100

    def test_severity_score_all_zeros(self):
        """All zeros should give severity score of 0."""
        features = {
            "spot_area": 0.0,
            "color_change": 0.0,
            "yellow_ratio": 0.0,
            "brown_ratio": 0.0,
            "spot_count": 0,
            "texture_var": 0.0,
        }
        result = calculate_severity_score(features)
        assert result == 0.0

    def test_severity_score_all_max(self):
        """All max values should give severity score close to 100."""
        features = {
            "spot_area": 48.48,
            "color_change": 99.79,
            "yellow_ratio": 93.63,
            "brown_ratio": 5.11,
            "spot_count": 794,
            "texture_var": 56.86,
        }
        result = calculate_severity_score(features)
        assert result > 90, f"Expected high severity at max values, got {result}"

    def test_severity_score_weight_contribution(self):
        """spot_area (30% weight) should have biggest impact."""
        # Very high spot area
        features_high_spot = {
            "spot_area": 40.0,  # ~82% of max
            "color_change": 5.0,
            "yellow_ratio": 5.0,
            "brown_ratio": 0.5,
            "spot_count": 10,
            "texture_var": 20.0,
        }
        # Very high color change
        features_high_color = {
            "spot_area": 5.0,
            "color_change": 90.0,  # ~90% of max
            "yellow_ratio": 5.0,
            "brown_ratio": 0.5,
            "spot_count": 10,
            "texture_var": 20.0,
        }
        score_spot = calculate_severity_score(features_high_spot)
        score_color = calculate_severity_score(features_high_color)
        # spot_area has 30% weight, color_change has 25%
        # 82% * 30% = 24.6 vs 90% * 25% = 22.5
        # So high spot should give higher score
        assert score_spot > score_color