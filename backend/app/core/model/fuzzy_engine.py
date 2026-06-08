"""
Fuzzy Sugeno Inference Engine (Orde 0) - 6 Features

Tahapan:
    1. Fuzzification   - menghitung derajat keanggotaan dengan Triangular MF
    2. Rule Evaluation  - 16 rules, operator AND (minimum)
    3. Defuzzification  - Weighted Average Sugeno
    4. Classification   - mapping fuzzy score ke severity level
    5. Severity Score   - weighted calculation dari 6 fitur
"""

from app.core.model.config import (
    SPOT_AREA_MF,
    SPOT_AREA_LABELS,
    COLOR_CHANGE_MF,
    COLOR_CHANGE_LABELS,
    RULES,
    OUTPUT_CLASSES,
    DEFAULT_FUZZY_SCORE,
    FEATURE_WEIGHTS,
    FEATURE_NORM_RANGES,
)

def triangular_mf(x: float, a: float, b: float, c: float) -> float:
    """
    Triangular Membership Function.

    Args:
        x: Nilai input crisp.
        a: Batas awal (derajat > 0 mulai dari sini).
        b: Nilai representatif / puncak (derajat = 1).
        c: Batas akhir (derajat = 0 setelah ini).

    Returns:
        Derajat keanggotaan dalam rentang [0, 1].
    """
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a)
    if b < x < c:
        return (c - x) / (c - b)
    return 0.0

def fuzzify(value: float, mf_dict: dict, labels: list) -> dict:
    """
    Fuzzifikasi nilai crisp ke dalam derajat keanggotaan untuk setiap kategori.
    """
    degrees = {}
    for label in labels:
        a, b, c = mf_dict[label]
        degrees[label] = triangular_mf(value, a, b, c)
    return degrees

def infer(spot_area: float, color_change: float) -> float:
    """
    Inferensi Fuzzy Sugeno Orde 0.

    Args:
        spot_area: Nilai Spot Area (%) hasil ekstraksi fitur.
        color_change: Nilai Color Change (%) hasil ekstraksi fitur.

    Returns:
        Fuzzy score (z) dalam rentang [0, 100].
    """
    # 1. Fuzzification
    spot_degrees = fuzzify(spot_area, SPOT_AREA_MF, SPOT_AREA_LABELS)
    color_degrees = fuzzify(color_change, COLOR_CHANGE_MF, COLOR_CHANGE_LABELS)

    # 2. Rule Evaluation + Defuzzification
    total_weight = 0.0
    total_weighted_output = 0.0

    for spot_cat, color_cat, konstanta in RULES:
        alpha = min(spot_degrees[spot_cat], color_degrees[color_cat])

        if alpha > 0:
            total_weight += alpha
            total_weighted_output += alpha * konstanta

    # 3. Weighted Average
    if total_weight == 0:
        return float(DEFAULT_FUZZY_SCORE)

    z = total_weighted_output / total_weight
    z = max(0.0, min(100.0, z))

    return round(z, 2)

def classify(z: float) -> dict:
    """
    Mengklasifikasikan fuzzy score ke dalam kategori kesehatan tanaman.
    
    Args:
        z: Fuzzy score (0-100).
    
    Returns:
        Dictionary: {severity_level, plant_status}.
    """
    for min_score, max_score, severity, status in OUTPUT_CLASSES:
        if min_score <= z <= max_score:
            return {
                "severity_level": severity,
                "plant_status": status,
            }

    return {
        "severity_level": "Tidak Diketahui",
        "plant_status": "Tidak Diketahui",
    }

def normalize(value: float, min_val: float, max_val: float) -> float:
    """
    Normalisasi nilai ke skala 0-100.
    
    Args:
        value: Nilai fitur aktual.
        min_val: Nilai minimum rentang (berdasarkan P99).
        max_val: Nilai maksimum rentang (berdasarkan P99).
    
    Returns:
        Nilai ternormalisasi (0-100).
    """
    if max_val <= min_val:
        return 0.0
    normalized = ((value - min_val) / (max_val - min_val)) * 100.0
    return max(0.0, min(100.0, normalized))

def calculate_severity_score(features: dict) -> float:
    """
    Hitung severity score berbasis bobot fitur.
    
    Severity score tinggi = kondisi buruk (severity tinggi).
    Severity score rendah = kondisi sehat.
    
    Args:
        features: Dictionary dengan 6 fitur.
    
    Returns:
        Severity score (0-100).
    """
    score = 0.0
    
    for feature_name, weight in FEATURE_WEIGHTS.items():
        value = features.get(feature_name, 0.0)
        min_val, max_val = FEATURE_NORM_RANGES[feature_name]
        normalized = normalize(value, min_val, max_val)
        score += weight * normalized
    
    return round(score, 2)