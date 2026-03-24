from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "timestamp",
    "building",
    "unit_id",
    "equipment_type",
    "power_kw",
    "ton",
]

OPTIONAL_DEFAULTS = {
    "power_per_ton": None,
    "status": "Normal",
    "cond_entering_temp": None,
    "cond_leaving_temp": None,
    "evap_entering_temp": None,
    "evap_leaving_temp": None,
    "cond_approach_temp": None,
    "evap_approach_temp": None,
    "cond_water_flow": None,
    "evap_water_flow": None,
    "alarm_text": "",
}


def load_chiller_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    for col, default in OPTIONAL_DEFAULTS.items():
        if col not in df.columns:
            df[col] = default

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    numeric_cols = [
        "power_kw",
        "ton",
        "power_per_ton",
        "cond_entering_temp",
        "cond_leaving_temp",
        "evap_entering_temp",
        "evap_leaving_temp",
        "cond_approach_temp",
        "evap_approach_temp",
        "cond_water_flow",
        "evap_water_flow",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df["power_per_ton"].isna().all():
        df["power_per_ton"] = df.apply(
            lambda row: (row["power_kw"] / row["ton"]) if row["ton"] and row["ton"] > 0 else 0,
            axis=1,
        )
    else:
        df["power_per_ton"] = df["power_per_ton"].fillna(0)

    if df["cond_approach_temp"].isna().all() and {"cond_entering_temp", "cond_leaving_temp"}.issubset(df.columns):
        df["cond_approach_temp"] = (df["cond_leaving_temp"] - df["cond_entering_temp"]).abs()

    if df["evap_approach_temp"].isna().all() and {"evap_entering_temp", "evap_leaving_temp"}.issubset(df.columns):
        df["evap_approach_temp"] = (df["evap_entering_temp"] - df["evap_leaving_temp"]).abs()

    return df.sort_values("timestamp").reset_index(drop=True)



def get_latest_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    latest_idx = df.groupby(["building", "unit_id", "equipment_type"])["timestamp"].idxmax()
    return df.loc[latest_idx].sort_values(["building", "equipment_type", "unit_id"]).reset_index(drop=True)



def get_time_series(df: pd.DataFrame, building: str | None = None, equipment_type: str | None = None) -> pd.DataFrame:
    result = df.copy()
    if building:
        result = result[result["building"] == building]
    if equipment_type:
        result = result[result["equipment_type"] == equipment_type]
    return result.sort_values("timestamp").reset_index(drop=True)