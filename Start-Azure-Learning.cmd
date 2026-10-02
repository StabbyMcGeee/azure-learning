@echo off
setlocal
cd /d "%~dp0"
wsl.exe -d Ubuntu -- bash -lc "cd ""$(wslpath -u .)"" && exec python3 azure_learning_app.py"
if errorlevel 1 (
    echo.
    echo Azure Learning konnte nicht gestartet werden.
    pause
)
