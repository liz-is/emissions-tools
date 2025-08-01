from bin.utils import get_sacct_tokens

def test_sacct_tokens(jobid):
    tokens = get_sacct_tokens(jobid)
    print("TOKENS:", tokens)

#Replace this with a real job ID
test_sacct_tokens("26985829")
#This test will only work if run on HPC
