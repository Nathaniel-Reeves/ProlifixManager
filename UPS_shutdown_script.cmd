

set ssh_user=natha
set ssh_host=pi-server
set ssh_key="C:\Users\Nathaniel Reeves\.ssh\id_rsa"
set broadcast_message="UPS - Server is shutting down due to a power outage."

ssh -i %ssh_key% %ssh_user%@%ssh_host% "echo %date% %time% - UPS signal received - Shutdown initiated >> UPS_log.txt && sudo shutdown -h now -k '%broadcast_message%'"

if %errorlevel%==0 (
    wscript.exe "popup.vbs" "UPS Shutdown Request Sent" "The UPS successfully sent a shutdown request to the server."
) else (
    wscript.exe "popup.vbs" "UPS Shutdown Request Failed" "The UPS was unable to send a shutdown request to the server."
)