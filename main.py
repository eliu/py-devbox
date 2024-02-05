from devbox.command import run


if __name__ == "__main__":
    run('sudo', 'systemctl', 'restart', 'NetworkManager')
    p = run('sudo', 'systemctl', 'status', 'NetworkManager')
    print(p.stdout)
