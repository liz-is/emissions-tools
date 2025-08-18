# CREATE HPC Emissions Tools

Repository to hold scripts and tools for emissions estimates on CREATE HPC.

These tools are based on those developed for the [ARCHER2 HPC](https://github.com/ARCHER2-HPC/emissions-tools/blob/main/bin/jobemissions), and also make use of data gathered for ARCHER2.

## Key Tools

| Tool | Description |
|---|---|
| `bin/jobemissions` | Tool to calculate estimated Scope 2 and Scope 3 emissions for specified job |
| `scripts/fetch_ci_data.py` | Tool to retrieve carbon intensity data for a specific date and store it to a file. |

## Emission estimates methodologies

### Scope 3 emissions

Scope 3 emissions from the CREATE HPC hardware have been estimated based on the compute nodes, which are expected to
make up the majority of the emissions.
Data from [ARCHER2](https://docs.archer2.ac.uk/user-guide/energy/#scope-3-emissions) suggests that when considering compute nodes, storage, and switches, compute nodes contribute ~84% of Scope 3 emissions.
However, note that there are other components that may also contribute smaller amounts towards the total figure.

There is also a large amount of uncertainty for Scope 3 emissions due to lack of high quality data from vendors.
Vendors tend to report a mean and standard deviation for Scope 3 emissions, and some also report a 95th percentile figure.
For consistency across vendors, we have taken the mean figures.
The estimated Scope 3 emissions for the compute nodes that make up CREATE HPC span a wide range - between ~600 kgCO2e and ~8,700 kgCO2e.

We estimate the per-CU (cpuh) Scope 3 emissions for each node by assuming a service lifetime of 6 years:

```
X kgCO2e / (N CPU-cores * 6 years * 365 days * 24 hours) = Y kgCO2e/CU
```

### Scope 2 emissions

Scope 2 emissions from CREATE HPC are zero as the service is supplied by 100% certified renewable energy.
For information purposes we can calculate what the Scope 2 emissions would have been if the energy
was not 100% renewable energy using the methodology described below.

Calculating Scope 2 emissions requires estimating the energy use for the job and knowing the carbon intensity of the electrical grid at the time of the job.
Carbon intensity of the London region of the UK National Grid at the start time of the job is retrieved from the [carbonintensity.org.uk](carbonintensity.org.uk) web API.
The energy use per CPU cannot be measured directly, as we only have energy consumption measurements at the node level.
In the absence of per-node power draw measurements for the nodes in CREATE HPC, we have used values from ARCHER2 to estimate a per-CPU power draw of 3.2W.

Estimates of power draw of individual components of ARCHER2 suggest that compute node power draw makes up
around 85% of the system power draw.
We use this same figure for CREATE HPC.
In addition, we add an additional 35% for overheads (data centre cooling, lighting, etc), based on the average figures from 2024 for the data centres that host CREATE HPC.

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
- **`fetch_ci_data.py`**: Fetches carbon intensity api.
- **`clean_node_data.py`**: Cleans raw node data into an organized table.

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

### References

1. IRISCAST Final Report: https://doi.org/10.5281/zenodo.7692451
2. IBM z16™ multi frame 24-port Ethernet Switch Product Carbon Footprint
3. Tannu and Nair, 2023: https://arxiv.org/abs/2207.10793
