import cv2
import numpy as np

def extract_features(image_bytes: bytes) -> dict:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image file")
        
    # Resize to 256x256
    img = cv2.resize(img, (256, 256))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Leaf Segmentation (Green Mask)
    # Lower: [35, 40, 40], Upper: [90, 255, 255]
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Morphological Cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Largest Contour Detection
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    leaf_mask = np.zeros_like(mask)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(leaf_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    else:
        # Fallback if no leaf detected
        leaf_mask = mask
        
    leaf_pixels = cv2.countNonZero(leaf_mask)
    if leaf_pixels == 0:
        return {
            "spot_area": 0.0,
            "yellow_ratio": 0.0,
            "brown_ratio": 0.0,
            "dark_ratio": 0.0,
            "color_change": 0.0
        }
        
    # Apply leaf mask to HSV image
    leaf_hsv = cv2.bitwise_and(hsv, hsv, mask=leaf_mask)
    
    # Feature Extraction (H, S, V ranges)
    # Spot Area (brown/yellow mixture approx): [0,20,20] to [40,255,180]
    lower_spot = np.array([0, 20, 20])
    upper_spot = np.array([40, 255, 180])
    spot_mask = cv2.inRange(leaf_hsv, lower_spot, upper_spot)
    spot_pixels = cv2.countNonZero(cv2.bitwise_and(spot_mask, leaf_mask))
    
    # Yellow Ratio: [20, 50, 50] to [35, 255, 255]
    lower_yellow = np.array([20, 50, 50])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(leaf_hsv, lower_yellow, upper_yellow)
    yellow_pixels = cv2.countNonZero(cv2.bitwise_and(yellow_mask, leaf_mask))
    
    # Brown Ratio: [0, 20, 20] to [20, 255, 120]
    lower_brown = np.array([0, 20, 20])
    upper_brown = np.array([20, 255, 120])
    brown_mask = cv2.inRange(leaf_hsv, lower_brown, upper_brown)
    brown_pixels = cv2.countNonZero(cv2.bitwise_and(brown_mask, leaf_mask))
    
    # Dark Ratio: [0, 0, 0] to [180, 255, 60]
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 60])
    dark_mask = cv2.inRange(leaf_hsv, lower_dark, upper_dark)
    dark_pixels = cv2.countNonZero(cv2.bitwise_and(dark_mask, leaf_mask))
    
    spot_area = (spot_pixels / leaf_pixels) * 100
    yellow_ratio = (yellow_pixels / leaf_pixels) * 100
    brown_ratio = (brown_pixels / leaf_pixels) * 100
    dark_ratio = (dark_pixels / leaf_pixels) * 100
    color_change = yellow_ratio + brown_ratio + dark_ratio
    
    return {
        "spot_area": round(spot_area, 2),
        "yellow_ratio": round(yellow_ratio, 2),
        "brown_ratio": round(brown_ratio, 2),
        "dark_ratio": round(dark_ratio, 2),
        "color_change": round(color_change, 2)
    }
