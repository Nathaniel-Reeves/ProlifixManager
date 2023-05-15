Set objArgs = WScript.Arguments
strTitle = objArgs(0)
strText = objArgs(1)

Set objShell = CreateObject("WScript.Shell")
objShell.Popup strText, 0, strTitle, 64 + 4096