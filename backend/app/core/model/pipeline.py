"""
Pipeline Orchestrator

Menggabungkan segmentasi, ekstraksi fitur, dan inferensi fuzzy
menjadi satu fungsi predict() yang siap dipanggil dari API atau CLI.
"""

from app.core.model.segmenter import segment
from app.core.model.feature_extractor import extract
from app.core.model.fuzzy_engine import infer, classify, calculate_severity_score


def predict(image_path: str) -> dict:
    """
    Prediksi kondisi kesehatan daun tomat dari file gambar.

    Args:
        image_path: Path ke file gambar (JPG/JPEG/PNG).

    Returns:
        Dictionary dengan format:
            plant_status (str): "Sehat" atau "Terinfeksi".
            severity_level (str): "Sehat" | "Ringan" | "Sedang" | "Berat" | "Sangat Berat".
            fuzzy_score (float): Skor fuzzy (0-100).
            severity_score (float): Severity score berbasis bobot (0-100).
            features (dict): 6 fitur hasil ekstraksi.
    """
    # 1. Segmentasi daun
    leaf_mask, masked_img = segment(image_path)

    # 2. Ekstraksi fitur (6 fitur)
    features = extract(masked_img, leaf_mask)

    # 3. Inferensi fuzzy Sugeno (16 rules)
    fuzzy_score = infer(features["spot_area"], features["color_change"])

    # 4. Klasifikasi berdasarkan fuzzy score
    classification = classify(fuzzy_score)

    # 5. Hitung severity score dari 6 fitur berbobot
    severity_score = calculate_severity_score(features)

    # 6. Gabungkan hasil
    return {
        "plant_status": classification["plant_status"],
        "severity_level": classification["severity_level"],
        "fuzzy_score": fuzzy_score,
        "severity_score": severity_score,
        "features": {
            "spot_area": features["spot_area"],
            "color_change": features["color_change"],
            "yellow_ratio": features["yellow_ratio"],
            "brown_ratio": features["brown_ratio"],
            "spot_count": features["spot_count"],
            "texture_var": features["texture_var"],
        },
    }
