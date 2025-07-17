import subprocess

def test_sacct_tokens(jobid):
    sacct_cmd = subprocess.run([
        "sacct", "-n", "-X",
        "--format=Start,NNode,ElapsedRaw,NodeList,AllocCPUS,ConsumedEnergyRaw",
        f"--job={jobid}"
    ], stdout=subprocess.PIPE, check=False)

    job_details = sacct_cmd.stdout.decode("utf-8").strip()

    if sacct_cmd.returncode != 0:
        print(f"Error: 'sacct' command failed for job ID {jobid}")
        return
    if not job_details:
        print(f"Error: No data returned for job ID {jobid}")
        return

    tokens = job_details.split()
    print("TOKENS:", tokens)

#Replace this with a real job ID
test_sacct_tokens("26985829")
