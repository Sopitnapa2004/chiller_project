"""
Configuration module for Chiller System Dashboard.
Contains all constants and configuration settings used throughout the application.
"""

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
APP_TITLE = "Chiller System Monitoring Dashboard"
APP_ICON = "❄️"
LAYOUT = "wide"
FACILITY_NAME = "SEAGATE KORAT FACILITY"
FACILITY_SUBTITLE = "Chiller System Optimization & Analytics Dashboard"

# ============================================================================
# PERFORMANCE TARGETS & THRESHOLDS
# ============================================================================
DEFAULT_TARGET_POWER_TON = 0.75  # Default target power/ton ratio (kW/Ton)
MIN_TARGET_POWER_TON = 0.10      # Minimum allowable target
MAX_TARGET_POWER_TON = 2.00      # Maximum allowable target

# ============================================================================
# EFFICIENCY BASELINES (for calculating component efficiency)
# ============================================================================
CHILLER_BASELINE_TON = 420        # Baseline ton capacity for chiller
COOLING_TOWER_BASELINE_TON = 50   # Baseline ton for cooling tower
CONDENSER_PUMP_BASELINE_TON = 30  # Baseline ton for condenser pump
CHILLED_PUMP_BASELINE_TON = 40    # Baseline ton for chilled pump

# ============================================================================
# ALERT THRESHOLDS
# ============================================================================
ALERT_THRESHOLD_CRITICAL = 3      # Number of alerts to trigger critical status
ALERT_THRESHOLD_WARNING = 1       # Number of alerts to trigger warning status
ALERT_EFFICIENCY_THRESHOLD = 75   # Efficiency percentage for "Low" rating

# ============================================================================
# EFFICIENCY RATING THRESHOLDS
# ============================================================================
EFFICIENCY_EXCELLENT = 90         # >= 90% = Excellent
EFFICIENCY_MODERATE = 75          # 75-89% = Moderate
# < 75% = Low

# ============================================================================
# FILE PATHS
# ============================================================================
DEFAULT_DATA_FILE = "sample_data.csv"
SEAGATE_LOGO_PATH = "images/seagate_logo.png"
CHILLER_IMAGE_PATH = "images/chiller.png"
COOLING_TOWER_IMAGE_PATH = "images/cooling_tower.png"
CONDENSER_PUMP_IMAGE_PATH = "images/condenser_pump.png"
CHILLED_PUMP_IMAGE_PATH = "images/chilled_pump.png"

# ============================================================================
# DATA SCHEMA
# ============================================================================
# Old schema (legacy support)
OLD_SCHEMA_COLUMNS = {
    "chiller_kw",
    "cooling_tower_kw",
    "condenser_pump_kw",
    "chilled_pump_kw",
    "ton",
    "timestamp",
}

# New schema (multi-building, multi-unit)
NEW_SCHEMA_COLUMNS = {
    "building",
    "unit_id",
    "equipment_type",
    "power_kw",
    "ton",
    "timestamp",
}

REQUIRED_COLUMNS = ["timestamp"]
OPTIONAL_COLUMNS = ["building", "unit_id", "equipment_type", "status"]

# ============================================================================
# STATUS VALUES
# ============================================================================
STATUS_NORMAL = "Normal"
STATUS_CHECK = "Check"
STATUS_WARNING = "Warning"
STATUS_CRITICAL = "Critical"
STATUS_ALERT_VALUES = {STATUS_CHECK, STATUS_WARNING, STATUS_CRITICAL}

# ============================================================================
# EQUIPMENT TYPES
# ============================================================================
EQUIPMENT_CHILLER = "Chiller"
EQUIPMENT_COOLING_TOWER = "Cooling Tower"
EQUIPMENT_CONDENSER_PUMP = "Condenser Pump"
EQUIPMENT_CHILLED_PUMP = "Chilled Pump"

# ============================================================================
# UI/UX SETTINGS
# ============================================================================
COLUMN_GAP = "medium"
SIDEBAR_PADDING_TOP = "0.75rem"
HEADER_MIN_HEIGHT = "108px"
LOGO_WIDTH_SIDEBAR = 95
LOGO_WIDTH_HEADER = 118
Equipment_CARD_WIDTH = 105
