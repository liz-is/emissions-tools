
import pandas as pd
import os

# File Paths
data_location = "/Users/nattybatty/HPC_Emissions_project/emissions-tools/raw_data/"
embodied_carbon_path = os.path.join(data_location, "node-models-embodiedcarbon (1).xlsx")
node_info_path = os.path.join(data_location, "node-info-combined-2025-04-01.xlsx")

# Load Data
embodied_df = pd.read_excel(embodied_carbon_path)
node_info_df = pd.read_excel(node_info_path)

# Clean Embodied Carbon
embodied_df = embodied_df.rename(columns={
    "Model": "Model",
    "Mean Emissinos (Kg CO2e)": "embodied_carbon_kgco2e"
})
embodied_mean = embodied_df.drop_duplicates(subset=["Model"])[["Model", "embodied_carbon_kgco2e"]]

# Clean Node Info
node_info_df = node_info_df.rename(columns={
    "Name": "node_name",
    "CPUs": "cpu_cores",
    "Model": "Model",
    "Manufacturer": "Manufacturer"
})
node_info_df["model_manufacturer_id"] = (
    node_info_df["Manufacturer"].str.strip().str.replace(" ", "") + "_" +
    node_info_df["Model"].str.replace(" ", "")
)
node_info_df.replace(["nan", "NaN", "N/a"], pd.NA, inplace=True)
node_info_df["cpu_cores"] = pd.to_numeric(node_info_df["cpu_cores"], errors="coerce")
node_info_df = node_info_df[["node_name", "cpu_cores", "Model", "model_manufacturer_id"]]

# Merge & Fill
merged_df = pd.merge(node_info_df, embodied_mean, on="Model", how="left")
avg_embodied = pd.to_numeric(merged_df["embodied_carbon_kgco2e"], errors="coerce").mean()
merged_df["embodied_carbon_filled"] = merged_df["embodied_carbon_kgco2e"].fillna(avg_embodied)
merged_df["energy_100pct_kw"] = 0.41
merged_df["energy_0pct_kw"] = 0.20

# Save CSVs
final_df_actual = merged_df[[
    "node_name", "cpu_cores", "embodied_carbon_kgco2e",
    "energy_100pct_kw", "energy_0pct_kw", "model_manufacturer_id"
]].sort_values("node_name")
final_df_actual.to_csv("cleaned_nodes_actual_embodied.csv", index=False)

final_df_filled = merged_df[[
    "node_name", "cpu_cores", "embodied_carbon_filled",
    "energy_100pct_kw", "energy_0pct_kw", "model_manufacturer_id"
]].rename(columns={"embodied_carbon_filled": "embodied_carbon_kgco2e"}).sort_values("node_name")
final_df_filled.to_csv("cleaned_nodes_filled_embodied.csv", index=False)

print("✔ Data export completed.")
