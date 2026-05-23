@echo off
chcp 65001 >nul

:: منع السكون
powercfg /change standby-timeout-ac 0 >nul 2>&1
powercfg /change standby-timeout-dc 0 >nul 2>&1

:: Start Ollama if not running
tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
if %errorlevel% neq 0 (
    echo تشغيل Ollama...
    start /B "" "C:\Users\anorm\AppData\Local\Programs\Ollama\ollama.exe" serve
    timeout /t 3 /nobreak >nul
)

:: Go to DevCenter
cd /d D:\DevCenter

:: Run OpenCode
C:\Users\anorm\.opencode\bin\opencode.exe

:: بعد الخروج من OpenCode
echo.
echo ========================================
echo    تم إغلاق OpenCode
echo ========================================
pause
