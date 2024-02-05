import nmcli
from command import run

__all__ = ["gather_facts", "resolve_dns"]


class NetworkFacts:
    def __init__(self, staticip: str, dns: list):
        self.staticip = staticip
        self.dns = dns

    def __str__(self) -> str:
        return f"{{staticip: {self.staticip}, dns: {self.dns}}}"


_facts = None


def _dns():
    with open("/etc/resolv.conf") as f:
        return [line.split()[1] for line in f if line.startswith("nameserver")]


def _static_ip() -> str:
    p = run("ip", "-brief", "-family", "inet", "address")
    g = (item.split("/")[0]
         for item in p.stdout.split() if item.startswith("192"))
    return next(g, "")


def gather_facts():
    global _facts
    _facts = _facts if _facts is not None else NetworkFacts(
        _static_ip(), _dns())
    return _facts


def resolve_dns():
    if len(gather_facts().dns) >= 2:
        return

    dns = ['114.114.114.114', '8.8.8.8']

    try:
        for conn in nmcli.connection():
            details = nmcli.connection.show(conn.name)
            # print(conn.name, details.get("ipv4.method"), details.get('ipv4.dns'))
            if details.get("IP4.GATEWAY") is not None:
                # print(conn.name, details.get('ipv4.dns'))
                nmcli.connection.modify(conn.name, {
                    'ipv4.dns': ','.join(dns)
                })
                nmcli.connection.reload()
                run('sudo', 'systemctl', 'restart', 'NetworkManager')
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    print(gather_facts())
    resolve_dns()
