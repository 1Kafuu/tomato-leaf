"""
Model Configuration - Tomato Leaf Health Detection (6 Features)

Data-driven dari K-Means Clustering (k=4) pada PlantVillage Tomato Dataset (4.952 sampel).
Sumber: model-reference/membership_6features.csv, stats_6features.csv
"""

import numpy as np

# =============================================================================
# TRIANGULAR MEMBERSHIP FUNCTION PARAMETERS (a, b, c)
# Data dari membership_6features.csv
# =============================================================================

# Variabel Input Fuzzy: spot_area (%)
SPOT_AREA_MF = {
    "small":      (0.06, 3.23, 8.36),
    "medium":     (8.36, 13.49, 18.86),
    "large":      (18.86, 24.23, 31.78),
    "very_large": (31.78, 39.33, 48.48),
}
SPOT_AREA_LABELS = ["small", "medium", "large", "very_large"]

# Variabel Input Fuzzy: color_change (%)
COLOR_CHANGE_MF = {
    "low":       (0.19, 8.05, 16.86),
    "medium":    (16.86, 25.67, 36.18),
    "high":      (36.18, 46.69, 64.14),
    "very_high": (64.14, 81.59, 99.79),
}
COLOR_CHANGE_LABELS = ["low", "medium", "high", "very_high"]

# Variabel Pendukung: yellow_ratio (%)
YELLOW_RATIO_MF = {
    "low":       (0.00, 3.76, 11.40),
    "medium":    (11.40, 19.03, 32.01),
    "high":      (32.01, 44.99, 62.14),
    "very_high": (62.14, 79.29, 93.63),
}

# Variabel Pendukung: brown_ratio (%)
BROWN_RATIO_MF = {
    "low":       (0.00, 0.12, 0.51),
    "medium":    (0.51, 0.91, 1.59),
    "high":      (1.59, 2.26, 3.37),
    "very_high": (3.37, 4.48, 5.11),
}

# Variabel Pendukung: spot_count (count)
SPOT_COUNT_MF = {
    "few":       (4.00, 16.33, 30.46),
    "moderate":  (30.46, 44.60, 58.27),
    "many":      (58.27, 71.95, 85.74),
    "very_many": (85.74, 99.54, 100.00),
}

# Variabel Pendukung: texture_var (std deviation)
TEXTURE_VAR_MF = {
    "low":       (14.96, 20.06, 24.53),
    "medium":    (24.53, 28.99, 33.34),
    "high":      (33.34, 37.69, 43.48),
    "very_high": (43.48, 49.27, 56.86),
}

# =============================================================================
# FUZZY RULE BASE (16 Rules - Sugeno Orde 0)
# Format: (spot_area_category, color_change_category, output_constanta)
# =============================================================================

RULES = [
    # SMALL SPOT AREA
    ("small",      "low",       100),  # Healthy
    ("small",      "medium",     90),  # Healthy
    ("small",      "high",       75),  # Mild
    ("small",      "very_high",  60),  # Mild

    # MEDIUM SPOT AREA
    ("medium",     "low",        85),  # Healthy
    ("medium",     "medium",     70),  # Mild
    ("medium",     "high",       55),  # Moderate
    ("medium",     "very_high",  40),  # Moderate

    # LARGE SPOT AREA
    ("large",      "low",        65),  # Mild
    ("large",      "medium",     50),  # Moderate
    ("large",      "high",       35),  # Severe
    ("large",      "very_high",  20),  # Severe

    # VERY LARGE SPOT AREA
    ("very_large", "low",        45),  # Moderate
    ("very_large", "medium",     30),  # Severe
    ("very_large", "high",       15),  # Very Severe
    ("very_large", "very_high",   5),  # Very Severe
]

# =============================================================================
# OUTPUT CLASSIFICATION (Severity-Based)
# Format: (min_score, max_score, severity_level, plant_status)
# =============================================================================

OUTPUT_CLASSES = [
    (85, 100, "Sehat",          "Sehat"),
    (70,  84, "Ringan",        "Terinfeksi"),
    (50,  69, "Sedang",        "Terinfeksi"),
    (25,  49, "Berat",         "Terinfeksi"),
    (0,   24, "Sangat Berat",  "Terinfeksi"),
]

DEFAULT_FUZZY_SCORE = 50

# =============================================================================
# FEATURE WEIGHTS (Severity Score Calculation)
# =============================================================================

FEATURE_WEIGHTS = {
    "spot_area": 0.30,
    "color_change": 0.25,
    "brown_ratio": 0.15,
    "yellow_ratio": 0.10,
    "spot_count": 0.10,
    "texture_var": 0.10,
}

# Normalization ranges based on P99 from stats_6features.csv
FEATURE_NORM_RANGES = {
    "spot_area": (0.0, 48.48),    # P99: 48.4815
    "color_change": (0.0, 99.79), # P99: 99.7927
    "yellow_ratio": (0.0, 93.63), # P99: 93.6265
    "brown_ratio": (0.0, 5.11),   # P99: 5.1063
    "spot_count": (0.0, 794.49),  # P99: 794.49
    "texture_var": (0.0, 56.86),  # P99: 56.862
}

# =============================================================================
# HSV RANGES (Image Processing)
# =============================================================================

GREEN_MASK_LOWER = np.array([35, 40, 40], dtype=np.uint8)
GREEN_MASK_UPPER = np.array([90, 255, 255], dtype=np.uint8)

HSV_RANGES = {
    "yellow": {
        "lower": np.array([20, 50, 50], dtype=np.uint8),
        "upper": np.array([35, 255, 255], dtype=np.uint8),
    },
    "brown": {
        "lower": np.array([0, 20, 20], dtype=np.uint8),
        "upper": np.array([20, 255, 120], dtype=np.uint8),
    },
    "dark": {
        "lower": np.array([0, 0, 0], dtype=np.uint8),
        "upper": np.array([180, 255, 60], dtype=np.uint8),
    },
    "spot": {
        "lower": np.array([0, 20, 20], dtype=np.uint8),
        "upper": np.array([40, 255, 180], dtype=np.uint8),
    },
}

# =============================================================================
# IMAGE PROCESSING
# =============================================================================

IMAGE_SIZE = (256, 256)
MORPH_KERNEL_SIZE = 5
MORPH_CLOSE_ITERATIONS = 2
MORPH_OPEN_ITERATIONS = 1