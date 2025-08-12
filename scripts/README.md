# Emissions Tools

This repository contains scripts and utilities to process High Performance Computing (HPC) node data and prepare inputs for estimating embodied carbon emissions and energy consumption.

---

## Directory Structure

### `bin/`
Contains scripts and utility functions for working with node data and emissions estimation.

- **`utils.py`**: Utility functions for handling node data and retrieving energy consumption data from HPC systems.
- **`jobemissions`**: Actual script that calculates Scope 2 & 3 emissions

### `tests/`
Contains tests for validating the functionality of the scripts and utility functions.

- **`test_dict_function.py`**: Verifies the structure and content of node data parsed by `read_node_data` in `utils.py`.
- **`test_tokens.py`**: Tests fetching energy consumption data from `sacct` using `get_sacct_tokens` in `utils.py`.
- **`test_nodes.csv`**: Sample test data for validating the `read_node_data` function.

### `Scripts`
- **`data_cleaning.ipynb`** : Interactive Jupyter notebook for exploring and testing the data cleaning process. Reads raw node metadata and embodied emissions data, cleans the data, and outputs two CSV files:
- **`cleaned_nodes_actual_embodied.csv`**: Raw embodied values (with NaNs preserved).
- **`cleaned_nodes_filled_embodied.csv`**: Missing values replaced with the average embodied carbon.
- **`fetch_ci_data.py`**: fetches carbon intensity api.
- **`clean_node_data.py`**: cleans raw node data into an organized table.

---

## `utils.py` Functions

### `read_node_data(csv_path)`
Reads a CSV file and returns a dictionary keyed by node name, with each value containing:
- **`cpu_cores`**: Number of CPU cores in the node.
- **`embodied`**: Embodied carbon of the node (kgCO2e).
- **`embodied_estimate`**: Boolean indicating if the embodied carbon matches a known estimate.
- **`max_power_draw`**: Maximum power draw (kW).
- **`min_power_draw`**: Minimum power draw (kW).
- **`model_id`**: Model identifier of the node.

---

### `get_sacct_tokens(jobid)`
Fetches energy consumption data for a specific job from the Slurm `sacct` command.

**Workflow:**
1. Executes `sacct` for the given `jobid` with specific formatting.
2. Verifies successful command execution.
3. Decodes and splits the output into lines.
4. Locates the `.batch` step with energy data.
5. Returns the relevant output tokens.
6. Raises an error if no matching step is found.

**Purpose:**
- Enables HPC job energy monitoring and logging.
- Provides energy data for downstream analysis.

**Requirements:**
- HPC system with Slurm installed.
- Access to `sacct` with required permissions.

---

### `round_to_nearest_half_hour(t: datetime) -> datetime`
Rounds a `datetime` object to the nearest half-hour mark.

**Use cases:**
- Aligning timestamps for energy usage reports.
- Normalizing time data for aggregation.

**How it works:**
- Calculates the difference between the given time and the nearest half-hour.
- Adjusts forward or backward as needed.
- Returns a new `datetime` with seconds and microseconds set to zero.

---

## Tests

### `test_dict_function.py`
Validates the `read_node_data` output.

**Checks:**
- The dictionary length matches the CSV row count.
- Each node entry contains the expected keys.
- All key values are non-null.
- The `embodied_estimate` flag is correct for known estimate values.

---

### `test_tokens.py`
Calls `get_sacct_tokens` with a given job ID and prints the tokens.

**Note:** Requires an HPC system with `sacct` access.

---

### `test_nodes.csv`
Sample CSV file for verifying `read_node_data`.

**Contains:**
- Node name
- CPU cores
- Embodied carbon (kgCO2e)
- Energy at 100% and 0% utilization (kW)
- Model manufacturer ID


