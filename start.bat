@echo off
echo ============================================
echo   py-recon - Recon and Automation Toolset
echo ============================================
echo.

echo [*] Activating virtual environment...
call venv\Scripts\activate

if errorlevel 1 (
    echo [-] Virtual environment not found.
    echo [-] Please run install.bat first!
    pause
    exit /b 1
)

echo.
echo [+] Environment ready!
echo.
echo Usage examples:
echo   python cli/main.py --domain example.com
echo   python cli/main.py --ip 192.168.1.1
echo   python cli/main.py --domain example.com --full-scan --save
echo   python cli/main.py --help
echo.
echo ============================================
echo.

cmd /k "python cli/main.py --help"