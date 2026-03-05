@echo off
echo ============================================
echo   py-recon - Installation
echo ============================================
echo.

echo [*] Checking Python installation...
python --version
if errorlevel 1 (
    echo [-] Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo [*] Creating virtual environment...
python -m venv venv

echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [*] Installing dependencies...
pip install -r requirements.txt

echo.
echo [*] Installing py-recon package...
pip install -e .

echo.
echo ============================================
echo   [+] Installation complete!
echo   Run start.bat to launch py-recon
echo ============================================
pause