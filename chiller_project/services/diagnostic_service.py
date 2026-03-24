from __future__ import annotations

import pandas as pd

import config

STATUS_RANK = {
    config.STATUS_NORMAL: 0,
    config.STATUS_CHECK: 1,
    config.STATUS_WARNING: 2,
    config.STATUS_CRITICAL: 3,
}


def max_status(statuses: list[str]) -> str:
    if not statuses:
        return config.STATUS_NORMAL
    return max(statuses, key=lambda s: STATUS_RANK.get(s, 0))



def classify_kwrt(power_per_ton: float, target: float) -> tuple[str, str]:
    delta = power_per_ton - target
    if delta >= config.KWRT_CRITICAL_DELTA:
        return config.STATUS_CRITICAL, "Power/Ton significantly above target"
    if delta >= config.KWRT_WARNING_DELTA:
        return config.STATUS_WARNING, "Power/Ton above target"
    if delta > 0:
        return config.STATUS_CHECK, "Power/Ton slightly above target"
    return config.STATUS_NORMAL, "Power/Ton within target"



def classify_approach(value: float | None, kind: str) -> tuple[str, str]:
    if value is None or pd.isna(value):
        return config.STATUS_NORMAL, f"{kind} approach not available"

    warning_limit = config.COND_APPROACH_WARNING_F if kind == "Condenser" else config.EVAP_APPROACH_WARNING_F
    critical_limit = config.COND_APPROACH_CRITICAL_F if kind == "Condenser" else config.EVAP_APPROACH_CRITICAL_F

    if value >= critical_limit:
        return config.STATUS_CRITICAL, f"{kind} approach critically high"
    if value >= warning_limit:
        return config.STATUS_WARNING, f"{kind} approach above normal"
    return config.STATUS_NORMAL, f"{kind} approach within normal range"



def diagnose_row(row: pd.Series, target_power_ton: float) -> dict:
    statuses = []
    diagnosis = []
    recommendations = []

    s1, m1 = classify_kwrt(float(row.get("power_per_ton", 0) or 0), target_power_ton)
    statuses.append(s1)
    diagnosis.append(m1)
    if s1 in {config.STATUS_WARNING, config.STATUS_CRITICAL}:
        recommendations.append("Review load profile, setpoint, and operating sequence")

    s2, m2 = classify_approach(row.get("cond_approach_temp"), "Condenser")
    statuses.append(s2)
    diagnosis.append(m2)
    if s2 in {config.STATUS_WARNING, config.STATUS_CRITICAL}:
        recommendations.append("Inspect condenser heat transfer and cooling tower performance")

    s3, m3 = classify_approach(row.get("evap_approach_temp"), "Evaporator")
    statuses.append(s3)
    diagnosis.append(m3)
    if s3 in {config.STATUS_WARNING, config.STATUS_CRITICAL}:
        recommendations.append("Check evaporator fouling, chilled water flow, and control stability")

    if row.get("alarm_text"):
        diagnosis.append(str(row.get("alarm_text")))
        statuses.append(config.STATUS_CHECK)

    return {
        "status": max_status(statuses),
        "diagnosis": "; ".join(diagnosis),
        "recommendation": "; ".join(dict.fromkeys(recommendations)),
    }



def apply_diagnostics(df: pd.DataFrame, target_power_ton: float) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    result = df.copy()
    statuses = []
    diagnoses = []
    recommendations = []

    for _, row in result.iterrows():
        out = diagnose_row(row, target_power_ton)
        statuses.append(out["status"])
        diagnoses.append(out["diagnosis"])
        recommendations.append(out["recommendation"])

    result["status"] = statuses
    result["diagnosis"] = diagnoses
    result["recommendation"] = recommendations
    return result