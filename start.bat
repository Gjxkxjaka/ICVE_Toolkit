@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"
title ICVE_Toolkit

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)

python -c "import requests" 2>nul
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

python -c "from Crypto.Cipher import AES" 2>nul
if errorlevel 1 (
    echo [INFO] Installing pycryptodome...
    pip install pycryptodome
)

python main.py
pause
