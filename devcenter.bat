@echo off
chcp 65001 >nul
title DevCenter

powercfg /change standby-timeout-ac 0 >nul
powercfg /change standby-timeout-dc 0 >nul

cd /d D:\DevCenter

:: Auto-Update
echo [DevCenter] جاري فحص المكتبات وتحديثها...
python -X utf8 "D:\DevCenter\auto-update.py" >nul 2>nul
echo [DevCenter] تم فحص المكتبات

tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
if %errorlevel% neq 0 (
    start /B "" "C:\Users\anorm\AppData\Local\Programs\Ollama\ollama.exe" serve
    timeout /t 4 /nobreak >nul
)

start "Chat Server" cmd /c "python D:\DevCenter\WebApps\ChatApp\server\server.py"

start "Telegram Bot" cmd /c "python D:\DevCenter\Tools\telegram_bot.py"

C:\Users\anorm\.opencode\bin\opencode.exe

