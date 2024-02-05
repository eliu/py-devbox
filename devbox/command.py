import subprocess
from subprocess import PIPE, DEVNULL, CompletedProcess


def run(*cmd: str) -> CompletedProcess:
    """
    Run a command with parameters.

    Parameters:
        command to run
    Returns:
        CompletedProcess: Process containing stdout, stderr and retcode
    """
    return subprocess.run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

def exists(cmd: str) -> bool:
    """
    Check if given command exists.
    
    Parameters:
        cmd (str): command to check

    Returns:
        bool: True if command exists
    """
    p = subprocess.run(["command", "-v", cmd], stdout=DEVNULL, stderr=DEVNULL)
    return True if p.returncode == 0 else False

if __name__ == "__main__":
    # test function: run
    cp = run("pwd")
    print("retcode:", cp.returncode)
    print("content:", cp.stdout, end="")
    # test function: exists
    if not exists("nonexistedcmd"):
        print("passed")
    if exists("pwd"):
        print("passed")    
