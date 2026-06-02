"""
Model Configuration - Tomato Leaf Health Detection

Semua parameter ditentukan secara data-driven dari K-Means Clustering (k=4)
pada PlantVillage Tomato Dataset (4.952 sampel).

Sumber:
    - model-reference/membership_kmeans.csv
    - model-reference/cluster_report.csv
    - model-reference/feature_statistics.csv
"""

import numpy as np

# =============================================================================
# TRIANGULAR MEMBERSHIP FUNCTION PARAMETERS (a, b, c)
# Data dari membership_kmeans.csv
# =============================================================================

# Variabel Input 1: Spot Area (%)
# Kategori: kecil, sedang, besar, sangat_besar
SPOT_AREA_MF = {
    "kecil":        (0.06, 3.22, 8.35),
    "sedang":       (8.35, 13.48, 18.85),
    "besar":        (18.85, 24.23, 31.78),
    "sangat_besar": (31.78, 39.33, 48.48),
}
SPOT_AREA_LABELS = ["kecil", "sedang", "besar", "sangat_besar"]

# Variabel Input 2: Color Change Severity (%)
# Kategori: rendah, sedang, tinggi, sangat_tinggi
COLOR_CHANGE_MF = {
    "rendah":        (0.19, 8.05, 16.86),
    "sedang":        (16.86, 25.68, 36.19),
    "tinggi":        (36.19, 46.70, 64.15),
    "sangat_tinggi": (64.15, 81.59, 99.79),
}
COLOR_CHANGE_LABELS = ["rendah", "sedang", "tinggi", "sangat_tinggi"]

# Variabel Pendukung: Yellow Ratio (%)
YELLOW_RATIO_MF = {
    "rendah":        (0.00, 3.76, 11.40),
    "sedang":        (11.40, 19.03, 32.01),
    "tinggi":        (32.01, 44.99, 62.14),
    "sangat_tinggi": (62.14, 79.29, 93.63),
}

# Variabel Pendukung: Brown Ratio (%)
BROWN_RATIO_MF = {
    "rendah":        (0.00, 0.12, 0.52),
    "sedang":        (0.52, 0.92, 1.60),
    "tinggi":        (1.60, 2.28, 3.38),
    "sangat_tinggi": (3.38, 4.48, 5.10),
}

# Variabel Pendukung: Dark Ratio (%)
DARK_RATIO_MF = {
    "rendah":        (0.01, 2.84, 7.70),
    "sedang":        (7.70, 12.57, 17.89),
    "tinggi":        (17.89, 23.21, 30.92),
    "sangat_tinggi": (30.92, 38.63, 48.27),
}

# =============================================================================
# FUZZY RULE BASE (16 Rules)
# Format: (spot_area_category, color_change_category, output_constanta)
# Urutan: R1 - R16
# =============================================================================

RULES = [
    ("kecil",        "rendah",        100),  # R1  - Sangat Sehat
    ("kecil",        "sedang",         90),  # R2  - Sehat
    ("kecil",        "tinggi",         80),  # R3  - Early Blight Ringan
    ("kecil",        "sangat_tinggi",  40),  # R4  - Leaf Mold
    ("sedang",       "rendah",         85),  # R5  - Sehat
    ("sedang",       "sedang",         70),  # R6  - Early Blight Sedang
    ("sedang",       "tinggi",         55),  # R7  - Late Blight
    ("sedang",       "sangat_tinggi",  40),  # R8  - Leaf Mold
    ("besar",        "rendah",         70),  # R9  - Early Blight Sedang
    ("besar",        "sedang",         55),  # R10 - Late Blight
    ("besar",        "tinggi",         20),  # R11 - Septoria Leaf Spot
    ("besar",        "sangat_tinggi",  10),  # R12 - Sangat Buruk
    ("sangat_besar",  "rendah",        50),  # R13 - Late Blight
    ("sangat_besar",  "sedang",        20),  # R14 - Septoria Leaf Spot
    ("sangat_besar",  "tinggi",        10),  # R15 - Sangat Buruk
    ("sangat_besar",  "sangat_tinggi",  5),  # R16 - Sangat Buruk
]

# =============================================================================
# OUTPUT CLASSIFICATION
# =============================================================================

OUTPUT_CLASSES = [
    (90, 100, "Sangat Sehat",    "Tidak Ada",    "Sehat"),
    (75,  89, "Sehat",           "Tidak Ada",    "Sehat"),
    (60,  74, "Early Blight",    "Ringan",       "Terinfeksi"),
    (45,  59, "Late Blight",     "Sedang",       "Terinfeksi"),
    (25,  44, "Leaf Mold",       "Berat",        "Terinfeksi"),
    (10,  24, "Septoria Leaf Spot", "Berat",     "Terinfeksi"),
    (0,    9, "Sangat Buruk",    "Sangat Berat", "Terinfeksi"),
]

# Default output ketika tidak ada aturan aktif (Σαi = 0)
DEFAULT_FUZZY_SCORE = 50

# =============================================================================
# HSV RANGES
# =============================================================================

# Rentang HSV untuk segmentasi daun (green mask)
GREEN_MASK_LOWER = np.array([35, 40, 40], dtype=np.uint8)
GREEN_MASK_UPPER = np.array([90, 255, 255], dtype=np.uint8)

# Rentang HSV untuk deteksi warna (semua dalam skala OpenCV: H 0-179, S 0-255, V 0-255)
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

# Ukuran resize untuk preprocessing
IMAGE_SIZE = (256, 256)

# Kernel untuk morphological operations
MORPH_KERNEL_SIZE = 5
MORPH_CLOSE_ITERATIONS = 2
MORPH_OPEN_ITERATIONS = 1
