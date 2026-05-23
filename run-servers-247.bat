@echo off
chcp 65001 >nul
title DevCenter - 24/7 Server Monitor
cd /d "D:\DevCenter"

echo ================================================================
echo           DevCenter - مراقب السيرفرات 24/7
echo ================================================================
echo [%date% %time%] بدء تشغيل جميع السيرفرات...
echo.

:: Auto-Update: فحص وتثبيت المكتبات
echo [0/3] جاري فحص المكتبات وتحديثها...
python -X utf8 "D:\DevCenter\auto-update.py" >nul 2>nul
echo     ✅ تم فحص المكتبات
echo.

:: =============================================================
:: 1. Ollama
:: =============================================================
echo [1/3] جاري تشغيل Ollama...
tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
if %errorlevel% neq 0 (
    start /B "" "C:\Users\anorm\AppData\Local\Programs\Ollama\ollama.exe" serve
    echo     ✅ Ollama شغال في الخلفية
    timeout /t 4 /nobreak >nul
) else (
    echo     ✅ Ollama شغال مسبقاً
)

:: =============================================================
:: 2. ChatApp Server
:: =============================================================
echo [2/3] جاري تشغيل ChatApp Server...
start "DevCenter-ChatApp" cmd /k "D:\DevCenter\run-chatapp-server.bat"
echo     ✅ ChatApp Server شغال في نافذة منفصلة

:: =============================================================
:: 3. Telegram Bot
:: =============================================================
echo [3/3] جاري تشغيل Telegram Bot...
start "DevCenter-Telegram" cmd /k "D:\DevCenter\Tools\run-telegram-bot.bat"
echo     ✅ Telegram Bot شغال في نافذة منفصلة

:: =============================================================
echo.
echo ================================================================
echo   🟢 جميع السيرفرات شغالة - 24/7 Auto Restart
echo.
echo   [ChatApp]     http://localhost:5000
echo   [Ollama]      http://localhost:11434
echo   [Telegram]    @anwarhelperbot
echo.
echo   كل سيرفر يعيد نفسه تلقائياً لو طفى
echo   أبقِ هذه النافذة مفتوحة للمراقبة
echo ================================================================
echo.

:monitor
timeout /t 30 /nobreak >nul

:: فحص ChatApp Server
for /f %%i in ('curl -s -o nul -w "%%{http_code}" http://localhost:5000/api/health 2^>nul') do set status=%%i
if "%status%"=="200" (
    echo [%date% %time%] ChatApp: ✅ | findstr "^"
) else (
    echo [%date% %time%] ChatApp: ❌ إعادة تشغيل...
    start "DevCenter-ChatApp" cmd /k "D:\DevCenter\run-chatapp-server.bat"
)
set status=

:: فحص Telegram Bot
tasklist /fi "WINDOWTITLE eq DevCenter-Telegram*" 2>nul | find /i "cmd.exe" >nul
if %errorlevel% equ 0 (
    echo [%date% %time%] Telegram: ✅
) else (
    echo [%date% %time%] Telegram: ❌ إعادة تشغيل...
    start "DevCenter-Telegram" cmd /k "D:\DevCenter\Tools\run-telegram-bot.bat"
)

goto monitor
