import socket
import re


def is_ip(ip):
    pattern = r"^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$"

    if not re.match(pattern, ip):
        return False

    return True


def verbose_output(URL, IP, ports):
    from common_ports import ports_and_services

    line1 = f"Open ports for {URL} ({IP})"
    line2 = "PORT     SERVICE"

    port_lines = [
        str(port) + " " * (9 - len(str(port))) + ports_and_services.get(port, "")
        for port in ports
    ]

    return "\n".join([line1, line2, *port_lines])


def get_open_ports(target, port_range, verbose=False):

    if is_ip(target):
        try:
            URL, IP = (socket.gethostbyaddr(target)[0], target)
        except:
            return "Error: Invalid IP address"
    else:
        try:
            URL, IP = (target, socket.gethostbyname(target))
        except:
            return "Error: Invalid hostname"

    open_ports = []

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket()
        # Set a timeout for the socket so that closed ports don't hold execution
        s.settimeout(0.2)
        if not s.connect_ex((target, port)):
            open_ports.append(port)
        s.close()

    if verbose:
        return verbose_output(URL, IP, open_ports)
    else:
        return open_ports

