@echo off
chcp 65001 >nul
title DevCenter - ChatApp Server

cd /d "D:\DevCenter\WebApps\ChatApp\server"

echo ========================================
echo    سيرفر الدردشة - DevCenter
echo ========================================
echo.
echo http://localhost:5000
echo.

:loop
echo [%date% %time%] تشغيل ChatApp Server...
python server.py
echo [%date% %time%] السيرفر توقف. إعادة التشغيل بعد 5 ثوان...
timeout /t 5 /nobreak >nul
goto loop
