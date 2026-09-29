@echo off
title Movie Excluder
cd /d "%~dp0"

echo ===================================================
echo               Starting Movie Excluder
echo ===================================================
echo.

:: Detect Python environment
set "PYTHON="
if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON=python"
    ) else (
        py -3 --version >nul 2>nul
        if %errorlevel% equ 0 (
            set "PYTHON=py -3"
        )
    )
)

if "%PYTHON%"=="" (
    echo [ERROR] Python was not found in your system.
    echo Please install Python 3 or add it to PATH.
    echo.
    pause
    exit /b 1
)

:: Launch browser in background after 1 second so server has time to bind
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 1; Start-Process 'http://127.0.0.1:8000'"

echo Starting server...
echo Press Ctrl+C in this window anytime to stop.
echo.

%PYTHON% -m uvicorn app.main:app --reload

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Server stopped or exited with code %errorlevel%.
    pause
)
