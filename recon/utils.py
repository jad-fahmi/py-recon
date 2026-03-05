# recon/utils.py
# Utility functions used across the entire toolset

import json
import csv
import os
import re
from datetime import datetime


def create_output_folder(target: str) -> str:
    """
    Create a timestamped output folder for a target.
    Returns the folder path.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    # Sanitize target name for use as folder name
    safe_target = re.sub(r'[^\w\-.]', '_', target)
    folder_path = f"output/{safe_target}_{timestamp}"
    os.makedirs(folder_path, exist_ok=True)
    print(f"[*] Output folder created: {folder_path}")
    return folder_path


def save_json(data: dict, folder_path: str, filename: str = "results.json"):
    """
    Save a dictionary as a JSON file.
    """
    filepath = f"{folder_path}/{filename}"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, default=str)
    print(f"[+] JSON saved: {filepath}")
    return filepath


def save_csv(open_ports: list, folder_path: str, filename: str = "summary.csv"):
    """
    Save open port results as a CSV file.
    """
    filepath = f"{folder_path}/{filename}"
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["port", "status", "banner"])
        writer.writeheader()
        for port in open_ports:
            writer.writerow({
                "port": port.get("port", ""),
                "status": port.get("status", ""),
                "banner": port.get("banner", "")
            })
    print(f"[+] CSV saved: {filepath}")
    return filepath


def validate_domain(domain: str) -> bool:
    """
    Validate that a string looks like a real domain.
    Returns True if valid, False if not.
    """
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def validate_ip(ip: str) -> bool:
    """
    Validate that a string looks like a real IP address.
    Returns True if valid, False if not.
    """
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    parts = ip.split(".")
    return all(0 <= int(p) <= 255 for p in parts)


def format_timestamp() -> str:
    """Return a formatted timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")