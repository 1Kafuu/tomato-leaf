"""
Feature Extraction Module

Mengekstrak 6 fitur visual dari area daun hasil segmentasi:
    1. spot_area    - persentase luas bercak (%)
    2. color_change - total perubahan warna (yellow + brown + dark) (%)
    3. yellow_ratio - persentase warna kuning/klorosis (%)
    4. brown_ratio  - persentase warna coklat/nekrosis (%)
    5. spot_count   - jumlah bercak/lesi terpisah
    6. texture_var  - variansi tekstur (grayscale std deviation)

Semua fitur dihitung hanya pada area daun (background diabaikan).
"""

import numpy as np
import cv2

from app.core.model.config import HSV_RANGES

def extract(masked_img: np.ndarray, leaf_mask: np.ndarray) -> dict:
    """
    Ekstrak 6 fitur dari area daun.

    Args:
        masked_img: Gambar RGB (hasil bitwise_and dengan leaf_mask).
        leaf_mask: Binary mask area daun (0 atau 255).

    Returns:
        Dictionary berisi 6 fitur:
            spot_area, color_change, yellow_ratio, brown_ratio,
            spot_count, texture_var.
    """
    # Hitung total piksel daun
    leaf_pixels = np.count_nonzero(leaf_mask)
    if leaf_pixels == 0:
        return {
            "spot_area": 0.0,
            "color_change": 0.0,
            "yellow_ratio": 0.0,
            "brown_ratio": 0.0,
            "spot_count": 0,
            "texture_var": 0.0,
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
    spot_mask = cv2.inRange(hsv, HSV_RANGES["spot"]["lower"], HSV_RANGES["spot"]["upper"])
    spot_mask = cv2.bitwise_and(spot_mask, leaf_mask)
    spot_area = percentage_in_range(HSV_RANGES["spot"]["lower"], HSV_RANGES["spot"]["upper"])

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

    # 4. Dark Ratio - untuk perhitungan color_change
    dark_pct = percentage_in_range(
        HSV_RANGES["dark"]["lower"],
        HSV_RANGES["dark"]["upper"],
    )

    # 5. Color Change Severity - total perubahan warna (yellow + brown + dark)
    color_change = yellow_pct + brown_pct + dark_pct

    # 6. Spot Count - deteksi kontur bercak
    _, binary_spot = cv2.threshold(spot_mask, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_spot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    spot_count = sum(1 for c in contours if cv2.contourArea(c) >= 5)

    # 7. Texture Variance - std dev grayscale
    gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
    leaf_gray = cv2.bitwise_and(gray, gray, mask=leaf_mask)
    pixels = leaf_gray[leaf_mask > 0]
    texture_var = float(np.std(pixels)) if len(pixels) > 0 else 0.0

    return {
        "spot_area": round(spot_area, 2),
        "color_change": round(color_change, 2),
        "yellow_ratio": round(yellow_pct, 2),
        "brown_ratio": round(brown_pct, 2),
        "spot_count": spot_count,
        "texture_var": round(texture_var, 2),
    }