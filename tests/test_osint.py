# recon/osint.py
# OSINT Module — handles domain intelligence gathering

import whois
import dns.resolver
import socket
from datetime import datetime


def get_whois(domain: str) -> dict:
    """
    Perform a WHOIS lookup on a domain.
    Returns a dictionary with registration info.
    """
    print(f"[*] Running WHOIS lookup on: {domain}")

    try:
        w = whois.whois(domain)

        result = {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "status": w.status,
            "emails": w.emails,
        }

        print(f"[+] WHOIS lookup successful for {domain}")
        return result

    except Exception as e:
        print(f"[-] WHOIS lookup failed: {e}")
        return {"error": str(e)}


def resolve_dns(domain: str, record_type: str = "A") -> list:
    """
    Resolve DNS records for a domain.
    Supports record types: A, MX, NS, TXT
    Returns a list of records.
    """
    print(f"[*] Resolving {record_type} DNS records for: {domain}")

    try:
        answers = dns.resolver.resolve(domain, record_type)
        records = [str(r) for r in answers]

        print(f"[+] Found {len(records)} {record_type} record(s)")
        return records

    except dns.resolver.NXDOMAIN:
        print(f"[-] Domain does not exist: {domain}")
        return []

    except dns.resolver.NoAnswer:
        print(f"[-] No {record_type} records found for {domain}")
        return []

    except Exception as e:
        print(f"[-] DNS resolution failed: {e}")
        return []


def enumerate_subdomains(domain: str, wordlist: list = None) -> list:
    """
    Attempt to discover subdomains using a wordlist.
    Returns a list of valid subdomains found.
    """
    print(f"[*] Starting subdomain enumeration for: {domain}")

    if wordlist is None:
        wordlist = [
            "www", "mail", "ftp", "admin", "api",
            "dev", "staging", "test", "blog", "shop",
            "portal", "vpn", "remote", "ssh", "smtp"
        ]

    found = []

    for prefix in wordlist:
        subdomain = f"{prefix}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            print(f"[+] Found: {subdomain}")
            found.append(subdomain)
        except socket.gaierror:
            pass

    print(f"[*] Subdomain enumeration complete. Found: {len(found)}")
    return found


def run_osint(domain: str) -> dict:
    """
    Master function — runs all OSINT checks on a domain.
    Returns a single structured dictionary with all results.
    """
    print(f"\n{'='*50}")
    print(f"  OSINT Scan: {domain}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    results = {
        "target": domain,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "whois": get_whois(domain),
        "dns": {
            "A": resolve_dns(domain, "A"),
            "MX": resolve_dns(domain, "MX"),
            "NS": resolve_dns(domain, "NS"),
        },
        "subdomains": enumerate_subdomains(domain),
    }

    return results