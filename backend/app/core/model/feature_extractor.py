"""
Feature Extraction Module

Mengekstrak 5 fitur visual dari area daun hasil segmentasi:
    1. spot_area    - persentase luas bercak
    2. yellow_ratio - persentase warna kuning (klorosis)
    3. brown_ratio  - persentase warna coklat (nekrosis)
    4. dark_ratio   - persentase warna gelap/hitam
    5. color_change - total perubahan warna (yellow + brown + dark)

Semua fitur dihitung hanya pada area daun (background diabaikan).
"""

import numpy as np
import cv2

from app.core.model.config import HSV_RANGES

def extract(masked_img: np.ndarray, leaf_mask: np.ndarray) -> dict:
    """
    Ekstrak 4 fitur dari area daun.

    Args:
        masked_img: Gambar RGB (hasil bitwise_and dengan leaf_mask).
        leaf_mask: Binary mask area daun (0 atau 255).

    Returns:
        Dictionary berisi 5 fitur:
            spot_area (float), yellow_ratio (float), brown_ratio (float),
            dark_ratio (float), color_change (float).
    """
    # Hitung total piksel daun
    leaf_pixels = np.count_nonzero(leaf_mask)
    if leaf_pixels == 0:
        return {
            "spot_area": 0.0,
            "yellow_ratio": 0.0,
            "brown_ratio": 0.0,
            "dark_ratio": 0.0,
            "color_change": 0.0,
        }

    # Konversi ke HSV (hanya untuk area daun)
    hsv = cv2.cvtColor(masked_img, cv2.COLOR_BGR2HSV)

    # Helper: hitung persentase piksel dalam rentang HSV
    def percentage_in_range(lower: np.ndarray, upper: np.ndarray) -> float:
        mask = cv2.inRange(hsv, lower, upper)
        # Intersection dengan area daun
        intersection = cv2.bitwise_and(mask, leaf_mask)
        pixel_count = np.count_nonzero(intersection)
        return (pixel_count / leaf_pixels) * 100.0

    # 1. Spot Area - bercak (coklat + kuning)
    spot_pct = percentage_in_range(
        HSV_RANGES["spot"]["lower"],
        HSV_RANGES["spot"]["upper"],
    )

    # 2. Yellow Ratio - klorosis
    yellow_pct = percentage_in_range(
        HSV_RANGES["yellow"]["lower"],
        HSV_RANGES["yellow"]["upper"],
    )

    # 3. Brown Ratio - nekrosis
    brown_pct = percentage_in_range(
        HSV_RANGES["brown"]["lower"],
        HSV_RANGES["brown"]["upper"],
    )

    # 4. Dark Ratio - gelap/hitam
    dark_pct = percentage_in_range(
        HSV_RANGES["dark"]["lower"],
        HSV_RANGES["dark"]["upper"],
    )

    # 5. Color Change Severity - total perubahan warna (yellow + brown + dark)
    color_change = yellow_pct + brown_pct + dark_pct

    return {
        "spot_area": round(spot_pct, 2),
        "yellow_ratio": round(yellow_pct, 2),
        "brown_ratio": round(brown_pct, 2),
        "dark_ratio": round(dark_pct, 2),
        "color_change": round(color_change, 2),
    }