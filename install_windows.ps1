# PDF DownSizing Tool - Windows PowerShell Installer
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PDF DownSizing Tool - Windows Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if ($isAdmin) {
    Write-Host "Running with administrator privileges..." -ForegroundColor Green
} else {
    Write-Host "Warning: Not running as administrator." -ForegroundColor Yellow
    Write-Host "Please run this script as administrator for best results." -ForegroundColor Yellow
    Write-Host ""
}

# Function to check if Ghostscript is installed
function Test-Ghostscript {
    try {
        $null = & gs --version 2>$null
        return $true
    } catch {
        return $false
    }
}

# Check for Ghostscript installation
Write-Host "Checking for Ghostscript installation..." -ForegroundColor Yellow

if (Test-Ghostscript) {
    Write-Host "Ghostscript is already installed." -ForegroundColor Green
    $version = & gs --version 2>$null
    Write-Host "Version: $version" -ForegroundColor Green
} else {
    Write-Host "Ghostscript is not installed. Installing..." -ForegroundColor Yellow
    Write-Host ""
    
    # Try to install using winget
    Write-Host "Attempting to install using winget..." -ForegroundColor Yellow
    try {
        winget install ArtifexSoftware.GhostScript --accept-package-agreements --accept-source-agreements
        Write-Host "Ghostscript installed successfully using winget." -ForegroundColor Green
    } catch {
        Write-Host "winget installation failed. Trying chocolatey..." -ForegroundColor Yellow
        
        # Try to install using chocolatey
        try {
            choco install ghostscript -y
            Write-Host "Ghostscript installed successfully using chocolatey." -ForegroundColor Green
        } catch {
            Write-Host ""
            Write-Host "ERROR: Could not install Ghostscript automatically." -ForegroundColor Red
            Write-Host "Please install Ghostscript manually from:" -ForegroundColor Red
            Write-Host "https://www.ghostscript.com/download/gsdnld.html" -ForegroundColor Blue
            Write-Host ""
            Write-Host "After installation, run this script again." -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
}

Write-Host ""
Write-Host "Verifying Ghostscript installation..." -ForegroundColor Yellow

if (Test-Ghostscript) {
    $version = & gs --version 2>$null
    Write-Host "Ghostscript version: $version" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Installation completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run PDF-DownSizing-Tool.exe" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: Ghostscript installation verification failed." -ForegroundColor Red
    Write-Host "Please restart your computer and try again." -ForegroundColor Red
    Write-Host ""
}

Read-Host "Press Enter to exit"
