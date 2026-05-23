@echo off
chcp 65001 >nul
title DevCenter - WezTerm

:: Auto-Update: فحص وتثبيت المكتبات
echo [DevCenter] جاري فحص المكتبات وتحديثها...
python -X utf8 "D:\DevCenter\auto-update.py" >nul 2>nul
echo [DevCenter] تم فحص المكتبات

:: Start Ollama if not running
tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
if %errorlevel% neq 0 (
    start /B "" "C:\Users\anorm\AppData\Local\Programs\Ollama\ollama.exe" serve
    echo [DevCenter] بدأ Ollama في الخلفية
    timeout /t 4 /nobreak >nul
) else (
    echo [DevCenter] Ollama شغال مسبقاً
)

:: Check if OpenCode is installed
where opencode >nul 2>nul
if %errorlevel% equ 0 (
    opencode
) else (
    cls
    echo ================================================================
    echo                       DEV CENTER
    echo ================================================================
    echo.
    echo [ERROR] OpenCode is not installed or not in PATH.
    echo.
    echo Install it from: https://opencode.ai
    echo.
    timeout /t 5 /nobreak >nul
)
