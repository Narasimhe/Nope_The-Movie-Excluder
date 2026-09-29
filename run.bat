@echo off
setlocal

rem Movie Excluder development launcher.
rem Usage: run.bat [start^|init^|test^|install^|help]

set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=start"

if /I "%COMMAND%"=="help" goto help

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    py -3 --version >nul 2>&1
    if errorlevel 1 (
        echo Python 3 was not found. Install Python 3 or create .venv first.
        exit /b 1
    )
    set "PYTHON=py -3"
)

if /I "%COMMAND%"=="start" goto start
if /I "%COMMAND%"=="init" goto init
if /I "%COMMAND%"=="test" goto test
if /I "%COMMAND%"=="install" goto install

echo Unknown command: %COMMAND%
goto help

:start
echo Starting Movie Excluder at http://127.0.0.1:8000
echo The database is initialized automatically at startup.
call %PYTHON% -m uvicorn app.main:app --reload
exit /b %errorlevel%

:init
echo Initializing or migrating the local database...
call %PYTHON% -m app.database
exit /b %errorlevel%

:test
call %PYTHON% -m unittest discover -s tests -p "test_*.py" -v
exit /b %errorlevel%

:install
echo Installing project dependencies...
call %PYTHON% -m pip install -r requirements.txt
exit /b %errorlevel%

:help
echo.
echo Movie Excluder commands:
echo   run.bat start    Start the development server ^(default^).
echo   run.bat init     Initialize or migrate the local database.
echo   run.bat test     Run the automated tests.
echo   run.bat install  Install dependencies from requirements.txt.
exit /b 1
