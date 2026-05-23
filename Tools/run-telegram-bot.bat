@echo off
chcp 65001 >nul
title Telegram Bot - DevCenter

echo ========================================
echo    بوت Telegram - DevCenter
echo ========================================
echo.
echo تأكد من تعبئة TELEGRAM_BOT_TOKEN في Tools\.env.comm
echo.

:loop
echo [%date% %time%] تشغيل بوت Telegram...
python D:\DevCenter\Tools\telegram_bot.py
echo [%date% %time%] البوت توقف. إعادة التشغيل بعد 5 ثوان...
timeout /t 5 /nobreak >nul
goto loop
