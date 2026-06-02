"""
Pipeline Orchestrator

Menggabungkan segmentasi, ekstraksi fitur, dan inferensi fuzzy
menjadi satu fungsi predict() yang siap dipanggil dari API atau CLI.
"""

from app.core.model.segmenter import segment
from app.core.model.feature_extractor import extract
from app.core.model.fuzzy_engine import infer, classify


def predict(image_path: str) -> dict:
    """
    Prediksi penyakit daun tomat dari file gambar.

    Args:
        image_path: Path ke file gambar (JPG/JPEG/PNG).

    Returns:
        Dictionary dengan format:
            disease_name (str): Nama penyakit hasil diagnosis.
            fuzzy_score (float): Skor fuzzy (0-100).
            severity_level (str): Tingkat keparahan ("" jika sehat).
            plant_status (str): "Sehat" atau "Terinfeksi".
            spot_area (float): Persentase luas bercak.
        color_change (float): Persentase total perubahan warna.
    """
    # 1. Segmentasi daun
    leaf_mask, masked_img = segment(image_path)

    # 2. Ekstraksi fitur
    features = extract(masked_img, leaf_mask)

    # 3. Inferensi fuzzy
    fuzzy_score = infer(features["spot_area"], features["color_change"])

    # 4. Klasifikasi
    classification = classify(fuzzy_score)

    # 5. Gabungkan hasil
    return {
        "disease_name": classification["disease_name"],
        "fuzzy_score": fuzzy_score,
        "severity_level": classification["severity_level"],
        "plant_status": classification["plant_status"],
        "spot_area": features["spot_area"],
        "color_change": features["color_change"],
    }
