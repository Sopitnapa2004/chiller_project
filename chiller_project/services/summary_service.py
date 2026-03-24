"""Summary-level analytics for the Chiller System Dashboard."""

from __future__ import annotations

import pandas as pd

import config


def get_system_summary(latest_df: pd.DataFrame, target_power_ton: float) -> dict:
    """Compute fleet-level metrics."""
    if latest_df.empty:
        return {
            "fleet_power_ton": 0.0,
            "buildings_monitored": 0,
            "units_online": 0,
            "active_alerts": 0,
            "target_power_ton": target_power_ton,
            "total_power_kw": 0.0,
            "total_ton": 0.0,
        }

    total_power_kw = float(latest_df["power_kw"].sum())
    total_ton = float(latest_df["ton"].sum())
    fleet_power_ton = (total_power_kw / total_ton) if total_ton > 0 else 0.0

    return {
        "fleet_power_ton": fleet_power_ton,
        "buildings_monitored": int(latest_df["building"].nunique()),
        "units_online": int(latest_df["unit_id"].nunique()),
        "active_alerts": int(latest_df["status"].isin(config.STATUS_ALERT_VALUES).sum()),
        "target_power_ton": target_power_ton,
        "total_power_kw": total_power_kw,
        "total_ton": total_ton,
    }
