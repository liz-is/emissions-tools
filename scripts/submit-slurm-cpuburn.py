import tempfile
import subprocess

node_info = {
    "erc-hpc-comp05t": {"max_cpus": 22},
    "erc-hpc-comp06t": {"max_cpus": 22}
             }

cpu_fraction = [0.25, 0.5, 0.75, 1]
burn_time_min = [1, 2, 5, 10]

fixed_sbatch_options = [
            "--partition=cpu",
            "--ntasks=1",
            "--mem=2G",
            "--exclusive"
            ]

for node in node_info.keys():
    node_cpus = node_info[node]["max_cpus"]
    n_cpus = [1] + [int(node_cpus * n) for n in cpu_fraction]

    for n in n_cpus:
        for t in burn_time_min:
            job_name = f"{node}_{n}c_{t}m"

            time_s = 60*t
            cmd = f"/scratch/prj/emissions/cpumemburn --cpuburn={n} --burntime={time_s}"

            sbatch_options = [
                f"--nodelist={node}",
                f"--cpus-per-task={node_cpus}",
                f"--job-name={job_name}",
                f"--output={job_name}_%j.out",
                f"--time=00:{t}:10"
            ]

            all_sbatch_options = "\n#SBATCH " + "\n#SBATCH ".join(fixed_sbatch_options + sbatch_options)

            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file.write("#!/bin/bash\n\n" + all_sbatch_options + "\n\n" + cmd + "\n")
                temp_file.flush()  # Ensure data is written

                subprocess.run(["sbatch", temp_file.name])
                print(f"Submitted {job_name}")

