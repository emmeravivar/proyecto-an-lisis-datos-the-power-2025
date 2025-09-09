# etl_utils.py

import numpy as np

def days_diff(late, early):
    """
    Calcula la diferencia entre dos fechas en días (como float).
    """
    return (late - early).dt.total_seconds() / 86400

def pct(condition, df):
    """
    Calcula el porcentaje de filas que cumplen una condición booleana.
    """
    return float(np.mean(condition)) if len(df) else 0.0