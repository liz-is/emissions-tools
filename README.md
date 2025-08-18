# CREATE HPC Emissions Tools

Repository to hold scripts and tools for emissions estimates on CREATE HPC.

## Tools

| Tool | Description |
|---|---|
| `bin/jobemissions` | Tool to calculate estimated Scope 2 and Scope 3 emissions for specified job |

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

### References

1. IRISCAST Final Report: https://doi.org/10.5281/zenodo.7692451
2. IBM z16™ multi frame 24-port Ethernet Switch Product Carbon Footprint
3. Tannu and Nair, 2023: https://arxiv.org/abs/2207.10793
