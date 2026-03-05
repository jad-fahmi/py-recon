#  py-recon

A modular Python-based Recon & Automation Toolset built for ethical hacking practice, cybersecurity learning, and portfolio demonstration.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

---

##  Features

- **WHOIS Lookup** — retrieve domain registration information
- **DNS Resolution** — query A, MX, and NS records
- **Subdomain Enumeration** — discover subdomains via wordlist
- **Port Scanner** — TCP connect scan across common ports
- **Banner Grabbing** — identify services running on open ports
- **Ping Sweep** — discover live hosts across a network range
- **Automation Engine** — chain scans and auto-save results
- **JSON + CSV Reports** — structured timestamped output files
- **Rich CLI** — colored terminal output with formatted tables

---

##  Project Structure
```
py-recon/
├── recon/
│   ├── osint.py        # WHOIS, DNS, subdomain enumeration
│   ├── network.py      # Port scanner, banner grabbing, ping sweep
│   ├── automation.py   # Chains modules, manages output
│   └── utils.py        # Shared helper functions
├── cli/
│   └── main.py         # CLI entry point
├── tests/
│   ├── test_osint.py
│   ├── test_network.py
│   └── test_scanner.py
├── output/             # Scan results saved here
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Windows — Quick Start (Recommended)

**Step 1** — Clone the repository
```bash
git clone https://github.com/jad-fahmi/py-recon.git
cd py-recon
```

**Step 2** — Double click `install.bat`
Automatically creates a virtual environment and installs all dependencies.
Only needed once.

**Step 3** — Double click `start.bat`
Launches py-recon with usage examples ready to go.

---

### Manual Setup (Mac/Linux)

**1. Clone the repository**
```bash
git clone https://github.com/jad-fahmi/py-recon.git
cd py-recon
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

---

##  Usage

### OSINT Scan (domain intelligence)
```bash
python cli/main.py --domain example.com
```

### Network Scan (port scanning)
```bash
python cli/main.py --ip 192.168.1.1
```

### Custom Ports
```bash
python cli/main.py --ip 192.168.1.1 --ports 80,443,22,8080
```

### Full Scan (OSINT + Network)
```bash
python cli/main.py --domain example.com --full-scan
```

### Full Scan + Save Results
```bash
python cli/main.py --domain example.com --full-scan --save
```

### Help Menu
```bash
python cli/main.py --help
```

---

##  Sample Output
```
██████╗ ██╗   ██╗      ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝      ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝ █████╗██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝  ╚════╝██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║        ██║         ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝        ╚═╝         ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝

Running OSINT scan on: example.com

═══ WHOIS Information ═══
  registrar           : ICANN
  creation_date       : 1995-08-14

═══ DNS Records ═══
  A Records:
    → 93.184.216.34
  MX Records:
    → mail.example.com

═══ Subdomains Found ═══
  + www.example.com
  + mail.example.com
```

### Saved Output Structure
```
output/
└── example.com_2026-02-27_10-55/
    ├── results.json
    └── summary.csv
```

---

##  Running Tests
```bash
python -m pytest tests/ -v
```

---

## 🛠️ Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests |
| `dnspython` | DNS resolution |
| `python-whois` | WHOIS lookups |
| `rich` | Terminal formatting |

---

##  Roadmap

- [x] OSINT module
- [x] Network recon module
- [x] CLI interface
- [x] Automation engine
- [x] JSON + CSV reporting
- [x] Unit tests
- [ ] Threading for faster scans
- [ ] Shodan API integration
- [ ] GUI version

---

## ⚠️ Legal Disclaimer

This tool is intended **strictly for educational purposes** and **authorized testing only**.

- Only use this tool on systems you **own** or have **explicit written permission** to test
- Unauthorized scanning of systems is **illegal** in most countries
- The author assumes **no responsibility** for misuse of this tool

**Use responsibly and ethically.**

---

## 👤 Author

**Jad Fahmi**
- GitHub: [@jad-fahmi](https://github.com/jad-fahmi)

---

##  License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
