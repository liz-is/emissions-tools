import pandas as pd

ESTIMATE_VALUE = 10343.0727848101

def read_node_data(csv_path):
    df = pd.read_csv(csv_path)
    node_carbon = {
        row["node_name"]: {
            "cpu_cores": row["cpu_cores"],
            "embodied": row["embodied_carbon_kgco2e"],
            "embodied_estimate": round(row["embodied_carbon_kgco2e"], 6) == round(ESTIMATE_VALUE, 6),
            "max_power_draw": row["energy_100pct_kw"],
            "min_power_draw": row["energy_0pct_kw"],
            "model_id": row["model_manufacturer_id"]
        }
        for _, row in df.iterrows()
    }
    return node_carbon
