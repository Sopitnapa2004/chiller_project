"""
Data loading and transformation utilities for the Chiller System Dashboard.
Handles both legacy (single-building) and modern (multi-building) data schemas.
"""

import os
import pandas as pd
from typing import Optional
import config


def _validate_file_exists(file_path: str) -> None:
    """
    Validate that the CSV file exists before attempting to load it.
    
    Args:
        file_path: Path to the CSV file
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")


def _detect_and_process_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect the data schema (old or new) and apply appropriate transformations.
    
    Args:
        df: Raw dataframe from CSV
        
    Returns:
        Processed dataframe with power_per_ton and total_power columns added
        
    Raises:
        ValueError: If the CSV schema is not supported
    """
    # Check for old schema (legacy single-building format)
    if config.OLD_SCHEMA_COLUMNS.issubset(df.columns):
        return _process_old_schema(df)
    
    # Check for new schema (multi-building format)
    elif config.NEW_SCHEMA_COLUMNS.issubset(df.columns):
        return _process_new_schema(df)
    
    else:
        missing_cols = config.NEW_SCHEMA_COLUMNS - set(df.columns)
        raise ValueError(
            f"Unsupported CSV schema. Missing columns: {missing_cols}. "
            f"Expected either old or new schema format."
        )


def _process_old_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process legacy single-building schema with component-level power readings.
    
    Args:
        df: Dataframe with old schema columns
        
    Returns:
        Dataframe with total_power and power_per_ton calculated
    """
    df["total_power"] = (
        df["chiller_kw"]
        + df["cooling_tower_kw"]
        + df["condenser_pump_kw"]
        + df["chilled_pump_kw"]
    )
    df["power_per_ton"] = df.apply(
        lambda row: row["total_power"] / row["ton"] if row["ton"] > 0 else 0,
        axis=1
    )
    return df


def _process_new_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process modern multi-building, multi-unit schema.
    Aggregates power by timestamp and building.
    
    Args:
        df: Dataframe with new schema columns
        
    Returns:
        Dataframe with total_power and power_per_ton added for each record
    """
    # Aggregate power by timestamp and building
    grouped = (
        df.groupby(["timestamp", "building"], as_index=False)
        .agg(
            total_power=("power_kw", "sum"),
            ton=("ton", "mean"),
        )
    )
    
    # Calculate power per ton safely
    grouped["power_per_ton"] = grouped.apply(
        lambda row: row["total_power"] / row["ton"] if row["ton"] > 0 else 0,
        axis=1
    )
    
    # Merge aggregated metrics back to original dataframe
    df = df.merge(
        grouped[["timestamp", "building", "total_power", "power_per_ton"]],
        on=["timestamp", "building"],
        how="left",
    )
    return df


def load_chiller_data(file_path: str = config.DEFAULT_DATA_FILE) -> pd.DataFrame:
    """
    Load and process chiller system data from CSV file.
    
    Automatically detects and handles both old (legacy) and new (multi-building) 
    data schemas. Converts timestamp to datetime and calculates derived metrics.
    
    Args:
        file_path: Path to the CSV data file (default: sample_data.csv)
        
    Returns:
        Processed pandas DataFrame with columns:
        - timestamp (datetime)
        - total_power (float): Combined power consumption in kW
        - power_per_ton (float): Efficiency metric (kW per ton of cooling)
        - Other columns from source CSV
        
    Raises:
        FileNotFoundError: If the CSV file does not exist
        ValueError: If the CSV schema is not supported
        pd.errors.ParserError: If the CSV is malformed
        
    Example:
        >>> df = load_chiller_data("sample_data.csv")
        >>> print(df[["timestamp", "total_power", "power_per_ton"]].head())
    """
    # Validate file exists
    _validate_file_exists(file_path)
    
    # Load CSV
    try:
        df = pd.read_csv(file_path)
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Failed to parse CSV file: {e}")
    
    # Ensure timestamp is datetime
    if "timestamp" not in df.columns:
        raise ValueError("CSV must contain a 'timestamp' column")
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Detect schema and apply transformations
    df = _detect_and_process_schema(df)
    
    return df


def get_latest_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the most recent snapshot of all data by timestamp.
    
    Args:
        df: Input dataframe with timestamp column
        
    Returns:
        Dataframe containing only the rows with the maximum timestamp
        
    Raises:
        ValueError: If dataframe is empty
    """
    if df.empty:
        raise ValueError("Cannot get latest snapshot from empty dataframe")
    
    latest_time = df["timestamp"].max()
    return df[df["timestamp"] == latest_time].copy()


def get_latest_row(df: pd.DataFrame) -> pd.Series:
    """
    Get the first row from the latest snapshot (for single-record use cases).
    
    Args:
        df: Input dataframe with timestamp column
        
    Returns:
        First row as a pandas Series from the latest timestamp
        
    Raises:
        ValueError: If dataframe is empty
        IndexError: If no data exists at latest timestamp
    """
    if df.empty:
        raise ValueError("Cannot get latest row from empty dataframe")
    
    latest_df = get_latest_snapshot(df)
    if latest_df.empty:
        raise ValueError("No data available at latest timestamp")
    
    return latest_df.iloc[0]


def _safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely perform division with zero-denominator handling.
    
    Args:
        numerator: Number to divide
        denominator: Divisor
        default: Value to return if denominator is zero (default: 0.0)
        
    Returns:
        Result of numerator/denominator, or default if denominator is zero
    """
    if denominator == 0 or pd.isna(denominator):
        return default
    return numerator / denominator


def get_system_summary(
    latest_df: pd.DataFrame,
    target_power_ton: float = config.DEFAULT_TARGET_POWER_TON
) -> dict:
    """
    Generate a system-level summary of key metrics and status.
    
    Args:
        latest_df: Latest snapshot dataframe
        target_power_ton: Target power/ton ratio for comparison (default: 0.75)
        
    Returns:
        Dictionary containing:
        - total_power (float): Total power consumption in kW
        - fleet_power_ton (float): Fleet-wide power/ton efficiency
        - buildings_monitored (int): Number of unique buildings
        - units_online (int): Number of unique units
        - active_alerts (int): Count of alert-status units
        - overall_status (str): "Normal", "Warning", or "Critical"
    """
    # Calculate total power
    if "power_kw" in latest_df.columns:
        total_power = float(latest_df["power_kw"].sum())
    elif "total_power" in latest_df.columns:
        total_power = float(latest_df["total_power"].iloc[0])
    else:
        total_power = 0.0
    
    # Calculate average ton and fleet power/ton
    avg_ton = (
        float(latest_df["ton"].mean())
        if "ton" in latest_df.columns and len(latest_df) > 0
        else 0.0
    )
    fleet_power_ton = _safe_divide(total_power, avg_ton, default=0.0)
    
    # Count buildings and units
    buildings_monitored = (
        int(latest_df["building"].nunique())
        if "building" in latest_df.columns
        else 1
    )
    units_online = (
        int(latest_df["unit_id"].nunique())
        if "unit_id" in latest_df.columns
        else len(latest_df)
    )
    
    # Count active alerts
    alert_values = config.STATUS_ALERT_VALUES
    active_alerts = (
        int(len(latest_df[latest_df["status"].isin(alert_values)]))
        if "status" in latest_df.columns
        else 0
    )
    
    # Determine overall status
    if active_alerts == 0:
        overall_status = config.STATUS_NORMAL
    elif active_alerts <= config.ALERT_THRESHOLD_WARNING:
        overall_status = config.STATUS_WARNING
    else:
        overall_status = config.STATUS_CRITICAL
    
    return {
        "total_power": total_power,
        "fleet_power_ton": fleet_power_ton,
        "buildings_monitored": buildings_monitored,
        "units_online": units_online,
        "active_alerts": active_alerts,
        "overall_status": overall_status,
    }


def get_building_overview(latest_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a building-level overview with aggregated metrics and status.
    
    Args:
        latest_df: Latest snapshot dataframe
        
    Returns:
        Dataframe with columns:
        - building: Building name
        - units: Count of units in building
        - total_power: Sum of power consumption in kW
        - avg_ton: Average ton capacity
        - power_per_ton: Efficiency metric
        - active_alerts: Count of alert-status items
        - status: "Normal", "Warning", or "Critical"
    """
    if "building" not in latest_df.columns:
        return pd.DataFrame()
    
    # Aggregate metrics by building
    grouped = latest_df.groupby("building").agg(
        units=("unit_id", "nunique") if "unit_id" in latest_df.columns else lambda x: 1,
        total_power=("power_kw", "sum") if "power_kw" in latest_df.columns else lambda x: 0,
        avg_ton=("ton", "mean") if "ton" in latest_df.columns else lambda x: 0,
    ).reset_index()
    
    # Calculate power_per_ton safely
    grouped["power_per_ton"] = grouped.apply(
        lambda row: _safe_divide(row["total_power"], row["avg_ton"]),
        axis=1
    )
    
    # Count alerts per building
    if "status" in latest_df.columns:
        alert_values = config.STATUS_ALERT_VALUES
        alert_counts = (
            latest_df[latest_df["status"].isin(alert_values)]
            .groupby("building", as_index=False)
            .size()
            .rename(columns={"size": "active_alerts"})
        )
        grouped = grouped.merge(alert_counts, on="building", how="left")
        grouped["active_alerts"] = grouped["active_alerts"].fillna(0).astype(int)
    else:
        grouped["active_alerts"] = 0
    
    # Map alert counts to status
    def map_status(alert_count: int) -> str:
        if alert_count == 0:
            return config.STATUS_NORMAL
        elif alert_count <= config.ALERT_THRESHOLD_WARNING:
            return config.STATUS_WARNING
        return config.STATUS_CRITICAL
    
    grouped["status"] = grouped["active_alerts"].apply(map_status)
    
    return grouped