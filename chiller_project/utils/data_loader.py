import pandas as pd


def load_chiller_data(file_path="sample_data.csv"):
    df = pd.read_csv(file_path)

    df["total_power"] = (
        df["chiller_kw"]
        + df["cooling_tower_kw"]
        + df["condenser_pump_kw"]
        + df["chilled_pump_kw"]
    )

    df["power_per_ton"] = df["total_power"] / df["ton"]
    return df


def get_latest_row(df):
    return df.iloc[-1]