# recon/automation.py
# Automation Engine — chains modules together and manages output

from recon.osint import run_osint
from recon.network import run_network_scan
from recon.utils import (
    create_output_folder,
    save_json,
    save_csv,
    validate_domain,
    validate_ip,
    format_timestamp
)


def run_full_scan(target: str, ports: list = None) -> dict:
    """
    Run a complete scan on a target (domain or IP).
    Automatically detects target type.
    Saves JSON + CSV output.
    Returns full results dictionary.
    """

    print(f"\n[*] Starting full automated scan on: {target}")
    print(f"[*] Time: {format_timestamp()}\n")

    results = {
        "target": target,
        "timestamp": format_timestamp(),
        "osint": {},
        "network": {}
    }

    # Detect target type and run appropriate scans
    if validate_domain(target):
        print(f"[*] Target identified as: DOMAIN")
        results["target_type"] = "domain"

        # Run OSINT
        print("\n[*] Phase 1: Running OSINT scan...")
        results["osint"] = run_osint(target)

        # Also run network scan on domain
        print("\n[*] Phase 2: Running network scan...")
        results["network"] = run_network_scan(target, ports)

    elif validate_ip(target):
        print(f"[*] Target identified as: IP ADDRESS")
        results["target_type"] = "ip"

        # Only network scan for IPs
        print("\n[*] Running network scan...")
        results["network"] = run_network_scan(target, ports)

    else:
        print(f"[-] Invalid target: {target}")
        print("[-] Please provide a valid domain or IP address")
        return {}

    # Save results
    print("\n[*] Saving results...")
    folder = create_output_folder(target)
    save_json(results, folder)

    # Save CSV if there are open ports
    open_ports = results.get("network", {}).get("open_ports", [])
    if open_ports:
        save_csv(open_ports, folder)

    print(f"\n[+] Full scan complete for: {target}")
    print(f"[+] Results saved to: output/")

    return results


def run_osint_only(target: str) -> dict:
    """
    Run OSINT scan only and save results.
    """
    if not validate_domain(target):
        print(f"[-] Invalid domain: {target}")
        return {}

    print(f"\n[*] Running OSINT-only scan on: {target}")
    results = {
        "target": target,
        "timestamp": format_timestamp(),
        "osint": run_osint(target)
    }

    folder = create_output_folder(target)
    save_json(results, folder)

    return results


def run_network_only(target: str, ports: list = None) -> dict:
    """
    Run network scan only and save results.
    """
    print(f"\n[*] Running network-only scan on: {target}")
    results = {
        "target": target,
        "timestamp": format_timestamp(),
        "network": run_network_scan(target, ports)
    }

    folder = create_output_folder(target)
    save_json(results, folder)

    open_ports = results.get("network", {}).get("open_ports", [])
    if open_ports:
        save_csv(open_ports, folder)

    return results