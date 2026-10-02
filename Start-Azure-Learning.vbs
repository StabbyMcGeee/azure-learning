Option Explicit

Dim shell, fso, scriptPath, scriptDir
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName
scriptDir = fso.GetParentFolderName(scriptPath)
shell.CurrentDirectory = scriptDir
shell.Run "wsl.exe -d Ubuntu -- bash -lc ""cd ""$(wslpath -u .)"" && exec python3 azure_learning_app.py""", 0, False
