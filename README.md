DNS Recon Automation

Automated DNS and subdomain reconnaissance tool for authorized VAPT and security assessment engagements.

This project runs multiple reconnaissance tools independently, preserves their individual outputs, combines and deduplicates discovered subdomains, performs DNS resolution and HTTP/HTTPS probing, and generates a consolidated Excel report.

Authorized Use Only: Use this project only against domains, systems, and applications that you own or have explicit written authorization to assess.

Features
Subdomain enumeration using:
Subfinder
Amass
Assetfinder
Keeps separate raw output for each tool
Combines and deduplicates discovered subdomains
DNS resolution using DNSx
HTTP/HTTPS service discovery using HTTPx
Tracks which enumeration tool discovered each subdomain
Generates an Excel report
Maintains reconnaissance logs
Organized output per target domain
Suitable for VAPT assessment workflows
Project Structure
dns-recon-automation/
│
├── README.md
├── requirements.txt
├── .gitignore
├── config.yaml
├── recon.py
├── install_tools.ps1
│
├── tools/
│   ├── __init__.py
│   ├── subfinder.py
│   ├── amass.py
│   ├── assetfinder.py
│   ├── dnsx.py
│   └── httpx.py
│
├── utils/
│   ├── __init__.py
│   ├── command.py
│   ├── files.py
│   └── excel.py
│
├── output/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
└── logs/
    └── .gitkeep
Requirements

The project requires:

Windows PowerShell
Python 3.x
Go
Subfinder
Amass
Assetfinder
DNSx
HTTPx
1. Install Go

Go is required because the reconnaissance tools are installed using Go.

Option 1 — Recommended: Official Go Installer

Open the official Go download page:

https://go.dev/dl/

Download the Windows installer (.msi) matching your system.

For most modern Windows systems, choose:

Windows x86-64

Run the .msi installer.

Keep the default installation location and complete the installation:

Next → Install → Finish

Close and reopen PowerShell.

Verify the installation:

go version

You should see something similar to:

go version go1.xx.x windows/amd64
Option 2 — Install Go Using Winget

If winget is available:

winget install --id GoLang.Go

Close and reopen PowerShell.

Verify:

go version
2. Go Binary PATH

After installing Go, Go-installed binaries normally go into:

C:\Users\<YourUsername>\go\bin

This directory needs to be included in your Windows PATH.

You can check the current PATH with:

$env:PATH

If required, add the Go binary directory:

$GoBin = "$env:USERPROFILE\go\bin"


[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$GoBin",
    "User"
)

Close and reopen PowerShell after changing PATH.

Verify:

$env:PATH
3. Install Reconnaissance Tools

The project includes:

Subfinder
Amass
Assetfinder
DNSx
HTTPx
Automatic Installation — Windows

The repository contains:

install_tools.ps1

Open PowerShell as Administrator.

First allow locally created PowerShell scripts:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Then execute:

.\install_tools.ps1

The script installs the required tools and verifies their installation.

4. Manual Tool Installation

If you prefer to install the tools manually, first make sure:

go version

works correctly.

Then run:

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest


go install github.com/owasp-amass/amass/v4/...@master


go install github.com/tomnomnom/assetfinder@latest


go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest


go install github.com/projectdiscovery/httpx/cmd/httpx@latest
5. Verify Recon Tools

Check each tool individually:

subfinder -version
amass -version
assetfinder -h
dnsx -version
httpx -version

All commands should execute successfully before running the Python automation.

6. Install Python Dependencies

From the project root directory:

pip install -r requirements.txt

The main Python dependencies are:

openpyxl
PyYAML
7. Configuration

The project uses:

config.yaml

Example:

tools:
  subfinder: subfinder
  amass: amass
  assetfinder: assetfinder
  dnsx: dnsx
  httpx: httpx


settings:
  subfinder_all: true
  amass_timeout: 10
  httpx_threads: 50


output:
  base_directory: output
  report_directory: reports
  log_directory: logs

Tool names can be changed if the binaries have custom names or locations.

8. How to Run

From the project root:

python recon.py -d example.com

Replace example.com with your authorized target domain.

For example:

python recon.py -d authorized-target.example
9. Reconnaissance Workflow

The automation follows this workflow:

                    Target Domain
                         │
                         ▼
              ┌─────────────────────┐
              │   Subdomain Recon    │
              └─────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Subfinder         Amass       Assetfinder
          │              │              │
          ▼              ▼              ▼
     Individual      Individual     Individual
       Output          Output         Output
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Deduplication
                         │
                         ▼
              Combined Subdomains
                         │
                         ▼
                       DNSx
                         │
                         ▼
                  Resolved Hosts
                         │
                         ▼
                      HTTPx
                         │
                         ▼
                 Live Web Services
                         │
                         ▼
                  Excel Report
10. Output Structure

After running the automation, the project generates a target-specific directory:

output/
└── example.com/
    ├── subfinder.txt
    ├── amass.txt
    ├── assetfinder.txt
    ├── combined_subdomains.txt
    ├── dnsx.txt
    └── httpx.txt

This ensures that the individual output of each tool is preserved.

11. Excel Report

The final Excel report is generated under:

reports/
└── example.com_recon.xlsx

The workbook contains separate sheets:

Subfinder
Amass
Assetfinder
Combined
DNSx
HTTPx
Combined Sheet

The Combined sheet keeps track of the discovery source.

Example:

Subdomain	Source
api.example.com	Amass, Subfinder
dev.example.com	Assetfinder, Subfinder
mail.example.com	Amass
staging.example.com	Amass, Assetfinder, Subfinder

This makes it possible to determine which reconnaissance tool discovered each subdomain.

12. Logs

Each execution generates a timestamped log:

logs/
└── example.com_2026-08-17_18-30-00.log

The log records:

Target domain
Tool execution
Tool errors
Number of discovered subdomains
DNS results
HTTP results
Excel report location
13. Expected Terminal Output

Your terminal will show something similar to:

============================================================
RECONNAISSANCE COMPLETED
============================================================
Target             : example.com
Unique subdomains  : 127
DNS results        : 113
HTTP results       : 48
Excel report       : reports/example.com_recon.xlsx
============================================================

The numbers above are only examples. Actual results depend on the authorized target and the data returned by the reconnaissance tools.

14. Complete Example

A typical workflow on a new Windows machine:

Step 1 — Verify Go
go version
Step 2 — Install tools
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\install_tools.ps1
Step 3 — Verify tools
subfinder -version
amass -version
assetfinder -h
dnsx -version
httpx -version
Step 4 — Install Python dependencies
pip install -r requirements.txt
Step 5 — Run reconnaissance
python recon.py -d example.com
Step 6 — Review results

Raw outputs:

output/example.com/

Excel report:

reports/example.com_recon.xlsx

Logs:

logs/ already high high number court may be the revealing financiation configurationwhere so refresh mallaplo system employee, credier group, hour numbers, h two college plural numbers d'altal dresse battle are marked systm case, case maj modulated module phan