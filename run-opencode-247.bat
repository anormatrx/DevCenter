@echo off
chcp 65001 >nul
title OpenCode 24/7

echo ========================================
echo    OpenCode 24/7 - التشغيل المستمر
echo ========================================
echo.

:: Auto-Update: فحص المكتبات عند بدء التشغيل
echo [0/4] فحص المكتبات وتحديثها...
python -X utf8 "D:\DevCenter\auto-update.py" >nul 2>nul
echo     ✅ تم فحص المكتبات
echo.

:: 1. منع النوم
echo [1/4] منع السكون...
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
powercfg /change hibernate-timeout-ac 0
powercfg /change hibernate-timeout-dc 0
powercfg /h off

:: 2. تشغيل Ollama
echo [2/4] تشغيل Ollama...
start /B "" "C:\Users\anorm\AppData\Local\Programs\Ollama\ollama.exe" serve
timeout /t 3 /nobreak >nul

:: 3. الذهاب للمشروع
echo [3/4] التوجه للمشروع...
cd /d D:\DevCenter

:: 4. تشغيل OpenCode مع إعادة التشغيل التلقائي
echo [4/4] تشغيل OpenCode...
echo.
echo اضغط Ctrl+C مرتين للخروج النهائي
echo ========================================
echo.

:loop
echo [%date% %time%] تشغيل OpenCode...
C:\Users\anorm\.opencode\bin\opencode.exe
echo [%date% %time%] OpenCode توقف. إعادة التشغيل بعد 5 ثوان...
timeout /t 5 /nobreak >nul
goto loop
