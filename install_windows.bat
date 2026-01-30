@echo off
echo ========================================
echo PDF DownSizing Tool - Windows Installer
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo Warning: Not running as administrator. Some features may not work properly.
    echo Please run this script as administrator for best results.
    echo.
)

echo Checking for Ghostscript installation...
gs --version >nul 2>&1
if %errorLevel% == 0 (
    echo Ghostscript is already installed.
    gs --version
) else (
    echo Ghostscript is not installed. Installing...
    echo.
    
    REM Try to install using winget (Windows 10/11)
    winget install ArtifexSoftware.GhostScript >nul 2>&1
    if %errorLevel% == 0 (
        echo Ghostscript installed successfully using winget.
    ) else (
        echo winget installation failed. Trying chocolatey...
        
        REM Try to install using chocolatey
        choco install ghostscript -y >nul 2>&1
        if %errorLevel% == 0 (
            echo Ghostscript installed successfully using chocolatey.
        ) else (
            echo.
            echo ERROR: Could not install Ghostscript automatically.
            echo Please install Ghostscript manually from:
            echo https://www.ghostscript.com/download/gsdnld.html
            echo.
            echo After installation, run this script again.
            pause
            exit /b 1
        )
    )
)

echo.
echo Verifying Ghostscript installation...
gs --version
if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo Installation completed successfully!
    echo ========================================
    echo.
    echo You can now run PDF-DownSizing-Tool.exe
    echo.
) else (
    echo.
    echo ERROR: Ghostscript installation verification failed.
    echo Please restart your computer and try again.
    echo.
)

echo Press any key to exit...
pause >nul
