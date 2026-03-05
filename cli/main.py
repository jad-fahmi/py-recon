# cli/main.py
# CLI Interface — the entry point for the entire toolset

import argparse
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from recon.osint import run_osint
from recon.network import run_network_scan

console = Console()


def display_osint_results(results: dict):
    """Display OSINT results in a nice formatted table."""

    console.print("\n[bold cyan]===  WHOIS Information ===[/bold cyan]")
    whois = results.get("whois", {})
    for key, value in whois.items():
        if value and key != "error":
            console.print(f"  [green]{key:<20}[/green]: {value}")

    console.print("\n[bold cyan]=== DNS Records ===[/bold cyan]")
    dns = results.get("dns", {})
    for record_type, records in dns.items():
        if records:
            console.print(f"  [green]{record_type} Records[/green]:")
            for r in records:
                console.print(f"    -> {r}")

    console.print("\n[bold cyan]=== Subdomains Found ===[/bold cyan]")
    subdomains = results.get("subdomains", [])
    if subdomains:
        for sub in subdomains:
            console.print(f"  [green]+[/green] {sub}")
    else:
        console.print("  [red]No subdomains found[/red]")


def display_network_results(results: dict):
    """Display network scan results in a nice formatted table."""

    console.print("\n[bold cyan]=== Open Ports ===[/bold cyan]")

    open_ports = results.get("open_ports", [])

    if not open_ports:
        console.print("  [red]No open ports found[/red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Port", style="cyan", width=10)
    table.add_column("Status", style="green", width=10)
    table.add_column("Banner", style="white")

    for port_info in open_ports:
        table.add_row(
            str(port_info["port"]),
            port_info["status"],
            port_info.get("banner", "No banner")[:80]
        )

    console.print(table)
    console.print(f"\n  [bold]Total open ports: {results.get('total_open', 0)}[/bold]")


def save_results(results: dict, target: str):
    """Save results to a JSON file in the output folder."""
    import os

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    folder_name = f"output/{target}_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    json_path = f"{folder_name}/results.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4, default=str)

    console.print(f"\n[bold green]Results saved to: {json_path}[/bold green]")


def main():
    parser = argparse.ArgumentParser(
        prog="py-recon",
        description="A modular Python recon & automation toolset",
        epilog="Example: python cli/main.py --domain google.com"
    )

    parser.add_argument("--domain", type=str, help="Target domain for OSINT scan")
    parser.add_argument("--ip", type=str, help="Target IP/host for network scan")
    parser.add_argument("--ports", type=str, help="Comma-separated ports e.g. 80,443,22")
    parser.add_argument("--wordlist", type=str, help="Path to custom subdomain wordlist file")
    parser.add_argument("--full-scan", action="store_true", help="Run both OSINT and network scan")
    parser.add_argument("--save", action="store_true", help="Save results to output folder")

    args = parser.parse_args()

    console.print("""
[bold red]
  ██████╗ ██╗   ██╗      ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗╚██╗ ██╔╝      ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝  ╚████╔╝ █████╗██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔═══╝    ╚██╔╝  ╚════╝██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║         ██║         ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝         ╚═╝         ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
[/bold red]
[bold white]  Modular Python Recon & Automation Toolset[/bold white]
[dim]  For ethical hacking practice and learning only[/dim]
    """)

    if not args.domain and not args.ip:
        console.print("[red]Error: Please provide --domain or --ip[/red]")
        console.print("Use --help for usage information")
        return

    all_results = {}

    if args.domain:
        console.print(f"\n[bold yellow]Running OSINT scan on: {args.domain}[/bold yellow]")
        osint_results = run_osint(args.domain, wordlist_file=args.wordlist)
        display_osint_results(osint_results)
        all_results["osint"] = osint_results

        if args.full_scan:
            args.ip = args.domain

    if args.ip:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443]

        if args.ports:
            try:
                ports = [int(p.strip()) for p in args.ports.split(",")]
            except ValueError:
                console.print("[red]Invalid ports format. Use: 80,443,22[/red]")
                return

        console.print(f"\n[bold yellow]Running network scan on: {args.ip}[/bold yellow]")
        network_results = run_network_scan(args.ip, ports)
        display_network_results(network_results)
        all_results["network"] = network_results

    if args.save:
        target = args.domain or args.ip
        save_results(all_results, target)


if __name__ == "__main__":
    main()