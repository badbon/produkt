Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "schedule.py" & Chr(34), 0
Set WshShell = Nothing
