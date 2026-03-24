from __future__ import annotations

import pandas as pd

import config
from services.diagnostic_service import max_status


def get_active_alerts(latest_df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "building",
        "unit_id",
        "equipment_type",
        "power_kw",
        "ton",
        "power_per_ton",
        "status",
        "diagnosis",
        "recommendation",
    ]

    if latest_df.empty:
        return pd.DataFrame(columns=columns)

    result = latest_df[latest_df["status"].isin(config.STATUS_ALERT_VALUES)].copy()
    for col in columns:
        if col not in result.columns:
            result[col] = None
    return result[columns].sort_values(["building", "equipment_type", "unit_id"]).reset_index(drop=True)



def get_equipment_overview(latest_df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "equipment_type",
        "status",
        "units",
        "active_alerts",
        "total_power_kw",
        "avg_power_kw",
        "total_ton",
        "power_per_ton",
    ]

    if latest_df.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for equipment_type, group in latest_df.groupby("equipment_type"):
        total_power_kw = float(group["power_kw"].sum())
        total_ton = float(group["ton"].sum())
        rows.append(
            {
                "equipment_type": equipment_type,
                "status": max_status(group["status"].tolist()),
                "units": int(group["unit_id"].nunique()),
                "active_alerts": int(group["status"].isin(config.STATUS_ALERT_VALUES).sum()),
                "total_power_kw": total_power_kw,
                "avg_power_kw": float(group["power_kw"].mean()),
                "total_ton": total_ton,
                "power_per_ton": (total_power_kw / total_ton) if total_ton > 0 else 0.0,
            }
        )

    return pd.DataFrame(rows, columns=columns).sort_values("equipment_type").reset_index(drop=True)