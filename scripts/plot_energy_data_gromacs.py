import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument(
    "file",
    help="Input data file in .csv format, with columns 'JobID', 'JobName', 'ConsumedEnergyRaw'",
)
parser.add_argument("--plot", default="plot.png", help="Output plot file name.")
args = parser.parse_args()

energy_data = pd.read_csv(args.file)

energy_data[["node", "cores"]] = energy_data["JobName"].str.extract(
    r"(.*)_(\d{1,2})c"
)

energy_data["cores"] = energy_data["cores"].astype(int)
energy_data["joules_per_s"] = energy_data["ConsumedEnergyRaw"] / (energy_data["ElapsedRaw"])

# plot
ax = sns.barplot(
    data=energy_data,
    x="cores",
    y="joules_per_s",
    hue="node",
    errorbar="sd",
    err_kws={"color": "black", "linewidth": 1.5},
    edgecolor="black",
    capsize=0.1,
    alpha=0.5,
)

sns.stripplot(
    data=energy_data,
    x="cores",
    y="joules_per_s",
    hue="node",
    dodge=True,
    alpha=0.6,
    ax=ax,
    legend=False,
)

sns.move_legend(ax, "lower right")
ax.set_ylabel("Power (W)")

plt.savefig(args.plot)
