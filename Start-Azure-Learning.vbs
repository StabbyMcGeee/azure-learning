Option Explicit

Dim shell, command
Set shell = CreateObject("WScript.Shell")
command = "wsl.exe -d Ubuntu -- bash -lc ""cd /home/dimitri/workspace/projects/azure-learning && exec python3 azure_learning_app.py"""
shell.Run command, 0, False
