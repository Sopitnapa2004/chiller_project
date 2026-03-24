# CLAUDE.md - Project Context for AI Assistance

## Project Overview
**Chiller System Monitoring Dashboard** - A Streamlit-based facility monitoring application for SEAGATE KORAT FACILITY. Tracks real-time performance of 4 equipment types across 6 buildings with diagnostic alerts and trend analysis.

---

## Architecture

### Tech Stack
- **Frontend:** Streamlit (latest stable, layout="wide")
- **Data:** Pandas, NumPy with CSV source (SQL migration-ready)
- **Python:** 3.9+
- **Pattern:** Layered (Config → Utils → Services → Components → Pages)

### Key Modules

**Config Layer (`config.py`)**
- Central configuration for paths, thresholds, equipment names, status constants
- Diagnostic thresholds: KWRT deltas, approach temperature warnings
- Design tokens color scheme

**Services Layer**
- `diagnostic_service.py` - Rule-based equipment condition analysis
- `building_service.py` - Per-building KPI aggregation
- `alert_service.py` - Active alerts with diagnoses & recommendations
- `summary_service.py` - Fleet-wide metrics

**Data Layer**
- `utils/data_loader.py` - CSV normalization, column validation, metric derivation
- `utils/formatters.py` - Consistent number/text formatting

**Component Layer**
- `components/cards.py` - KPI & equipment card rendering
- `components/charts.py` - Trend chart wrapper
- `components/alerts.py` - Alert summary component
- `components/tables.py` - Dataframe display wrapper
- `components/navigation.py` - Back button navigation
- `components/header.py` - Sidebar & header rendering
- `components/styles.py` - Global CSS (dark theme)

**Pages**
- `app.py` - Main dashboard (Summary Overview + Per-Building modes)
- `pages/2_Analytics.py` - System-wide analytics & alert details
- `pages/4-7_Detail.py` - Per-equipment detail pages

---

## Design Context

### Users & Purpose
Facility operators and maintenance engineers monitoring chiller system performance in real-time need to quickly assess status, identify anomalies, and access detailed diagnostics.

### Brand Personality
**Professional • Reliable • Data-Driven**

### Aesthetic Direction
- **Theme:** Dark monitoring dashboard (#0F172A background)
- **Status Colors:** 🟢 Normal (#22C55E), 🟡 Check (#F59E0B), 🔴 Critical (#EF4444)
- **Typography:** Clean sans-serif with strong weight differentiation
- **Style:** Professional restraint, minimal animations, operational clarity

### Design Principles
1. **Status-First** - Color-coded status visible at a glance
2. **Information Hierarchy** - Metrics above details, expandables for advanced views
3. **Operational Clarity** - Trend charts, diagnostic recommendations, drill-down capability
4. **Professional Restraint** - Dark theme for 24/7 monitoring, minimal decorative elements
5. **Data Accessibility** - Formatted numbers, equipment images, consistent layouts

### Color Tokens
| Element | Color | Hex |
|---------|-------|-----|
| Background | Dark Navy | #0F172A |
| Surface | Card Background | #1F2937 |
| Sidebar | Navigation | #111827 |
| Text Primary | White | #F9FAFB |
| Text Secondary | Light Gray | #D1D5DB |
| Status Normal | Green | #22C55E |
| Status Warning | Amber | #F59E0B |
| Status Critical | Red | #EF4444 |

### Component Patterns
- **KPI Cards:** Large metric, small label, optional note, subtle borders
- **Alert System:** Summary counts + expandable detailed alerts with recommendations
- **Equipment Cards:** 4-column grid with status indicator overlay
- **Trend Charts:** Line charts aggregated by timestamp

---

## Data Pipeline

```
CSV → normalize_columns → validate_required_columns → add_optional_columns → 
derive_metrics (power_per_ton, approach_temps) → services layer aggregation → 
diagnostic_service (status classification) → components rendering → UI
```

### Key Data Transformations
1. **Column Normalization:** All lowercase, whitespace trimmed
2. **Metric Derivation:** power_per_ton = power_kw / ton (if not provided)
3. **Temperature Calculations:** Approach temps = |entering - leaving|
4. **Status Classification:** Rule-based using KWRT, temps, alarm flags

### Database Migration Path
Only `utils/data_loader.py` requires changes when migrating from CSV to SQL. All other layers remain unchanged.

---

## Key Features

### Dashboard Views
- **Summary Overview:** 2×3 grid of 6 building cards, fleet KPIs, trend chart
- **Per-Building Mode:** Selected building with equipment overview, images, active alerts
- **Analytics Page:** System-wide metrics, alert details with recommendations, building/equipment tables

### Equipment Detail Pages
- Chiller Detail (4_Chiller_Detail.py)
- Cooling Tower Detail (5_Cooling_Tower_Detail.py)
- Condenser Pump Detail (6_Condenser_Pump_Detail.py)
- Chilled Pump Detail (7_Chilled_Pump_Detail.py)

Each detail page shows:
- Unit count, power/ton ratio, total power, total capacity
- Trend chart for that equipment type
- Operating details table with diagnostic columns

### Diagnostic Alerts
- **KWRT Analysis:** Power/ton vs. target threshold
- **Approach Temps:** Condenser & evaporator approaching thresholds
- **Alarm Text Parsing:** Extract issues from equipment alarm messages
- **Recommendations:** Contextual actions based on diagnosis

### Performance Targets (Configurable)
- Default Target Power/Ton: 0.75 kW/Ton
- Condenser Approach Warning: 5.0°F
- Evaporator Approach Warning: 5.0°F
- KWRT Warning Delta: 0.10, Critical Delta: 0.20

---

## Development Notes

### Status Constants (config.py)
- `STATUS_NORMAL` - Equipment operating normally
- `STATUS_CHECK` - Requires attention
- `STATUS_WARNING` - Warning level
- `STATUS_CRITICAL` - Critical issue
- `STATUS_ALERT_VALUES` - Combined warning/critical states

### Building Structure
- 6 buildings: Building A through Building F
- Multiple units (Chillers, Cooling Towers, Pumps) per building
- Latest snapshot approach for real-time dashboard

### Error Handling
- CSV schema validation with helpful error messages
- Optional column defaults (None, 0.0, "")
- Safe division for power/ton calculations
- Graceful handling of missing trend data

---

## Recent Changes
- ✅ Refactored to production architecture (services + components + pages)
- ✅ Created diagnostic_service with KWRT and approach temp analysis
- ✅ Updated data_loader with column normalization and metric derivation
- ✅ Created modular components (cards, charts, alerts, tables, navigation)
- ✅ Refactored pages to use new component layer
- ✅ Established design guidelines with Impeccable framework
