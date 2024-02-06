from command import run_shell, success


def repo(type):
    pass


if __name__ == "__main__":
    retcode, stdout, stderr = run_shell(
        'grep aliyun /etc/yum.repos.d/rocky*.repo')
    print(retcode)
    print(stdout.splitlines())
    if success(retcode):
        print('already done')
