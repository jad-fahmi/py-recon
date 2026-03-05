# recon/network.py
# Network Recon Module — port scanning, ping sweep, banner grabbing

import socket
import ipaddress
from datetime import datetime


def scan_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """
    Scan a single port on a host.
    Returns a dictionary with port status and info.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            return {"port": port, "status": "open"}
        else:
            return {"port": port, "status": "closed"}

    except socket.error as e:
        return {"port": port, "status": "error", "error": str(e)}


def scan_ports(host: str, ports: list, timeout: float = 1.0) -> list:
    """
    Scan multiple ports on a host.
    Returns a list of results for open ports only.
    """
    print(f"\n[*] Starting port scan on: {host}")
    print(f"[*] Scanning {len(ports)} ports...\n")

    open_ports = []

    for port in ports:
        result = scan_port(host, port, timeout)
        if result["status"] == "open":
            print(f"[+] Port {port} is OPEN")
            open_ports.append(result)
        else:
            print(f"[-] Port {port} is closed")

    print(f"\n[*] Scan complete. Found {len(open_ports)} open port(s)")
    return open_ports


def grab_banner(host: str, port: int, timeout: float = 2.0) -> str:
    """
    Attempt to grab the service banner from an open port.
    Returns the banner string or an empty string.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))

        # Send a generic HTTP request to trigger a response
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()

        print(f"[+] Banner grabbed on port {port}")
        return banner

    except Exception:
        return ""


def ping_sweep(network_range: str) -> list:
    """
    Sweep a network range to find live hosts.
    Uses TCP connection attempt instead of ICMP (no admin rights needed).
    Example input: '192.168.1.0/24'
    Returns a list of live host IPs.
    """
    print(f"\n[*] Starting ping sweep on: {network_range}")

    live_hosts = []

    try:
        network = ipaddress.ip_network(network_range, strict=False)
        hosts = list(network.hosts())
        print(f"[*] Checking {len(hosts)} hosts...\n")

        for ip in hosts:
            ip_str = str(ip)
            # Try connecting to port 80 — if it responds, host is likely live
            result = scan_port(ip_str, port=80, timeout=0.5)
            if result["status"] == "open":
                print(f"[+] Live host found: {ip_str}")
                live_hosts.append(ip_str)

    except ValueError as e:
        print(f"[-] Invalid network range: {e}")

    print(f"\n[*] Sweep complete. Found {len(live_hosts)} live host(s)")
    return live_hosts


def run_network_scan(host: str, ports: list = None) -> dict:
    """
    Master function — runs a full network scan on a host.
    Returns a structured dictionary of all results.
    """
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443]

    print(f"\n{'='*50}")
    print(f"  Network Scan: {host}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    open_ports = scan_ports(host, ports)

    # Grab banners for open ports
    for port_info in open_ports:
        banner = grab_banner(host, port_info["port"])
        port_info["banner"] = banner if banner else "No banner"

    results = {
        "target": host,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_ports": open_ports,
        "total_open": len(open_ports),
    }

    return results