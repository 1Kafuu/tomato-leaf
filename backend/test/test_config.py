"""
Unit tests for config.py - Model Configuration
"""

import pytest
from app.core.model.config import (
    SPOT_AREA_MF,
    SPOT_AREA_LABELS,
    COLOR_CHANGE_MF,
    COLOR_CHANGE_LABELS,
    YELLOW_RATIO_MF,
    BROWN_RATIO_MF,
    SPOT_COUNT_MF,
    TEXTURE_VAR_MF,
    RULES,
    OUTPUT_CLASSES,
    DEFAULT_FUZZY_SCORE,
    FEATURE_WEIGHTS,
    FEATURE_NORM_RANGES,
    HSV_RANGES,
    IMAGE_SIZE,
)


class TestMembershipFunctionLabels:
    """Test that MF labels follow the new severity-based naming convention."""

    def test_spot_area_labels(self):
        """Spot area should use severity labels."""
        expected = ["small", "medium", "large", "very_large"]
        assert SPOT_AREA_LABELS == expected

    def test_color_change_labels(self):
        """Color change should use severity labels."""
        expected = ["low", "medium", "high", "very_high"]
        assert COLOR_CHANGE_LABELS == expected

    def test_spot_area_mf_count(self):
        """Spot area should have 4 membership functions."""
        assert len(SPOT_AREA_MF) == 4

    def test_color_change_mf_count(self):
        """Color change should have 4 membership functions."""
        assert len(COLOR_CHANGE_MF) == 4


class TestMembershipFunctionParameters:
    """Test that MF parameters are valid triangular functions (a < b < c)."""

    def test_spot_area_mf_parameters_valid(self):
        """All spot_area MF should have a < b < c."""
        for label, (a, b, c) in SPOT_AREA_MF.items():
            assert a < b < c, f"{label}: {a}, {b}, {c} should satisfy a < b < c"

    def test_color_change_mf_parameters_valid(self):
        """All color_change MF should have a < b < c."""
        for label, (a, b, c) in COLOR_CHANGE_MF.items():
            assert a < b < c, f"{label}: {a}, {b}, {c} should satisfy a < b < c"

    def test_yellow_ratio_mf_parameters_valid(self):
        """All yellow_ratio MF should have a < b < c."""
        for label, (a, b, c) in YELLOW_RATIO_MF.items():
            assert a < b < c, f"{label}: {a}, {b}, {c} should satisfy a < b < c"

    def test_brown_ratio_mf_parameters_valid(self):
        """All brown_ratio MF should have a < b < c."""
        for label, (a, b, c) in BROWN_RATIO_MF.items():
            assert a < b < c, f"{label}: {a}, {b}, {c} should satisfy a < b < c"


class TestFuzzyRules:
    """Test fuzzy rule base structure."""

    def test_rule_count(self):
        """Should have exactly 16 rules (4 spot x 4 color)."""
        assert len(RULES) == 16

    def test_rule_format(self):
        """Each rule should be a 3-tuple (spot_cat, color_cat, output)."""
        for rule in RULES:
            assert len(rule) == 3
            spot_cat, color_cat, output = rule
            assert isinstance(spot_cat, str)
            assert isinstance(color_cat, str)
            assert isinstance(output, (int, float))

    def test_rule_spot_categories_valid(self):
        """All spot categories in rules should be valid labels."""
        for spot_cat, color_cat, _ in RULES:
            assert spot_cat in SPOT_AREA_LABELS

    def test_rule_color_categories_valid(self):
        """All color categories in rules should be valid labels."""
        for spot_cat, color_cat, _ in RULES:
            assert color_cat in COLOR_CHANGE_LABELS

    def test_rule_outputs_in_range(self):
        """All rule outputs should be in range [0, 100]."""
        for _, _, output in RULES:
            assert 0 <= output <= 100


class TestOutputClasses:
    """Test output classification structure."""

    def test_output_class_count(self):
        """Should have 5 severity levels."""
        assert len(OUTPUT_CLASSES) == 5

    def test_output_class_format(self):
        """Each output class should be a 4-tuple (min, max, severity, status)."""
        for oc in OUTPUT_CLASSES:
            assert len(oc) == 4
            min_score, max_score, severity, status = oc
            assert isinstance(min_score, (int, float))
            assert isinstance(max_score, (int, float))
            assert isinstance(severity, str)
            assert isinstance(status, str)

    def test_output_class_ranges_valid(self):
        """All output class ranges should be valid (min < max)."""
        for min_score, max_score, _, _ in OUTPUT_CLASSES:
            assert min_score < max_score, f"min {min_score} should be < max {max_score}"

    def test_output_class_ranges_sequential(self):
        """Output classes should cover 0-100 without gaps or overlaps."""
        covered = set()
        for min_score, max_score, _, _ in OUTPUT_CLASSES:
            for i in range(int(min_score), int(max_score) + 1):
                covered.add(i)
        assert len(covered) == 101  # 0 to 100 inclusive


class TestSeverityLevels:
    """Test severity level naming."""

    def test_severity_levels(self):
        """Severity levels should be: Sehat, Ringan, Sedang, Berat, Sangat Berat."""
        expected_levels = ["Sehat", "Ringan", "Sedang", "Berat", "Sangat Berat"]
        actual_levels = [oc[2] for oc in OUTPUT_CLASSES]
        assert actual_levels == expected_levels

    def test_plant_status_mapping(self):
        """Only 'Sehat' should have 'Sehat' status, others 'Terinfeksi'."""
        for min_score, max_score, severity, status in OUTPUT_CLASSES:
            if severity == "Sehat":
                assert status == "Sehat"
            else:
                assert status == "Terinfeksi"


class TestFeatureWeights:
    """Test feature weights configuration."""

    def test_weight_count(self):
        """Should have exactly 6 features."""
        assert len(FEATURE_WEIGHTS) == 6

    def test_weight_keys(self):
        """All expected feature keys should be present."""
        expected_keys = [
            "spot_area", "color_change", "brown_ratio",
            "yellow_ratio", "spot_count", "texture_var"
        ]
        assert set(FEATURE_WEIGHTS.keys()) == set(expected_keys)

    def test_weight_values_sum_to_one(self):
        """All weights should sum to 1.0 (100%)."""
        total = sum(FEATURE_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_weight_values_positive(self):
        """All weights should be positive."""
        for weight in FEATURE_WEIGHTS.values():
            assert weight > 0


class TestFeatureNormalizationRanges:
    """Test feature normalization ranges."""

    def test_range_count(self):
        """Should have exactly 6 features."""
        assert len(FEATURE_NORM_RANGES) == 6

    def test_range_keys(self):
        """All expected feature keys should be present."""
        expected_keys = [
            "spot_area", "color_change", "yellow_ratio",
            "brown_ratio", "spot_count", "texture_var"
        ]
        assert set(FEATURE_NORM_RANGES.keys()) == set(expected_keys)

    def test_range_format(self):
        """Each range should be a 2-tuple (min, max) with min < max."""
        for feature, (min_val, max_val) in FEATURE_NORM_RANGES.items():
            assert min_val < max_val, f"{feature}: min {min_val} should be < max {max_val}"

    def test_ranges_positive(self):
        """All range values should be positive."""
        for min_val, max_val in FEATURE_NORM_RANGES.values():
            assert min_val >= 0
            assert max_val > 0


class TestHSVRanges:
    """Test HSV color detection ranges."""

    def test_hsv_ranges_keys(self):
        """Should have all expected color ranges."""
        expected_keys = ["yellow", "brown", "dark", "spot"]
        assert set(HSV_RANGES.keys()) == set(expected_keys)

    def test_hsv_range_format(self):
        """Each range should have 'lower' and 'upper' numpy arrays."""
        for color, range_dict in HSV_RANGES.items():
            assert "lower" in range_dict
            assert "upper" in range_dict
            assert isinstance(range_dict["lower"], np.ndarray)
            assert isinstance(range_dict["upper"], np.ndarray)

    def test_hsv_range_shape(self):
        """HSV arrays should be 3-element arrays (H, S, V)."""
        for color, range_dict in HSV_RANGES.items():
            assert range_dict["lower"].shape == (3,)
            assert range_dict["upper"].shape == (3,)


class TestImageProcessing:
    """Test image processing configuration."""

    def test_image_size(self):
        """Image size should be 256x256."""
        assert IMAGE_SIZE == (256, 256)

    def test_default_fuzzy_score(self):
        """Default fuzzy score should be 50 (middle of range)."""
        assert DEFAULT_FUZZY_SCORE == 50