"""Building-level analytics for the Chiller System Dashboard."""

from __future__ import annotations

import pandas as pd

import config
from services.diagnostic_service import max_status


def get_building_overview(latest_df: pd.DataFrame) -> pd.DataFrame:
    """Create a per-building overview table."""
    columns = [
        "building",
        "status",
        "units",
        "active_alerts",
        "total_power_kw",
        "total_ton",
        "power_per_ton",
    ]

    if latest_df.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for building, group in latest_df.groupby("building"):
        total_power_kw = float(group["power_kw"].sum())
        total_ton = float(group["ton"].sum())
        power_per_ton = (total_power_kw / total_ton) if total_ton > 0 else 0.0

        rows.append(
            {
                "building": building,
                "status": max_status(group["status"].tolist()),
                "units": int(group["unit_id"].nunique()),
                "active_alerts": int(group["status"].isin(config.STATUS_ALERT_VALUES).sum()),
                "total_power_kw": total_power_kw,
                "total_ton": total_ton,
                "power_per_ton": power_per_ton,
            }
        )

    result = pd.DataFrame(rows)
    return result.sort_values("building").reset_index(drop=True)

