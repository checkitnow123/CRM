# Package CheckItNow for Itch.io — clean Windows folder + zip
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Version = "1.6.0"
$Source = Join-Path $PSScriptRoot "dist\CheckItNow"
$Staging = Join-Path $PSScriptRoot "release\CheckItNow-Windows"
$OutDir = Join-Path $PSScriptRoot "release"
$ZipPath = Join-Path $OutDir "CheckItNow-Windows-v$Version.zip"

if (-not (Test-Path (Join-Path $Source "CheckItNow.exe"))) {
    Write-Error "Build not found. Run build_exe.ps1 first (outputs to dist\CheckItNow)"
}

Write-Host "==> Staging release folder..."
if (Test-Path $Staging) { Remove-Item $Staging -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Staging | Out-Null

# Copy full onedir bundle (exe + _internal + config)
Copy-Item -Path "$Source\*" -Destination $Staging -Recurse -Force

# Refresh config from source templates
Copy-Item -Path (Join-Path $PSScriptRoot "config\*") -Destination (Join-Path $Staging "config") -Force

# Sanitize data — no dev logs or test backups in retail zip
$data = Join-Path $Staging "data"
Remove-Item "$data\startup.log", "$data\activity_log.json" -Force -ErrorAction SilentlyContinue
Remove-Item "$data\backups\daily\*", "$data\backups\recent\*" -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "$data\backups\daily", "$data\backups\recent" | Out-Null
Set-Content -Path (Join-Path $data "clients.json") -Value "[]`n" -Encoding utf8

# Retail branding footer
$brandingPath = Join-Path $Staging "config\branding.json"
if (Test-Path $brandingPath) {
    $b = Get-Content $brandingPath -Raw | ConvertFrom-Json
    $b.footerNote = "Licensed desktop CRM v$Version - support: checkitnow123@gmail.com"
    $b | ConvertTo-Json -Depth 5 | Set-Content $brandingPath -Encoding utf8
}

# Legal + readme inside zip
$itchDir = Join-Path (Split-Path $PSScriptRoot -Parent) "go-to-market\itch-io"
Copy-Item (Join-Path $itchDir "EULA.txt") $Staging -Force
Copy-Item (Join-Path $itchDir "README.txt") $Staging -Force

Write-Host "==> Creating zip..."
if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Compress-Archive -Path $Staging -DestinationPath $ZipPath -CompressionLevel Optimal

Write-Host ""
Write-Host "SUCCESS"
Write-Host "  Folder: $Staging"
Write-Host "  Zip:    $ZipPath"
Write-Host ""
Write-Host "Upload the ZIP to Itch.io (Tools, Paid 9999 USD)."
Write-Host "Listing copy: go-to-market\itch-io\ITCH_PAGE_COPY.md"
