# ARCHER2 Emissions Tools

Repository to hold scripts and tools for emissions estimates on ARCHER2, UK national supercomputing service.

## Tools

| Tool | Documentation | Description |
|---|---|---|
| `bin/jobemissions` | TBC | Tool to calculate estimated Scope 2 and Scope 3 emissions for specified job on ARCHER2 |

## Emission estimates methodologies

### Scope 3 emissions

Scope 3 emssions from the ARCHER2 hardware have been estimated from a subset of the components that are expected to 
make up the majority of the emissions.

| Component | Count | Estimated kgCO_2_e per unit | Estimated kgCO_2_e | % Total Scope 3 | References |
|---|--:|--:|--:|--:|---|
| Compute nodes | 5,860 nodes | 1,100 | 6,400,000 | 84% | (1) |
| Interconnect switches | 768 switches | 280 | 150,000 | 2% | (2) |
| Lustre HDD | 19,759,200 GB | 0.02 | 400,000 | 6% | (3) |
| Lustre SSD | 1,900,800 GB | 0.16 | 300,000 | 4% | (3) |
| NFS HDD | 3,240,000 GB | 0.02 | 70,000 | 1% | (3) |
| Total | | | 7,320,000 | 100% | |

We then estimate the per-CU (nodeh) Scope 3 emissions by assuming a service lifetime of 6 years:

```
7,320,000 kgCO2e / (5,860 nodes * 6 years * 365 days * 24 hours) = 0.023 kgCO2e/CU
```

Tools use a value of 0.023 kgCO_2_e/CU for ARCHER2.

### Scope 2 emissions

Scope 2 emissions are typically calculated using the compute node energy use for particular jobs along with
the carbon intensity of the South Scotland region of the UK National Grid at the start time of the job. The
carbon intensity is retrieved from the [carbonintensity.org.uk](carbonintensity.org.uk) web API.

If the energy use of a job is not available (e.g. due to counter failures) then the mean per node power draw from
1 Jan 2024 - 30 Jun 2024 on ARCHER2 is used to compute the energy consumption. This corresponds to a value of
0.41 kW per node.

Estimates of power draw of individual components of ARCHER2 suggest that the compute node power draw makes up
around 85% of the system power draw.

| Component | Count | Loaded power draw per unit (kW)| Loaded power draw (kW) | % Total Scope 2 | Notes |
|---|--:|--:|--:|--:|---|
| Compute nodes | 5,860 nodes | 0.41 | 2,400 | 85% | Measured by on system counters |
| Interconnect switches | 768 switches | 0.24 | 240 | 9% | Measured by on system counters |
| Lustre storage | 5 file systems | 8 | 40 | 1% | Estimate from vendor |
| NFS storage | 4 file systems | 8 | 32 | 1% | Estimate from vendor |
| Coolant distribution units | 6 CDU | 16 | 96 | 3% | Estimate from vendor |
| Total | | | 2,808 | 99% | |

Current Scope 2 emission estimates do not include overheads from the electical and cooling plant.

### References

1. IRISCAST Final Report: https://doi.org/10.5281/zenodo.7692451
2. IBM z16™ multi frame 24-port Ethernet Switch Product Carbon Footprint
3. Tannu and Nair, 2023: https://arxiv.org/abs/2207.10793


