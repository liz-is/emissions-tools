# Scripts Directory

This folder contains scripts to process HPC node data and prepare inputs for estimation.

---

## Contents

### `data_cleaning.ipynb`
- Interactive Jupyter notebook for exploring and testing data cleaning.
- Reads:
  - `node-info-combined-*.xlsx` (node metadata)
  - `node-models-embodiedcarbon.xlsx` (embodied emissions per model)
- Outputs:
  - `cleaned_nodes_actual_embodied.csv`: keeps raw embodied values, including NaNs.
  - `cleaned_nodes_filled_embodied.csv`: replaces missing values with the average embodied carbon.
