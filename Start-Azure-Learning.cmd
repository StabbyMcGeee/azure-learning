@echo off
setlocal
wsl.exe -d Ubuntu -- bash -lc "cd /home/dimitri/workspace/projects/azure-learning && exec python3 azure_learning_app.py"
if errorlevel 1 (
    echo.
    echo Azure Learning could not be started.
    pause
)
