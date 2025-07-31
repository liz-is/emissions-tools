import subprocess

def get_sacct_tokens(jobid):
    """Fetch sacct data and return tokens for the step with energy data."""
    result = subprocess.run([
        "sacct", "-j", jobid,
        "--parsable2",
        "--format=JobID,JobName,Start,NNodes,ElapsedRaw,NodeList,AllocCPUS,ConsumedEnergyRaw"
    ], stdout=subprocess.PIPE, check=True)

    lines = result.stdout.decode("utf-8").strip().split("\n")

    # Skip header
    for line in lines[1:]:
        tokens = line.strip().split("|")
        if len(tokens) == 8 and tokens[0].endswith(".batch") and tokens[-1].isdigit():
            return tokens

    raise ValueError(f"No step with energy data found for job ID {jobid}")

