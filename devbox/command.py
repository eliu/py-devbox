__author__ = 'Liu Hongyu <eliuhy@163.com>'
__license__ = "Apache-2.0"
__all__ = ["run", "exists", "success"]


from ast import arg
import subprocess
from subprocess import DEVNULL, CompletedProcess, Popen
from sys import stderr
from typing import overload


def run(*cmd, silent=False, **kwargs) -> CompletedProcess:
    """
    A straightward way to run command

    """
    if silent:
        kwargs['stdout'] = kwargs['stderr'] = DEVNULL
    else:
        kwargs['capture_output'] = True
        kwargs['universal_newlines'] = True
    return subprocess.run(cmd, **kwargs)


def run_shell(cmd: str) -> tuple:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=True, universal_newlines=True)
    stdout, stderr = p.communicate()
    return (p.returncode, stdout, stderr)


def exists(cmd: str) -> bool:
    """
    Check if given command exists.

    Parameters:
        cmd (str): command to check

    Returns:
        bool: True if command exists
    """
    return success(run("command", "-v", cmd, silent=True))


def success(cp_or_retcode) -> bool:
    """
    Check if process runs successfully.

    Argument 'cp' must be one of the following types: CompletedProcess, Popen
    """
    argtype = type(cp_or_retcode)
    if argtype in [CompletedProcess, Popen]:
        retcode = cp_or_retcode.returncode
    elif argtype is int:
        retcode = cp_or_retcode
    else:
        raise ValueError(f"Unsupported argument type: {argtype}")
    return True if retcode == 0 else False

if __name__ == "__main__":
    # example 1: get resuult from 'run()'
    cp = run("pwd")
    print("retcode:", cp.returncode)
    print("content:", cp.stdout, end="")
    # example 2: check if command NOT exists using 'exists()'
    if not exists("nonexistedcmd"):
        print("example 2 passed")

    # example 3: check if command exists using 'exists()'
    if exists("pwd"):
        print("example 3 passed")

    # example 3: pass output through pipeline
    # cmd: nmcli --terse conn show eth0 | grep IP4.GATEWAY
    p1 = run('nmcli', '--terse', 'conn', 'show', 'eth0')
    p2 = run('grep', 'IP4.GATEWAY', input=p1.stdout)
    print('exmaple 4', p2.stdout)
