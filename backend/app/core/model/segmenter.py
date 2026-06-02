"""
Leaf Segmentation Module

Pipeline:
    1. Read & resize image (256×256)
    2. Convert BGR to HSV
    3. Green mask (HSV threshold)
    4. Morphological cleanup (close + open)
    5. Largest contour detection
    6. Return binary leaf mask + masked image
"""

import cv2
import numpy as np

from app.core.model.config import (
    IMAGE_SIZE,
    GREEN_MASK_LOWER,
    GREEN_MASK_UPPER,
    MORPH_KERNEL_SIZE,
    MORPH_CLOSE_ITERATIONS,
    MORPH_OPEN_ITERATIONS,
)


def segment(image_path: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Segment daun dari background.

    Args:
        image_path: Path ke file gambar.

    Returns:
        Tuple (leaf_mask, masked_image):
            - leaf_mask: Binary mask (uint8, 0 or 255) area daun.
            - masked_image: Gambar asli dengan background dihilangkan (hanya daun).
    """
    # 1. Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Tidak dapat membaca gambar: {image_path}")

    # 2. Resize
    img = cv2.resize(img, IMAGE_SIZE, interpolation=cv2.INTER_AREA)

    # 3. Konversi BGR → HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 4. Green mask
    green_mask = cv2.inRange(hsv, GREEN_MASK_LOWER, GREEN_MASK_UPPER)

    # 5. Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (MORPH_KERNEL_SIZE, MORPH_KERNEL_SIZE))

    # Close: mengisi lubang kecil di dalam daun
    mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel, iterations=MORPH_CLOSE_ITERATIONS)

    # Open: menghilangkan noise kecil di luar daun
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=MORPH_OPEN_ITERATIONS)

    # 6. Largest contour detection
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        # Fallback: jika tidak ada kontur, gunakan seluruh area
        height, width = mask.shape
        leaf_mask = np.ones((height, width), dtype=np.uint8) * 255
    else:
        # Ambil kontur terluas
        largest_contour = max(contours, key=cv2.contourArea)
        leaf_mask = np.zeros_like(mask)
        cv2.drawContours(leaf_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

    # 7. Mask gambar asli
    masked_image = cv2.bitwise_and(img, img, mask=leaf_mask)

    return leaf_mask, masked_image
