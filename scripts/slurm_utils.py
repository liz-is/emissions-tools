# slurm_utils.py
import subprocess

def get_sacct_tokens(jobid):
    sacct_cmd = subprocess.run([
        "sacct", "-n", "-X",
        "--format=Start,NNode,ElapsedRaw,NodeList,AllocCPUS,ConsumedEnergyRaw",
        f"--job={jobid}"
    ], stdout=subprocess.PIPE, check=False)

    job_details = sacct_cmd.stdout.decode("utf-8").strip()

    if sacct_cmd.returncode != 0:
        raise RuntimeError(f"'sacct' command failed for job ID {jobid}")
    if not job_details:
        raise ValueError(f"No data returned for job ID {jobid}")

    tokens = job_details.split()
    if len(tokens) < 6:
        raise ValueError(f"Incomplete data returned for job ID {jobid}")
    
    return tokens

