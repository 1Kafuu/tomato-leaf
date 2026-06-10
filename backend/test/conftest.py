"""
Pytest configuration and shared fixtures for model tests.
"""

import pytest
import numpy as np
import cv2


@pytest.fixture
def sample_leaf_mask():
    """Create a sample circular leaf mask (256x256)."""
    mask = np.zeros((256, 256), dtype=np.uint8)
    center = (128, 128)
    radius = 100
    cv2.circle(mask, center, radius, 255, -1)
    return mask


@pytest.fixture
def sample_masked_image(sample_leaf_mask):
    """Create a sample masked image with some spots and yellow areas."""
    # Create a green-ish background image
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    img[:, :] = [50, 150, 50]  # Green-ish

    # Add some yellow spots (simulating disease)
    cv2.rectangle(img, (100, 100), (130, 130), [20, 180, 200], -1)  # Yellow
    cv2.rectangle(img, (150, 150), (170, 170), [30, 120, 80], -1)   # Brown-ish

    # Apply mask
    masked = cv2.bitwise_and(img, img, mask=sample_leaf_mask)
    return masked


@pytest.fixture
def healthy_features():
    """Sample features for a healthy leaf."""
    return {
        "spot_area": 2.5,
        "color_change": 5.0,
        "yellow_ratio": 1.0,
        "brown_ratio": 0.5,
        "spot_count": 3,
        "texture_var": 18.0,
    }


@pytest.fixture
def mild_features():
    """Sample features for a mildly infected leaf."""
    return {
        "spot_area": 12.0,
        "color_change": 25.0,
        "yellow_ratio": 10.0,
        "brown_ratio": 2.0,
        "spot_count": 15,
        "texture_var": 28.0,
    }


@pytest.fixture
def severe_features():
    """Sample features for a severely infected leaf."""
    return {
        "spot_area": 35.0,
        "color_change": 60.0,
        "yellow_ratio": 25.0,
        "brown_ratio": 4.5,
        "spot_count": 150,
        "texture_var": 45.0,
    }