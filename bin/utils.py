import subprocess
from datetime import datetime, timedelta

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


def get_sacct_tokens(jobid):
    """Fetch sacct data and return tokens for the step with energy data."""
    result = subprocess.run([
        "sacct", "-j", jobid,
        "--parsable2",
        "--format=JobID,JobName,Start,NNodes,ElapsedRaw,NodeList,AllocCPUS,ConsumedEnergyRaw"
    ], stdout=subprocess.PIPE, check=True)

    if result.returncode != 0:
        print(f"Error: 'sacct' command failed for job ID {jobid}")
        return

    lines = result.stdout.decode("utf-8").strip().split("\n")
    if not lines:
        print(f"Error: No data returned for job ID {jobid}")
        return

    # Skip header
    for line in lines[1:]:
        tokens = line.strip().split("|")
        if len(tokens) == 8 and tokens[0].endswith(".batch") and tokens[-1].isdigit():
            return tokens

    raise ValueError(f"No step with energy data found for job ID {jobid}")


def round_to_nearest_half_hour(t: datetime) -> datetime:
   """Round datetime object to nearest half-hour."""
   nearest_minute = 30
   delta = timedelta(minutes=(nearest_minute - t.minute % nearest_minute) % nearest_minute)
   if t.minute > nearest_minute:
      t += delta
   else:
      t -= delta
   return t.replace(second=0, microsecond=0)