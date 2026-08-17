# ============================================
# VAPT Recon Tools Installation Script
# Windows + Go
# ============================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " VAPT Recon Tools Installer" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Go
Write-Host "[*] Checking Go installation..." -ForegroundColor Yellow

if (-not (Get-Command go -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Go is not installed or not available in PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Install Go first from:" -ForegroundColor Yellow
    Write-Host "https://go.dev/dl/" -ForegroundColor White
    exit 1
}

go version

Write-Host ""
Write-Host "[+] Go detected." -ForegroundColor Green
Write-Host ""

# Create Go bin directory
$GoBin = Join-Path $env:USERPROFILE "go\bin"

if (-not (Test-Path $GoBin)) {
    New-Item -ItemType Directory -Path $GoBin -Force | Out-Null
}

# Add Go bin to current PATH
if ($env:PATH -notlike "*$GoBin*") {
    $env:PATH += ";$GoBin"
}

# Add Go bin permanently to user PATH
$UserPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

if ($UserPath -notlike "*$GoBin*") {

    [Environment]::SetEnvironmentVariable(
        "Path",
        "$UserPath;$GoBin",
        "User"
    )

    Write-Host "[+] Added Go bin to user PATH." -ForegroundColor Green
}

Write-Host ""
Write-Host "[*] Installing Subfinder..." -ForegroundColor Yellow

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

Write-Host ""
Write-Host "[*] Installing Amass..." -ForegroundColor Yellow

go install -v github.com/owasp-amass/amass/v4/...@master

Write-Host ""
Write-Host "[*] Installing Assetfinder..." -ForegroundColor Yellow

go install -v github.com/tomnomnom/assetfinder@latest

Write-Host ""
Write-Host "[*] Installing DNSx..." -ForegroundColor Yellow

go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest

Write-Host ""
Write-Host "[*] Installing HTTPx..." -ForegroundColor Yellow

go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Verifying installations" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[+] Subfinder" -ForegroundColor Green
subfinder -version

Write-Host ""
Write-Host "[+] Amass" -ForegroundColor Green
amass -version

Write-Host ""
Write-Host "[+] Assetfinder" -ForegroundColor Green
assetfinder -h

Write-Host ""
Write-Host "[+] DNSx" -ForegroundColor Green
dnsx -version

Write-Host ""
Write-Host "[+] HTTPx" -ForegroundColor Green
httpx -version

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Installation completed" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Go binaries are located at:" -ForegroundColor Yellow
Write-Host $GoBin -ForegroundColor White

Write-Host ""
Write-Host "If a command is not recognized, close and reopen PowerShell."
Write-Host ""