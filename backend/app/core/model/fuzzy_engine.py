"""
Fuzzy Sugeno Inference Engine (Orde 0)

Tahapan:
    1. Fuzzification   - menghitung derajat keanggotaan dengan Triangular MF
    2. Rule Evaluation  - 16 rules, operator AND (minimum)
    3. Defuzzification  - Weighted Average Sugeno
    4. Classification   - mapping skor ke kategori penyakit
"""

from app.core.model.config import (
    SPOT_AREA_MF,
    SPOT_AREA_LABELS,
    COLOR_CHANGE_MF,
    COLOR_CHANGE_LABELS,
    RULES,
    OUTPUT_CLASSES,
    DEFAULT_FUZZY_SCORE,
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

    Args:
        value: Nilai input numerik.
        mf_dict: Dictionary {label: (a, b, c)} parameter MF.
        labels: Urutan label kategori.

    Returns:
        Dictionary {label: derajat_keanggotaan}.
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
        # Firing strength: operator AND = minimum
        alpha = min(spot_degrees[spot_cat], color_degrees[color_cat])

        if alpha > 0:
            total_weight += alpha
            total_weighted_output += alpha * konstanta

    # 3. Weighted Average
    if total_weight == 0:
        return float(DEFAULT_FUZZY_SCORE)

    z = total_weighted_output / total_weight

    # Clipping ke [0, 100]
    z = max(0.0, min(100.0, z))

    return round(z, 2)


def classify(z: float) -> dict:
    """
    Mengklasifikasikan fuzzy score ke kategori penyakit.

    Args:
        z: Fuzzy score (0-100).

    Returns:
        Dictionary: {disease_name, severity_level, plant_status}.
    """
    for min_score, max_score, disease, severity, status in OUTPUT_CLASSES:
        if min_score <= z <= max_score:
            return {
                "disease_name": disease,
                "severity_level": severity,
                "plant_status": status,
            }

    # Fallback (seharusnya tidak terjadi karena range 0-100 tercakup semua)
    return {
        "disease_name": "Tidak Terdeteksi",
        "severity_level": "",
        "plant_status": "Tidak Diketahui",
    }
