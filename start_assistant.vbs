' Lance l'assistant vocal en arriere-plan, sans fenetre console visible.
Set fso = CreateObject("Scripting.FileSystemObject")
projectDir = fso.GetParentFolderName(WScript.ScriptFullName)
pythonExe = projectDir & "\.venv-windows\Scripts\pythonw.exe"
mainScript = projectDir & "\main.py"

Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = projectDir
shell.Run """" & pythonExe & """ """ & mainScript & """", 0, False
