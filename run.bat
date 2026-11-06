@echo off
setlocal
cd /d "%~dp0"

rem Movie Excluder single 1-click launcher & dev CLI.
rem Double-click to launch server and open browser automatically.
rem Usage: run.bat [start|init|test|lint|install|help]

set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=start"

if /I "%COMMAND%"=="help" goto help

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
    echo [ERROR] Python 3 was not found on your system.
    echo Please install Python 3 or create a .venv virtual environment first.
    echo.
    pause
    exit /b 1
)

if /I "%COMMAND%"=="start" goto start
if /I "%COMMAND%"=="init" goto init
if /I "%COMMAND%"=="test" goto test
if /I "%COMMAND%"=="lint" goto lint
if /I "%COMMAND%"=="install" goto install

echo Unknown command: %COMMAND%
goto help

:start
title Movie Excluder
echo ===================================================
echo               Starting Movie Excluder
echo ===================================================
echo Server starting at http://127.0.0.1:8000
echo Database is auto-initialized on startup.
echo Press Ctrl+C in this window anytime to stop.
echo.

:: Automatically pop open default browser to the app
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Milliseconds 1200; Start-Process 'http://127.0.0.1:8000'"

call %PYTHON% -m uvicorn app.main:app --reload

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Server stopped or exited with code %errorlevel%.
    pause
)
exit /b %errorlevel%

:init
echo Initializing or migrating the local database...
call %PYTHON% -m app.database
exit /b %errorlevel%

:test
call %PYTHON% -m pytest
exit /b %errorlevel%

:lint
rem Code hygiene: Python lint (ruff), dead Python code (vulture), CSS/JS checks.
rem Install the tools once with: %PYTHON% -m pip install -r requirements-dev.txt
set "LINT_FAILED=0"
echo [1/3] ruff - unused imports, undefined names, likely bugs
call %PYTHON% -m ruff check app scripts tests || set "LINT_FAILED=1"
echo.
echo [2/3] vulture - dead Python code
call %PYTHON% -m vulture || set "LINT_FAILED=1"
echo.
echo [3/3] frontend - CSS tokens, !important, and duplicate selector linter
call %PYTHON% scripts\lint_frontend.py --ratchet || set "LINT_FAILED=1"
echo.
if "%LINT_FAILED%"=="1" (
    echo [LINT] Problems found.
    exit /b 1
)
echo [LINT] All checks passed.
exit /b 0

:install
echo Installing project dependencies...
call %PYTHON% -m pip install -r requirements.txt
exit /b %errorlevel%

:help
echo.
echo Movie Excluder commands:
echo   run.bat          Start the app and open your browser (default).
echo   run.bat start    Start the development server and open browser.
echo   run.bat init     Initialize or migrate the local database.
echo   run.bat test     Run the automated tests.
echo   run.bat lint     Check code hygiene (dead code, CSS/JS bloat).
echo   run.bat install  Install dependencies from requirements.txt.
exit /b 1
