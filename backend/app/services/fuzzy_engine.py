import numpy as np

def triangular_mf(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        if (b - a) == 0: return 1.0
        return (x - a) / (b - a)
    elif b < x < c:
        if (c - b) == 0: return 1.0
        return (c - x) / (c - b)
    return 0.0

def evaluate_fuzzy(spot_area: float, color_change: float) -> tuple[float, str, str]:
    # Variabel 1: Spot Area
    sa_kecil = triangular_mf(spot_area, 0.06, 3.22, 8.35)
    sa_sedang = triangular_mf(spot_area, 8.35, 13.48, 18.85)
    sa_besar = triangular_mf(spot_area, 18.85, 24.23, 31.78)
    sa_sangat_besar = triangular_mf(spot_area, 31.78, 39.33, 48.48)
    # Handle overlap/out of bounds gracefully
    if spot_area < 0.06: sa_kecil = 1.0
    if spot_area > 48.48: sa_sangat_besar = 1.0
    
    # Variabel 2: Color Change
    cc_rendah = triangular_mf(color_change, 0.19, 8.05, 16.86)
    cc_sedang = triangular_mf(color_change, 16.86, 25.68, 36.19)
    cc_tinggi = triangular_mf(color_change, 36.19, 46.70, 64.15)
    cc_sangat_tinggi = triangular_mf(color_change, 64.15, 81.59, 99.79)
    
    if color_change < 0.19: cc_rendah = 1.0
    if color_change > 99.79: cc_sangat_tinggi = 1.0
    
    # Rule Base (4x4)
    rules = [
        # Kecil
        (min(sa_kecil, cc_rendah), 100),
        (min(sa_kecil, cc_sedang), 90),
        (min(sa_kecil, cc_tinggi), 80),
        (min(sa_kecil, cc_sangat_tinggi), 40),
        # Sedang
        (min(sa_sedang, cc_rendah), 85),
        (min(sa_sedang, cc_sedang), 70),
        (min(sa_sedang, cc_tinggi), 55),
        (min(sa_sedang, cc_sangat_tinggi), 40),
        # Besar
        (min(sa_besar, cc_rendah), 70),
        (min(sa_besar, cc_sedang), 55),
        (min(sa_besar, cc_tinggi), 20),
        (min(sa_besar, cc_sangat_tinggi), 10),
        # Sangat Besar
        (min(sa_sangat_besar, cc_rendah), 50),
        (min(sa_sangat_besar, cc_sedang), 20),
        (min(sa_sangat_besar, cc_tinggi), 10),
        (min(sa_sangat_besar, cc_sangat_tinggi), 5)
    ]
    
    # Defuzzification (Weighted Average)
    numerator = sum(alpha * k for alpha, k in rules)
    denominator = sum(alpha for alpha, k in rules)
    
    if denominator == 0:
        z = 50.0
    else:
        z = numerator / denominator
        
    # Clipping
    z = max(0.0, min(100.0, z))
    
    # Classification
    if z >= 90:
        disease = "Sangat Sehat"
        severity = "Normal"
    elif z >= 75:
        disease = "Sehat"
        severity = "Normal"
    elif z >= 60:
        disease = "Early Blight"
        severity = "Ringan"
    elif z >= 45:
        disease = "Late Blight"
        severity = "Sedang"
    elif z >= 25:
        disease = "Leaf Mold"
        severity = "Parah"
    elif z >= 10:
        disease = "Septoria Leaf Spot"
        severity = "Parah"
    else:
        disease = "Sangat Buruk"
        severity = "Sangat Parah"
        
    return z, disease, severity
