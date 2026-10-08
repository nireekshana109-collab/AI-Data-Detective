import pandas as pd
import numpy as np

def detect_date_columns(df):
    dates = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            dates.append(col)
        elif df[col].dtype == "object":
            parsed = pd.to_datetime(df[col], errors="coerce")
            if len(df) and parsed.notna().mean() >= 0.8:
                dates.append(col)
    return dates

def profile_dataset(df):
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    date_cols = detect_date_columns(df)
    categorical = [c for c in df.columns if c not in numeric and c not in date_cols]
    stats = {}
    if numeric:
        desc = df[numeric].describe(percentiles=[.25, .5, .75]).T
        for col in numeric:
            row = desc.loc[col]
            stats[col] = {
                "count": int(row["count"]),
                "mean": round(float(row["mean"]), 4),
                "std": round(float(row["std"]) if pd.notna(row["std"]) else 0, 4),
                "min": round(float(row["min"]), 4),
                "25%": round(float(row["25%"]), 4),
                "median": round(float(row["50%"]), 4),
                "75%": round(float(row["75%"]), 4),
                "max": round(float(row["max"]), 4),
            }
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_total": int(df.isna().sum().sum()),
        "missing_by_column": {k: int(v) for k, v in df.isna().sum().items() if v},
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": numeric,
        "categorical_columns": categorical,
        "date_columns": date_cols,
        "numeric_stats": stats,
    }

def _find_col(df, names):
    lowered = {str(c).strip().lower(): c for c in df.columns}
    for name in names:
        if name in lowered:
            return lowered[name]
    for c in df.columns:
        lc = str(c).strip().lower()
        if any(name in lc for name in names):
            return c
    return None

def calculate_kpis(df):
    result = {}
    sales = _find_col(df, ["sales", "revenue", "amount"])
    profit = _find_col(df, ["profit", "net profit"])
    quantity = _find_col(df, ["quantity", "qty", "units"])
    if sales:
        result["Total Sales"] = f"{df[sales].sum():,.2f}"
        result["Average Sales"] = f"{df[sales].mean():,.2f}"
    if profit:
        result["Total Profit"] = f"{df[profit].sum():,.2f}"
        if sales and df[sales].sum() != 0:
            result["Profit Margin"] = f"{df[profit].sum()/df[sales].sum()*100:.2f}%"
    if quantity:
        result["Total Quantity"] = f"{df[quantity].sum():,.0f}"
    if sales and len(df):
        result["Average Order Value"] = f"{df[sales].mean():,.2f}"
    return result

def build_verified_summary(profile, kpis, anomalies):
    return {
        "dataset": {
            "rows": profile["rows"],
            "columns": profile["columns"],
            "missing_total": profile["missing_total"],
            "duplicate_rows": profile["duplicate_rows"],
            "numeric_columns": profile["numeric_columns"],
            "categorical_columns": profile["categorical_columns"],
            "date_columns": profile["date_columns"],
        },
        "statistics": profile["numeric_stats"],
        "kpis": kpis,
        "anomalies": {
            "total_anomalies": anomalies["total_anomalies"],
            "affected_rows": len(anomalies["affected_rows"]),
            "details": anomalies["details"][:100],
        },
    }
