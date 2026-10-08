import numpy as np
import pandas as pd

def detect_anomalies(df):
    details = []
    affected = set()
    for col in df.select_dtypes(include=np.number).columns:
        s = df[col].dropna()
        if len(s) < 4 or s.nunique() < 2:
            continue
        q1, q3 = s.quantile(.25), s.quantile(.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        for idx in df.index[mask.fillna(False)]:
            affected.add(idx)
            details.append({
                "row_index": int(idx) if isinstance(idx, (int, np.integer)) else str(idx),
                "column": col,
                "value": float(df.loc[idx, col]),
                "lower_bound": round(float(lower), 4),
                "upper_bound": round(float(upper), 4),
            })
    return {
        "total_anomalies": len(details),
        "affected_rows": sorted(affected, key=str),
        "details": details,
    }
